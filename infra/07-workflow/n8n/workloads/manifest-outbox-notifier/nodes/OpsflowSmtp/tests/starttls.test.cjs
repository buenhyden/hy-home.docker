'use strict';

// Owned loopback SMTP bytes exercise the real adapter; no Mailpit/HOME service is used.
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const net = require('node:net');
const os = require('node:os');
const path = require('node:path');
const tls = require('node:tls');
const { spawn, execFileSync } = require('node:child_process');

const profile = 'mailpit-starttls-auth-v1';
const claim = { id: 1, run_id: 'a'.repeat(64), source: 'hy-home.docker', row_count: 1,
  lease_token: '22222222-2222-4222-8222-222222222222', lease_until: '2099-01-01T00:00:00.000Z' };
const credential = { host: 'mailpit', port: 1025, secure: false, disableStartTls: false,
  user: 'synthetic-capture', password: crypto.randomBytes(24).toString('hex'), hostName: '' };
let directory;

function openssl(args) {
  execFileSync('/usr/bin/openssl', args, { cwd: directory, stdio: 'ignore', timeout: 10000 });
}

before(() => {
  directory = fs.mkdtempSync(path.join(os.tmpdir(), 'opsflow-starttls-'));
  fs.chmodSync(directory, 0o700);
  openssl(['req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-subj', '/CN=Opsflow Synthetic CA',
    '-keyout', 'ca.key', '-out', 'ca.pem', '-days', '1']);
  for (const [name, hostname] of [['server', 'mailpit'], ['wrong-name', 'other.invalid']]) {
    openssl(['req', '-newkey', 'rsa:2048', '-nodes', '-subj', '/CN=' + hostname,
      '-addext', 'subjectAltName=DNS:' + hostname, '-keyout', name + '.key', '-out', name + '.csr']);
    openssl(['x509', '-req', '-in', name + '.csr', '-CA', 'ca.pem', '-CAkey', 'ca.key',
      '-CAcreateserial', '-out', name + '.pem', '-days', '1', '-copy_extensions', 'copy']);
  }
});
after(() => { if (directory) fs.rmSync(directory, { recursive: true, force: true }); });

const CHILD = String.raw`
const readline = require('node:readline');
const net = require('node:net');
const { sendClaim, createCaptureTransport } = require(process.env.OPSFLOW_TRANSPORT_MODULE);
const reader = readline.createInterface({ input: process.stdin });
const cancellation = new AbortController();
let started = false;
reader.on('line', async line => {
  if (started) { if (line === 'abort') cancellation.abort(); return; }
  started = true;
  let socket;
  try {
    const input = JSON.parse(line);
    const factory = options => createCaptureTransport(options, selected => {
      if (selected.host !== 'mailpit' || selected.port !== 1025) throw new Error('closed_destination');
      socket = net.createConnection({ host: '127.0.0.1', port: input.port });
      return socket;
    });
    const outcome = await sendClaim(input.claim, input.credential, cancellation.signal, factory, input.profile);
    process.stdout.write(JSON.stringify({ outcome, destroyed: socket.destroyed }) + '\n');
  } catch { process.stdout.write(JSON.stringify({ error: 'synthetic_client_failed' }) + '\n'); process.exitCode = 1; }
  finally { reader.close(); process.stdin.destroy(); }
});
`;

function command(socket, encrypted, line, receive, session) {
    const { settings, facts, track, context, authorized } = session;
    if (line.startsWith('EHLO')) {
      socket.write(encrypted ? '250-owned\r\n250 AUTH PLAIN LOGIN\r\n' : '250-owned\r\n250 STARTTLS\r\n');
    } else if (line === 'STARTTLS') {
      if (settings.noStarttls) { socket.write('454 TLS unavailable\r\n'); return; }
      socket.write('220 upgrade\r\n');
      socket.removeListener('data', receive);
      if (settings.holdHandshake) { if (settings.onPhase) settings.onPhase('handshake'); return; }
      const secured = track(new tls.TLSSocket(socket, { isServer: true, secureContext: context }));
      secured.once('secure', () => { facts.tls++; wire(secured, true, session); });
    } else if (line.startsWith('AUTH ')) {
      facts.auth++;
      if (!encrypted) facts.authBeforeTls++;
      const expected = Buffer.from('\0' + credential.user + '\0' + credential.password).toString('base64');
      const valid = encrypted && line === 'AUTH PLAIN ' + expected;
      if (valid) authorized.add(socket);
      socket.write(valid ? '235 authenticated\r\n' : '535 rejected\r\n');
    } else if (line.startsWith('MAIL FROM:')) {
      facts.mail++;
      socket.write(authorized.has(socket) && line === 'MAIL FROM:<notifier@opsflow.invalid>' ? '250 sender\r\n' : '550 rejected\r\n');
    } else if (line.startsWith('RCPT TO:')) {
      socket.write(line === 'RCPT TO:<manifest@opsflow.invalid>' ? '250 recipient\r\n' : '550 rejected\r\n');
    } else if (line === 'QUIT') socket.end('221 done\r\n');
    else socket.write('250 ok\r\n');
}

