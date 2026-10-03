import assert from 'node:assert/strict';
import { readFile, readdir } from 'node:fs/promises';
import { test } from 'node:test';

test('shared Button package has executable, typed and styled exports', async () => {
  const pkg = JSON.parse(await readFile(new URL('../packages/ui/package.json', import.meta.url)));
  assert.equal(pkg.private, true);
  assert.equal(pkg.license, 'UNLICENSED');
  assert.ok(pkg.exports['.'].types);
  assert.ok(pkg.exports['./styles.css']);
  const { Button } = await import('@hy-home/storybook-ui');
  assert.equal(typeof Button, 'function');
});

test('static build includes required component and docs manifests', async () => {
  const base = new URL('../storybook-static/manifests/', import.meta.url);
  const components = JSON.parse(await readFile(new URL('components.json', base)));
  const docs = JSON.parse(await readFile(new URL('docs.json', base)));
  const button = Object.values(components.components).find((entry) => entry.name === 'Button');
  assert.ok(button);
  assert.equal(button.error, undefined);
  assert.ok(button.reactDocgen?.props?.label);
  const cssFiles = (await readdir(new URL('../storybook-static/assets/', import.meta.url))).filter((name) => name.endsWith('.css'));
  const styles = (await Promise.all(cssFiles.map((name) => readFile(new URL(`../storybook-static/assets/${name}`, import.meta.url), 'utf8')))).join('\n');
  assert.match(styles, /storybook-button--primary/);
  assert.ok(docs.docs && typeof docs.docs === 'object');
});
