---
trigger: always_on
glob: "**/*.{py,js,ts,jsx,tsx}"
description: "Security Injection (OWASP A03): SQLi, XSS, and Command Injection prevention."
---
# Security Injection Standards (OWASP A03)

## 1. SQL Injection (SQLi)

- **Parameterized Queries**: ALWAYS use parameterized queries or prepared statements.
  - **Python**: `cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))`.
  - **JS/Node**: Use libraries/ORMs that support binding (`pg`, `Prisma`, `TypeORM`).
- **ORM**: Prefer ORMs (Django, SQLAlchemy, TypeORM) as they handle escaping by default. Avoid "Raw SQL" features with string concatenation.

## 2. Cross-Site Scripting (XSS)

- **Sanitization**: Sanitize user HTML input using libraries like `DOMPurify` (JS) or `bleach` (Python).
- **Context**: Escape data appropriate for the context (HTML body, attribute, JS variable).
- **React/Vue**: Use default data binding `{}`. Avoid `dangerouslySetInnerHTML` or `v-html` unless absolutely necessary and sanitized.

## 3. Command Injection

- **Avoid Shell Execution**: Avoid `os.system`, `subprocess.Popen(shell=True)`, `exec()`.
- **Arguments**: Pass arguments as an array/list, not a concatenated string.
  - **Safe**: `subprocess.run(["ls", dirname])`
  - **Unsafe**: `subprocess.run("ls " + dirname, shell=True)`

## 4. Code Injection

- **No Eval**: Avoid `eval()`, `new Function()`, `exec()`, or dynamic imports with user input.

### Example: Secure SQL

#### Good (Parameterized)

```python
cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
```

#### Bad (Concatenation)

```python
cursor.execute(f"SELECT * FROM products WHERE category = '{category}'")
```
