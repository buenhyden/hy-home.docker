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

export async function handleRequest(request: Request): Promise<Response> {
  const url = new URL(request.url);
  if (url.pathname !== '/mcp') return new Response('Not found', { status: 404 });
  if (!['GET', 'POST', 'DELETE'].includes(request.method)) return new Response('Method not allowed', { status: 405 });
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) return new Response('Forbidden origin', { status: 403 });
  return mcp(request);
}

async function serve(req: IncomingMessage, res: ServerResponse, port: number): Promise<void> {
  const authority = `127.0.0.1:${port}`;
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
    const request = new Request(`http://${authority}${req.url}`, {
      method: req.method,
      headers: req.headers as HeadersInit,
      body: chunks.length ? Buffer.concat(chunks) : undefined,
    });
    const response = await handleRequest(request);
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
  createServer((req, res) => void serve(req, res, port)).listen(port, '127.0.0.1', () => {
    console.log(`Storybook docs MCP listening on http://127.0.0.1:${port}/mcp`);
  });
}
