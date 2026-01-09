---
trigger: always_on
glob: "**/*.{js,jsx,ts,tsx}"
description: "JavaScript Security: Prevention of integrity failures (OWASP A08)."
---
# JavaScript Integrity Standards (OWASP A08)

## 1. Dependency Management

- **Audit**: Run `npm audit` or `yarn audit` in CI pipelines.
- **Lockfiles**: Always commit `package-lock.json` or `yarn.lock`.
- **Scripts**: Avoid `npm install` for untrusted packages.

## 2. Browser Integrity

- **SRI**: Use Subresource Integrity (SRI) for all CDN scripts.
- **CSP**: Implement strict Content Security Policy.

## 3. Code Safety

- **Deserialization**: Validate JSON before parsing if untrusted.
- **Prototype Pollution**: Use `Object.create(null)` or freeze prototypes. avoid `items[key] = value` on unbounded inputs.
- **Dynamic Imports**: Use allowlists for variable imports.

### Example: SRI & Parsing

#### Good

```html
<script src="https://cdn.example.com/lib.js" integrity="sha384-..." crossorigin="anonymous"></script>
```

```javascript
// Safer JSON parse (reviver or schema validation)
const data = JSON.parse(jsonString);
if (!validateSchema(data)) throw new Error("Invalid");
```
