---
trigger: always_on
glob: "**/*.ipynb"
description: "Jupyter Notebook: Reproducibility, Cell Order, and Cleanup."
---
# Jupyter Notebook Standards

## 1. Reproducibility

- **Top-to-Bottom**: Notebooks MUST be runnable from top to bottom (Restart & Run All).
- **Seeds**: Set seeds for all random operations.
- **Dependencies**: List or import all required libraries in the first cell.

### Example: Cell Order

**Good**

1. Imports & Config
2. Data Loading
3. Preprocessing
4. Modeling
5. Evaluation

**Bad**
> Jumping back and forth between cells, redefining variables in cell 10 that were used in cell 2.

## 2. Cleanliness

- **Drafting**: Delete "temp" or "debug" cells before committing.
- **Narrative**: Use Markdown cells to explain the logic and findings between code cells.
- **Output Size**: Clear large outputs (huge tables/plots) if not necessary for the documentation to keep file sizes small.

### Example: Documentation

**Good**

```markdown
### Data Cleaning
We are dropping rows with missing 'target' values because they cannot be used for training.
```

```python
df = df.dropna(subset=['target'])
```

**Bad**

```python
df = df.dropna() # Why? No explanation.
```

## 3. Version Control

- **Strip Output**: Use `nbstripout` or similar tools to avoid committing binary blob outputs (diff noise).
