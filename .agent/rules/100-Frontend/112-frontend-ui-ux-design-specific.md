---
trigger: always_on
glob: "**/*.{css,scss,html,jsx,tsx,vue}"
description: "UI/UX Design: Visual hierarchy, accessibility (WCAG), and responsive best practices."
---
# UI/UX Design Standards

## 1. Visual Hierarchy

- **Contrast**: Use size, color, and weight to guide attention (H1 > H2 > Body).
- **Whitespace**: Use generous whitespace to reduce cognitive load.
- **Consistency**: Stick to a defined color palette and typography scale.

## 2. Accessibility (A11y)

- **Contrast Ratio**: AA standard (4.5:1) for text.
- **Semantic HTML**: Use `<button>`, `<nav>`, `<main>` over `<div>`.
- **Alt Text**: All images must have meaningful `alt` attributes.
- **Keyboard**: Ensure all interactive elements are reachable via Tab.

## 3. Responsiveness

- **Mobile-First**: Design for small screens first, then scale up.
- **Touch Targets**: Min 44x44px for clickable elements on mobile.
- **Fluid Layouts**: Use relative units (`rem`, `%`) over fixed pixels (`px`).

## 4. Performance UX

- **CLS (Shift)**: Reserve space for images/ads to prevent layout shifts.
- **LCP (Loading)**: optimize largest content paint (lazy load below fold, eager above).
- **Feedback**: Immediate visual feedback for all interactions (hover, active, focus).

### Example: Accessible Button

#### Good

```jsx
<button 
  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
  aria-label="Submit form"
>
  Submit
</button>
```

#### Bad

```jsx
<div onClick={submit}>Submit</div> <!-- Not semantic, no keyboard support -->
```
