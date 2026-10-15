'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');
const { sendClaim, validateClaim, transportOptions, messageFor, POLICY } = require('../dist/transport.js');

const claim = Object.freeze({
  id: '9223372036854775807',
  run_id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  source: 'hy-home.docker', row_count: 7,
  lease_token: '22222222-2222-4222-8222-222222222222', lease_until: '2099-01-01T00:00:00.000Z',
});
const credential = Object.freeze({ host: 'mailpit', port: 1025, secure: false, disableStartTls: true, user: '', password: '', hostName: '' });

test('restricted send accepts only expected recipient and strips driver payload', async () => {
  const sent = [];
  const result = await sendClaim(claim, credential, undefined, (options) => {
    assert.equal(options.host, 'mailpit');
    return { sendMail: async mail => { sent.push(mail); return { accepted: ['manifest@opsflow.invalid'], rejected: [], response: 'PRIVATE_DRIVER_MARKER', extra: claim.lease_token }; }, close: () => {} };
  });
  assert.deepEqual(result, { run_id: claim.run_id, state: 'accepted_by_smtp' });
  assert.equal(sent.length, 1);
  assert.equal(sent[0].messageId, `<opsflow.${claim.run_id}@opsflow.invalid>`);
  assert.ok(!JSON.stringify(sent).includes(claim.lease_token));
});

test('claim schema rejects unknown data, injection, invalid scalars, and copied capability', () => {
  for (const row of [null, [], {}, { ...claim, id: true }, { ...claim, id: 0 }, { ...claim, id: Number.MAX_SAFE_INTEGER + 1 }, { ...claim, id: '9223372036854775808' }, { ...claim, id: '01' }, { ...claim, id: '-1' }, { ...claim, run_id: 'bad' }, { ...claim, run_id: claim.run_id.toUpperCase().replace('1111', 'ABCD') }, { ...claim, source: 'x\r\nBcc:external@example.org' }, { ...claim, row_count: -1 }, { ...claim, row_count: '1' }, { ...claim, row_count: true }, { ...claim, lease_token: claim.run_id }, { ...claim, lease_token: 'PRIVATE_MARKER' }, { ...claim, cc: 'outside@example.org' }]) {
    assert.throws(() => validateClaim(row), /^Error: OPSFLOW_INVALID_CLAIM$/);
  }
  assert.deepEqual(validateClaim({ ...claim, id: 1, row_count: 1 }), { ...claim, id: 1, row_count: 1 });
});

test('denied endpoint, TLS mode, real auth, proxy and credential headers never create transport', async () => {
  for (const changes of [{ host: 'stalwart' }, { host: 'smtp.example.org' }, { host: 'MAILPIT' }, { port: 25 }, { port: '1025' }, { secure: true }, { disableStartTls: false }, { user: 'actual-user' }, { password: 'dummy' }, { hostName: 'bad\r\n' }, { proxy: 'http://example.org' }, { arbitrary: true }]) {
    let calls = 0;
    await assert.rejects(sendClaim(claim, { ...credential, ...changes }, undefined, () => { calls += 1; }), /^Error: OPSFLOW_INVALID_CREDENTIAL$/);
    assert.equal(calls, 0);
  }
});

test('supplied draft producer run source and count contract is explicit', () => {
  for (const source of ['hy-home.docker', 'hy-home.k8s', 'Project-Template', 'blog-data']) {
    assert.equal(validateClaim({ ...claim, source, row_count: 5000 }).source, source);
  }
  for (const changes of [{ row_count: 0 }, { row_count: 5001 }, { row_count: 1.5 }, { source: 'synthetic' }, { run_id: '11111111-1111-4111-8111-111111111111' }, { run_id: 'a'.repeat(63) }, { run_id: 'a'.repeat(65) }, { run_id: 'A'.repeat(64) }]) {
    assert.throws(() => validateClaim({ ...claim, ...changes }), /^Error: OPSFLOW_INVALID_CLAIM$/);
  }
});

test('claim scalars reject every trailing line terminator without transport', () => {
  for (const ending of ['\n', '\r', '\r\n', '\u2028', '\u2029']) {
    for (const key of ['id', 'run_id', 'lease_token']) {
      assert.throws(() => validateClaim({ ...claim, [key]: claim[key] + ending }), /^Error: OPSFLOW_INVALID_CLAIM$/);
    }
  }
});

test('mail has bounded fixed envelope and no arbitrary file URL or header surface', () => {
  const options = transportOptions(credential);
  assert.equal(options.connectionTimeout, 3000);
  assert.equal(options.greetingTimeout, 3000);
  assert.equal(options.socketTimeout, 5000);
  assert.equal(options.dnsTimeout, 3000);
  assert.equal(options.disableFileAccess, true);
  assert.equal(options.disableUrlAccess, true);
  assert.equal(options.logger, false);
  assert.equal(options.debug, false);
  assert.equal(options.ignoreTLS, true);
  assert.equal(options.secure, false);
  const mail = messageFor(claim);
  assert.deepEqual(Object.keys(mail).sort(), ['disableFileAccess', 'disableUrlAccess', 'envelope', 'from', 'messageId', 'subject', 'text', 'to'].sort());
  assert.ok(Buffer.byteLength(mail.text) < POLICY.maxTextBytes);
  assert.equal(mail.from, 'notifier@opsflow.invalid');
  assert.deepEqual(mail.envelope, { from: mail.from, to: ['manifest@opsflow.invalid'] });
  assert.equal(messageFor({ ...claim, id: 3, lease_token: '33333333-3333-4333-8333-333333333333' }).messageId, mail.messageId);
});

