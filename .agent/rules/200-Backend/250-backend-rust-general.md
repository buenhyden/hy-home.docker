---
trigger: always_on
glob: "**/*.rs"
description: "Rust General: Ownership, Error Handling, Concurrency, and Clippy."
---
# Rust General Standards

## 1. Safety & Ownership

- **Unwrap**: explicit `unwrap()` is forbidden in production code. Use `expect("msg")` if you are mathematically certain, or `?` to propagate.
- **Clones**: Avoid excessive cloning. Use `&str` and references where possible.
- **Lifetimes**: Explicitly annotate lifetimes only when the compiler cannot infer them. Prefer owning data in structs if references get too complex.

### Example: Error Handling

**Good**

```rust
fn read_config() -> Result<Config, ConfigError> {
    let content = fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}
```

**Bad**

```rust
fn read_config() -> Config {
    // Panics if file missing
    let content = fs::read_to_string("config.toml").unwrap(); 
    toml::from_str(&content).unwrap()
}
```

## 2. Concurrency (Async/Tokio)

- **Blocking**: NEVER block a thread in async code (e.g., `std::thread::sleep`, `fs::read`). Use `tokio::time::sleep` / `tokio::fs`.
- **Send + Sync**: Ensure types shared across threads implement `Send` (move) and `Sync` (share reference).

## 3. Tooling & Lints

- **Clippy**: Code must pass `cargo clippy -- -D warnings`.
- **Fmt**: Run `cargo fmt` on every commit.
- **Modules**: Keep `mod.rs` clean. Prefer defining modules in `foo.rs` instead of `foo/mod.rs` (2018 edition style).
