---
trigger: always_on
glob: "**/*.py"
description: "XGBoost: Efficiency, API selection, and Configuration specific rules."
---
# XGBoost Specific Rules

## 1. API Selection

- **Scikit-learn API**: Use `XGBClassifier`/`XGBRegressor` for standard pipelines.
- **Native API**: Use `xgb.train` ONLY when you need fine-grained control or custom objectives.
- **DMatrix**: If using Native API, convert data to `DMatrix` once to avoid overhead.

## 2. Configuration & Performance

- **Tree Method**: Prefer `tree_method='hist'` for modern systems (faster).
- **Device**: Use `device='cuda'` if GPU is available.
- **Monitoring**: Use `eval_set` and early stopping during training.

### Example: Efficient Training

**Good**

```python
clf = xgb.XGBClassifier(
    tree_method="hist",
    device="cuda",
    early_stopping_rounds=10,
    n_estimators=500
)
clf.fit(X_train, y_train, eval_set=[(X_val, y_val)])
```

## 3. Code Style

- **Docstrings**: Use NumPy-style docstrings.
- **Type Hints**: Annotate training functions with `np.ndarray` or `pd.DataFrame`.

### Example: Typed Function

**Good**

```python
def train_model(X: pd.DataFrame, y: pd.Series) -> xgb.XGBClassifier:
    """Trains an XGBoost classifier."""
    model = xgb.XGBClassifier(random_state=42)
    model.fit(X, y)
    return model
```
