---
trigger: always_on
glob: "**/*.{py,ipynb}"
description: "Data Visualization: Matplotlib, Seaborn, and Plotting Best Practices."
---
# Data Visualization Standards

## 1. Plotting Hygiene

- **Labels**: ALWAYS label X/Y axes and provide a clear title.
- **Readability**: Adjust font sizes and figure sizes for the intended medium (report vs dashboard).
- **Legends**: Include legends for multi-series plots.

### Example: Basic Hygiene

**Good**

```python
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='User Growth')
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Monthly Active Users')
plt.legend()
plt.show()
```

**Bad**

```python
plt.plot(x, y) # No context, impossible to interpret
```

## 3. Matplotlib Standards

- **Object-Oriented Style**: ALWAYS use the OO interface (`fig, ax = plt.subplots()`) over the state-machine (`plt.plot()`) to avoid state confusion.
- **Resource Management**: Explicitly close figures (`plt.close(fig)`) in loops to leak memory.
- **Tight Layout**: Use `fig.tight_layout()` to prevent label clipping.

## 4. Seaborn Standards

- **Data Format**: Use "tidy" (long-form) Pandas DataFrames.
- **Theming**: Set global themes (`sns.set_theme()`) for consistency.
- **Faceting**: Use Figure-level functions (`relplot`, `displot`) for easy subplots.

## 5. Plotly Standards

- **Plotly Express**: Use `plotly.express` (px) for rapid prototyping.
- **Performance**: Use WebGL traces (`scattergl`) for >10k points.
- **Static Export**: Use `kaleido` for reports (`fig.write_image()`).

## 3. Interpretation

- **Scale**: Use log scales for power-law distributions.
- **Zero Baseline**: Bar charts should almost always start at zero.
