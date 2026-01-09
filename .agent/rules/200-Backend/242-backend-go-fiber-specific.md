---
trigger: always_on
glob: "**/*.go"
description: "Go Fiber: Express-style framework, Middleware, and Context patterns."
---
# Go Fiber Standards

## 1. Application Setup

- **Instance**: Use `fiber.New()` with a configuration struct.
- **Graceful Shutdown**: Listen for OS signals and call `app.Shutdown()`.

### Example: Setup

**Good**

```go
app := fiber.New(fiber.Config{
    ReadTimeout:  10 * time.Second,
    ErrorHandler: customErrorHandler,
})
```

**Bad**

```go
app := fiber.New() // No timeouts, uses defaults (potentially insecure)
```

## 2. Context & Parsing

- **Body Parsing**: Use `c.BodyParser(&dto)` for JSON with validation.
- **Params**: Use `c.Params("id")` for type-safe path params.

### Example: Parsing

**Good**

```go
var dto CreateUserDTO
if err := c.BodyParser(&dto); err != nil {
    return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
}
```

**Bad**

```go
body := string(c.Body()) // Manually parsing raw body bytes
```

## 3. Middleware

- **Built-in**: Use `logger.New()`, `cors.New()`, `recover.New()`.
- **Custom**: Middleware signature is `func(c *fiber.Ctx) error`. Call `c.Next()` to proceed.

## 4. Performance

- **Prefork**: `Prefork: true` enables SO_REUSEPORT for N workers.
- **JSON Encoder**: Swap to `goccy/go-json` for faster serialization.
