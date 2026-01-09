---
trigger: always_on
glob: "**/*.{js,ts,py,java,go,html}"
description: "Web Security: XSS, CSRF, Injection, and Secure Headers."
---
# Web Security Standards

## 1. Input Sanitization & XSS

- **Output Encoding**: Encrypt or encode data before rendering it in HTML to prevent script injection.
- **Frameworks**: Trust modern frameworks (React, Vue) to escape by default, but NEVER use `dangerouslySetInnerHTML` or `v-html` with untrusted user input.
- **CSP**: Use a strict Content Security Policy to prevent unauthorized scripts from running.

### Example: XSS Prevention

#### Good (XSS)

```javascript
// Automatically escaped by framework
<div>{userInput}</div>
```

#### Bad (XSS)

```javascript
// Direct injection - VULNERABLE
element.innerHTML = userInput;
```

## 2. Injections (SQL/Command)

- **Parameterized Queries**: Never concatenate strings to build SQL queries.
- **ORM/ODM**: Use built-in validation of query builders.
- **OS Commands**: Avoid executing shell commands with user-provided arguments.

### Example: SQLi

#### Good (SQLi)

```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

#### Bad (SQLi)

```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}") # VULNERABLE
```

## 3. Cookie & CSRF Security

- **Hardened Cookies**: Always set `HttpOnly`, `Secure`, and `SameSite=Lax/Strict`.
- **CSRF Tokens**: Mandatory for state-changing requests (POST, PUT, DELETE) in cookie-based auth environments.

## 4. Secure Headers

- **HSTS**: Force HTTPS using `Strict-Transport-Security`.
- **X-Frame-Options**: Prevent Clickjacking by setting to `DENY` or `SAMEORIGIN`.
- **Feature-Policy**: Restrict access to Browser APIs (Camera, Mic) if not needed.

## 5. File Upload Security

- **Validation**: Validate file type using *magic numbers* (signatures), not just extensions.
- **Storage**: Store uploaded files outside the web root or rename them with random hashes.
- **Scanning**: Scan for malware if possible; limit file size and strict MIME types.

### Example: Secure Upload

#### Good (Upload)

```javascript
// Validate via magic bytes (hex signature)
if (fileSignature !== '89504e47') { // PNG
  throw "Invalid file type";
}
```

## 6. Secure Sessions

- **Storage**: Use a secure store (Redis, Postgres), never in-memory for production.
- **Regeneration**: Regenerate session IDs after login (`req.session.regenerate()`) to prevent fixation.
- **Timeout**: Set absolute timeouts and idle timeouts.

## 7. Node.js Ecosystem Specifics

- **Dependencies**: Run `npm audit` in CI. Always commit `package-lock.json`.
- **Libraries**:
  - Validation: Use `zod`, `joi`, or `validator.js`.
  - Rate Limiting: Use `express-rate-limit`.
- **Middleware**: Use `helmet` to set secure HTTP headers automatically.
- **ReDoS**: Avoid vulnerable Regex. Use specialized libraries for complex validations (email, URL).
- **NoSQL Injection**: Sanitize inputs before querying MongoDB (use Mongoose or sanitization libs).
