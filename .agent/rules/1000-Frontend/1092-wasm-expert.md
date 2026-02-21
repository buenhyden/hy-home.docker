---
trigger: always_on
glob: "**/*.{wasm,rs,js,ts,cpp,c}"
description: "WebAssembly (WASM) Standards: Enforces performance-critical compilation, memory management, and JS interop best practices."
---

# WebAssembly (WASM) Standards

- **Role**: WASM Systems Architect
- **Purpose**: Define standards for high-performance WebAssembly module development and browser integration.
- **Activates When**: Developing or integrating WASM modules using Rust, C++, or AssemblyScript.

**Trigger**: always_on — Apply during the development and integration of WASM assets.

## 1. Standards

### Principles

- **[REQ-WASM-01] Performance-Critical Usage**
  - WASM SHOULD be reserved for CPU-intensive tasks (e.g., image processing, crypto) where JS performance is insufficient.
- **[REQ-WASM-02] Boundary Efficiency**
  - Communication between JavaScript and WASM MUST be minimized to reduce overhead.
- **[REQ-WASM-03] Size-Aware Compilation**
  - Modules MUST be compiled with size optimizations (e.g., `wasm-opt`, `wee_alloc`) for production.

### Compilation Targets

| Source | Preferred Toolchain | Target |
| --- | --- | --- |
| Rust | `wasm-pack` / `wasm-bindgen` | `wasm32-unknown-unknown` |
| C / C++ | Emscripten | `wasm32-emscripten` |
| TypeScript | AssemblyScript | `wasm32-as` |

### Must

- **[REQ-WASM-04] Streaming Instantiation**
  - Large WASM modules MUST be loaded using `WebAssembly.instantiateStreaming()` to optimize startup time.
- **[REQ-WASM-05] Linear Memory Safety**
  - Memory bounds MUST be validated when passing data between JS TypedArrays and WASM memory.
- **[REQ-WASM-06] Explicit Termination**
  - Modules managing system-like resources MUST provide an explicit cleanup or de-initialization method.

### Must Not

- **[BAN-WASM-01] Blocking UI Thread**
  - Heavy WASM computation MUST NOT occur on the main thread; use Web Workers.
- **[BAN-WASM-02] Shared State Oversaturation**
  - Avoid excessive use of `SharedArrayBuffer` without proper synchronization (Mutexes/Atomics).

### Failure Handling

- **Stop Condition**: Stop execution if a WASM panic occurs and provide a structured error bridge to JS.

## 2. Procedures

- **[PROC-WASM-01] Build Pipeline**
  - IF building for production THEN MUST run `wasm-opt -Oz` on the binary.
- **[PROC-WASM-02] Binding Generation**
  - Use `wasm-bindgen` in Rust to handle complex JS types automatically.

## 3. Examples

### Streaming Load

```javascript
const { instance } = await WebAssembly.instantiateStreaming(
  fetch('module.wasm'),
  importObject
);
```

## 4. Validation Criteria

- **[VAL-WASM-01] Performance Benchmark**
  - [ ] WASM implementation provides > 2x speedup for the targeted CPU-intensive task.
- **[VAL-WASM-02] Binary Size**
  - [ ] Production WASM binaries are compressed (Gzip/Brotli) and minimized.
- **[VAL-WASM-03] Interop Safety**
  - [ ] All data transfers use TypedArrays and validated offsets.
