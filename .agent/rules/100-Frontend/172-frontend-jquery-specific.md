---
trigger: always_on
glob: "**/*.{js,html}"
description: "jQuery: Modern Usage, Event Handling, AJAX, and Migration."
---
# jQuery Standards

## 1. Modern Alternatives

- **Prefer Vanilla**: For new projects, prefer vanilla JS or modern frameworks.
- **Legacy Support**: jQuery is acceptable for maintaining legacy codebases.

### Example: Vanilla vs jQuery

**Good (Modern)**

```javascript
document.querySelectorAll('.item').forEach(el => el.classList.add('active'));
```

**Good (jQuery Legacy)**

```javascript
$('.item').addClass('active');
```

## 2. Selector Performance

- **Cache Selectors**: Store jQuery objects in variables.
- **Specific Selectors**: Use IDs and classes, avoid universal selectors.

### Example: Caching

**Good**

```javascript
const $items = $('.item');
$items.addClass('active');
$items.on('click', handler);
```

**Bad**

```javascript
$('.item').addClass('active');
$('.item').on('click', handler);  // Querying DOM twice
```

## 3. Event Handling

- **on()**: Use delegated events for dynamic content.
- **off()**: Unbind events to prevent memory leaks.

### Example: Delegation

**Good**

```javascript
$('#container').on('click', '.dynamic-button', function() {
    // Works for dynamically added buttons
});
```

**Bad**

```javascript
$('.dynamic-button').click(function() {
    // Won't work for buttons added later
});
```

## 4. AJAX

- **$.ajax()**: Use with Promise-style `.done()`, `.fail()`, `.always()`.
- **Fetch API**: For new code, prefer native `fetch()`.

### Example: AJAX

**Good**

```javascript
$.ajax({
    url: '/api/data',
    method: 'GET'
}).done(data => console.log(data))
  .fail(err => console.error(err));
```

## 5. Migration Path

- **jQuery 3.x**: Migrate to latest jQuery 3.x.
- **Gradual**: Gradually replace with vanilla JS.
