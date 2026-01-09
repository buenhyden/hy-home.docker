---
trigger: always_on
glob: "**/*.js,**/*.ts"
description: "D3.js: Data-Driven Documents Best Practices."
---
# D3.js Standards

## 1. Modularity

- **Import Specifics**: Do NOT import the entire `d3` object. Import only needed modules (`d3-selection`, `d3-scale`, etc.) to enable tree-shaking.

### Example: Imports

**Good**

```javascript
import { select } from 'd3-selection';
import { scaleLinear } from 'd3-scale';
```

**Bad**

```javascript
import * as d3 from 'd3';
```

## 2. Structure using Joins

- **Join Pattern**: ALWAYS use the `.join()` pattern (Enter/Update/Exit) introduced in D3v5+. It is cleaner and more concise than manual `enter().append()... merge()`.

### Example: Join

**Good**

```javascript
svg.selectAll('circle')
  .data(data, d => d.id)
  .join(
    enter => enter.append('circle').attr('r', 0).call(e => e.transition().attr('r', 5)),
    update => update.call(u => u.transition().attr('cx', d => d.x)),
    exit => exit.remove()
  );
```

## 3. Sizing

- **Responsive**: Use `viewBox` and `preserveAspectRatio` for responsive SVGs. Avoid hardcoding pixel width/height directly in a way that breaks on resize.

## 4. Accessibility

- **ARIA**: Add `title` and `desc` tags inside your SVG and ARIA labels (`aria-label`, `role="img"`) to ensure charts are accessible.
