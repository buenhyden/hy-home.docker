/** @type { import('@storybook/react').Preview } */
const preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    // Accessibility configuration
    a11y: {
      // Optional: configuration for the a11y addon
      // element: '#root',
      // manual: false,
    },
    // Backgrounds for theming visualization
    backgrounds: {
      default: "light",
      values: [
        {
          name: "light",
          value: "#ffffff",
        },
        {
          name: "dark",
          value: "#333333",
        },
      ],
    },
  },
};

export default preview;
