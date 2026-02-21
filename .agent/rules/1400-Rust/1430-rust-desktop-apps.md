---
trigger: always_on
glob: "**/*.{js,ts,rs,json,toml}"
description: "Desktop Application Standards: Enforces security and architectural constraints for Electron and Tauri development."
---

# Desktop Application Standards

- **Role**: Desktop Integration Architect
- **Purpose**: Define security and architectural standards for cross-platform desktop applications.
- **Activates When**: Developing or configuring Electron or Tauri applications.

**Trigger**: always_on — Apply during desktop application development.

## 1. Standards

### Principles

- **[REQ-DSK-01] Isolated Execution**
  - Desktop applications MUST maintain strict isolation between the UI renderer and system-level processes.
- **[REQ-DSK-02] Least Privilege Scoping**
  - Filesystem and API access MUST be restricted to the minimum required scope.
- **[REQ-DSK-03] Secure Inter-Process Communication (IPC)**
  - All IPC handlers MUST validate arguments and use specific, non-vague channel names.

### Framework Constraints

| Framework | Security Requirement | Priority |
| --- | --- | --- |
| Electron | `contextIsolation: true` | Critical |
| Electron | `nodeIntegration: false` | Critical |
| Tauri | Filystem `scope` limited | Critical |

### Must

- **[REQ-DSK-04] Preload Gatekeeping**
  - Electron apps MUST use preload scripts and `contextBridge` to expose limited APIs.
- **[REQ-DSK-05] Command Validation**
  - Tauri commands MUST return `Result<T, E>` to ensure structured error handling.
- **[REQ-DSK-06] Validated IPC**
  - Every IPC message MUST be validated for type and content authenticity on the receiving side.

### Must Not

- **[BAN-DSK-01] Node Direct Exposure**
  - Electron apps MUST NOT expose the full `node` environment directly to the renderer.
- **[BAN-DSK-02] Unscoped FS Access**
  - Tauri apps MUST NOT use permissive `*` filesystem scopes without justification.

### Failure Handling

- **Stop Condition**: Stop execution if an unvalidated IPC message is received from the renderer.

## 2. Procedures

- **[PROC-DSK-01] Security Audit**
  - IF modifying `webPreferences` or `tauri.conf.json` THEN MUST re-verify isolation settings.
- **[PROC-DSK-02] Update Management**
  - Use `electron-updater` with mandatory code signing for production releases.

## 3. Examples

### Secure Electron Config

```javascript
webPreferences: {
  contextIsolation: true,
  nodeIntegration: false,
  preload: path.join(__dirname, 'preload.js')
}
```

## 4. Validation Criteria

- **[VAL-DSK-01] Isolation Verification**
  - [ ] Renderer has zero direct access to `process` or `require`.
- **[VAL-DSK-02] Scope Compliance**
  - [ ] Filesystem access is limited to `$APP_DATA/*` or specific user-selected paths.
- **[VAL-DSK-03] Type Safety**
  - [ ] All IPC communications use strongly typed payloads.