test('empty, unknown, multiple, rejected and missing acceptance remain uncertain', async () => {
  for (const info of [undefined, null, {}, { accepted: [], rejected: [] }, { accepted: ['other@opsflow.invalid'], rejected: [] }, { accepted: ['manifest@opsflow.invalid'], rejected: ['other@opsflow.invalid'] }, { accepted: ['manifest@opsflow.invalid', 'other@opsflow.invalid'], rejected: [] }, { accepted: ['manifest@opsflow.invalid'] }, { accepted: 'manifest@opsflow.invalid', rejected: [] }]) {
    let closed = 0;
    const result = await sendClaim(claim, credential, undefined, () => ({ sendMail: async () => info, close: () => { closed += 1; } }));
    assert.deepEqual(result, { run_id: claim.run_id, state: 'uncertain' });
    assert.equal(closed, 1);
  }
});

test('rejection, synchronous creation/send and cleanup failures are redacted', async () => {
  for (const factory of [() => { throw new Error('PRIVATE_MARKER'); }, () => ({ sendMail: () => { throw new Error('PRIVATE_MARKER'); }, close: () => {} }), () => ({ sendMail: async () => { throw new Error('PRIVATE_MARKER'); }, close: () => {} }), () => ({ sendMail: async () => ({ accepted: ['manifest@opsflow.invalid'], rejected: [] }), close: () => { throw new Error('PRIVATE_MARKER'); } })]) {
    assert.deepEqual(await sendClaim(claim, credential, undefined, factory), { run_id: claim.run_id, state: 'uncertain' });
  }
});

test('cancel before send causes no transport; cancel during send closes transport promptly', async () => {
  const prior = new AbortController(); prior.abort();
  let calls = 0;
  assert.deepEqual(await sendClaim(claim, credential, prior.signal, () => { calls += 1; }), { run_id: claim.run_id, state: 'cancelled' });
  assert.equal(calls, 0);
  const active = new AbortController(); let closed = 0;
  const pending = sendClaim(claim, credential, active.signal, () => ({ sendMail: () => { setImmediate(() => active.abort()); return new Promise(() => {}); }, close: () => { closed += 1; } }));
  assert.deepEqual(await pending, { run_id: claim.run_id, state: 'uncertain' });
  assert.equal(closed, 1);
});

test('abort during transport creation causes no SMTP dispatch', async () => {
  const controller = new AbortController(); let sends = 0; let closed = 0;
  const result = await sendClaim(claim, credential, controller.signal, () => {
    controller.abort();
    return { sendMail: async () => { sends += 1; }, close: () => { closed += 1; } };
  });
  assert.deepEqual(result, { run_id: claim.run_id, state: 'cancelled' });
  assert.equal(sends, 0); assert.equal(closed, 1);
});

test('deadline closes a hung transport and reports uncertainty', async (t) => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  let closed = 0;
  const pending = sendClaim(claim, credential, undefined, () => ({ sendMail: () => new Promise(() => {}), close: () => { closed += 1; } }));
  t.mock.timers.tick(POLICY.totalTimeoutMs);
  assert.deepEqual(await pending, { run_id: claim.run_id, state: 'uncertain' });
  assert.equal(closed, 1);
});


test('server lease expiry or insufficient SMTP/ack reserve never opens transport', async () => {
  for (const offset of [-1, 0, 19000]) {
    let opened = 0;
    const stale = { ...claim, lease_until: new Date(Date.now() + offset).toISOString() };
    const result = await sendClaim(stale, credential, undefined, () => { opened++; throw new Error('must not open'); });
    assert.equal(opened, 0);
    assert.equal(result.state, 'cancelled');
  }
});


test('lease deadline rejects missing malformed noncanonical and impossible timestamps', () => {
  for (const lease_until of [undefined, null, '', '2099-01-01', '2099-01-01T00:00:00Z', '2099-02-30T00:00:00.000Z', '2099-01-01T00:00:00.000Z\n', '2099-01-01T00:00:00.000+00:00']) {
    assert.throws(() => validateClaim({ ...claim, lease_until }), /^Error: OPSFLOW_INVALID_CLAIM$/);
  }
});

test('lease expiring during transport creation never dispatches SMTP', async () => {
  const originalNow = Date.now;
  const now = originalNow();
  let sends = 0;
  let closed = 0;
  try {
    const row = { ...claim, lease_until: new Date(now + 60000).toISOString() };
    const result = await sendClaim(row, credential, undefined, () => {
      Date.now = () => now + 40000;
      return { sendMail: async () => { sends++; }, close: () => { closed++; } };
    });
    assert.equal(result.state, 'cancelled');
    assert.equal(sends, 0);
    assert.equal(closed, 1);
  } finally { Date.now = originalNow; }
});
