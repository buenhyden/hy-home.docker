import { createHash } from 'node:crypto';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createStorybookMcpHandler } from '@storybook/mcp';

const staticDir = join(dirname(fileURLToPath(import.meta.url)), '..', 'storybook-static');
const allowedPaths = new Map([
  ['./manifests/components.json', 'components.json'],
  ['./manifests/docs.json', 'docs.json'],
]);
const METADATA_PATH = '/.well-known/oauth-protected-resource';
// Clock skew allowed between Keycloak and this server.
const SKEW_SECONDS = 30;

export function verifyManifest(name: string, content: string, revision: { manifestSha256?: Record<string, string> }): void {
  const digest = createHash('sha256').update(content).digest('hex');
  if (revision.manifestSha256?.[name] !== digest) throw new Error('Manifest revision mismatch');
}

async function readCheckedManifest(path: string): Promise<string> {
  const name = allowedPaths.get(path);
  if (!name) throw new Error('Unsupported manifest path');
  const revision = JSON.parse(await readFile(join(staticDir, 'revision.json'), 'utf8'));
  const content = await readFile(join(staticDir, 'manifests', name), 'utf8');
  verifyManifest(name, content, revision);
  return content;
}

const mcp = await createStorybookMcpHandler({
  manifestProvider: async (_request, path) => readCheckedManifest(path),
});

/** Remote mode: the public resource URL and the Keycloak token it accepts. */
export interface RemoteConfig {
  resource: URL;
  issuer: string;
  audience: string;
  scope: string;
  readerGroup: string;
}

export type KeyLookup = (kid: string) => Promise<JsonWebKey | undefined>;

export interface RemoteAuth {
  config: RemoteConfig;
  keys: KeyLookup;
}

export function remoteConfig(env: NodeJS.ProcessEnv): RemoteConfig | undefined {
  if (!env.STORYBOOK_MCP_RESOURCE) return undefined;
  const resource = new URL(env.STORYBOOK_MCP_RESOURCE);
  const config = {
    resource,
    issuer: env.STORYBOOK_MCP_ISSUER ?? '',
    // MCP authorization: the token audience is this resource's own URL.
    audience: resource.href,
    scope: env.STORYBOOK_MCP_SCOPE ?? '',
    readerGroup: env.STORYBOOK_MCP_READER_GROUP ?? '',
  };
  if (resource.protocol !== 'https:' || !config.issuer.startsWith('https://') || !config.scope || !config.readerGroup) {
    throw new Error('Remote MCP needs an https resource and issuer, a scope and a reader group');
  }
  return config;
}

const b64url = (value: string) => Buffer.from(value, 'base64url');

/** 200 for a reader, 401 for a missing or invalid token, 403 for a valid token without the reader group. */
export async function verifyBearer(header: string | null, config: RemoteConfig, keys: KeyLookup, now = Date.now() / 1000): Promise<200 | 401 | 403> {
  const match = /^Bearer ([\w-]+)\.([\w-]+)\.([\w-]+)$/.exec(header ?? '');
  if (!match) return 401;
  const [, head, body, signature] = match;
  let protectedHeader: { alg?: string; kid?: string };
  let claims: { iss?: string; aud?: string | string[]; exp?: number; nbf?: number; groups?: unknown };
  try {
    protectedHeader = JSON.parse(b64url(head).toString('utf8'));
    claims = JSON.parse(b64url(body).toString('utf8'));
  } catch {
    return 401;
  }
  // Only Keycloak's RS256 signing keys; never 'none' or a symmetric algorithm.
  if (protectedHeader.alg !== 'RS256' || typeof protectedHeader.kid !== 'string') return 401;
  const jwk = await keys(protectedHeader.kid);
  if (!jwk || jwk.kty !== 'RSA' || !jwk.n || !jwk.e) return 401;
  const key = await crypto.subtle.importKey('jwk', { kty: 'RSA', n: jwk.n, e: jwk.e }, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
  const signed = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64url(signature), Buffer.from(`${head}.${body}`));
  if (!signed || claims.iss !== config.issuer || ![claims.aud].flat().includes(config.audience)) return 401;
  if (typeof claims.exp !== 'number' || claims.exp + SKEW_SECONDS <= now || (claims.nbf ?? 0) > now + SKEW_SECONDS) return 401;
  return Array.isArray(claims.groups) && claims.groups.includes(config.readerGroup) ? 200 : 403;
}

