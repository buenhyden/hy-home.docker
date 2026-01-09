---
trigger: always_on
glob: "package.json,**/*.ts"
description: "VSCode Extensions: Activation, Webviews, Testing, and Commands."
---
# VSCode Extension Standards

## 1. Activation

- **Events**: Use specific `activationEvents` (`onCommand`, `onLanguage`). Avoid `*`.
- **Lazy Load**: Import heavy modules inside the command handler.

### Example: Activation

**Good**

```json
"activationEvents": ["onCommand:myExt.hello"]
```

**Bad**

```json
"activationEvents": ["*"] // Slows down VSCode startup for everyone
```

## 2. Webviews

- **CSP**: Strict `Content-Security-Policy` in Webview HTML.
- **Message Passing**: Use `postMessage` for Main <-> Webview communication.

### Example: CSP

**Good**

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src ${webview.cspSource};">
```

**Bad**

```html
<!-- No CSP: XSS Vulnerability in Editor -->
```

## 3. Testing

- **Framework**: Use `@vscode/test-electron` for integration tests.
- **Mocking**: Mock `vscode` API for unit tests.

### Example: Test

**Good**

```typescript
import * as vscode from 'vscode';
import * as assert from 'assert';

suite('Extension Test Suite', () => {
  test('Sample test', async () => {
    const ext = vscode.extensions.getExtension('myExt');
    assert.ok(ext);
  });
});
```
