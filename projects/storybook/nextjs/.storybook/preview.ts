import '@hy-home/storybook-ui/styles.css';

import type { Preview } from '@storybook/nextjs-vite';

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },

    // Any accessibility violation fails the story test run.
    a11y: { test: 'error' },
  },
};

export default preview;
