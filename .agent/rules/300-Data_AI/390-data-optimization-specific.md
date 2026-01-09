---
trigger: always_on
glob: "**/*.{py,sql}"
description: "Data Optimization: Vectorization (Pandas/NumPy) and SQL Batching."
---
# Data Optimization Standards

## 1. Vectorization (Python)

- **No Loops**: "Loops are slow". Use Pandas/NumPy vectorized operations.
- **Broadcasting**: Leverage array broadcasting instead of `apply()`.

### Example: Vectorization

**Good**

```python
df['total'] = df['price'] * df['quantity']
```

**Bad**

```python
# 1000x slower
for i, row in df.iterrows():
    df.at[i, 'total'] = row['price'] * row['quantity']
```

## 2. Batch Processing

- **Bulk Insert**: Insert rows in chunks (e.g., 1000 at a time), not one by one.
- **Streaming**: Stream large datasets (GBs) instead of loading `result.fetchall()` into RAM.

### Example: Bulk

**Good**

```python
db.bulk_insert(records, chunk_size=1000)
```

**Bad**

```python
for r in records:
    db.insert(r)
```
