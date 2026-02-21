---
description: Create Python project with uv (Astral), type hints, and testing setup
---

1. **Initialize Python project with uv**

    Create a new Python project using uv for ultra-fast package management.

    ```bash
    # Install uv if not already installed
    # curl -LsSf https://astral.sh/uv/install.sh | sh

    # Create new project
    uv init my-python-project
    cd my-python-project
    ```

    Project structure created:

    ```
    my-python-project/
    ├── src/
    │   └── my_python_project/
    │       └── __init__.py
    ├── tests/
    │   └── __init__.py
    ├── pyproject.toml
    ├── .python-version
    └── README.md
    ```

2. **Add Dependencies**

    Add dependencies using `uv add`. This updates `pyproject.toml` and lockfile automatically.

    ```bash
    # Add runtime dependencies
    uv add requests

    # Add dev dependencies
    uv add --dev pytest pytest-cov black mypy ruff
    ```

3. **Configure Code Quality Tools**

    Update `pyproject.toml` with configurations for Ruff, Black (via Ruff in modern setups usually, but here keeping consistent), and Mypy.

    ```toml
    [tool.ruff]
    line-length = 88
    target-version = "py311"
    select = ["E", "F", "I", "N", "W", "B", "C4"]

    [tool.mypy]
    python_version = "3.11"
    warn_return_any = true
    warn_unused_configs = true
    disallow_untyped_defs = true
    disallow_incomplete_defs = true

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = "test_*.py"
    python_classes = "Test*"
    python_functions = "test_*"
    ```

// turbo
4. **Sync Environment**

    Ensure virtual environment is in sync.

    ```bash
    uv sync
    ```

5. **Create project structure**

    Set up recommended directory structure.

    ```bash
    mkdir -p src/my_python_project/{api,core,utils}
    mkdir -p tests/{unit,integration}
    ```

    Create `__init__.py` files:

    ```bash
    touch src/my_python_project/{api,core,utils}/__init__.py
    touch tests/{unit,integration}/__init__.py
    ```

6. **Create example module with type hints**

    Create `src/my_python_project/core/example.py`:

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

    Execute tests using `uv run`.

    ```bash
    uv run pytest -v
    ```

    Expected: All tests pass.

// turbo
9. **Run code quality checks**

    Execute linting and type checking via `uv run`.

    ```bash
    # Format (using ruff format is recommended with uv, but black works too)
    uv run black .

    # Lint
    uv run ruff check .

    # Type check
    uv run mypy src
    ```

    Expected: No errors.

10. **Initialize Git**

    Initialize git repository and make initial commit.

    ```bash
    git init
    git add .
    git commit -m "chore: initialize Python project with uv"
    ```

    **Next Steps:**

    - Review `agent/rules/200-Backend/210-backend-python-general.md` for Python best practices
    - Add FastAPI/Django if building web API
    - Setup CI/CD pipeline
