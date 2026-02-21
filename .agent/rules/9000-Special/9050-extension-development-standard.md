---
trigger: always_on
glob: "**/*.{js,ts,json}"
description: "Extension Development Standards: Enforces security, architectural, and performance standards for Chrome (MV3) and VS Code extensions."
---

# Extension Development Standards

- **Role**: Extension Integration Specialist
- **Purpose**: Define standards for building secure, performant, and reliable extensions for browsers and IDEs.
- **Activates When**: Developing or configuring Chrome (MV3) or VS Code extensions.

**Trigger**: always_on — Apply during the development and packaging of extensions.

## 1. Standards

### Principles

- **[REQ-EXT-01] Isolated Volatility**
  - Extension logic MUST handle the volatile lifecycle of service workers and background processes without assuming permanent state.
- **[REQ-EXT-02] Least Privilege**
  - Extensions MUST only request the minimum required permissions necessary for their documented functionality.
- **[REQ-EXT-03] Modern Purity (MV3)**
  - All new Chrome extensions MUST target Manifest V3 and utilize Service Workers over persistent background pages.

### Platform Specifics

| Platform | Core Security Constraint | State Management |
| --- | --- | --- |
| Chrome (MV3) | Strict CSP (No eval) | `chrome.storage.local` |
| VS Code | Webview CSP | `vscode.SecretStorage` |

### Must

- **[REQ-EXT-04] Typed Messaging**
  - Inter-process communication (IPC) and internal messaging MUST use strongly-typed payloads.
- **[REQ-EXT-05] Context Isolation**
  - Extensions MUST maintain strict isolation between content scripts and page-level JavaScript.
- **[REQ-EXT-06] Lazy Command Activation**
  - VS Code commands MUST be lazily loaded and avoid broad activation events (e.g., `*`).

### Must Not

- **[BAN-EXT-01] Global State Persistence**
  - Service workers MUST NOT rely on global variables for long-term state (use `chrome.storage`).
- **[BAN-EXT-02] External Code Execution**
  - Extensions MUST NOT load or execute remote code (e.g., from external CDNs) in accordance with MV3 security.

### Failure Handling

- **Stop Condition**: Stop execution if a message payload fails validation or matches a banned pattern.

## 2. Procedures

- **[PROC-EXT-01] Permission Review**
  - IF adding a new permission THEN MUST justify its necessity in the `manifest.json` comments.
- **[PROC-EXT-02] UI Handoff**
  - Prefer standard IDE UI components (QuickPick, TreeView) in VS Code over custom Webviews.

## 3. Examples

### Chrome MV3 Storage

```javascript
// Good: Persisting state in a service worker
async function saveState(data) {
  await chrome.storage.local.set({ appState: data });
}
```

## 4. Validation Criteria

- **[VAL-EXT-01] Manifest Compliance**
  - [ ] `manifest.json` passes the official Chrome validator and is MV3 compliant.
- **[VAL-EXT-02] Security Audit**
  - [ ] No `eval()` or unauthorized remote scripts are present in the package.
- **[VAL-EXT-03] Activation Precision**
  - [ ] VS Code activation events are scoped to specific commands or file types.
