---
trigger: always_on
glob: "**/*.rs"
description: "Rust Web: Axum, Tower middleware, and type-safe routing."
---
# Rust Web Specifics (Axum)

## 1. Routing & Handlers

- **Axum**: Prefer `axum` for modern, type-safe web development.
- **Extractors**: Use `Path`, `Query`, and `Json` extractors in handler signatures.
- **Routers**: Compose routers using `.nest()` and `.merge()`.

## 2. State & Middleware

- **State**: Use `with_state` for dependency injection (DB pools, config).
- **Tower**: Use `tower` and `tower-http` for middleware (CORS, Trace, Compression).

## 3. Async & Runtime

- **Tokio**: Use `tokio` as the default async runtime.
- **Concurrency**: Avoid blocking operations in async handlers; use `spawn_blocking` if necessary.

## 4. Errors

- **`IntoResponse`**: Implement `IntoResponse` for custom error enums to return consistent HTTP errors.
