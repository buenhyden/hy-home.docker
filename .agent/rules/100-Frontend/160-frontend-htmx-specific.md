---
trigger: always_on
glob: "**/*.{html,js}"
description: "HTMX: Hypermedia-driven UI, Partial Updates, and Attributes."
---
# HTMX Standards

## 1. Basic Interaction

- **Triggers**: Be explicit. `hx-trigger="click"`, `hx-trigger="keyup delay:500ms"`.
- **Swapping**: Use `hx-swap="outerHTML"` to replace the target fully, or `innerHTML` for children.

### Example: Search

**Good**

```html
<input 
  type="text" 
  name="q" 
  hx-get="/search" 
  hx-trigger="keyup changed delay:500ms" 
  hx-target="#results" 
/>
```

**Bad**

```html
<!-- spams server on every keypress -->
<input hx-get="/search" hx-trigger="keyup" /> 
```

## 2. Server Response

- **HTML Fragments**: The server MUST return partial HTML (e.g., `<li>Item</li>`), NOT a full page or JSON.
- **OOB**: Use Out-Of-Band swaps (`hx-swap-oob="true"`) to update other parts of the page (e.g., cart count).

### Example: Response

**Good** (Server returns)

```html
<div class="success">Saved!</div>
```

**Bad** (Server returns)

```json
{ "status": "success" } <!-- Client HTMX can't render JSON -->
```
