---
trigger: always_on
glob: "**/*.rs"
description: "Rocket 0.5+ Best Practices: Async routing, request guards, and fairings."
---
# Rocket Framework Standards

## 1. Async Architecture

- **Async Handlers**: Rocket 0.5+ is fully async. All routes must be `async fn`.
- **Blocking I/O**: NEVER block the async runtime. Use `tokio::task::spawn_blocking` for CPU-heavy or blocking sync operations.

### Example: Async Route

**Good**

```rust
#[get("/hello/<name>")]
async fn hello(name: String) -> String {
    format!("Hello, {}!", name)
}
```

## 2. Request Guards

- **Validation**: Use Request Guards (`FromRequest`) for authentication and authorization logic, keeping handlers clean.
- **Strict Typing**: Use `Json<T>`, `Form<T>`, and `State<T>` to strictly type inputs.

### Example: Guard

**Good**

```rust
#[rocket::async_trait]
impl<'r> FromRequest<'r> for AdminUser {
    type Error = ();
    async fn from_request(req: &'r Request<'_>) -> Outcome<Self, ()> {
        // Validation logic
    }
}

#[get("/admin")]
fn admin_panel(_user: AdminUser) { ... }
```

## 3. Database

- **Rocket DB Pools**: Use `rocket_db_pools` for async database connections (SQLx/Diesel). Avoid managing connection pools manually.

## 4. Configuration

- **Rocket.toml**: Use `Rocket.toml` for defaults but override secrets with environment variables (`ROCKET_SECRET_KEY`).
