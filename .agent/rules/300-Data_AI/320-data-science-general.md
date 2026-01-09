---
trigger: always_on
glob: "**/*.{py,ipynb}"
description: "Data Science & Analysis: EDA, Cleaning, Feature Engineering, and Reproducibility."
---
# Data Science & Analysis Standards

## 1. Exploratory Data Analysis (EDA)

- **Visualization**: Start with distributions (Histograms) and correlations (Heatmaps).
- **Outliers**: Identify and document how outliers are handled (removal, capping, or keeping).
- **Missing Data**: Use a systematic approach for imputation (Mean, Median, K-NN) rather than just dropping rows.

## 2. Data Cleaning Lifecycle

- **Type Casting**: Ensure numeric columns are not stored as strings.
- **Formatting**: Standardize string values (lower-case, trim whitespace).
- **Deduplication**: Check for duplicate records early in the pipeline.

### Example: Cleaning

**Good**

```python
df['category'] = df['category'].str.lower().str.strip()
df = df.drop_duplicates(subset=['user_id', 'timestamp'])
```

**Bad**

```python
# Assuming data is clean and proceeding to modeling
model.fit(X, y) # Fails or produces biased results due to ' Category' vs 'category'
```

## 3. Feature Engineering

- **Scaling**: Standardize (Z-score) or Normalize (Min-Max) features for distance-based models.
- **Encoding**: Use One-Hot for low cardinality and Target/Binary encoding for high cardinality categories.
- **Leaking**: NEVER use information from the target variable to engineer features (Data Leakage).

## 4. Reproducibility & Integrity

- **Random States**: Always use `random_state` or `np.random.seed`.
- **Environment**: Use `requirements.txt` or `environment.yml` to lock library versions.
- **Versioned Data**: Track datasets using `DVC` or similar if the data evolves over time.