function wire(socket, encrypted, session) {
  const { facts, settings, authorized } = session;
  let buffer = '';
  let dataMode = false;
  socket.on('data', function receive(bytes) {
    buffer += bytes.toString('utf8');
    if (buffer.length > 8192) { socket.destroy(); return; }
    while (buffer.includes('\r\n')) {
      const index = buffer.indexOf('\r\n');
      const line = buffer.slice(0, index);
      buffer = buffer.slice(index + 2);
      if (dataMode) {
        if (line !== '.') { facts.body += line + '\n'; continue; }
        facts.captured++;
        dataMode = false;
        if (settings.onPhase) settings.onPhase('captured');
        if (!settings.holdData) socket.write('250 captured\r\n');
        continue;
      }
      const verb = line.split(' ', 1)[0];
      facts.commands.push(verb);
      if (verb === 'DATA') {
        dataMode = authorized.has(socket);
        socket.write(dataMode ? '354 continue\r\n' : '530 authentication required\r\n');
      } else command(socket, encrypted, line, receive, session);
    }
  });
}

function smtpServer(settings = {}) {
  const sockets = new Set();
  const facts = { tls: 0, auth: 0, authBeforeTls: 0, mail: 0, captured: 0, body: '', commands: [] };
  const certName = settings.wrongName ? 'wrong-name' : 'server';
  const context = tls.createSecureContext({ key: fs.readFileSync(path.join(directory, certName + '.key')),
    cert: fs.readFileSync(path.join(directory, certName + '.pem')) });
  const track = socket => {
    sockets.add(socket);
    socket.on('error', () => {}); // Expected certificate/auth/cancellation failures stay inside this fixture.
    socket.once('close', () => sockets.delete(socket));
    return socket;
  };
  const session = { settings, facts, track, context, authorized: new WeakSet() };
  const server = net.createServer(socket => {
    track(socket);
    wire(socket, false, session);
    socket.write('220 owned-synthetic\r\n');
  });
  return { facts, sockets, server,
    listen: () => new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); }),
    close: () => new Promise(resolve => { for (const socket of sockets) socket.destroy(); server.close(resolve); }),
  };
}

async function client(fixture, settings = {}) {
  const env = { ...process.env, OPSFLOW_TRANSPORT_MODULE: require.resolve('../dist/transport.js') };
  delete env.NODE_EXTRA_CA_CERTS;
  if (!settings.untrusted) env.NODE_EXTRA_CA_CERTS = path.join(directory, 'ca.pem');
  const child = spawn(process.execPath, ['-e', CHILD], { env, stdio: ['pipe', 'pipe', 'pipe'] });
  fixture.abort = () => { if (!child.stdin.destroyed) child.stdin.write('abort\n'); };
  let output = '';
  let errorOutput = '';
  child.stdout.on('data', bytes => { output += bytes; });
  child.stderr.on('data', bytes => { errorOutput += bytes; });
  const timer = setTimeout(() => child.kill('SIGKILL'), 8000);
  child.stdin.write(JSON.stringify({ port: fixture.server.address().port, profile, claim,
    credential: { ...credential, ...settings.credential } }) + '\n');
  try {
    const code = await new Promise((resolve, reject) => { child.once('error', reject); child.once('exit', resolve); });
    assert.equal(code, 0, 'owned client exits successfully');
    assert.equal(errorOutput, '', 'no TLS/credential diagnostics escape');
    assert.ok(!output.includes(credential.password));
    return JSON.parse(output);
  } finally { clearTimeout(timer); child.stdin.destroy(); }
}

async function run(settings, check) {
  const fixture = smtpServer(settings);
  await fixture.listen();
  try {
    await check(fixture);
    const until = Date.now() + 1000;
    while (fixture.sockets.size && Date.now() < until) await new Promise(resolve => setTimeout(resolve, 5));
    assert.equal(fixture.sockets.size, 0, 'both raw and upgraded server sockets closed before fixture teardown');
  }
  finally { await fixture.close(); }
}

test('actual Nodemailer upgrades owned socket, authenticates only inside verified TLS and sends fixed capture', async () => {
  await run({}, async fixture => {
    const result = await client(fixture);
    assert.deepEqual(result, { outcome: { run_id: claim.run_id, state: 'accepted_by_smtp' }, destroyed: true });
    assert.equal(fixture.facts.tls, 1);
    assert.equal(fixture.facts.auth, 1);
    assert.equal(fixture.facts.authBeforeTls, 0);
    assert.equal(fixture.facts.captured, 1);
    assert.ok(fixture.facts.body.includes('Manifest published'));
    assert.ok(!fixture.facts.body.includes(claim.lease_token));
  });
});

for (const [name, settings] of [['wrong user', { credential: { user: 'other-synthetic' } }],
  ['wrong password', { credential: { password: crypto.randomBytes(24).toString('hex') } }],
  ['untrusted CA', { untrusted: true }], ['wrong certificate hostname', { wrongName: true }],
  ['STARTTLS refusal without plaintext fallback', { noStarttls: true }]]) {
  test('actual authenticated capture rejects ' + name, async () => {
    await run(settings, async fixture => {
      const result = await client(fixture, settings);
      assert.equal(result.outcome.state, 'uncertain');
      assert.equal(result.destroyed, true);
      assert.equal(fixture.facts.authBeforeTls, 0);
      assert.equal(fixture.facts.mail, 0);
      assert.equal(fixture.facts.captured, 0);
    });
  });
}

for (const phase of ['handshake', 'captured']) {
  test('cancellation closes owned ' + phase + ' socket and preserves uncertainty', async () => {
    let active;
    await run({ holdHandshake: phase === 'handshake', holdData: phase === 'captured',
      onPhase: reached => { if (reached === phase) active.abort(); } }, async fixture => {
      active = fixture;
      const result = await client(fixture);
      assert.equal(result.outcome.state, 'uncertain');
      assert.equal(result.destroyed, true);
      assert.equal(fixture.facts.captured, phase === 'captured' ? 1 : 0);
      assert.equal(fixture.facts.authBeforeTls, 0);
    });
  });
}
