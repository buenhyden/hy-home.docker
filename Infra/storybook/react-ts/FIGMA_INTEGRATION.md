# Figma Integration for Storybook (TypeScript)

This project uses `@storybook/addon-designs` to embed Figma designs directly into Storybook.

## How to Link Figma Files

1. **Install the Figma Plugin**: Ensure `@storybook/addon-designs` is installed and registered in `.storybook/main.ts`.
2. **Add Parameters to Stories**:
    In your `*.stories.tsx` (or `.ts`) file, you can type-safe your parameters.

    ```typescript
    import type { Meta, StoryObj } from '@storybook/react-vite';
    import { Button } from './Button';

    const meta = {
      title: 'Example/Button',
      component: Button,
      parameters: {
        design: {
          type: 'figma',
          url: 'https://www.figma.com/file/LKQ4FJ4bTnCSjedbRpk931/Sample-File',
        },
      },
    } satisfies Meta<typeof Button>;
    
    export default meta;
    type Story = StoryObj<typeof meta>;

    export const Primary: Story = {
      args: {
        primary: true,
        label: 'Button',
      },
    };
    ```

3. **View in Storybook**:
    Open the "Design" tab in the addon panel to see the live Figma frame.
