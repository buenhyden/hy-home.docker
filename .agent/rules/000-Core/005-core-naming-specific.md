---
trigger: always_on
glob: "**/*"
description: "Naming Conventions: Casing, Files, Database, Generics, and Boolean usage."
---
# Naming Standards

## 1. Code Casing Standards

- **CamelCase** (`myVariable`): JavaScript/TypeScript/Java/Go variables & functions.
- **PascalCase** (`MyClass`): Classes, Interfaces, React Components.
- **snake_case** (`my_variable`): Python/Rust/SQL variables & functions.
- **kebab-case** (`my-file.ts`): URLs, CSS classes, and File names (JS/TS).
- **SCREAMING_SNAKE_CASE** (`MAX_RETRIES`): Constants and Environment variables.

## 2. Boolean Naming

- **Prefixes**: ALWAYS use `is`, `has`, `can`, `should`, or `did`.
- **Positivity**: Avoid negative logic. `isEnabled` is better than `isDisabled` or `isNotEnabled`.

### Example: Booleans

**Good**

```javascript
const isVisible = true;
const hasAccess = false;
if (!isVisible) { ... }
```

**Bad**

```javascript
const visible = true; // Ambiguous: Is it a boolean or string?
const noAccess = true; // Double negative: !noAccess is confusing
```

## 3. Function Naming (Verbs)

- **Action**: Start with a verb (`get`, `set`, `fetch`, `create`, `delete`).
- **Specificity**: `getUserById` is better than `getUser`.

### Example: Functions

**Good**

```python
def fetch_user_data(user_id: str): ...
def calculate_total(items: list): ...
```

**Bad**

```python
def user_data(user_id): ... # Is this a getter? A setter? A factory?
def handle_stuff(items): ... # Too vague
```

## 4. File Naming

- **JS/TS**: Use `kebab-case` (`user-profile.tsx`, `api-client.ts`).
- **Python**: Use `snake_case` (`user_profile.py`).
- **Classes**: If the file exports a single class, match the class name (`UserProfile.java`).

## 5. Acronyms

- **Treat as Words**: Avoid all-caps for acronyms in names to improve readability.
- **Convention**: `XmlHttpRequest` over `XMLHTTPRequest`.

### Example: Acronyms

**Good**

```java
public class HttpConnection { ... }
public String parseHtml(String input);
```

**Bad**

```java
public class HTTPConnection { ... }
public String parseHTML(String input); // Hard to read parseHTMLInput
```

## 6. Advanced & Language Specifics

- **Interfaces (TS)**: Do NOT use `I` prefix (`User` vs `IUser`). Use `Props` suffix for components (`ButtonProps`).
- **Generics**: Use `T` for simple types, or descriptive names (`TRequest`, `TResponse`) for complex ones.
- **Private Members**: Use `_` prefix for private terms in languages without strict privacy (Python `_internal_method`, JS conventions).

## 7. Database Naming (SQL)

- **Tables**: Use **Singular** snake_case (`user`, `order_item`) OR **Plural** snake_case (`users`, `order_items`) but **BE CONSISTENT** project-wide.
- **Columns**: `snake_case`. Foreign keys should match table + id (`user_id`).
- **Indexes**: `idx_table_column`.
