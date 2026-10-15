'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const transport = require('../dist/transport.js');
const { OpsflowSmtp } = require('../dist/OpsflowSmtp.node.js');
const claim = { id: 1, run_id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', source: 'hy-home.docker', row_count: 1, lease_token: '22222222-2222-4222-8222-222222222222', lease_until: '2099-01-01T00:00:00.000Z' };
const credential = { host: 'mailpit', port: 1025, secure: false, disableStartTls: true, user: '', password: '', hostName: '' };
const descriptor = { name: 'Opsflow SMTP Capture', type: 'n8n-nodes-opsflow.opsflowSmtp', typeVersion: 1, position: [0, 0], parameters: {} };
function context(overrides = {}) {
  return { getInputData: () => [{ json: { valid: true } }], getNodeParameter: (name, index) => { assert.equal(name, 'claim'); assert.equal(index, 0); return claim; }, getCredentials: async type => { assert.equal(type, 'smtp'); return credential; }, getExecutionCancelSignal: () => undefined, getNode: () => descriptor, ...overrides };
}

test('native node has only closed claim and SMTP credential surface', () => {
  const d = new OpsflowSmtp().description;
  assert.equal(d.name, 'opsflowSmtp'); assert.equal(d.version, 1);
  assert.deepEqual(d.credentials, [{ name: 'smtp', required: true }]);
  assert.equal(d.properties.length, 1); assert.equal(d.properties[0].name, 'claim');
  assert.equal(d.properties[0].type, 'json');
});

test('native execution obtains smtp credential and forwards abort signal with redacted result', async t => {
  const signal = new AbortController().signal;
  t.mock.method(transport, 'sendClaim', async (row, cred, cancel) => {
    assert.deepEqual(row, claim); assert.deepEqual(cred, credential); assert.equal(cancel, signal);
    return { run_id: row.run_id, state: 'accepted_by_smtp', extra: 'PRIVATE_DRIVER_MARKER' };
  });
  const result = await OpsflowSmtp.prototype.execute.call(context({ getExecutionCancelSignal: () => signal }));
  assert.deepEqual(result, [[{ json: { run_id: claim.run_id, state: 'accepted_by_smtp' }, pairedItem: { item: 0 } }]]);
  assert.ok(!JSON.stringify(result).includes(claim.lease_token));
});

test('empty input obtains no claim or credential', async () => {
  assert.deepEqual(await OpsflowSmtp.prototype.execute.call(context({ getInputData: () => [], getCredentials: () => { throw new Error('must not read'); }, getNodeParameter: () => { throw new Error('must not read'); } })), [[]]);
});

test('invalid cardinality binary claim and driver errors fail with static codes only', async t => {
  for (const overrides of [{ getInputData: () => [{ json: {} }, { json: {} }] }, { getInputData: () => [{ json: {}, binary: {} }] }, { getNodeParameter: () => ({ ...claim, extra: 'PRIVATE_CLAIM_MARKER' }) }, { getCredentials: () => { throw new Error('PRIVATE_CREDENTIAL_MARKER'); } }, { getNodeParameter: () => { throw new Error('PRIVATE_PARAMETER_MARKER'); } }]) {
    await assert.rejects(OpsflowSmtp.prototype.execute.call(context(overrides)), error => {
      assert.ok(/^OPSFLOW_/.test(error.message));
      assert.ok(!JSON.stringify(error).includes('PRIVATE_'));
      assert.equal(error.cause.message, error.message);
      assert.deepEqual(error.node.parameters, {});
      return true;
    });
  }
  t.mock.method(transport, 'sendClaim', async () => { throw new Error('PRIVATE_TRANSPORT_MARKER'); });
  await assert.rejects(OpsflowSmtp.prototype.execute.call(context()), /^NodeOperationError: OPSFLOW_NODE_FAILED$/);
});

test('error envelope never copies node credential references or literal claim payload', async () => {
  await assert.rejects(OpsflowSmtp.prototype.execute.call(context({
    getNodeParameter: () => ({ ...claim, extra: 'PRIVATE_LITERAL_MARKER' }),
    getNode: () => ({ ...descriptor, parameters: { claim: { ...claim, extra: 'PRIVATE_LITERAL_MARKER' } }, credentials: { smtp: { id: 'PRIVATE_ID_MARKER', name: 'PRIVATE_REFERENCE_MARKER' } } }),
  })), error => {
    assert.ok(!JSON.stringify(error).includes('PRIVATE_'));
    assert.ok(!JSON.stringify(error).includes(claim.lease_token));
    return true;
  });
});
