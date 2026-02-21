---
description: Comprehensive workflow for Data Science analysis and production pipelines
---

# Data Science Workflow

Based on `320-data-science-general.md` and `321-data-science-pandas-specific.md`.

## For Exploratory Data Analysis (EDA)

1. **Setup Environment**

    Create organized workspace with notebook and virtual environment.

    ```bash
    # Create project structure
    mkdir -p notebooks data/{raw,processed} models
    touch notebooks/$(date +%Y%m%d)_exploratory_analysis.ipynb
    ```

    **Notebook imports:**

    ```python
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Configuration
    pd.set_option('display.max_columns', None)
    np.random.seed(42)
    sns.set_style('whitegrid')
    %matplotlib inline
    ```

2. **Data Loading & Initial Exploration**

    Load data and perform initial checks.

    ```python
    # Load data
    df = pd.read_csv('data/raw/dataset.csv')

    # Initial exploration
    print(df.head())
    print(df.info())
    print(df.describe())

    # Check for issues
    print("Missing values:\n", df.isna().sum())
    print("Duplicates:", df.duplicated().sum())
    print("Data types:\n", df.dtypes)
    ```

    **Check distributions:**

    ```python
    # Numerical distributions
    df.hist(figsize=(15, 10), bins=30)
    plt.tight_layout()
    plt.show()

    # Categorical value counts
    for col in df.select_dtypes(include='object').columns:
        print(f"\n{col}:\n{df[col].value_counts()}")
    ```

3. **Data Cleaning & Transformation**

    Create reproducible cleaning pipeline.

    ```python
    def clean_data(df):
        """Create reproducible cleaning function."""
        df = df.copy()

        # Fix data types
        df['date'] = pd.to_datetime(df['date'])
        df['category'] = df['category'].astype('category')

        # Handle missing values
        df['numeric_col'].fillna(df['numeric_col'].median(), inplace=True)
        df.dropna(subset=['critical_col'], inplace=True)

        # Remove duplicates
        df = df.drop_duplicates()

        return df

    # Apply cleaning
    df_clean = clean_data(df)
    ```

4. **Analysis & Visualization**

    Ask questions, visualize, interpret.

    ```python
    # Question: What is the relationship between X and Y?

    # Visualization
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_clean, x='feature_x', y='feature_y', hue='category')
    plt.title('Relationship between X and Y')
    plt.show()
    ```

    **Insight**: Write markdown observations after each plot.

5. **Statistical Modeling (Optional)**

    Build predictive models if needed.

    ```python
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier

    # Prepare data
    X = df_clean[['feature1', 'feature2', 'feature3']]
    y = df_clean['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Build and evaluate model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    print(f"Train score: {model.score(X_train, y_train):.3f}")
    print(f"Test score: {model.score(X_test, y_test):.3f}")
    ```

6. **Report Findings**

    Summarize insights in notebook.

    - Key findings (top or bottom of notebook)
    - Visualizations with explanations
    - Recommendations or next steps
    - Export clean data: `df_clean.to_csv('data/processed/clean_data.csv', index=False)`

---

## For Production ML Pipelines

1. **Exploratory Data Analysis (EDA)**

    Understand data before pipeline construction.

    - Check distributions and outliers
    - Identify missing values patterns
    - Analyze feature correlations
    - Document data quality issues

2. **Feature Engineering**

    Design reproducible transformations.

    ```python
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer

    # Define transformers
    numeric_features = ['age', 'income', 'score']
    categorical_features = ['category', 'region']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    ```

    **Critical**: Prevent data leakage - fit transformers on training data ONLY.

3. **Build scikit-learn Pipeline**

    Combine preprocessing and modeling.

    ```python
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestClassifier

    # Create full pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])

    # Fit pipeline
    pipeline.fit(X_train, y_train)

    # Pipeline ensures preprocessing applied consistently
    y_pred = pipeline.predict(X_test)
    ```

4. **Cross-Validation**

    Evaluate model robustness.

    ```python
    from sklearn.model_selection import cross_val_score

    # 5-fold cross-validation
    cv_scores = cross_val_score(
        pipeline, X_train, y_train,
        cv=5, scoring='accuracy'
    )

    print(f"CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    ```

5. **Hyperparameter Tuning**

    Optimize model parameters.

    ```python
    from sklearn.model_selection import GridSearchCV

    param_grid = {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [10, 20, None],
        'preprocessor__num__with_mean': [True, False]
    }

    grid_search = GridSearchCV(
        pipeline, param_grid, cv=5,
        scoring='accuracy', n_jobs=-1
    )

    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.3f}")
    ```

6. **Final Validation**

    Evaluate on held-out test set.

    ```python
    from sklearn.metrics import classification_report, confusion_matrix

    # Use best model from grid search
    best_pipeline = grid_search.best_estimator_

    # Evaluate on test set
    y_pred = best_pipeline.predict(X_test)

    print("Test Set Performance:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Check reproducibility
    # Re-run with same random seed should give identical results
    ```

7. **Model Persistence**

    Save trained pipeline for deployment.

    ```python
    import joblib

    # Save model
    joblib.dump(best_pipeline, 'models/production_model.pkl')

    # Load for inference
    loaded_model = joblib.load('models/production_model.pkl')
    predictions = loaded_model.predict(new_data)
    ```

---

## Best Practices

### Data Quality

- Always validate data before modeling
- Document assumptions and data transformations
- Version datasets (e.g., `data_v1.csv`, `data_v2.csv`)

### Reproducibility

- Set random seeds (`np.random.seed(42)`)
- Use virtual environments (venv, conda)
- Track dependencies (`requirements.txt`, `environment.yml`)
- Version control notebooks (use nbstripout for clean diffs)

### Pipeline Design

- **Always fit on training data only** (prevent leakage)
- Use sklearn Pipelines for consistent preprocessing
- Separate train/validation/test splits properly
- Consider stratification for imbalanced datasets

### Code Organization

- Extract reusable functions from notebooks
- Move production code to `.py` modules
- Write unit tests for custom transformers
- Use configuration files for hyperparameters

---

## See Also

- `agent/rules/320-data-science-general.md` - Data science principles
- `agent/rules/321-data-science-pandas-specific.md` - Pandas best practices
- `agent/rules/323-data-science-pytorch-specific.md` - Deep learning workflows
- `agent/rules/324-data-science-scikit-specific.md` - Scikit-learn patterns
- `agent/workflows/workflow-ml-training.md` - PyTorch model training
