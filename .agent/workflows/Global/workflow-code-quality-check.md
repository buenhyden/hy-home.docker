---
description: Run comprehensive code quality checks (linting, formatting, type checking)
---

1. **Identify project type and stack**

    Determine the primary language/framework to run appropriate quality tools.

    Check for:
    - `package.json` → JavaScript/TypeScript (Node.js, React, etc.)
    - `pyproject.toml` or `requirements.txt` → Python
    - `go.mod` → Go
    - `Cargo.toml` → Rust
    - `pubspec.yaml` → Flutter/Dart

2. **JavaScript/TypeScript quality checks**

    Run linting, formatting, and type checking for JS/TS projects.

    // turbo
    **ESLint (Linting):**

    ```bash
    npm run lint
    # or if not in scripts
    npx eslint . --ext .js,.jsx,.ts,.tsx
    ```

    Fix auto-fixable issues:

    ```bash
    npx eslint . --ext .js,.jsx,.ts,.tsx --fix
    ```

    // turbo
    **Prettier (Formatting):**

    ```bash
    # Check formatting
    npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,md}"

    # Fix formatting
    npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"
    ```

    // turbo
    **TypeScript (Type Checking):**

    ```bash
    npx tsc --noEmit
    ```

    Expected: No type errors.

    **Additional checks:**

    ```bash
    # Check for unused dependencies
    npx depcheck

    # Check for security vulnerabilities
    npm audit
    ```

3. **Python quality checks**

    Run linting, formatting, and type checking for Python projects.

    // turbo
    **Black (Formatting):**

    ```bash
    # Check formatting
    black --check .

    # Fix formatting
    black .
    ```

    // turbo
    **Ruff (Linting):**

    ```bash
    # Lint
    ruff check .

    # Fix auto-fixable issues
    ruff check --fix .
    ```

    Alternative: Use flake8

    ```bash
    flake8 . --max-line-length=88 --extend-ignore=E203
    ```

    // turbo
    **Mypy (Type Checking):**

    ```bash
    mypy .
    ```

    For strict mode:

    ```bash
    mypy . --strict
    ```

    // turbo
    **isort (Import Sorting):**

    ```bash
    # Check
    isort --check-only .

    # Fix
    isort .
    ```

    **Security check:**

    ```bash
    uv pip install safety
    safety check
    ```

4. **Go quality checks**

    Run linting, formatting, and vetting for Go projects.

    // turbo
    **gofmt (Formatting):**

    ```bash
    # Check formatting
    gofmt -l .

    # Fix formatting
    gofmt -w .
    ```

    // turbo
    **golangci-lint (Comprehensive Linting):**

    ```bash
    golangci-lint run
    ```

    If not installed:

    ```bash
    go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
    ```

    // turbo
    **go vet (Code Vetting):**

    ```bash
    go vet ./...
    ```

    // turbo
    **staticcheck (Advanced Analysis):**

    ```bash
    staticcheck ./...
    ```

    If not installed:

    ```bash
    go install honnef.co/go/tools/cmd/staticcheck@latest
    ```

5. **Rust quality checks**

    Run linting and formatting for Rust projects.

    // turbo
    **rustfmt (Formatting):**

    ```bash
    # Check formatting
    cargo fmt -- --check

    # Fix formatting
    cargo fmt
    ```

    // turbo
    **Clippy (Linting):**

    ```bash
    cargo clippy -- -D warnings
    ```

    Fix suggestions:

    ```bash
    cargo clippy --fix
    ```

    // turbo
    **cargo check (Quick Compile Check):**

    ```bash
    cargo check
    ```

6. **Flutter/Dart quality checks**

    Run analysis and formatting for Flutter projects.

    // turbo
    **dart format (Formatting):**

    ```bash
    # Check formatting
    dart format --output=none --set-exit-if-changed .

    # Fix formatting
    dart format .
    ```

    // turbo
    **flutter analyze (Analysis):**

    ```bash
    flutter analyze
    ```

    Expected: No analysis issues.

7. **Check code complexity**

    Identify overly complex functions that need refactoring.

    **Python (radon):**

    ```bash
    uv pip install radon
    radon cc . -a -nb  # Cyclomatic complexity
    radon mi . -nb     # Maintainability index
    ```

    **JavaScript (escomplex):**

    ```bash
    npx escomplex --format markdown src/**/*.js
    ```

    Target: Cyclomatic complexity < 10 per function.

