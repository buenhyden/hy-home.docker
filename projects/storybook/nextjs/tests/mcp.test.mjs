import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { createServer, request as httpRequest } from 'node:http';
import { once } from 'node:events';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { handleRequest, verifyManifest } from '../mcp/server.ts';

const endpoint = 'http://127.0.0.1:7613/mcp';

async function rpc(id, method, params = {}) {
  const response = await handleRequest(new Request(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream' },
    body: JSON.stringify({ jsonrpc: '2.0', id, method, params }),
  }));
  assert.equal(response.status, 200);
  const data = (await response.text()).split('\n').find((line) => line.startsWith('data: '));
  assert.ok(data);
  return JSON.parse(data.slice(6));
}

test('local MCP only exposes docs and resolves built component/docs entries', async () => {
  const init = await rpc(1, 'initialize', {
    protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'synthetic-test', version: '0.1' },
  });
  assert.equal(init.result.protocolVersion, '2025-06-18');
  const list = await rpc(2, 'tools/list');
  assert.deepEqual(list.result.tools.map((tool) => tool.name).sort(), ['docs-list', 'docs-show', 'docs-show-story']);
  const entries = await rpc(3, 'tools/call', { name: 'docs-list', arguments: {} });
  assert.match(entries.result.content[0].text, /example-button/);
  const button = await rpc(4, 'tools/call', { name: 'docs-show', arguments: { id: 'example-button' } });
  assert.match(button.result.content[0].text, /@hy-home\/storybook-ui/);
  const docs = JSON.parse(await readFile(new URL('../storybook-static/manifests/docs.json', import.meta.url)));
  const docId = Object.keys(docs.docs)[0];
  const documentation = await rpc(5, 'tools/call', { name: 'docs-show', arguments: { id: docId } });
  assert.equal(documentation.result.isError, undefined);
  const forbidden = await rpc(6, 'tools/call', { name: 'stories-preview', arguments: {} });
  assert.equal(forbidden.result.isError, true);
  const reconnect = await rpc(7, 'tools/list');
  assert.equal(reconnect.result.tools.length, 3);
});

test('manifest hashes and origin are enforced', async () => {
  const staticDir = new URL('../storybook-static/', import.meta.url);
  const revision = JSON.parse(await readFile(new URL('revision.json', staticDir)));
  for (const name of ['components.json', 'docs.json']) {
    const bytes = await readFile(new URL(`manifests/${name}`, staticDir));
    assert.equal(revision.manifestSha256[name], createHash('sha256').update(bytes).digest('hex'));
  }
  assert.throws(() => verifyManifest('components.json', '{}', revision), /revision mismatch/);
  const rejected = await handleRequest(new Request(endpoint, { method: 'POST', headers: { origin: 'https://untrusted.example' } }));
  assert.equal(rejected.status, 403);
  const missing = await handleRequest(new Request('http://127.0.0.1:7613/no-such-route'));
  assert.equal(missing.status, 404);
});


test('HTTP transport rejects a forged Host and oversized request', async () => {
  const probe = createServer();
  probe.listen(0, '127.0.0.1');
  await once(probe, 'listening');
  const { port } = probe.address();
  probe.close();
  await once(probe, 'close');
  const child = spawn(process.execPath, ['--experimental-strip-types', new URL('../mcp/server.ts', import.meta.url).pathname], {
    env: { ...process.env, STORYBOOK_MCP_PORT: String(port) },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  try {
    await Promise.race([
      once(child.stdout, 'data'),
      once(child, 'exit').then(() => { throw new Error('MCP server exited before listening'); }),
    ]);
    const send = (headers, body) => new Promise((resolve, reject) => {
      const req = httpRequest({ hostname: '127.0.0.1', port, path: '/mcp', method: 'POST', headers }, (res) => {
        res.resume();
        res.on('end', () => resolve(res.statusCode));
      });
      req.on('error', reject);
      req.end(body);
    });
    assert.equal(await send({ host: 'forged.example' }, '{}'), 403);
    assert.equal(await send({ host: `127.0.0.1:${port}` }, Buffer.alloc(1024 * 1024 + 1)), 413);
  } finally {
    child.kill();
    if (child.exitCode === null) await once(child, 'exit');
  }
});
