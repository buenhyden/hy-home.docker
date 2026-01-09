---
trigger: always_on
glob: "**/*.{css,scss,sass,less}"
description: "CSS Best Practices: BEM, Mobile-First, and Performance optimizations."
---
# CSS Standards

## 1. Architecture & Organization

- **Methodology**: Use **BEM** (Block-Element-Modifier), **CSS Modules**, or **Styled Components** to prevent global namespace pollution.
  - **BEM**:
    - `block`
  - `block__element`
  - `block--modifier`
- **File Structure** (ITCSS-inspired):
  - `base/` (Reset, Typography)
  - `components/` (Buttons, Cards)
  - `layout/` (Grid, Header)
  - `utilities/` (Spacing, Colors)

## 2. Responsive Design

- **Mobile-First**: Define base styles for mobile, then use `min-width` media queries to enhance for tablet/desktop.
- **Relative Units**:
  - `rem` for font-sizes and spacing (accessibility).
  - `%`, `vw`, `vh` for layout dimensions.
  - Avoid fixed `px` for containers.
- **Container Queries**: Use `@container` for component-level responsiveness where supported.

## 3. Styling Best Practices

- **Avoid ID Selectors**: `#id` has too high specificity. Use classes `.class`.
- **Avoid `!important`**: Only use for utility classes that *must* override (e.g., `u-hidden`).
- **Variables**: Use **CSS Custom Properties** (`--var-name`) for tokens (colors, fonts, spacing).
- **Z-Index**: maintain a `z-index` scale/map in variables to avoid conflicting layers.

## 4. Performance

- **Animations**: Animate only `transform` and `opacity` (compositor-only properties). Avoid animating `width`, `height`, `margin`.
- **Selectors**: Keep selectors shallow (max 3 levels deep in SCSS nesting).

## 5. Accessibility

- **Focus**: ensure `:focus` styles are visible.
- **Contrast**: Meet WCAG AA standards.
- **Motion**: Respect `prefers-reduced-motion`.
