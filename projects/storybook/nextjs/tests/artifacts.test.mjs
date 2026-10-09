import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir } from 'node:fs/promises';
import { test } from 'node:test';

test('shared UI package has executable, typed and styled exports', async () => {
  const pkg = JSON.parse(await readFile(new URL('../packages/ui/package.json', import.meta.url)));
  assert.equal(pkg.private, true);
  assert.equal(pkg.license, 'UNLICENSED');
  assert.ok(pkg.exports['.'].types);
  assert.ok(pkg.exports['./styles.css']);
  const { AsyncState, Button } = await import('@hy-home/storybook-ui');
  assert.equal(typeof Button, 'function');
  assert.equal(typeof AsyncState, 'function');
});

test('static build includes required component and docs manifests', async () => {
  const base = new URL('../storybook-static/manifests/', import.meta.url);
  const components = JSON.parse(await readFile(new URL('components.json', base)));
  const docs = JSON.parse(await readFile(new URL('docs.json', base)));
  // Only the reviewed package components reach the manifest; no example UI.
  const names = Object.values(components.components).map((entry) => entry.name).sort();
  assert.deepEqual(names, ['AsyncState', 'Button']);
  for (const entry of Object.values(components.components)) assert.equal(entry.error, undefined);
  const button = Object.values(components.components).find((entry) => entry.name === 'Button');
  assert.ok(button.reactDocgen?.props?.variant);
  assert.ok(button.reactDocgen?.props?.loading);
  const cssFiles = (await readdir(new URL('../storybook-static/assets/', import.meta.url))).filter((name) => name.endsWith('.css'));
  const styles = (await Promise.all(cssFiles.map((name) => readFile(new URL(`../storybook-static/assets/${name}`, import.meta.url), 'utf8')))).join('\n');
  assert.match(styles, /hy-button--primary/);
  assert.match(styles, /--hy-color-primary-base/);
  assert.match(styles, /prefers-reduced-motion/);
  assert.ok(docs.docs && typeof docs.docs === 'object');
});

test('revision.json ties the static output to its lockfile and UI package', async () => {
  const revision = JSON.parse(await readFile(new URL('../storybook-static/revision.json', import.meta.url)));
  const lockfile = await readFile(new URL('../package-lock.json', import.meta.url));
  const ui = JSON.parse(await readFile(new URL('../packages/ui/package.json', import.meta.url)));
  assert.equal(revision.lockfileSha256, createHash('sha256').update(lockfile).digest('hex'));
  assert.deepEqual(revision.uiPackage, { name: ui.name, version: ui.version });
  assert.ok(revision.sourceRevision === 'uncommitted' || /^[0-9a-f]{40}$/.test(revision.sourceRevision));
});
