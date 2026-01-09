---
trigger: always_on
glob: "main.js,preload.js,**/*.ts"
description: "Electron: IPC Security, Context Isolation, and Auto-Update."
---
# Electron Standards

## 1. Security (Context Isolation)

- **Isolation**: `contextIsolation: true` is Mandatory.
- **Node Integration**: `nodeIntegration: false`. Do NOT expose Node.js to Renderer.

### Example: Preferences

**Good**

```javascript
webPreferences: {
  contextIsolation: true,
  nodeIntegration: false,
  preload: path.join(__dirname, 'preload.js')
}
```

**Bad**

```javascript
webPreferences: {
  nodeIntegration: true // Renderer can require('fs') and delete files
}
```

## 2. IPC (Inter-Process Communication)

- **Validation**: Validate ALL arguments in Main process handlers.
- **Channels**: Use specific channel names (`files:read`) not generic ones.

## 3. Auto-Update

- **Module**: Use `electron-updater` (from `electron-builder`).
- **Signing**: Code sign your app for macOS and Windows.
- **Differential**: Enable differential updates to reduce download size.

### Example: Update

**Good**

```typescript
import { autoUpdater } from 'electron-updater';
autoUpdater.checkForUpdatesAndNotify();
```

**Bad**

```text
// No auto-update: Users stuck on old versions forever
```
