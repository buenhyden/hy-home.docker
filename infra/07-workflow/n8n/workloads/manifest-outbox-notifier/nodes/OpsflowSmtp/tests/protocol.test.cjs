'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { Duplex } = require('node:stream');
const { createCaptureTransport, sendClaim, POLICY } = require('../dist/transport.js');
const claim = { id: 1, run_id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', source: 'hy-home.docker', row_count: 1, lease_token: '22222222-2222-4222-8222-222222222222', lease_until: '2099-01-01T00:00:00.000Z' };
const credential = { host: 'mailpit', port: 1025, secure: false, disableStartTls: true, user: '', password: '', hostName: '' };

// A byte stream only: no listen(), DNS lookup, net connect, SMTP server or credential.
class SyntheticSocket extends Duplex {
  constructor(replyMode) {
    super(); this.replyMode = replyMode; this.transcript = ''; this.buffer = ''; this.dataMode = false; this.timeouts = [];
  }
  _read() {}
  setTimeout(value) { this.timeouts.push(value); return this; }
  setKeepAlive() { return this; }
  setNoDelay() { return this; }
  _write(chunk, encoding, callback) {
    const bytes = chunk.toString(); this.transcript += bytes; this.buffer += bytes;
    if (this.dataMode) {
      if (this.buffer.endsWith('\r\n.\r\n')) {
        this.dataMode = false; this.buffer = '';
        if (this.replyMode === 'loss') this.destroy();
        else setImmediate(() => this.push('250 captured synthetic\r\n'));
      }
    } else {
      while (this.buffer.includes('\r\n')) {
        const index = this.buffer.indexOf('\r\n'); const command = this.buffer.slice(0, index); this.buffer = this.buffer.slice(index + 2);
        const reply = command.startsWith('EHLO') ? '250-synthetic\r\n250 STARTTLS\r\n' : command === 'DATA' ? '354 continue\r\n' : '250 ok\r\n';
        if (command === 'DATA') this.dataMode = true;
        setImmediate(() => this.push(reply));
      }
    }
    callback();
  }
}

test('actual Nodemailer adapter sends fixed MIME into in-memory SMTP bytes and destroys socket', async () => {
  const socket = new SyntheticSocket('accept');
  const factory = options => createCaptureTransport(options, given => {
    assert.deepEqual(given, { host: 'mailpit', port: 1025 });
    setImmediate(() => { socket.emit('connect'); setImmediate(() => socket.push('220 synthetic\r\n')); });
    return socket;
  });
  assert.deepEqual(await sendClaim(claim, credential, undefined, factory), { run_id: claim.run_id, state: 'accepted_by_smtp' });
  assert.equal(socket.destroyed, true);
  assert.ok(socket.timeouts.includes(POLICY.socketTimeout));
  const unfolded = socket.transcript.replace(/\r\n[ \t]+/g, ' ');
  assert.ok(unfolded.includes(`Message-ID: <opsflow.${claim.run_id}@opsflow.invalid>`));
  assert.ok(socket.transcript.includes('RCPT TO:<manifest@opsflow.invalid>'));
  assert.ok(!socket.transcript.includes(claim.lease_token));
  assert.ok(!socket.transcript.includes('STARTTLS\r\n'));
  assert.ok(!socket.transcript.includes('AUTH '));
});

test('actual Nodemailer adapter treats DATA response loss as uncertain and destroys socket', async () => {
  const socket = new SyntheticSocket('loss');
  const factory = options => createCaptureTransport(options, () => {
    setImmediate(() => { socket.emit('connect'); setImmediate(() => socket.push('220 synthetic\r\n')); });
    return socket;
  });
  assert.deepEqual(await sendClaim(claim, credential, undefined, factory), { run_id: claim.run_id, state: 'uncertain' });
  assert.equal(socket.destroyed, true);
});

test('actual Nodemailer adapter cancellation destroys pending greeting socket', async () => {
  const socket = new SyntheticSocket('accept');
  const cancellation = new AbortController();
  const factory = options => createCaptureTransport(options, () => {
    setImmediate(() => { socket.emit('connect'); setImmediate(() => cancellation.abort()); });
    return socket;
  });
  assert.deepEqual(await sendClaim(claim, credential, cancellation.signal, factory), { run_id: claim.run_id, state: 'uncertain' });
  assert.equal(socket.destroyed, true);
});
