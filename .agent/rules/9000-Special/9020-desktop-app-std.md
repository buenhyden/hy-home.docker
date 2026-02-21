---
trigger: always_on
glob: ["**/electron/**", "**/tauri/**", "**/src-tauri/**"]
description: "Desktop Application Standards: Enforces security isolation in Electron/Tauri and signed update mechanisms."
---

# Desktop Application Standards

- **Role**: Desktop Platform Architect
- **Purpose**: Define security and performance standards for building multi-platform desktop applications using Electron or Tauri frameworks.
- **Activates When**: Developing desktop UI components, configuring native interfaces, or managing desktop release pipelines.

**Trigger**: always_on — Apply during the implementation of desktop application features.

## 1. Standards

### Principles

- **[REQ-DSK-01] Strict Process Isolation**
  - Desktop applications MUST maintain strict isolation between the UI renderers and the system-level processes (Node.js/Rust).
- **[REQ-DSK-02] Verified Update Chains**
  - Update mechanisms MUST be cryptographically signed and verified to prevent malicious binary injection.
- **[REQ-DSK-03] Resource Stewardship**
  - Desktop apps MUST optimize for memory and CPU usage to prevent impacting host system performance.

### Framework Hardening

| Framework | Requirement ID | Critical Configuration |
| --- | --- | --- |
| Electron | [REQ-DSK-04] | `contextIsolation: true`, `nodeIntegration: false` |
| Tauri | [REQ-DSK-05] | `allowlist` restricted to required APIs |
| All | [REQ-DSK-06] | CSP (Content Security Policy) enabled |

### Must

- **[REQ-DSK-07] Preload Validation**
  - Electron apps MUST utilize `preload` scripts for bridge communication, exposing only necessary APIs via `contextBridge`.
- **[REQ-DSK-08] Capability Whitelisting**
  - Tauri applications MUST explicitly whitelist only the required native modules and file system paths in `tauri.conf.json`.
- **[REQ-DSK-09] Manifest Level Signing**
  - All distributed binaries MUST be signed with a valid Developer ID (Apple) or Authenticode (Windows) certificate.

### Must Not

- **[BAN-DSK-01] Remote Content Injection**
  - Do NOT load untrusted remote URLs directly into a renderer with native access enabled.
- **[BAN-DSK-02] Privileged File Access**
  - Desktop applications MUST NOT request root/Administrator privileges unless strictly required for system maintenance tasks.

### Failure Handling

- **Stop Condition**: Stop feature deployment if a security audit identifies `nodeIntegration` enabled in a renderer process.

## 2. Procedures

- **[PROC-DSK-01] Security Surface Review**
  - IF adding a new native bridge API THEN MUST conduct a threat model review of the exposed functionality.
- **[PROC-DSK-02] Performance Baseline**
  - Verify quarterly that the app's idle memory usage remains within the project's defined budget.

## 3. Examples

### Secure contextBridge (Electron)

```javascript
// preload.js
contextBridge.exposeInMainWorld('myAPI', {
  doThing: () => ipcRenderer.invoke('do-thing')
});
```

## 4. Validation Criteria

- **[VAL-DSK-01] CSP Compliance**
  - [ ] Every renderer process implements a restrictive Content Security Policy.
- **[VAL-DSK-02] Injection Pass**
  - [ ] Automated tests confirm that untrusted UI strings cannot execute native bridge commands.
- **[VAL-DSK-03] Update Integrity**
  - [ ] Binary validation confirms that the update manifest is signed with the project's private key.
