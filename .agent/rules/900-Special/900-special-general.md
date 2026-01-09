---
trigger: always_on
glob: "**/*"
description: "Special Domains: Sandboxing, Resource Constraints, and Environment Checks."
---
# Special Domains General Standards

## 1. Environment Checks

- **Runtime detection**: Verify API availability before use.
- **Fail Gracefully**: If API is missing, show UI warning, don't crash.

### Example: detection

**Good**

```javascript
if (typeof chrome !== 'undefined' && chrome.runtime) { ... }
```

**Bad**

```javascript
chrome.runtime.sendMessage(...) // Throws ReferenceError in normal browser
```

## 2. Resource Constraints

- **Lightweight**: Extensions/Scrapers run in limited environments. Minimize dependencies.
- **Cleanup**: Remove event listeners and timers when context is destroyed.

### Example: Cleanup

**Good**

```javascript
useEffect(() => {
  const listener = ...;
  return () => listener.remove();
}, []);
```

**Bad**

```javascript
setInterval(...) // Runs forever, leaks memory
```
