---
trigger: always_on
glob: "**/*.{js,html}"
description: "jQuery Standards: Enforces selector performance, event delegation, and modern gradual migration path."
---

# jQuery Standards

- **Role**: Legacy Modernization Engineer
- **Purpose**: Define standards for maintaining and gradually modernizing legacy jQuery codebases.
- **Activates When**: Editing JavaScript or HTML files that utilize the jQuery library.

**Trigger**: always_on — Apply during the maintenance of jQuery-dependent assets.

## 1. Standards

### Principles

- **[REQ-JQUERY-01] Performance thru Caching**
  - jQuery selectors MUST be cached in variables (prefixed with `$`) if used more than once to avoid redundant DOM traversal.
- **[REQ-JQUERY-02] Event Delegation**
  - Use `.on()` with delegation for elements that may be added dynamically to the DOM.
- **[REQ-JQUERY-03] Modern Preference**
  - For all new logic where feasible, native Vanilla JS solutions MUST be prioritized over jQuery equivalents.

### Modernization Mapping

| jQuery Method | Vanilla Alternative | Recommendation |
| --- | --- | --- |
| `$('.item')` | `document.querySelectorAll('.item')` | Use for simple selections |
| `$.ajax()` | `fetch()` | **Primary Choice for new API calls** |
| `.addClass()` | `.classList.add()` | Use for single element manipulation |

### Must

- **[REQ-JQUERY-04] Selector Specificity**
  - Selectors MUST be as specific as possible (using IDs) to optimize Chrome's selector engine performance.
- **[REQ-JQUERY-05] Promise-Style AJAX**
  - All `$.ajax()` calls MUST use the Promise-based methods (`.done()`, `.fail()`) instead of success/error callbacks.
- **[REQ-JQUERY-06] Explicit Cleanup**
  - Event listeners on large DOM trees MUST be explicitly unbound using `.off()` before element removal to prevent memory leaks.

### Must Not

- **[BAN-JQUERY-01] Context-Free Selectors**
  - Universal selectors (e.g., `$('*')`) or overly broad selectors SHOULD NOT be used in performance-sensitive paths.
- **[BAN-JQUERY-02] Mixed DOM Manipulation**
  - Avoid mixing direct native DOM manipulation (e.g., `innerHTML`) with jQuery's `.html()` on the same element to prevent state desync.

### Failure Handling

- **Stop Condition**: Stop execution if a selector returns an empty set in a critical application path (e.g., form submission).

## 2. Procedures

- **[PROC-JQUERY-01] Migration Path**
  - IF modifying a legacy function THEN MUST check if it can be reasonably refactored to Vanilla JS in < 15 minutes.
- **[PROC-JQUERY-02] Version Audit**
  - Ensure the project is using the latest stable 3.x version of jQuery to avoid known security vulnerabilities.

## 3. Examples

### Efficient Selection

```javascript
const $container = $('#app-container');
const $items = $container.find('.item'); // Scoped selection is faster
```

## 4. Validation Criteria

- **[VAL-JQUERY-01] Leak Prevention**
  - [ ] All dynamic event listeners are properly delegated or cleaned up.
- **[VAL-JQUERY-02] Asset Analysis**
  - [ ] Bundle analysis shows jQuery is only included in the non-modern variant of the build if possible.
- **[VAL-JQUERY-03] Functional Parity**
  - [ ] Polyfills are present for any Vanilla JS replacements used in the migration path.
