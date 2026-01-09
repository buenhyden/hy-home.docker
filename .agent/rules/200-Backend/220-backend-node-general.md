---
trigger: always_on
glob: "**/*.{js,ts}"
description: "Node.js General: Async patterns, Error handling, and Modern JS."
---
# Node.js General Standards

## 1. Async & Promises

- **Async/Await**: Use over raw callbacks or `.then()`.
- **Top Level**: Use top-level await (Node 14+).

### Example: Async

**Good**

```ts
async function getUser(id) {
  try {
    const user = await db.find(id);
    return user;
  } catch (err) {
    throw new AppError('DB_ERROR', err);
  }
}
```

**Bad**

```ts
function getUser(id) {
  return db.find(id).then(user => {
    return user;
  }); // Unnecessary promise chain
}
```

## 2. Code Quality

- **Imports**: Use ES Modules (`import`).
- **Equality**: Strict equality `===` always.

## 3. Error Handling

- **Objects**: Throw `Error` objects, never strings.
- **Handling**: Always handle Promise rejections.

## 4. Dependencies & Versioning

- **Engines**: Strict `engines` field in `package.json`.
- **Managers**: Use `npm`, `pnpm`, or `yarn` consistently. Commit `lock` files.
- **.nvmrc**: Include in root for version alignment.

```json
"engines": { "node": ">=20.0.0" }
```

### Example: Errors

**Good**

```ts
throw new Error("User not found");
```

**Bad**

```ts
throw "User not found"; // No stack trace
```
