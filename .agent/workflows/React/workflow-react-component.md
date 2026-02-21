---
description: Create React component with TypeScript, tests, and Storybook documentation
---

1. **Determine component type**

    Decide on component category and structure.

    **Component types:**

    - **UI Component**: Reusable visual element (Button, Card, Input)
    - **Layout Component**: Structure/container (Header, Sidebar, Container)
    - **Feature Component**: Business logic (UserProfile, ProductList)
    - **Page Component**: Route-level component

    **Recommended location:**

    ```
    src/components/
    ├── ui/           # UI components
    ├── layout/       # Layout components
    └── features/     # Feature components
    ```

2. **Create component file**

    Create component file with TypeScript and proper naming.

    ```bash
    # For UI component
    mkdir -p src/components/ui/Button
    touch src/components/ui/Button/Button.tsx
    touch src/components/ui/Button/Button.test.tsx
    touch src/components/ui/Button/Button.stories.tsx
    touch src/components/ui/Button/index.ts
    ```

    **Follow naming convention:**

    - Component file: `ComponentName.tsx` (PascalCase)
    - Test file: `ComponentName.test.tsx`
    - Stories: `ComponentName.stories.tsx`
    - Export: `index.ts`

3. **Define component props interface**

    Create TypeScript interface for component props.

    Create `src/components/ui/Button/Button.tsx`:

    ```typescript
    import React from 'react';

    export interface ButtonProps {
      /** Button text content */
      children: React.ReactNode;
      /** Button visual variant */
      variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
      /** Button size */
      size?: 'sm' | 'md' | 'lg';
      /** Disabled state */
      disabled?: boolean;
      /** Click handler */
      onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
      /** Additional CSS classes */
      className?: string;
      /** HTML button type */
      type?: 'button' | 'submit' | 'reset';
    }
    ```

4. **Implement component logic**

    Write component implementation following React best practices.

    ```typescript
    import { cva, type VariantProps } from 'class-variance-authority';
    import { cn } from '@/lib/utils';

    const buttonVariants = cva(
      'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50',
      {
        variants: {
          variant: {
            primary: 'bg-blue-600 text-white hover:bg-blue-700',
            secondary: 'bg-gray-600 text-white hover:bg-gray-700',
            outline: 'border border-gray-300 bg-white hover:bg-gray-50',
            ghost: 'hover:bg-gray-100',
          },
          size: {
            sm: 'h-8 px-3 text-sm',
            md: 'h-10 px-4',
            lg: 'h-12 px-6 text-lg',
          },
        },
        defaultVariants: {
          variant: 'primary',
          size: 'md',
        },
      }
    );

    export function Button({
      children,
      variant,
      size,
      className,
      disabled,
      onClick,
      type = 'button',
    }: ButtonProps) {
      return (
        <button
          type={type}
          disabled={disabled}
          onClick={onClick}
          className={cn(buttonVariants({ variant, size }), className)}
        >
          {children}
        </button>
      );
    }
    ```

    Install dependencies:

    ```bash
    npm install class-variance-authority clsx tailwind-merge
    ```

5. **Create barrel export**

    Add index file for clean imports.

    Create `src/components/ui/Button/index.ts`:

    ```typescript
    export { Button } from './Button';
    export type { ButtonProps } from './Button';
    ```

6. **Write unit tests**

    Create comprehensive tests for component.

    Create `src/components/ui/Button/Button.test.tsx`:

    ```tsx
    import { render, screen, fireEvent } from '@testing-library/react';
    import { Button } from './Button';

    describe('Button', () => {
      it('renders with children', () => {
        render(<Button>Click me</Button>);
        expect(screen.getByText('Click me')).toBeInTheDocument();
      });

      it('calls onClick when clicked', () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>Click me</Button>);

        fireEvent.click(screen.getByText('Click me'));
        expect(handleClick).toHaveBeenCalledTimes(1);
      });

      it('does not call onClick when disabled', () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick} disabled>Click me</Button>);

        fireEvent.click(screen.getByText('Click me'));
        expect(handleClick).not.toHaveBeenCalled();
      });

      it('applies variant classes correctly', () => {
        const { rerender } = render(<Button variant="primary">Primary</Button>);
        expect(screen.getByRole('button')).toHaveClass('bg-blue-600');

        rerender(<Button variant="secondary">Secondary</Button>);
        expect(screen.getByRole('button')).toHaveClass('bg-gray-600');
      });

      it('applies size classes correctly', () => {
        const { rerender } = render(<Button size="sm">Small</Button>);
        expect(screen.getByRole('button')).toHaveClass('h-8');

        rerender(<Button size="lg">Large</Button>);
        expect(screen.getByRole('button')).toHaveClass('h-12');
      });

      it('merges custom className', () => {
        render(<Button className="custom-class">Button</Button>);
        expect(screen.getByRole('button')).toHaveClass('custom-class');
      });
    });
    ```

