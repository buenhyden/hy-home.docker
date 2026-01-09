---
trigger: always_on
glob: "**/*.py"
description: "Scikit-Learn: Pipelines, Preprocessing, and Model Selection."
---
# Scikit-Learn Standards

## 1. Pipelines

- **Usage**: Always use `Pipeline` to bundle preprocessing and modeling. Prevents data leakage.
- **Scaling**: fit scaler ONLY on Train set.

### Example: Pipeline

**Good**

```python
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC())
])
pipe.fit(X_train, y_train) # Safe
```

**Bad**

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X) # Leak! Fits on Test data too if split later
X_train, X_test = train_test_split(X_scaled)
```

## 2. Model Selection

- **Cross Val**: Use `cross_val_score` or `GridSearchCV`.
- **Metrics**: Use appropriate metrics (F1 for imbalanced, MSE for regression).

### Example: Leakage

**Good**

```python
# Split First
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

**Bad**

```python
# Smote/Oversampling BEFORE split = Leakage
X_resampled, y_resampled = SMOTE().fit_resample(X, y)
X_train, X_test = train_test_split(X_resampled) # Test set now contains synthetic copies of Train data
```
