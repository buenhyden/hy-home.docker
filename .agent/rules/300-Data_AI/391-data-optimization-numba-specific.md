---
trigger: always_on
glob: "**/*.py"
description: "Numba: JIT Compilation Standards."
---
# Numba Standards

## 1. Compilation Modes

- **nopython**: ALWAYS use `nopython=True` (or `@njit`, which is an alias). If Numba falls back to object mode, performance is often worse than CPython.
- **Failures**: Fix code that causes object mode fallback (usually unsupported Python objects or dynamic types).

### Example: njit

**Good**

```python
from numba import njit

@njit
def fast_loop(x):
    res = 0
    for i in range(len(x)):
        res += x[i]
    return res
```

## 2. Parallelism

- **Parallel**: Use `parallel=True` and `prange` (Numba's parallel range) for explicit loop parallelization when operations are independent.

### Example: Parallel Loop

**Good**

```python
from numba import njit, prange

@njit(parallel=True)
def parallel_calc(arr):
    res = 0
    for i in prange(len(arr)):
        res += arr[i] ** 2
    return res
```

## 3. Type Stability

- **Types**: Ensure variables within JIT functions have stable types. Numba infers types at compile time.
- **Arguments**: Pass numpy arrays or scalar types. Avoid lists or dicts (though typed lists/dicts exist, they are slower/complex).
