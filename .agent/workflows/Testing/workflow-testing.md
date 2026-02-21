---
description: Setup testing environment and run comprehensive test suite with coverage
---

1. **Identify testing framework**

    Check which testing framework is used in the project.

    Look for:
    - `package.json` → Jest, Vitest, Mocha (JavaScript/TypeScript)
    - `pyproject.toml` or `requirements.txt` → pytest (Python)
    - `go.mod` → testing package (Go)
    - `Cargo.toml` → cargo test (Rust)

2. **Install testing dependencies**

    Install necessary testing tools and coverage reporters.

    **For JavaScript/TypeScript (Jest):**

    ```bash
    npm install --save-dev jest @testing-library/react @testing-library/jest-dom
    npm install --save-dev @testing-library/user-event jest-environment-jsdom
    npm install --save-dev @types/jest  # TypeScript
    ```

    **For JavaScript/TypeScript (Vitest):**

    ```bash
    npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
    npm install --save-dev @vitest/ui @vitest/coverage-v8
    ```

    **For Python (pytest):**

    ```bash
    uv pip install pytest pytest-cov pytest-mock
    uv pip install pytest-asyncio  # for async tests
    ```

    **For Go:**

    ```bash
    # Built-in, no installation needed
    go install github.com/onsi/ginkgo/v2/ginkgo@latest  # if using Ginkgo
    go install github.com/onsi/gomega/...@latest
    ```

3. **Configure test framework**

    Setup test configuration based on project needs.

    **Jest (`jest.config.js`):**

    ```javascript
    module.exports = {
      testEnvironment: 'jsdom',
      setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
      collectCoverageFrom: [
        'src/**/*.{js,jsx,ts,tsx}',
        '!src/**/*.d.ts',
        '!src/**/*.stories.{js,jsx,ts,tsx}',
      ],
      coverageThreshold: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    };
    ```

    **Vitest (`vitest.config.ts`):**

    ```typescript
    import { defineConfig } from 'vitest/config';

    export default defineConfig({
      test: {
        environment: 'jsdom',
        globals: true,
        setupFiles: './vitest.setup.ts',
        coverage: {
          reporter: ['text', 'json', 'html'],
          exclude: ['**/*.config.*', '**/*.d.ts'],
        },
      },
    });
    ```

    **pytest (`pyproject.toml`):**

    ```toml
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    python_files = "test_*.py"
    python_classes = "Test*"
    python_functions = "test_*"
    addopts = "-v --cov=src --cov-report=html --cov-report=term"
    ```

4. **Create test directory structure**

    Organize tests following best practices (based on `600-Testing` rules).

    ```bash
    # For JavaScript/TypeScript
    mkdir -p src/__tests__/{unit,integration,e2e}
    mkdir -p src/components/__tests__

    # For Python
    mkdir -p tests/{unit,integration,e2e}
    mkdir -p tests/fixtures

    # For Go
    mkdir -p internal/pkg_test
    ```

    Follow **Test Pyramid**:
    - Unit Tests: 70-80% (isolated functions)
    - Integration Tests: 15-20% (component interaction)
    - E2E Tests: 5-10% (user journey)

5. **Write sample unit test**

    Create an example test following AAA pattern (Arrange-Act-Assert).

    **JavaScript/TypeScript (Jest/Vitest):**

    Create `src/utils/__tests__/example.test.ts`:

    ```typescript
    import { add } from '../math';

    describe('Math utilities', () => {
      it('should add two numbers correctly', () => {
        // Arrange
        const a = 2;
        const b = 3;

        // Act
        const result = add(a, b);

        // Assert
        expect(result).toBe(5);
      });

      it('should handle negative numbers', () => {
        expect(add(-1, 1)).toBe(0);
      });

      it('should handle edge case: zero', () => {
        expect(add(0, 0)).toBe(0);
      });
    });
    ```

    **Python (pytest):**

    Create `tests/unit/test_example.py`:

    ```python
    import pytest
    from src.utils.math import add


    def test_add_two_numbers():
        """Test adding two positive numbers."""
        # Arrange
        a = 2
        b = 3

        # Act
        result = add(a, b)

        # Assert
        assert result == 5


    def test_add_negative_numbers():
        """Test adding negative numbers."""
        assert add(-1, 1) == 0


    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 1, 2),
        (-1, -1, -2),
        (100, 200, 300),
    ])
    def test_add_parametrized(a, b, expected):
        """Test addition with multiple inputs."""
        assert add(a, b) == expected
    ```

