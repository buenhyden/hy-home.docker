---
version: "0.2.0"
name: "hy-home shared UI"
description: "Quiet, legible controls for internal developer tools."
colors:
  primary-base: "#3d43a8"
  primary-hover: "#2f3486"
  surface-base: "#ffffff"
  surface-muted: "#f4f5f7"
  text-primary: "#1f2328"
  text-secondary: "#57606a"
  text-on-primary: "#ffffff"
  border-subtle: "#d0d7de"
  state-error: "#b42318"
  state-warning: "#8a5a00"
  focus-ring: "#1f6feb"
typography:
  body-md:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 14px
    lineHeight: 1.5
    fontWeight: 400
  heading-md:
    fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: 18px
    lineHeight: 1.3
    fontWeight: 600
rounded:
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    background: colors.primary-base
    foreground: colors.text-on-primary
    radius: rounded.md
    paddingInline: spacing.md
  button-secondary:
    background: colors.surface-base
    foreground: colors.text-primary
    border: colors.border-subtle
    radius: rounded.md
    paddingInline: spacing.md
  async-state:
    background: colors.surface-muted
    foreground: colors.text-primary
    border: colors.border-subtle
    radius: rounded.md
    padding: spacing.md
---

# Design System

## Authority

This file is the design-system authority for hy-home UI. Its values are
implemented as CSS custom properties in
`projects/storybook/nextjs/packages/ui/src/styles.css` (`--hy-color-*`,
`--hy-font-*`, `--hy-rounded-*`, `--hy-spacing-*`); a test fails when the two
differ. Components read only these tokens. A value not expressible here needs
a recorded deviation in the owning Spec.

## Brand & Style

Internal developer tools: quiet surfaces, one clear primary action per view,
and states that say what happened and what the reader can do next.

## Colors

| Token | Use |
| --- | --- |
| `primary-base`, `primary-hover` | The single main action of a view |
| `surface-base`, `surface-muted` | Page and panel backgrounds |
| `text-primary`, `text-secondary`, `text-on-primary` | Body, supporting and on-primary text |
| `border-subtle` | Control and panel borders |
| `state-error`, `state-warning` | Failure and timeout headings |
| `focus-ring` | The 3px keyboard focus outline |

Every text colour meets WCAG AA contrast on the surface it is used on.

## Typography

`body-md` for body and controls, `heading-md` for state headings.

## Components

| Component | API | States |
| --- | --- | --- |
| `Button` | `label`, `variant` (`primary`, `secondary`), `size`, `type`, `disabled`, `loading`, `onClick` | default, hover, focus-visible, disabled, loading |
| `AsyncState` | `status`, `title`, `message`, `onRetry`, `retryLabel`, `children` | loading, empty, error, forbidden (403), timeout, ready |

Composition: a view renders one `AsyncState` per request and its content only
when the status is `ready`. Retry is offered for `error` and `timeout` only.

## Accessibility and Motion

Controls are reachable by keyboard, show the focus ring and work with Enter
and Space. Failures are alerts; loading and empty results are status
messages. Animation stops under `prefers-reduced-motion: reduce`. Layouts wrap
at 320px without horizontal overflow.

## Versioning

`version` follows `@hy-home/storybook-ui`. A removed or renamed token or
component prop is a breaking change and bumps the version.
