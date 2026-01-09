---
trigger: always_on
glob: "**/*.py"
description: "NumPy: Numerical computing, broadcasting, and vectorization."
---
# NumPy Standards

## 1. Core Principles

- **Vectorization**: Replace all loops with array operations.
- **Broadcasting**: Leverage broadcasting for shape-agnostic math.
- **Views**: Be aware when slicing returns a view vs copy. Use `.copy()` if needed.

## 2. Dtypes & Memory

- **Explicit Dtypes**: Always specify `dtype=` when creating arrays (e.g., `np.float32`).
- **Pre-allocation**: Use `np.zeros` or `np.empty` then fill, rather than `append`.

## 3. Shape Handling

- **Dimensions**: Use `arrays.shape` checks in assertions.
- **Reshaping**: Use `-1` for inferred dimensions in `.reshape()`.
- **New Axis**: Use `np.newaxis` or `None` instead of `reshape` for simple dimension adding.

## 4. Testing

- **Comparison**: Use `np.testing.assert_allclose` for floats. `==` is dangerous for floats.
