---
trigger: always_on
glob: "**/*.{html,jsx,tsx,vue,svelte,css}"
description: "Tailwind CSS: Utility-first design, mobile-first responsiveness, and accessibility."
---
# Tailwind CSS Best Practices

## 1. Core Principles

- **Utility-First**: Use standardized utility classes (`p-4`, `flex`) over custom CSS classes.
- **Mobile-First**: Define base styles for mobile, then use prefixes (`md:`, `lg:`) for larger screens.
- **Design System**: Stick to the config (spacing `1-4-8`, colors `blue-500`). Don't use arbitrary values (`w-[123px]`) unless absolutely necessary.

## 2. Organization & Architecture

- **Class Ordering**: `Layout -> Box Model -> Typography -> Visuals -> Misc`. Use `prettier-plugin-tailwindcss`.
- **Component Extraction**: Extract repeating patterns into React/Vue components, NOT `@apply` classes.
- **Dark Mode**: Use the `dark:` variant (`bg-white dark:bg-gray-900`).

## 3. Accessibility

- **Focus States**: Always define `focus-visible:` for interactive elements.
- **Screen Readers**: Use `sr-only` for visually hidden but accessible labels.
- **Contrast**: Ensure text colors meet WCAG contrast ratios.

### Example: Responsive & Accessible Component

#### Good

```jsx
<button className="
  flex items-center justify-center        <!-- Layout -->
  px-4 py-2                               <!-- Spacing -->
  font-medium text-white                  <!-- Typography -->
  bg-blue-600 rounded-lg                  <!-- Visuals -->
  hover:bg-blue-700 focus-visible:ring-2  <!-- States -->
  transition-colors duration-200          <!-- Misc -->
">
  Submit
</button>
```

#### Bad

```css
.btn-primary {
  @apply flex px-4 py-2 bg-blue-600 text-white hover:bg-blue-700;
}
```
