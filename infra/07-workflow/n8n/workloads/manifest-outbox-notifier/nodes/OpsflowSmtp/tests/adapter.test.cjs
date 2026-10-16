'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { EventEmitter } = require('node:events');
const { createCaptureTransport, transportOptions, messageFor, POLICY } = require('../dist/transport.js');
const credential = { host: 'mailpit', port: 1025, secure: false, disableStartTls: true, user: '', password: '', hostName: '' };
const claim = { id: 1, run_id: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', source: 'hy-home.docker', row_count: 1, lease_token: '22222222-2222-4222-8222-222222222222', lease_until: '2099-01-01T00:00:00.000Z' };

function fixture() {
  const socket = new EventEmitter();
  let destroyed = 0; let closed = 0; let options;
  socket.destroy = error => { destroyed += 1; if (error) socket.emit('error', error); socket.emit('close'); };
  const transport = createCaptureTransport(transportOptions(credential), given => {
    assert.deepEqual(given, { host: 'mailpit', port: 1025 }); return socket;
  }, given => {
    options = given;
    return { sendMail: async message => message, close: () => { closed += 1; } };
  });
  return { socket, transport, options, counts: () => ({ destroyed, closed }) };
}

test('adapter uses owned socket, closes it once and has no broad transport flags', async () => {
  const f = fixture();
  assert.equal(f.options.host, 'mailpit');
  assert.equal(f.options.port, 1025);
  assert.equal(f.options.pool, false);
  assert.equal(f.options.logger, false);
  let captured;
  f.options.getSocket({}, (error, result) => { assert.equal(error, null); captured = result.connection; });
  f.socket.emit('connect');
  assert.equal(captured, f.socket);
  assert.deepEqual(await f.transport.sendMail(messageFor(claim)), messageFor(claim));
  f.transport.close(); f.transport.close();
  assert.deepEqual(f.counts(), { destroyed: 1, closed: 1 });
  let failure;
  f.options.getSocket({}, error => { failure = error.message; });
  assert.equal(failure, 'OPSFLOW_TRANSPORT_CLOSED');
});

test('connection error exposes no driver error and clears connection timer', () => {
  const f = fixture(); let failure;
  f.options.getSocket({}, error => { failure = error.message; });
  f.socket.emit('error', new Error('PRIVATE_SOCKET_ERROR'));
  assert.equal(failure, 'OPSFLOW_CONNECT_FAILED');
  assert.equal(f.socket.listenerCount('connect'), 0);
  f.transport.close();
});

test('connection deadline destroys the owned socket and clears all temporary listeners', t => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const f = fixture(); let failure;
  f.options.getSocket({}, error => { failure = error.message; });
  t.mock.timers.tick(POLICY.connectionTimeout);
  assert.equal(failure, 'OPSFLOW_CONNECT_FAILED');
  assert.deepEqual(f.counts(), { destroyed: 1, closed: 0 });
  assert.equal(f.socket.listenerCount('connect'), 0);
  f.transport.close();
});

test('cancellation before a connection clears its pending deadline', t => {
  t.mock.timers.enable({ apis: ['setTimeout'] });
  const f = fixture();
  f.options.getSocket({}, () => { throw new Error('callback must not fire after cancellation'); });
  f.transport.close();
  t.mock.timers.tick(POLICY.connectionTimeout);
  assert.deepEqual(f.counts(), { destroyed: 1, closed: 1 });
  assert.equal(f.socket.listenerCount('error'), 0);
});

test('adapter close with no socket is safe', () => {
  const f = fixture(); f.transport.close();
  assert.deepEqual(f.counts(), { destroyed: 0, closed: 1 });
});
