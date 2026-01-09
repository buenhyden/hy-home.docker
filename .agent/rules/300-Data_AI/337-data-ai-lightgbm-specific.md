---
trigger: always_on
glob: "**/*.py"
description: "LightGBM: Model Training, Hyperparameters, and Reproducibility specific rules."
---
# LightGBM Specific Rules

## 1. API Usage

- **Scikit-learn API**: Use `LGBMClassifier` and `LGBMRegressor` for compatibility with sklearn pipelines.
- **Reproducibility**: ALWAYS set `random_state` (or `seed`) and `deterministic=True`.

## 2. Data Handling

- **Categoricals**: Use native categorical support (`categorical_feature` parameter). Do NOT one-hot encode high-cardinality features manually.
- **Missing Values**: LightGBM handles NaNs natively. Only impute if you have a specific reason.

### Example: Categorical Features

**Good**

```python
# Pass indices of categorical columns
clf = lgb.LGBMClassifier(categorical_feature=[0, 2])
clf.fit(X, y)
```

## 3. Hyperparameters

- **Tuning**: Use tools like Optuna. Do not manually guess.
- **Overfitting Prevention**:
  - `num_leaves` must be `< 2^max_depth`.
  - Use `early_stopping` with a validation set.
  - increasing `min_data_in_leaf` can prevent overfitting.

### Example: Safe Configuration

**Good**

```python
model = lgb.LGBMClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    num_leaves=31, # < 2^6 (64)
    max_depth=6,
    random_state=42
)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[lgb.early_stopping(50)]
)
```
