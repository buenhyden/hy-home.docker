---
trigger: always_on
glob: "**/*.py"
description: "SciPy: Scientific Computing Standards."
---
# SciPy Standards

## 1. Modules

- **Specific Imports**: Import submodules explicitly (e.g., `from scipy import optimize`, `from scipy import stats`). The top-level `scipy` package imports almost nothing.

### Example: Imports

**Good**

```python
from scipy import stats
stat, p = stats.ttest_ind(group1, group2)
```

**Bad**

```python
import scipy
# scipy.stats is likely not available unless explicitly imported sometimes
```

## 2. API Selection

- **Modern APIs**: Prefer newer APIs over legacy ones (e.g., use `scipy.signal.sosfilt` (Second-Order Sections) over `tf2zpk` for deeper stability in filter design).
- **Optimization**: Use `optimize.minimize` as the unified interface rather than specific solvers unless you have a specific reason (e.g., `fmin_bfgs`).

## 3. Sparse Matrices

- **Format**: Choose the right sparse matrix format:
  - `LIL` or `DOK` for constructing matrices.
  - `CSR` or `CSC` for arithmetic and vector operations.
- **Conversion**: explicitly convert to CSR/CSC before doing heavy math (`.tocsr()`).
