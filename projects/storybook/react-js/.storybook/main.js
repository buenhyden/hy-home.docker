/** @type { import('@storybook/react-vite').StorybookConfig } */
const config = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-interactions",
    "@storybook/addon-a11y",
    "@storybook/addon-designs",
    "@storybook/addon-vitest",
    "@storybook/addon-docs",
    "@storybook/addon-onboarding",
    "@chromatic-com/storybook",
  ],
  framework: "@storybook/react-vite",
  docs: {
    autodocs: "tag",
  },
};
export default config;
