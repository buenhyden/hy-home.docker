---
trigger: always_on
glob: "**/*.js,**/*.ts"
description: "Security: Insecure Design Patterns (JavaScript)."
---
# JavaScript Insecure Design Patterns

## 1. Prototype Pollution

- **Object.freeze**: Freeze sensitive configuration objects.
- **Safe Merge**: Use safe deep-merge libraries (or `Object.assign` carefully) preventing modification of `__proto__`.
- **Map/Set**: Use `Map` instead of plain Objects for hashmaps to avoid prototype inheritance issues.

### Example: Map vs Object

**Good**

```javascript
const cache = new Map();
cache.set('key', 'value');
```

**Bad**

```javascript
const cache = {};
// Attacker controls 'key' -> "__proto__"
cache[key] = value; 
```

## 2. Dependencies (Supply Chain)

- **Audit**: Regularly run `npm audit`.
- **Lockfiles**: Commit `package-lock.json` to ensure reproducible builds.
- **Scripts**: Be cautious of `postinstall` scripts in dependencies.

## 3. Client-Side Security (XSS)

- **Context-Aware Encoding**: Encode data based on where it is placed (HTML body, attribute, script).
- **CSP**: Content Security Policy headers are mandatory to mitigate XSS impact.
- **Eval**: Never use `eval()` or `new Function()`.
