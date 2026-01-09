---
trigger: always_on
glob: "**/*.{js,ts}"
description: "Express.js: Middleware, Error Handling, and Validation."
---
# Express.js Standards

## 1. Middleware Pattern

- **Async**: Use `express-async-errors` or a wrapper function to catch async errors. Express 4 doesn't catch them automatically.
- **Validation**: Middleware (Zod/Joi) runs before the controller.

### Example: Async Wrapper

**Good**

```ts
router.get('/users', asyncHandler(async (req, res) => {
  const users = await db.getUsers();
  res.json(users);
}));
```

**Bad**

```ts
router.get('/users', async (req, res) => {
  const users = await db.getUsers(); // If this throws, request hangs
  res.json(users);
});
```

## 2. Architecture

- **Controllers**: Keep them thin. Parse request -> Call Service -> Send Response.
- **Services**: Contain business logic. No `req` or `res` objects in services.

### Example: Layering

**Good**

```ts
// Controller
const login = async (req, res) => {
  const token = await authService.login(req.body);
  res.json({ token });
};
```

**Bad**

```ts
// Controller
const login = async (req, res) => {
  // Logic inside controller
  const user = await db.find({ email: req.body.email });
  if (!user) return res.status(401).send();
  ...
};
```
