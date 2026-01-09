---
trigger: always_on
glob: "src-tauri/**/*"
description: "Tauri: Command Security, Allowlist, Async, and Error Handling."
---
# Tauri Standards

## 1. Security (Allowlist)

- **Scope**: Scope filesystem access strictly in `tauri.conf.json`.
- **Commands**: Expose Rust functions via `#[tauri::command]`.

### Example: Allowlist

**Good**

```json
"fs": {
  "scope": ["$APP_DATA/*"]
}
```

**Bad**

```json
"fs": {
  "scope": ["**/*"] // Access entire disk
}
```

## 2. Commands (Async & Types)

- **Arguments**: Use typed arguments in Rust.
- **Async**: Use `async fn` for heavy tasks to avoid freezing UI.

### Example: Async

**Good**

```rust
#[tauri::command]
async fn heavy_computation() -> String { ... }
```

**Bad**

```rust
#[tauri::command]
fn heavy_computation() { 
  // Blocks Main Thread
}
```

## 3. Error Handling

- **Result**: Return `Result<T, E>` from commands. Frontend receives structured errors.
- **Enum**: Define custom error enums for clear error types.

### Example: Error

**Good**

```rust
#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(path).map_err(|e| e.to_string())
}
```

**Bad**

```rust
#[tauri::command]
fn read_file(path: String) -> String {
    fs::read_to_string(path).unwrap() // Panics on error
}
```
