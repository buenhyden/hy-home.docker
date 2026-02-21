# During-Development Guide (Human Centric)

This guide outlines how human developers manage the AI Coder Agents and ensure code quality via Local QA during the implementation phase.

## 1. Commanding the Coder Agents

In this phase, you are the conductor. The **Backend Coder Agent** and **Frontend Coder Agent** execute the work.

- Inform the Coder Agents to implement the exact spec located in `specs/[target-feature]-spec.md`.
- **Enforce Constraints**: The agents are governed by `.agent/workflows/` to refuse inventing undocumented functions/APIs. If they get stuck, they will prompt you.
- Provide domain context or clarify ambiguities in the spec if the AI is halted.

## 2. Managing Implementation Quality (QA)

While the AI writes the code, your role is to oversee the structure and testing layers.

- **Check Test Coverage**: As per the engineering standards, all new code requires **> 80% test coverage**. Enforce this rule strictly upon the Coder Agents.
- **Ensure TDD Accuracy**: The Coder Agents must write Unit & Integration tests matching the Given-When-Then criteria from the PRD/Spec. You must inspect that positive *and* negative edge cases (error handling) are tested.
- **Reject Code Without Tests**: If an agent outputs business logic without unit or integration tests, command it to erase the logic until the test suite is built locally.

## 3. Human Local Verification (Pre-PR Gate)

Before allowing the agents to generate a Pull Request, the Human developer runs the local verifications:

1. **Test Suite**: Run the local test runner (e.g., `npm run test`, `pytest`). All tests must pass, and the coverage report must show > 80%.
2. **Linting & Types**: Run the static analyzers (e.g., `npm run lint`, `tsc`). Zero errors are accepted.
3. **Run Application Locally (E2E/Functional QA)**: Execute the application locally to verify no immediate runtime panics were introduced and that the core feature operates as expected.

Once you have verified the code locally, command the system to push to a branch and open a Pull Request, invoking the **Reviewer Agent** for the Post-Development phase.
