---
trigger: model_decision
glob: ["**/*.rs", "**/Cargo.toml"]
description: "Rust Development Standards: Enforces memory safety, zero-cost abstractions, idiomatic error handling, and Tokio-based concurrency."
---

# Rust Development Standards

- **Role**: Senior Rust Systems Engineer
- **Purpose**: Define standards for building high-performance, memory-safe, and concurrent systems using idiomatic Rust and the modern ecosystem.
- **Activates When**: Developing Rust binaries, libraries, or configuring Cargo workspace members.

**Trigger**: model_decision — Apply during all Rust development and systems design phases.

## 1. Standards

### Principles

- **[REQ-RST-01] Ownership & Safety Primacy**
  - Leverage Rust's borrow checker to ensure compile-time memory safety. The use of `unsafe` is PROHIBITED unless strictly required for hardware/FFI interaction.
- **[REQ-RST-02] Zero-Cost Abstractions**
  - Utilize traits, generics, and macros to build powerful abstractions that do not impose runtime overhead.
- **[REQ-RST-03] Explicit Error Result Handling**
  - Favor the `Result<T, E>` pattern for all fallible operations. The use of `.unwrap()` or `.expect()` is PROHIBITED in production code.

### Rust Ecosystem Baseline

| Category | Requirement ID | Critical Tooling |
| --- | --- | --- |
| Async | [REQ-RST-04] | `tokio` (Asynchronous runtime) |
| CLI / Arg | [REQ-RST-05] | `clap` (Derive pattern) |
| Error Mgmt | [REQ-RST-06] | `thiserror` (lib) / `anyhow` (bin) |
| Serialization| [REQ-RST-07] | `serde` (JSON/YAML/etc.) |

### Must

- **[REQ-RST-08] Clippy-Linter Compliance**
  - All code MUST pass the `clippy` linter audit without warnings using the `all` and `pedantic` groups where applicable.
- **[REQ-RST-09] Explicit Documentation (rustdoc)**
  - Public items MUST include doc comments (`///`) with descriptive text and usage examples.
- **[REQ-RST-10] Standardized Workspace Layout**
  - Projects MUST follow the standard Cargo structure (`/src`, `/tests`, `/examples`) and maintain a clean `Cargo.toml`.

### Must Not

- **[BAN-RST-01] Brute-Force Unwrapping**
  - Do NOT use `.unwrap()` as a shortcut for error handling; utilize the `?` operator or explicit pattern matching.
- **[BAN-RST-02] Shared Mutable State**
  - Minimize the use of `Arc<Mutex<T>>` where ownership transfer or channels can achieve the same goals.

### Failure Handling

- **Stop Condition**: Stop execution if the `cargo test` suite identifies a regression or if a memory leak is identified in long-running integration tests.

## 2. Procedures

- **[PROC-RST-01] Idiomatic Error Refactor**
  - IF a function returns a generic error THEN MUST refactor it to use a custom `enum` error type via `thiserror` for better diagnostic clarity.
- **[PROC-RST-02] Dependency Hygiene**
  - Periodically run `cargo audit` to detect vulnerabilities in the crate dependency graph.

## 3. Examples

### Safe Async Result (Good)

```rust
async fn fetch_data() -> Result<Data, MyError> {
    let res = client.get(url).await.map_err(MyError::from)?;
    Ok(res)
}
```

## 4. Validation Criteria

- **[VAL-RST-01] Clippy Integrity**
  - [ ] `cargo clippy` returns zero warnings or errors.
- **[VAL-RST-02] Format Adherence**
  - [ ] `cargo fmt --check` confirms that all files follow the standard Rust style.
- **[VAL-RST-03] Test Coverage Sufficiency**
  - [ ] Core business logic crates demonstrate > 85% unit test coverage.
