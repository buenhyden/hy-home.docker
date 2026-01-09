---
trigger: always_on
glob: "**/*.{py,ipynb}"
description: "Data Science & Analysis: NumPy, Pandas, Visualization (Matplotlib/Seaborn), and ML practices."
---
# Python Data Science Standards

## 1. NumPy Best Practices

- **Vectorization**: Always prefer vector operations over loops.
- **Broadcasting**: Use broadcasting for dimension-agnostic operations.
- **Dtypes**: Explicitly set data types for memory optimization.

## 2. Pandas Data Manipulation

- **Chaining**: Use method chaining (`.assign().query().pipe()`) for readable pipelines.
- **Memory**: Use `category` dtype for low-cardinality string columns.
- **Parquet**: Prefer Parquet over CSV for storage (types, compression).

## 3. Visualization

- **Matplotlib**: Use Object-Oriented interface (`fig, ax = plt.subplots()`).
- **Seaborn**: Use for statistical plots.
- **Clarity**: Always label axes, title plots, and use colorblind-friendly palettes.

## 4. Machine Learning (Scikit-Learn)

- **Pipelines**: Use `Pipeline` to prevent data leakage (transformation inside CV).
- **Splitting**: Always split data into Train/Val/Test.
- **Reproducibility**: Set `random_state`.

### Example: Vectorization & Pipelines

#### Good

```python
# NumPy Vectorization
import numpy as np
arr = np.array([1, 2, 3])
result = arr * 2

# Sklearn Pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression())
])
```

#### Bad

```python
# Slow Loops
result = []
for x in arr:
    result.append(x * 2)

# Leakage (Transforming before split)
data = scaler.fit_transform(raw_data)
X_train, X_test = train_test_split(data) # Leakage!
```
