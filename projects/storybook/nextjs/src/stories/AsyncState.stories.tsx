import type { Meta, StoryObj } from '@storybook/nextjs-vite';

import { expect, fn, userEvent, within } from 'storybook/test';

import { AsyncState } from '../../packages/ui/src/AsyncState';

const meta = {
  title: 'UI/AsyncState',
  component: AsyncState,
  tags: ['autodocs'],
  args: { status: 'loading' },
} satisfies Meta<typeof AsyncState>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Loading: Story = {
  play: async ({ canvasElement }) => {
    const region = within(canvasElement).getByRole('status');
    await expect(region).toHaveAttribute('aria-busy', 'true');
    await expect(region).toHaveTextContent('Loading');
  },
};

export const Empty: Story = {
  args: { status: 'empty', message: 'No dashboards have been created.' },
  play: async ({ canvasElement }) => {
    await expect(within(canvasElement).getByRole('status')).not.toHaveAttribute('aria-busy');
  },
};

export const Error: Story = {
  args: { status: 'error', message: 'The service answered 500.', onRetry: fn() },
  play: async ({ args, canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByRole('alert')).toHaveTextContent('Something went wrong');
    await userEvent.click(canvas.getByRole('button', { name: 'Try again' }));
    await expect(args.onRetry).toHaveBeenCalledOnce();
  },
};

/** A 403 is not retried: retrying cannot grant access. */
export const Forbidden: Story = {
  args: { status: 'forbidden', message: 'Ask an administrator for access.', onRetry: fn() },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByRole('alert')).toHaveTextContent('You do not have access');
    await expect(canvas.queryByRole('button')).toBeNull();
  },
};

export const Timeout: Story = {
  args: { status: 'timeout', onRetry: fn(), retryLabel: 'Retry now' },
  play: async ({ args, canvasElement }) => {
    const button = within(canvasElement).getByRole('button', { name: 'Retry now' });
    await userEvent.tab();
    await expect(button).toHaveFocus();
    await userEvent.keyboard('{Enter}');
    await expect(args.onRetry).toHaveBeenCalledOnce();
  },
};

export const Ready: Story = {
  args: { status: 'ready', children: <p>Loaded content</p> },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByText('Loaded content')).toBeVisible();
    await expect(canvas.queryByRole('status')).toBeNull();
  },
};

/** At a 320px phone width a long message wraps instead of overflowing. */
export const Narrow: Story = {
  args: {
    status: 'error',
    message: 'https://storybook.example.test/a/very/long/unbroken/path/that/would/overflow',
    onRetry: fn(),
  },
  decorators: [(Story) => <div style={{ width: 320 }}><Story /></div>],
  play: async ({ canvasElement }) => {
    const region = within(canvasElement).getByRole('alert');
    await expect(region.scrollWidth).toBeLessThanOrEqual(region.clientWidth);
    await expect(region.getBoundingClientRect().width).toBeLessThanOrEqual(320);
  },
};