/** Keycloak's signing keys from its discovery document, refreshed for an unknown key id. */
export function keycloakKeys(issuer: string): KeyLookup {
  let cache = new Map<string, JsonWebKey>();
  let fetchedAt = 0;
  return async (kid) => {
    if (!cache.has(kid) && Date.now() - fetchedAt > 30_000) {
      fetchedAt = Date.now();
      const discovery = await (await fetch(`${issuer}/.well-known/openid-configuration`)).json();
      if (discovery.issuer !== issuer) throw new Error('Issuer mismatch in discovery');
      const set = await (await fetch(discovery.jwks_uri)).json();
      cache = new Map(set.keys.filter((k: { kid?: string }) => k.kid).map((k: JsonWebKey & { kid: string }) => [k.kid, k]));
    }
    return cache.get(kid);
  };
}

export function protectedResourceMetadata(config: RemoteConfig) {
  return {
    resource: config.resource.href,
    authorization_servers: [config.issuer],
    scopes_supported: [config.scope],
    bearer_methods_supported: ['header'],
  };
}

export async function handleRequest(request: Request, remote?: RemoteAuth): Promise<Response> {
  const url = new URL(request.url);
  if (remote && request.method === 'GET' && (url.pathname === METADATA_PATH || url.pathname === `${METADATA_PATH}/mcp`)) {
    return Response.json(protectedResourceMetadata(remote.config));
  }
  if (url.pathname !== '/mcp') return new Response('Not found', { status: 404 });
  if (!['GET', 'POST', 'DELETE'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) return new Response('Forbidden origin', { status: 403 });
  if (remote) {
    const metadata = `scope="${remote.config.scope}", resource_metadata="${remote.config.resource.origin}${METADATA_PATH}/mcp"`;
    const status = await verifyBearer(request.headers.get('authorization'), remote.config, remote.keys);
    if (status === 401) {
      return new Response('Unauthorized', { status, headers: { 'www-authenticate': `Bearer ${metadata}` } });
    }
    if (status === 403) {
      return new Response('Forbidden', { status, headers: { 'www-authenticate': `Bearer error="insufficient_scope", ${metadata}` } });
    }
  }
  return mcp(request);
}

async function serve(req: IncomingMessage, res: ServerResponse, authority: string, base: string, remote?: RemoteAuth): Promise<void> {
  if (req.headers.host !== authority) {
    res.writeHead(403).end('Forbidden host');
    return;
  }
  try {
    const chunks: Buffer[] = [];
    let length = 0;
    for await (const chunk of req) {
      length += chunk.length;
      if (length > 1024 * 1024) {
        res.writeHead(413).end('Request too large');
        return;
      }
      chunks.push(chunk);
    }
    const request = new Request(`${base}${req.url}`, {
      method: req.method,
      headers: req.headers as HeadersInit,
      body: chunks.length ? Buffer.concat(chunks) : undefined,
    });
    const response = await handleRequest(request, remote);
    res.writeHead(response.status, Object.fromEntries(response.headers));
    if (response.body) {
      for await (const chunk of response.body) res.write(chunk);
    }
    res.end();
  } catch {
    res.writeHead(503).end('Manifest or MCP unavailable');
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const port = Number(process.env.STORYBOOK_MCP_PORT || '7613');
  if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Invalid STORYBOOK_MCP_PORT');
  const config = remoteConfig(process.env);
  // Local mode answers only loopback; remote mode only its public host, behind Traefik TLS.
  const remote = config && { config, keys: keycloakKeys(config.issuer) };
  const authority = config ? config.resource.host : `127.0.0.1:${port}`;
  const base = config ? config.resource.origin : `http://${authority}`;
  createServer((req, res) => void serve(req, res, authority, base, remote)).listen(port, config ? '0.0.0.0' : '127.0.0.1', () => {
    console.log(`Storybook docs MCP listening on ${config ? config.resource.href : `http://${authority}/mcp`}`);
  });
}
