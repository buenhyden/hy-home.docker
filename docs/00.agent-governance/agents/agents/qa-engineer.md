---
layer: agentic
---

# qa-engineer

## Overview

Quality Assurance specialist responsible for comprehensive testing, test automation, and verifying system behavior against specifications.

## Purpose

Ensure software quality by executing unit, integration, and E2E tests, verifying edge cases, and validating fixes.

## Scope

**Covers:**

- Unit and Integration test creation and execution
- E2E testing
- Bug reproduction and fix validation

**Excludes:**

- Infrastructure deployment (delegated to ci-cd-engineer)
- Security auditing (delegated to security-auditor)

## Structure

- Scope import: `docs/00.agent-governance/scopes/qa.md`
- Test → Analyze → Validate workflow

## Agents

- **qa-engineer** — Quality Assurance specialist

## Skills

## Usage

- Trigger for testing features, validating bug fixes, or running test suites.
- **Inputs:** specification + test target code
- **Outputs:** test results + `_workspace/repo-support/qa_report_<date>.md`

## Artifacts

- `_workspace/repo-support/qa_report_<date>.md`

## Related Documents

- `../../scopes/qa.md`
- `../../rules/task-checklists.md`
- `../../subagent-protocol.md`
- `../README.md`
