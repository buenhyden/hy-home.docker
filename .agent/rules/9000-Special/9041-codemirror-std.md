---
trigger: always_on
glob: "**/*.{js,ts,jsx,tsx}"
description: "CodeMirror 6 Standards: Enforces state immutability, transactional updates, and performance optimization for modern editors."
---

# CodeMirror 6 Standards

- **Role**: Editor Experience Developer
- **Purpose**: Define standards for implementing high-performance code editors using the CodeMirror 6 (CM6) library.
- **Activates When**: Developing or configuring CodeMirror editor instances.

**Trigger**: always_on — Apply during the setup and configuration of code editor components.

## 1. Standards

### Principles

- **[REQ-CM6-01] Functional State**
  - `EditorState` MUST be treated as strictly immutable. Changes MUST only be applied via transactions.
- **[REQ-CM6-02] Version Purity**
  - Only CM6 modular packages MUST be used. Do NOT include legacy CM5 global properties or packages.
- **[REQ-CM6-03] Modular Extension**
  - All editor functionality (keymaps, themes, syntax) MUST be configured via the `extensions` array in `EditorState`.

### Core Workflow

1. Define `EditorState` with initial `doc` and `extensions`.
2. Instantiate `EditorView` with the state and a parent DOM element.
3. Update state using `view.dispatch(view.state.update(...))`.

### Must

- **[REQ-CM6-04] Transaction Batching**
  - Multiple document or state changes MUST be batched into a single transaction where possible to minimize DOM re-renders.
- **[REQ-CM6-05] Event Debouncing**
  - Listeners for `update` events that trigger heavy logic (e.g., linting, sync) MUST be debounced.
- **[REQ-CM6-06] Semantic Keymaps**
  - Custom keymaps MUST be defined using the `keymap.of()` extension and should follow platform conventions.

### Must Not

- **[BAN-CM6-01] Direct DOM Injection**
  - The editor's internal DOM MUST NOT be manipulated directly outside of the CodeMirror view API.
- **[BAN-CM6-02] Global Instances**
  - Avoid creating multiple monolithic editor instances without explicit cleanup on component unmount.

### Failure Handling

- **Stop Condition**: Stop initialization if a required language extension or theme package fails to load.

## 2. Procedures

- **[PROC-CM6-01] Configuration Management**
  - IF adding a new editor feature THEN MUST implement it as a modular `Extension` for testability.
- **[PROC-CM6-02] State Persistence**
  - Use `state.toJSON()` and `state.fromJSON()` for reliable editor state persistence and restoration.

## 3. Examples

### Basic Setup

```javascript
const state = EditorState.create({
  doc: "initial code",
  extensions: [basicSetup, javascript()]
});
const view = new EditorView({ state, parent: document.body });
```

## 4. Validation Criteria

- **[VAL-CM6-01] Immutable Flow**
  - [ ] Every state change is verified to occur via the `dispatch` mechanism.
- **[VAL-CM6-02] Performance Profile**
  - [ ] Editor remains responsive (typing latency < 16ms) even with large documents.
- **[VAL-CM6-03] Extension Audit**
  - [ ] All active extensions are documented and serve a specific functional requirement.
