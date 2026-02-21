# Post-Development Guide (Human Centric)

This guide outlines the human responsibilities after code is implemented, focusing on Pull Request review oversight, CI/CD validations, and operations handoff.

## 1. Overseeing the Reviewer Agent

When a Pull Request is opened, the **Reviewer Agent** conducts the initial pass based on its `.agent/workflows/` rules.

- Wait for the Reviewer Agent to finish its spec-compliance, security, and static analysis checks.
- Do not dismiss the AI Reviewer's comments unless they hallucinate a requirement not present in the original Spec.
- Command the Coder Agents to fix any failing checks identified by the Reviewer Agent.

## 2. The Human Code Review (QA & Architecture Gate)

Once the AI Reviewer approves, the Human Developer performs the final merge review:

- **Business Logic Review**: Does the code actually solve the PRD's business need efficiently?
- **Architectural Integrity**: Does the code adhere to the constraints defined in `ARCHITECTURE.md` and any associated `docs/adr/`?
- **Test Integrity**: Review the tests—are they meaningful? Did the Coder agents just write tests passing `true === true` to satisfy coverage metrics?

## 3. Validating CI/CD Pipelines

Before clicking merge, verify the automated Quality Gates:

- CI pipeline returns a green checkmark for Linting and Type Checking.
- CI pipeline returns a green checkmark for Unit & Integration tests.
- Security scanners report zero new vulnerabilities.

## 4. Runbooks & Deployment (DevOps Agent)

If the PR alters deployment mechanics or introduces new infrastructure:

- Direct the **DevOps Agent** to update or create an operational playbook in the `runbooks/` folder.
- **Verification**: You must verify that the DevOps agent used `templates/operations/runbook-template.md` and did **not** place it in `docs/runbook`.

Once documentation is complete, tests are green, and the PR is locally and mechanically approved, you may merge the feature to `main`.
