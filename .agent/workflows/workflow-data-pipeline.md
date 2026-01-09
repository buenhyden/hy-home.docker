---
description: Standard workflow for data science pipelines
---

# Data Pipeline Workflow

Based on `320-data-science-general.md` and `310-data-science-python-specific.md`.

1. **Exploratory Data Analysis (EDA)**
   - Check distributions.
   - Check missing values.

2. **Cleaning**
   - Type casting.
   - Deduplication.
   - Handle missing data (Impute/Drop).

3. **Feature Engineering**
   - Scaling (StandardScaler).
   - Encoding (OneHot).
   - **Crucial**: Prevent Data Leakage (Fit on Train ONLY).

4. **Modeling**
   - Use Pipelines (`sklearn.pipeline.Pipeline`).
   - Cross-Validate.

5. **Validation**
   - Evaluate on Test Set.
   - check reproducibility (Seeds).
