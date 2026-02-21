# Global Testing Strategy

This directory serves as the root for all project-wide tests (e.g., global integration suites, E2E tests, and load tests).

**Important Note on Co-location (`[REQ-FSTR-09]`)**: Unit tests specific to a single component MUST be co-located in the same directory as the component file (e.g., within `src/features/auth/components/`). This `tests/` directory is reserved for tests that span across multiple components or the entire application. It sets the global standard, but it does NOT replace the strict co-location rule for unit logic.

## 1. Governance & Standards

All tests written in this repository **MUST** adhere to the rules defined in `.agent/rules/0700-Testing_and_QA/0700-testing-and-qa-standard.md`.

## 2. The Testing Pyramid `[REQ-TST-01]`

We strictly enforce the testing pyramid methodology to balance execution speed with confidence:

- **Unit Tests (~70%)**: Fast, isolated tests focusing on single functions or components. MUST be strictly co-located with the source code (`[REQ-FSTR-09]`) unless they are generic shared-utility tests that belong in a dedicated `unit/` folder here.
- **Integration Tests (~20%)**: Slower tests verifying that multiple units (or external dependencies like databases) work together. Stored in `integration/`.
- **End-to-End (E2E) Tests (~10%)**: Heaviest tests running against a fully deployed environment (or robust mock) simulating real user journeys. Stored in `e2e/`.

## 3. Mandatory Quality Gates

- **`[REQ-TST-04]` Coverage Minimum**: The global project code coverage must be **>= 80%**. Pull Requests that drop the coverage below this baseline will fail the CI gate.
- **`[REQ-TST-09]` Explicit Assertions**: Tests must use the **AAA (Arrange-Act-Assert)** pattern. "Blind" tests that merely check if a function doesn't crash are prohibited. Assertions must verify the expected state or output value.
- **`[REQ-TST-10]` CI Integrity**: No code may merge to `main` without a 100% pass rate on all required test suites.

## 4. Test Isolation `[REQ-TST-08]`

Every test must be capable of running independently and in any order.

- **Never** rely on state mutated by previous tests.
- Always implement explicit Setup (e.g., `beforeEach`) and Teardown (e.g., `afterEach`) logic to reset databases or mock interfaces.
