---
trigger: always_on
glob: ["**/*.{js,ts,tsx,jsx}"]
description: "Browser API Standards: Enforces modern storage, observers, and hardware interface patterns with progressive enhancement."
---

# Browser API Standards

- **Role**: Web Platform Engineer
- **Purpose**: Define standards for utilizing native browser APIs to build high-performance, resilient, and progressively enhanced web applications.
- **Activates When**: Implementing storage logic (LocalStorage/IndexedDB), using DOM observers, or interacting with hardware APIs (Geolocation, Notifications).

**Trigger**: always_on — Apply during the implementation of native browser-based features.

## 1. Standards

### Principles

- **[REQ-BRW-01] Feature-Detection First**
  - All modern browser APIs MUST be utilized behind an explicit feature detection check to ensure graceful fallback for legacy browsers.
- **[REQ-BRW-02] Progressive Enhancement**
  - Core functionality MUST NOT depend on advanced browser APIs (e.g., WebRTC) if a simpler, server-side-driven fallback exists.
- **[REQ-BRW-03] Resource Stewardship**
  - Observers (Intersection, Mutation, Resize) MUST be explicitly disconnected when no longer needed to prevent memory leaks.

### API Usage Baseline

| API | Requirement ID | Critical Implementation |
| --- | --- | --- |
| Storage | [REQ-BRW-04] | `localStorage` (Sync) / `IndexedDB` (Big Data) |
| Observers | [REQ-BRW-05] | `disconnect()` on component unmount |
| Workers | [REQ-BRW-06] | Offload heavy computations from UI thread |
| Hardward | [REQ-BRW-07] | Explicit user permission prompts |

### Must

- **[REQ-BRW-08] Secure Storage Handling**
  - Sensitive data (Tokens, Personal Info) MUST NOT be stored in `localStorage` in plain text. Use appropriate encryption or session-bound storage.
- **[REQ-BRW-09] Explicit Cleanup Lifecycle**
  - Every observer and event listener attached to the `window` or `document` MUST be disconnected in the component's unmount/teardown phase.
- **[REQ-BRW-10] Non-Blocking Path Execution**
  - Heavy DOM manipulations detected by `MutationObserver` MUST be batched to prevent recursive layout trashing.

### Must Not

- **[BAN-BRW-01] Synchronous Storage Blocking**
  - Avoid large-scale reads/writes to `localStorage` inside the main rendering loop; utilize `sessionStorage` or `IndexedDB` for larger datasets.
- **[BAN-BRW-02] Unsolicited Permission Prompts**
  - Do NOT trigger Geolocation or Notification permission prompts immediately upon page load. Always trigger based on a user action.

### Failure Handling

- **Stop Condition**: Stop feature execution if a browser API is identified to cause "Long Tasks" (> 50ms) that degrade the frame rate.

## 2. Procedures

- **[PROC-BRW-01] Polyfill Audit**
  - IF an API is not supported by the target browser baseline THEN MUST identify and implement a verified polyfill or fallback strategy.
- **[PROC-BRW-02] Permission lifecycle review**
  - Regularly verify that permission-restricted features handle the "Denied" state gracefully without crashing the UI.

## 3. Examples

### Clean Observer Teardown (Good)

```javascript
const observer = new ResizeObserver(entries => { /* ... */ });
useEffect(() => {
  observer.observe(target);
  return () => observer.disconnect();
}, []);
```

## 4. Validation Criteria

- **[VAL-BRW-01] Browser Compatibility Pass**
  - [ ] Cross-browser testing confirms that the application functions (with fallbacks) on the defined minimum browser versions.
- **[VAL-BRW-02] Memory Leak verification**
  - [ ] DevTools Memory tab confirms zero growth in "Observer" or "Listener" counts during page navigation.
- **[VAL-BRW-03] Security Flag Audit**
  - [ ] audit confirms that storage keys are appropriately prefixed and redacted where necessary.