// turbo
7. **Run tests**

    Execute tests to verify component behavior.

    ```bash
    npm test -- Button.test
    ```

    Expected: All tests pass.

8. **Create Storybook stories**

    Document component with Storybook.

    Create `src/components/ui/Button/Button.stories.tsx`:

    ```tsx
    import type { Meta, StoryObj } from '@storybook/react';
    import { Button } from './Button';

    const meta = {
      title: 'UI/Button',
      component: Button,
      parameters: {
        layout: 'centered',
      },
      tags: ['autodocs'],
      argTypes: {
        variant: {
          control: 'select',
          options: ['primary', 'secondary', 'outline', 'ghost'],
        },
        size: {
          control: 'select',
          options: ['sm', 'md', 'lg'],
        },
        disabled: {
          control: 'boolean',
        },
      },
    } satisfies Meta<typeof Button>;

    export default meta;
    type Story = StoryObj<typeof meta>;

    export const Primary: Story = {
      args: {
        children: 'Primary Button',
        variant: 'primary',
      },
    };

    export const Secondary: Story = {
      args: {
        children: 'Secondary Button',
        variant: 'secondary',
      },
    };

    export const Outline: Story = {
      args: {
        children: 'Outline Button',
        variant: 'outline',
      },
    };

    export const Small: Story = {
      args: {
        children: 'Small Button',
        size: 'sm',
      },
    };

    export const Large: Story = {
      args: {
        children: 'Large Button',
        size: 'lg',
      },
    };

    export const Disabled: Story = {
      args: {
        children: 'Disabled Button',
        disabled: true,
      },
    };

    export const WithIcon: Story = {
      args: {
        children: (
          <>
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
            </svg>
            Button with Icon
          </>
        ),
      },
    };
    ```

9. **Add accessibility features**

    Ensure component is accessible.

    **ARIA attributes:**

    ```typescript
    export function Button({
      children,
      'aria-label': ariaLabel,
      'aria-describedby': ariaDescribedby,
      ...props
    }: ButtonProps & React.AriaAttributes) {
      return (
        <button
          aria-label={ariaLabel}
          aria-describedby={ariaDescribedby}
          {...props}
        >
          {children}
        </button>
      );
    }
    ```

    **Accessibility checklist:**

    - [ ] Keyboard accessible (Tab, Enter, Space)
    - [ ] Focus visible
    - [ ] Screen reader friendly
    - [ ] ARIA attributes when needed
    - [ ] Color contrast > 4.5:1

10. **Document component usage**

    Create usage documentation.

    Add to `Button.tsx` docstring:

    ```typescript
    /**
     * Button component with multiple variants and sizes.
     *
     * @example
     * ```tsx
     * <Button onClick={() => console.log('clicked')}>
     *   Click me
     * </Button>
     *
     * <Button variant="outline" size="sm">
     *   Small Outline
     * </Button>
     * ```
     */
    export function Button({ ... }) { ... }
    ```

11. **Use component in app**

    Import and use the component.

    ```tsx
    // src/App.tsx
    import { Button } from '@/components/ui/Button';

    function App() {
      const handleClick = () => {
        console.log('Button clicked!');
      };

      return (
        <div className="p-4">
          <Button onClick={handleClick}>
            Click Me
          </Button>

          <Button variant="outline" className="ml-2">
            Outline
          </Button>

          <Button variant="ghost" size="sm">
            Small Ghost
          </Button>
        </div>
      );
    }
    ```

12. **Create component variations**

    Add related component variants if needed.

    **IconButton.tsx:**

    ```typescript
    import { Button, ButtonProps } from './Button';

    interface IconButtonProps extends Omit<ButtonProps, 'children'> {
      icon: React.ReactNode;
      'aria-label': string;  // Required for accessibility
    }

    export function IconButton({ icon, ...props }: IconButtonProps) {
      return (
        <Button {...props} className="p-2">
          {icon}
        </Button>
      );
    }
    ```
