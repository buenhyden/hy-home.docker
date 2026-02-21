---
description: Create Python project with Poetry, type hints, and testing setup
---

1. **Initialize Python project with Poetry**

    Create a new Python project using Poetry for dependency management.

    ```bash
    # Install Poetry if not already installed
    # curl -sSL https://install.python-poetry.org | python3 -

    # Create new project
    poetry new my-python-project
    cd my-python-project
    ```

    Project structure created:

    ```
    my-python-project/
    ├── my_python_project/
    │   └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── pyproject.toml
    └── README.md
    ```

2. **Configure pyproject.toml**

    Update `pyproject.toml` with Python version and dependencies based on `200-Backend/210-backend-python-general.md`.

    ```toml
    [tool.poetry]
    name = "my-python-project"
    version = "0.1.0"
    description = ""
    authors = ["Your Name <you@example.com>"]
    readme = "README.md"
    packages = [{include = "my_python_project"}]

    [tool.poetry.dependencies]
    python = "^3.11"

    [tool.poetry.group.dev.dependencies]
    pytest = "^7.4.0"
    pytest-cov = "^4.1.0"
    black = "^23.7.0"
    mypy = "^1.4.1"
    ruff = "^0.0.285"

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    ```

// turbo
3. **Install dependencies**

    Install all dependencies including dev dependencies.

    ```bash
    poetry install
    ```

    Creates virtual environment and installs packages.

4. **Setup code quality tools**

    Configure Black, Mypy, and Ruff for code quality.

    Create `pyproject.toml` configurations:

    ```toml
    [tool.black]
    line-length = 88
    target-version = ['py311']
    include = '\.pyi?$'

    [tool.mypy]
    python_version = "3.11"
    warn_return_any = true
    warn_unused_configs = true
    disallow_untyped_defs = true
    disallow_incomplete_defs = true

    [tool.ruff]
    line-length = 88
    target-version = "py311"
    select = ["E", "F", "I", "N", "W", "B", "C4"]

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = "test_*.py"
    python_classes = "Test*"
    python_functions = "test_*"
    ```

5. **Create project structure**

    Set up recommended directory structure per Python best practices.

    ```bash
    mkdir -p my_python_project/{api,core,utils}
    mkdir -p tests/{unit,integration}
    ```

    Create `__init__.py` files:

    ```bash
    touch my_python_project/{api,core,utils}/__init__.py
    touch tests/{unit,integration}/__init__.py
    ```

6. **Create example module with type hints**

    Create `my_python_project/core/example.py` with proper type annotations:

    ```python
    """Example module demonstrating Python best practices."""
    from typing import Optional


    def greet(name: str, greeting: Optional[str] = None) -> str:
        """
        Generate a greeting message.

        Args:
            name: The name of the person to greet.
            greeting: Optional custom greeting. Defaults to "Hello".

        Returns:
            A formatted greeting string.

        Examples:
            >>> greet("World")
            'Hello, World!'
            >>> greet("Alice", "Hi")
            'Hi, Alice!'
        """
        if greeting is None:
            greeting = "Hello"
        return f"{greeting}, {name}!"
    ```

7. **Create initial test**

    Create `tests/unit/test_example.py`:

    ```python
    """Tests for the example module."""
    import pytest
    from my_python_project.core.example import greet


    def test_greet_default():
        """Test greeting with default message."""
        assert greet("World") == "Hello, World!"


    def test_greet_custom():
        """Test greeting with custom message."""
        assert greet("Alice", "Hi") == "Hi, Alice!"


    def test_greet_empty_name():
        """Test greeting with empty string."""
        assert greet("") == "Hello, !"
    ```

// turbo
8. **Run tests**

    Execute tests to verify setup.

    ```bash
    poetry run pytest -v
    ```

    Expected: All tests pass.

// turbo
9. **Run code quality checks**

    Execute linting and type checking.

    ```bash
    # Format code
    poetry run black .

    # Lint
    poetry run ruff check .

    # Type check
    poetry run mypy my_python_project
    ```

    Expected: No errors.

10. **Setup pre-commit hooks (optional)**

    Create `.pre-commit-config.yaml`:

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
      - repo: https://github.com/pre-commit/mirrors-mypy
        rev: v1.4.1
        hooks:
          - id: mypy
            additional_dependencies: [types-all]
    ```

    Install pre-commit:

    ```bash
    poetry add --group dev pre-commit
    poetry run pre-commit install
    ```

11. **Create README**

    Update `README.md` with project information:

    ```markdown
    # My Python Project

    ## Setup

    ```bash
    poetry install
    ```

    ## Testing

    ```bash
    poetry run pytest
    ```

    ## Code Quality

    ```bash
    # Format
    poetry run black .

    # Lint
    poetry run ruff check .

    # Type check
    poetry run mypy my_python_project
    ```

    ## Development

    ```bash
    poetry shell  # Activate virtual environment
    ```

    ```

12. **Initialize Git**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize Python project with Poetry"
    ```

    **Next Steps:**

    - Review `agent/rules/200-Backend/210-backend-python-general.md` for Python best practices
    - Add FastAPI/Django if building web API (see `/workflow-fastapi-api` or `/workflow-django-feature`)
    - Setup CI/CD pipeline (`/.github/workflows/python-ci.yml`)
    - Consider adding Pydantic for data validation