8. **Check for code smells**

    Detect common anti-patterns and code smells.

    **Python (pylint):**

    ```bash
    pylint your_module --disable=C0111  # Disable docstring warnings if needed
    ```

    **JavaScript/TypeScript (SonarQube):**
    Use SonarQube or SonarCloud for comprehensive analysis.

9. **Run all quality checks together**

    Create a single command to run all quality checks.

    **For JavaScript/TypeScript (add to package.json):**

    ```json
    {
      "scripts": {
        "quality": "npm run lint && npm run format:check && npm run typecheck",
        "quality:fix": "npm run lint:fix && npm run format:write",
        "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
        "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
        "format:check": "prettier --check \"**/*.{js,jsx,ts,tsx,json,css,md}\"",
        "format:write": "prettier --write \"**/*.{js,jsx,ts,tsx,json,css,md}\"",
        "typecheck": "tsc --noEmit"
      }
    }
    ```

    Run:

    ```bash
    npm run quality
    ```

    **For Python (create Makefile):**

    ```makefile
    .PHONY: quality quality-fix

    quality:
     black --check .
     ruff check .
     mypy .
     isort --check-only .

    quality-fix:
     black .
     ruff check --fix .
     isort .
    ```

    Run:

    ```bash
    make quality
    ```

    **For Go (create Makefile):**

    ```makefile
    .PHONY: quality

    quality:
     gofmt -l .
     golangci-lint run
     go vet ./...
     staticcheck ./...
    ```

    Run:

    ```bash
    make quality
    ```

10. **Generate quality report**

    Create a summary report of code quality issues.

    ```bash
    # Create report directory
    mkdir -p reports

    # JavaScript/TypeScript (ESLint JSON output)
    npx eslint . --ext .js,.jsx,.ts,.tsx --format json --output-file reports/eslint-report.json

    # Python (combine outputs)
    {
      echo "# Code Quality Report - $(date)"
      echo ""
      echo "## Black (Formatting)"
      black --check . 2>&1
      echo ""
      echo "## Ruff (Linting)"
      ruff check . 2>&1
      echo ""
      echo "## Mypy (Type Checking)"
      mypy . 2>&1
    } > reports/quality-report.md
    ```

11. **Setup pre-commit hooks**

    Auto-run quality checks before each commit.

    **Install pre-commit:**

    ```bash
    uv tool install pre-commit
    ```

    **Create `.pre-commit-config.yaml`:**

    For Python:

    ```yaml
    repos:
      - repo: https://github.com/psf/black
        rev: 23.7.0
        hooks:
          - id: black
      - repo: https://github.com/charliermarsh/ruff-pre-commit
        rev: v0.0.285
        hooks:
          - id: ruff
            args: [--fix]
      - repo: https://github.com/pre-commit/mirrors-mypy
        rev: v1.4.1
        hooks:
          - id: mypy
    ```

    For JavaScript/TypeScript:

    ```yaml
    repos:
      - repo: https://github.com/pre-commit/mirrors-eslint
        rev: v8.46.0
        hooks:
          - id: eslint
            files: \.(js|jsx|ts|tsx)$
            args: [--fix]
      - repo: https://github.com/pre-commit/mirrors-prettier
        rev: v3.0.1
        hooks:
          - id: prettier
    ```

    **Install hooks:**

    ```bash
    pre-commit install
    ```

12. **Review and fix issues**

    Review all reported issues and fix them.

    **Priority order:**
    1. **Critical**: Type errors, syntax errors
    2. **High**: Security issues, potential bugs
    3. **Medium**: Code smells, complexity warnings
    4. **Low**: Style inconsistencies, formatting

    **Common fixes:**
    - Remove unused imports
    - Add missing type annotations
    - Simplify complex functions (break into smaller ones)
    - Fix naming conventions
    - Add docstrings/comments to complex logic

    **Next Steps:**
    - Setup CI/CD to run quality checks automatically
    - Review `agent/rules/000-Core/006-core-clean-code-quality.md` for quality standards
    - Consider SonarQube for continuous code quality monitoring
    - Setup code coverage thresholds (>80% recommended)
