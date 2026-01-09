---
trigger: always_on
glob: "**/*.py"
description: "Statsmodels: Statistical Modeling Standards."
---
# Statsmodels Standards

## 1. Input Data

- **Pandas**: Use pandas DataFrames with clearly named columns as inputs. Avoid raw numpy arrays where possible to keep model summaries readable.
- **Constants**: Remember to add a constant column manually (`sm.add_constant(X)`) for regression models (OLS), as statsmodels does not add intercept by default.

### Example: OLS

**Good**

```python
import statsmodels.api as sm
X = sm.add_constant(df[['feature1', 'feature2']])
model = sm.OLS(df['target'], X).fit()
```

## 2. Formulas

- **R-Style**: Use the formula API (`statsmodels.formula.api`) for concise model specification, especially when interactions or categorical variables are involved.

### Example: Formula

**Good**

```python
import statsmodels.formula.api as smf
model = smf.ols('target ~ feature1 + feature2 * category', data=df).fit()
```

## 3. Diagnostics

- **Assumptions**: Always check model assumptions (homoscedasticity, normality of residuals) using built-in diagnostic plots and tests (`model.summary()`, `sm.stats.diagnostic`).
