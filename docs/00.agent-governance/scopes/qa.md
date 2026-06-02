---
layer: qa
title: 'Quality Assurance Scope'
---

# Quality Assurance Scope

**Protocols for verification, testing, and continuous quality monitoring.**

## 1. Context & Objective

- **Goal**: Maintain zero-defect production state and verify all technical specs.
- **Philosophy**: **TDD-First** and measurement-driven validation.
- **Criteria**: Mandatory compliance with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Test Suite**:
  - **Unit / Target**: Mandatory ≥90% coverage for domain logic (both overall and changed code) when the repository has a measurable suite for that layer.
  - **E2E**: Critical paths verified via **Playwright**.
  - **Load**: API performance verified via **k6** or **Locust**.
- **Execution Boundary (Local vs Remote)**:
  - **Local**: Fail-fast validation (e.g., `pre-commit` for formatting/linting, `pre-push` for structural contract scripts).
  - **Remote (GitHub CI)**: The ultimate SSoT quality gate. Heavy analysis (e.g., E2E, Zizmor SARIF upload, SonarQube) belongs here.
  - **Anti-Duplication**: Do not execute the same heavy workloads redundantly. If a dedicated CI job exists for a task (e.g., `zizmor`, `eslint`), skip it in the CI `pre-commit` runner.
- **Applicability**: Mark coverage N/A for docs-only, policy-only, infrastructure configuration, or validation-script changes when no domain-code coverage signal applies.

## 3. Implementation Flow

1. **Red**: Write failing tests based on the spec (`docs/03.specs/`).
2. **Green**: Implement minimal code to pass.
3. **Refactor**: Clean code patterns without changing behavior.
4. **Finalize**: Run all repository-available test and validation commands relevant to the touched area.

For debugging work, establish a root-cause hypothesis and reproduction evidence
before applying fixes. For documentation-only or governance-only work, TDD is
N/A, but the task still needs repository-contract, traceability, diff hygiene,
and manual evidence for any policy claims.

## 3.1 Change-Type Verification Matrix

Use the smallest meaningful checks for the touched layer. When a listed check is
not applicable, record the skipped-check rationale in the task evidence.

| Change Type                                  | Local Checks                                                                                                                                                                                            | CI-Only / Remote Gate                                            | Hook or Script Evidence                                                | Skip Rationale Required                                              |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Documentation-only stage docs                | `git diff --check`, `check-repo-contracts.sh`, `check-doc-traceability.sh`, and LLM Wiki index regeneration via `scripts/knowledge/generate-llm-wiki-index.sh` when docs are added, removed, or renamed | Remote docs traceability and repo contracts                      | Post-edit validation hook, task evidence, progress log                 | Domain tests, coverage, Docker runtime checks                        |
| Archive/tombstone migration                  | Documentation checks plus stale active-reference scans for archived subjects and `docs/98.archive` status/template checks                                                                               | Remote docs traceability and repo contracts                      | Archive ledger update, tombstone metadata, task evidence, progress log | Domain tests, coverage, Docker runtime checks                        |
| Governance or provider policy docs           | Documentation checks plus `sync-provider-surfaces.sh` when provider surfaces are affected                                                                                                               | Remote repo contracts and required checks                        | Provider sync output and policy-gate evidence                          | Runtime tests unless behavior/config changed                         |
| Provider adapter, hook, or validation script | Targeted script self-check, repo contracts, provider sync, quickwin/template-security baselines when relevant                                                                                           | Required GitHub quality gates and security scans                 | Hook validation or script command output                               | CI-only tools such as SARIF upload are named, not duplicated locally |
| Runtime, Docker, or Compose config           | Compose validation, hardening scripts, targeted service smoke checks when safe                                                                                                                          | Compose and hardening jobs, any protected-branch required checks | Docker/Compose command output or explicit approval gate                | Live service mutation skipped unless approved                        |
| CI workflow or GitHub protection             | Static workflow validation, repo contracts, ruleset documentation review                                                                                                                                | GitHub Actions jobs, branch protection/ruleset verification      | `gh` or workflow evidence where approved                               | Local execution of GitHub-only jobs such as `zizmor` SARIF upload    |
| Model policy or reasoning-effort config      | Stage 00 policy review, provider sync, validator support check                                                                                                                                          | Required repo contracts after generated surfaces update          | Validator output and task evidence                                     | Any unsupported value remains blocked, not skipped                   |

## 3.2 Generated-Artifact Freshness

Some artifacts are generated from repository content and must be regenerated as
part of QA before completion. Treat regeneration as a verification step, not an
optional cleanup.

- **LLM Wiki index**: when documents are added, removed, or renamed under indexed
  scopes, regenerate `docs/90.references/llm-wiki/index.md` with
  `bash scripts/knowledge/generate-llm-wiki-index.sh`. `check-repo-contracts.sh`
  enforces freshness locally and in the `repo-contracts` CI job; a stale index is
  a hard failure.
- **Knowledge graph**: refresh `graphify-out/` with `graphify update .` after
  code or doc changes when the CLI is available; report when it is skipped.
- **General rule**: never hand-edit a generated artifact to pass a check. Re-run
  its generator and commit the generated result as a separate logical unit.

## 4. Operational Procedures

- **Regression**: Add regression tests for every bug fix.
- **Refactor evidence**: For behavior-preserving refactors, run checks that cover the touched behavior and state that no behavior change is intended.
- **Reporting**: Publish test results to the session summary or `docs/04.execution/tasks/`.

## 5. Maintenance & Safety

- **Flakiness**: Immediately isolate and fix flaky E2E tests.
- **Audit**: Conduct monthly quality audits of test infrastructure.

## 6. File Ownership SSOT

| Path Pattern                                                  | Owner Agent                       | Read-Only For          |
| ------------------------------------------------------------- | --------------------------------- | ---------------------- |
| `projects/storybook/`                                         | `code-reviewer`                   | layer agents (read)    |
| `scripts/validation/check-storybook-contract.sh`              | `code-reviewer`                   | all other agents       |
| Test configuration files (`vitest.config.*`, `jest.config.*`) | layer agent that owns the service | `code-reviewer` (read) |

QA-specific owned files are limited in this infrastructure-focused repository. Each layer scope defines test ownership for its own services.

## 7. Subagent Bridge

```text
# QA engineer agent preamble
@import docs/00.agent-governance/scopes/qa.md
# TDD-first pattern — red → green → refactor → finalize
# 90% coverage mandatory · regression evidence mandatory
```

Spawn via the active runtime's delegated-agent facility. Do not embed QA policy inline in agent files.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
- [Quality standards](../rules/quality-standards.md)
- [Documentation protocol](../rules/documentation-protocol.md)
- [Postflight checklist](../rules/postflight-checklist.md)
