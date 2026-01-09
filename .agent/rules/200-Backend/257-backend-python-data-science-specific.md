---
trigger: always_on
glob: "**/*.{py,ipynb}"
description: "Python Data Science: Best practices for Pandas, Numpy, and Matplotlib."
---
# Python Data Science Standards

## 1. NumPy

- **Vectorization**: Always prefer vectorized operations over loops.
- **Broadcasting**: Use broadcasting for arithmetic on arrays of different shapes.
- **Types**: Be mindful of dtypes (`float32` vs `float64`) for memory optimization.

## 2. Pandas

- **Chaining**: Use method chaining (`.assign()`, `.pipe()`) for readable transformations.
- **Indexing**: Use `.loc` (label-based) and `.iloc` (position-based) explicitly. Avoid chained indexing `df['col'][0]`.
- **Parquet**: Prefer Parquet for storage over CSV (faster, typed, smaller).
- **Memory**: Use `category` dtype for low-cardinality string columns.

## 3. Visualization

- **Matplotlib**: Use object-oriented API (`fig, ax = plt.subplots()`). Avoid state-based (`plt.plot()`).
- **Seaborn**: Use for statistical plots.
- **Clarity**: Always label axes, provide legends, and use colorblind-friendly palettes.

## 4. Notebooks (Jupyter)

- **Order**: Cells must execute linearly from top to bottom.
- **Imports**: All imports at the top.
- **Version Control**: Strip outputs before committing or use tools like `jupytext`.
- **Reproducibility**: Set random seeds (`np.random.seed(42)`).

## 5. Pipeline

- **Scikit-Learn**: Use `Pipeline` to encapsulate preprocessing and modeling.
- **Split**: Always split data into Train/Validation/Test sets to prevent leakage.
