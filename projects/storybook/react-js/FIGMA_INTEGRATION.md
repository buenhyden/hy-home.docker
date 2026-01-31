# Figma Integration for Storybook

This project uses `@storybook/addon-designs` to embed Figma designs directly into Storybook.

## How to Link Figma Files

1. **Install the Figma Plugin**: Ensure `@storybook/addon-designs` is installed and registered in `.storybook/main.js`.
2. **Add Parameters to Stories**:
    In your `*.stories.js` file, add the `design` parameter to the story object or the default export.

    ```javascript
    export const Primary = {
      args: {
        primary: true,
        label: 'Button',
      },
      parameters: {
        design: {
          type: 'figma',
          url: 'https://www.figma.com/file/LKQ4FJ4bTnCSjedbRpk931/Sample-File', // Replace with your Figma File URL
        },
      },
    };
    ```

3. **View in Storybook**:
    Open the "Design" tab in the addon panel to see the live Figma frame.

## Automation

To synchronize design tokens or assets more deeply, consider using tools like **Specify** or **Tokens Studio for Figma**, which can export JSON tokens that this project can consume.
