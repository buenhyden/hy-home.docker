import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const output = join(import.meta.dirname, '..', 'storybook-static');
const hashes: Record<string, string> = {};
for (const name of ['components.json', 'docs.json']) {
  const content = await readFile(join(output, 'manifests', name));
  hashes[name] = createHash('sha256').update(content).digest('hex');
}
await writeFile(join(output, 'revision.json'), `${JSON.stringify({
  sourceRevision: process.env.STORYBOOK_SOURCE_REVISION || 'uncommitted',
  manifestSha256: hashes,
})}\n`);
