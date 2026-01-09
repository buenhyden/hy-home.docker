---
trigger: always_on
glob: "**/*.cpp,**/*.h,**/*.td"
description: "LLVM: Compiler Infrastructure Standards."
---
# LLVM Standards

## 1. Coding Style

- **Naming**: Follow LLVM Coding Standards (PascalCase for types, camelCase for functions/variables).
- **Headers**: Minimize includes in headers. Use forward declarations.
- **RTTI**: Do NOT use RTTI (`dynamic_cast`). Use LLVM's `isa<>`, `cast<>`, and `dyn_cast<>` templates.

### Example: Casting

**Good**

```cpp
if (auto *I = dyn_cast<Instruction>(V)) {
    ...
}
```

## 2. Memory Management

- **Data Structures**: Use LLVM-specific containers (`SmallVector`, `DenseMap`, `StringRef`) instead of STL (`std::vector`, `std::map`, `std::string`) for efficiency (cache locality, small object optimization).
- **Ownership**: Be clear about ownership. Passes normally don't own IR; Modules/Functions do.

## 3. Testing

- **LIT**: Use `lit` (LLVM Integrated Tester) and `FileCheck` for regression tests.
- **IR Tests**: Write tests against LLVM IR (`.ll` files), not just C/C++ frontend output, to verify middle-end optimizations.
