---
trigger: always_on
glob: "**/*.py"
description: "Pandas: Data manipulation, vectorization, and performance best practices."
---
# Pandas Standards

## 1. Syntax & Imports

- **Import**: `import pandas as pd`.
- **Method Chaining**: Prefer method chaining (`df.query(...).assign(...)`) over multiple intermediate variables.
- **Access**: Use `.loc` and `.iloc` for explicit setting to avoid `SettingWithCopyWarning`.

## 2. Performance (Vectorization)

- **No Loops**: Avoid `for row in df.iterrows()` or `.apply(axis=1)` if possible.
- **Vectorized Ops**: Use native pandas/numpy array operations (`df['a'] + df['b']`).
- **`eval()` / `query()`**: Use for complex filtering/calculation on large dataframes (C-engine optimized).

## 3. Data Loading

- **Types**: Specify `dtype` and `usecols` in `read_csv` to optimize memory.
- **Dates**: Use `parse_dates` argument.

## 4. Types & Nulls

- **Nullable Types**: Use `Int64`, `Float32`, `StringDtype` for nullable native types.
- **Null Handling**: Explicitly `fillna`, `dropna`, or `interpolate`.

## 5. Testing

- **Equality**: Use `pd.testing.assert_frame_equal` and `assert_series_equal`. Do not use `==`.
