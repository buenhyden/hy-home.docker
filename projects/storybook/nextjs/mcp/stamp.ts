import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const root = join(import.meta.dirname, '..');
const output = join(root, 'storybook-static');
const sha256 = (content: Buffer) => createHash('sha256').update(content).digest('hex');
const hashes: Record<string, string> = {};
for (const name of ['components.json', 'docs.json']) {
  hashes[name] = sha256(await readFile(join(output, 'manifests', name)));
}
const ui = JSON.parse(await readFile(join(root, 'packages', 'ui', 'package.json'), 'utf8'));
// The image build passes the commit it exported; a local build stays 'uncommitted'.
await writeFile(join(output, 'revision.json'), `${JSON.stringify({
  sourceRevision: process.env.STORYBOOK_SOURCE_REVISION || 'uncommitted',
  lockfileSha256: sha256(await readFile(join(root, 'package-lock.json'))),
  uiPackage: { name: ui.name, version: ui.version },
  manifestSha256: hashes,
})}\n`);
