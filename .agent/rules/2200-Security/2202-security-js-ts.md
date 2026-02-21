---
trigger: always_on
glob: "**/*.{js,ts,jsx,tsx}"
description: "JavaScript & TypeScript Security Standards: Enforces XSS prevention, prototype pollution safeguards, and secure Node.js patterns."
---

# JS & TS Security Standards

- **Role**: JS/TS Security Engineer
- **Purpose**: Define standards for mitigating language-specific vulnerabilities (e.g., Prototype Pollution) and ensuring secure patterns in Node.js and Browser environments.
- **Activates When**: Developing frontend or backend code using JavaScript or TypeScript.

**Trigger**: always_on — Apply during the implementation of JS/TS application components.

## 1. Standards

### Principles

- **[REQ-JS_SEC-01] Immutable Prototypes**
  - Objects and classes MUST be protected against Prototype Pollution. Use `Map` or `Object.create(null)` for plain dictionaries.
- **[REQ-JS_SEC-02] Secure Execution Sink**
  - The use of dynamic execution sinks such as `eval()`, `new Function()`, or `setTimeout` with string arguments is STRICTLY PROHIBITED.
- **[REQ-JS_SEC-03] Browser State Safety**
  - Sensitive tokens (JWT, Secrets) MUST NOT be stored in `localStorage` or `sessionStorage` (XSS-vulnerable). Use `HttpOnly; Secure` cookies.

### Security Framework

| Domain | Requirement ID | Critical Action |
| --- | --- | --- |
| Sanitization | [REQ-JS_SEC-04] | Use DOMPurify for HTML |
| Headers | [REQ-JS_SEC-05] | Use Helmet (Node.js) |
| Validation | [REQ-JS_SEC-06] | Use Zod / Joi |
| Auth | [REQ-JS_SEC-07] | rotation on Login |

### Must

- **[REQ-JS_SEC-08] Server-Side Sanitization**
  - All input MUST be validated and sanitized on the server-side, regardless of client-side validation logic.
- **[REQ-JS_SEC-09] Strict Mime-Type Checks**
  - File upload handlers MUST verify "Magic Numbers" (buffer signatures) rather than trusting file extensions.
- **[REQ-JS_SEC-10] Lockfile Integrity**
  - The `package-lock.json` or `yarn.lock` MUST be committed to ensure reproducible and audited builds.

### Must Not

- **[BAN-JS_SEC-01] Direct HTML Injection**
  - JS frameworks MUST NOT use `dangerouslySetInnerHTML` or `v-html` with untrusted data without sanitization.
- **[BAN-JS_SEC-02] Unchecked Prototype Merge**
  - Deep-merge operations MUST NOT attempt to merge properties with the key `__proto__` or `constructor.prototype`.

### Failure Handling

- **Stop Condition**: Stop execution if a supply chain audit (`npm audit`) identifies a "Critical" vulnerability in a direct dependency.

## 2. Procedures

- **[PROC-JS_SEC-01] Header Audit**
  - IF deploying a Node.js API THEN MUST verify that Helmet is active with a strict `Content-Security-Policy`.
- **[PROC-JS_SEC-02] Sanitization Loop**
  - Ensure all user-generated content displayed in the UI is passed through a verified sanitizer before rendering.

## 3. Examples

### Safe Dictionary Setup

```javascript
// Good: Using Map to avoid prototype pollution
const safeStore = new Map();
safeStore.set('key', value);
```

## 4. Validation Criteria

- **[VAL-JS_SEC-01] Pollution Scan**
  - [ ] Automated tests confirm that `__proto__` injection attempts fail.
- **[VAL-JS_SEC-02] Cookie Verification**
  - [ ] Browser audit confirms that session cookies have the `HttpOnly` and `Secure` flags set.
- **[VAL-JS_SEC-03] Dependency Audit**
  - [ ] `npm audit` returns a zero-critical vulnerability report for the current build.