// turbo
6. **Run unit tests**

    Execute the unit test suite.

    ```bash
    # Jest
    npm test

    # Vitest
    npm run test

    # pytest
    pytest tests/unit

    # Go
    go test ./... -v

    # Rust
    cargo test
    ```

    Expected: Tests pass. If any fail, review and fix.

// turbo
7. **Run tests with coverage**

    Generate code coverage report.

    ```bash
    # Jest
    npm test -- --coverage

    # Vitest
    npm run test -- --coverage

    # pytest
    pytest --cov=src --cov-report=html

    # Go
    go test ./... -coverprofile=coverage.out
    go tool cover -html=coverage.out

    # Rust
    cargo install cargo-tarpaulin
    cargo tarpaulin --out Html
    ```

    **Coverage targets** (from `600-Testing` standards):
    - Overall: >80%
    - Critical business logic: >90%
    - Utils/helpers: >70%

8. **Review coverage report**

    Open and analyze coverage report.

    ```bash
    # JavaScript/TypeScript
    open coverage/lcov-report/index.html

    # Python
    open htmlcov/index.html

    # Go
    # Already opened in step 7

    # Rust
    open tarpaulin-report.html
    ```

    Identify uncovered lines and add tests for:
    - Edge cases (null, empty, boundaries)
    - Error conditions
    - Complex logic branches

9. **Setup mocking for external dependencies**

    Configure mocks for APIs, databases, external services.

    **JavaScript (Jest):**

    ```javascript
    // __mocks__/api.ts
    export const fetchUser = jest.fn().mockResolvedValue({
      id: '123',
      name: 'Test User',
    });
    ```

    **Python (pytest with pytest-mock):**

    ```python
    def test_api_call(mocker):
        """Test function that calls external API."""
        # Mock the API call
        mock_response = mocker.Mock()
        mock_response.json.return_value = {'data': 'test'}
        mocker.patch('requests.get', return_value=mock_response)

        # Test your function
        result = fetch_data()
        assert result['data'] == 'test'
    ```

10. **Write integration tests**

    Test component interactions (no external services).

    Create `tests/integration/test_user_workflow.py`:

    ```python
    def test_user_creation_and_retrieval(db_session):
        """Test creating and retrieving a user."""
        # Arrange
        user_data = {'email': 'test@example.com', 'name': 'Test User'}

        # Act: Create user
        user = create_user(db_session, user_data)

        # Act: Retrieve user
        retrieved = get_user_by_email(db_session, 'test@example.com')

        # Assert
        assert retrieved.name == 'Test User'
        assert retrieved.email == 'test@example.com'
    ```

// turbo
11. **Run all tests**

    Execute complete test suite (unit + integration).

    ```bash
    # JavaScript/TypeScript
    npm run test:all

    # Python
    pytest

    # Go
    go test ./... -v

    # Rust
    cargo test --all
    ```

12. **Setup continuous testing**

    Configure test automation for development.

    **Add to `package.json`:**

    ```json
    {
      "scripts": {
        "test": "vitest",
        "test:unit": "vitest run src",
        "test:integration": "vitest run tests/integration",
        "test:watch": "vitest watch",
        "test:coverage": "vitest run --coverage",
        "test:ui": "vitest --ui"
      }
    }
    ```

    **For CI/CD**, create `.github/workflows/test.yml`:

    ```yaml
    name: Tests
    on: [push, pull_request]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - uses: actions/setup-node@v3
            with:
              node-version: '18'
          - run: npm ci
          - run: npm test -- --coverage
          - uses: codecov/codecov-action@v3
    ```

    **Next Steps:**
    - Review `agent/rules/600-Testing` for testing best practices
    - Add E2E tests with Playwright or Cypress (`/workflow-playwright-testing`)
    - Setup mutation testing for test quality verification
    - Configure test parallelization for faster execution
