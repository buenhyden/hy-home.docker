---
trigger: always_on
glob: "**/*.{html,css,scss,js,ts,jsx,tsx,vue,svelte}"
description: "Frontend Core: Accessibility, Styling Architecture, State, and Performance."
---
# Frontend General Standards

## 1. Semantic HTML & Accessibility

### Core Semantics

- **Landmarks**: Use `<header>`, `<main>`, `<footer>`, `<nav>`, `<aside>` to define page structure.
- **Forms**: Always wrap inputs in `<form>` and label them with `<label>` (explicit linkage via `htmlFor`/`id`).

- **Semantics First**: Use `<button>` for actions, `<a>` for navigation.
- **ARIA**: Use ARIA labels *only* when semantic tags are insufficient.
- **Keyboard**: Ensure all interactive elements are focusable and usable via keyboard.

### Example: Accessibility

**Good**

```html
<button onClick={save}>Save</button>
```

**Bad**

```html
<!-- Not focusable, no Role -->
<div onClick={save}>Save</div>
```

## 2. Component Design principles

- **Pure Props**: Data flows down, events bubble up.
- **Custom Hooks**: Extract logic to `useSomething()` when a component exceeds ~100 lines.
- **Dumb vs Smart**: Separate "Presentational" (UI only) from "Container" (Data fetching) components.

## 3. State Management

- **Local First**: Use `useState` or `useReducer` for component-local state.
- **Context API**: Use for global UI state (Theme, User), NOT for high-frequency data (use Zustand/Redux for that).
- **Immutability**: Always create new references for updates.

## 4. Performance Checklist

- **CLS (Shift)**: Always set `width`/`height` on images/video.
- **Code Splitting**: Use `React.lazy` or dynamic imports for routes.
- **Tree Shaking**: Import specific functions, not whole libraries (`import { map } from 'lodash'`).
