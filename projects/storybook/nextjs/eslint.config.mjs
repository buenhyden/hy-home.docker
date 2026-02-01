// For more info, see https://github.com/storybookjs/eslint-plugin-storybook#configuration-flat-config-format
import storybook from 'eslint-plugin-storybook';

import { defineConfig, globalIgnores } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';

const sharedIgnores = [
  '.agent/workflows/',
  '.agent/rules/',
  '.history/',
  '.git/',
  'node_modules/',
  'dist/',
  'coverage/',
  'storybook-static/',
  '*.min.js',
];

const nextDefaultIgnores = ['.next/**', 'out/**', 'build/**', 'next-env.d.ts'];

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  globalIgnores([...nextDefaultIgnores, ...sharedIgnores]),
  ...storybook.configs['flat/recommended'],
]);

export default eslintConfig;
