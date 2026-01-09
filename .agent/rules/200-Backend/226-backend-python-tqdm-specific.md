---
trigger: always_on
glob: "**/*.py"
description: "TQDM: Progress Bar Best Practices."
---
# TQDM Standards

## 1. Usage

- **Context Manager**: Use `tqdm` as a context manager (`with tqdm(...) as pbar:`) or wrap iterables directly.
- **Imports**: Import explicitly: `from tqdm import tqdm, trange`.

### Example: Loop

**Good**

```python
for item in tqdm(items, desc="Processing"):
    process(item)
```

## 2. Visualization

- **Updates**: For manual updates, always instantiate with `total=N` so the bar renders correctly.
- **Descriptions**: Use `set_description()` and `set_postfix()` to provide useful, real-time context (e.g., current loss, accuracy).

## 3. Environment

- **Notebooks**: Use `tqdm.auto` or `tqdm.notebook` if running in Jupyter to get HTML widgets instead of text bars.
