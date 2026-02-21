---
description: Build and test components in isolation with Storybook
---

1. **Install Storybook**:
   - Initialize Storybook in your project.
   // turbo
   - Run `npx storybook@latest init`

2. **Create Your First Story**:
   - Create a story file next to your component.

   ```tsx
   // components/Button.stories.tsx
   import type { Meta, StoryObj } from '@storybook/react';
   import { Button } from './Button';

   const meta: Meta<typeof Button> = {
     title: 'Components/Button',
     component: Button,
     tags: ['autodocs'],
   };

   export default meta;
   type Story = StoryObj<typeof Button>;

   export const Primary: Story = {
     args: {
       variant: 'primary',
       children: 'Click me',
     },
   };

   export const Secondary: Story = {
     args: {
       variant: 'secondary',
       children: 'Click me',
     },
   };
   ```

3. **Run Storybook**:
   - Start the dev server.
   // turbo
   - Run `npm run storybook`

4. **Add Interactions**:
   - Test component behavior.

   ```tsx
   import { userEvent, within } from '@storybook/testing-library';
   import { expect } from '@storybook/jest';

   export const Clicked: Story = {
     play: async ({ canvasElement }) => {
       const canvas = within(canvasElement);
       await userEvent.click(canvas.getByRole('button'));
       await expect(canvas.getByText('Clicked!')).toBeInTheDocument();
     },
   };
   ```

5. **Build Static Storybook**:
   - Deploy as a static site.
   // turbo
   - Run `npm run build-storybook`

6. **Pro Tips**:
   - Use Chromatic for visual regression testing.
   - Document props with JSDoc comments.
   - Use args for interactive controls in Storybook UI.
