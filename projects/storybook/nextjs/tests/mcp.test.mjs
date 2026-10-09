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
  assert.match(entries.result.content[0].text, /ui-button/);
  assert.match(entries.result.content[0].text, /ui-asyncstate/);
  assert.doesNotMatch(entries.result.content[0].text, /example-(header|page)/);
  const button = await rpc(4, 'tools/call', { name: 'docs-show', arguments: { id: 'ui-button' } });
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

// Remote mode (SPEC-0219): synthetic Keycloak key and tokens, no network.
const { generateKeyPairSync, createSign } = await import('node:crypto');
const { handleRequest: remoteHandle, verifyBearer, remoteConfig, protectedResourceMetadata } = await import('../mcp/server.ts');
const { publicKey, privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });
const issuer = 'https://keycloak.hy.test/realms/r';
const resource = 'https://storybook-mcp.hy.test/mcp';
const config = remoteConfig({
  STORYBOOK_MCP_RESOURCE: 'https://storybook-mcp.hy.test/mcp',
  STORYBOOK_MCP_ISSUER: issuer,
  STORYBOOK_MCP_SCOPE: 'storybook-mcp',
  STORYBOOK_MCP_READER_GROUP: '/admins',
});
const keys = async (kid) => (kid === 'k1' ? publicKey.export({ format: 'jwk' }) : undefined);
const encode = (value) => Buffer.from(JSON.stringify(value)).toString('base64url');
function token(claims = {}, header = {}) {
  const now = Math.floor(Date.now() / 1000);
  const head = encode({ alg: 'RS256', kid: 'k1', ...header });
  const body = encode({ iss: issuer, aud: [resource, 'account'], exp: now + 300, groups: ['/admins'], ...claims });
  const signature = createSign('RSA-SHA256').update(`${head}.${body}`).sign(privateKey).toString('base64url');
  return `Bearer ${head}.${body}.${signature}`;
}

test('remote bearer tokens need the issuer, audience, lifetime, key and reader group', async () => {
  const now = Math.floor(Date.now() / 1000);
  assert.equal(await verifyBearer(token(), config, keys), 200);
  assert.equal(await verifyBearer(token({ aud: resource }), config, keys), 200);
  assert.equal(await verifyBearer(token({ groups: ['/users'] }), config, keys), 403);
  assert.equal(await verifyBearer(token({ groups: undefined }), config, keys), 403);
  const refused = {
    'no header': null,
    'not bearer': 'Basic abc',
    issuer: token({ iss: 'https://evil.example/realms/r' }),
    audience: token({ aud: 'oauth2-proxy' }),
    'audience prefix': token({ aud: 'https://storybook-mcp.hy.test/' }),
    expired: token({ exp: now - 120 }),
    'not yet valid': token({ nbf: now + 600 }),
    'no expiry': token({ exp: undefined }),
    'alg none': token({}, { alg: 'none' }),
    'symmetric alg': token({}, { alg: 'HS256' }),
    'unknown key': token({}, { kid: 'k2' }),
    tampered: token().replace(/\.([\w-]+)\./, `.${encode({ iss: issuer, aud: resource, exp: now + 300, groups: ['/admins'], sub: 'x' })}.`),
  };
  for (const [name, header] of Object.entries(refused)) {
    assert.equal(await verifyBearer(header, config, keys), 401, name);
  }
});

test('remote MCP answers 401 with resource metadata, 403 for non-readers and serves readers', async () => {
  const remote = { config, keys };
  const endpoint = 'https://storybook-mcp.hy.test/mcp';
  const call = (authorization) => remoteHandle(new Request(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream', ...(authorization ? { authorization } : {}) },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/list' }),
  }), remote);
  const anonymous = await call();
  assert.equal(anonymous.status, 401);
  assert.equal(anonymous.headers.get('www-authenticate'),
    'Bearer scope="storybook-mcp", resource_metadata="https://storybook-mcp.hy.test/.well-known/oauth-protected-resource/mcp"');
  const outsider = await call(token({ groups: [] }));
  assert.equal(outsider.status, 403);
  assert.match(outsider.headers.get('www-authenticate'), /insufficient_scope/);
  const reader = await call(token());
  assert.equal(reader.status, 200);
  const tools = JSON.parse((await reader.text()).split('\n').find((line) => line.startsWith('data: ')).slice(6));
  assert.deepEqual(tools.result.tools.map((tool) => tool.name).sort(), ['docs-list', 'docs-show', 'docs-show-story']);
  const metadata = await remoteHandle(new Request('https://storybook-mcp.hy.test/.well-known/oauth-protected-resource/mcp'), remote);
  assert.deepEqual(await metadata.json(), protectedResourceMetadata(config));
  assert.deepEqual(protectedResourceMetadata(config), {
    resource, authorization_servers: [issuer], scopes_supported: ['storybook-mcp'], bearer_methods_supported: ['header'],
  });
  // Local mode has no metadata route.
  assert.equal((await remoteHandle(new Request('http://127.0.0.1:7613/.well-known/oauth-protected-resource'))).status, 404);
});

test('remote mode refuses plain http and missing scope or group', () => {
  const base = { STORYBOOK_MCP_RESOURCE: 'https://m.hy.test/mcp', STORYBOOK_MCP_ISSUER: issuer, STORYBOOK_MCP_SCOPE: 'a', STORYBOOK_MCP_READER_GROUP: '/g' };
  assert.equal(remoteConfig({}), undefined);
  for (const change of [{ STORYBOOK_MCP_RESOURCE: 'http://m.hy.test/mcp' }, { STORYBOOK_MCP_ISSUER: 'http://kc/realms/r' },
    { STORYBOOK_MCP_SCOPE: '' }, { STORYBOOK_MCP_READER_GROUP: '' }]) {
    assert.throws(() => remoteConfig({ ...base, ...change }), /Remote MCP needs/);
  }
});
