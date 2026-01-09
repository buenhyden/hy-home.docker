---
trigger: always_on
glob: "**/*.js,**/*.ts,**/*.jsx,**/*.tsx"
description: "CodeMirror 6: Modern Editor Standards."
---
# CodeMirror 6 Standards

## 1. Versioning

- **CM6 Only**: Use exclusively CodeMirror 6 packages (`@codemirror/state`, `@codemirror/view`). Do NOT use the legacy properties or global `CodeMirror` object from v5.

## 2. State Management

- **Immutability**: `EditorState` is immutable. Use transactions (`state.update()`) and `view.dispatch()` to make changes.
- **Extensions**: Configure everything (keymaps, themes, language support) via the `extensions` array in `EditorState`.

### Example: Setup

**Good**

```javascript
import { EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";

const startState = EditorState.create({
  doc: "Hello World",
  extensions: [keymap.of(defaultKeymap)]
});
```

## 3. Performance

- **Batching**: Batch updates into a single transaction where possible.
- **Debouncing**: Debounce listeners for `update` events if they perform heavy logic (like linting or saving).
