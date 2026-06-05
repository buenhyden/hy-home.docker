---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-06-02-governance-optimization.md -->

# Governance Optimization (I1+I2) Implementation Plan

> Implementation plan for the governance optimization round. Scope is limited to
> I1 (new service Project Template) and I2 (code review request/acceptance loop).

## Overview

This document is the implementation plan for workspace governance optimization.
After Phase 1 diagnosis confirmed that the foundation is solid (contract checks
pass), it applies only the two highest-value practical items first.

## Context

Phase 1 investigation found that Stage 00 governance, QA/CI, Template Contract,
Model Policy, and Claude harness parity were already satisfied, and both
`check-repo-contracts.sh` and `check-doc-traceability.sh` had `failures=0`.
Therefore, the need was gap filling rather than rebuilding. The diagnosis found
two practical gaps. First, there was no copyable standard seed for new service
onboarding (`examples/` was empty). Second, the code review request to acceptance
to implementation discipline was not codified.

## Goals & In-Scope

- **Goals**: Provide a seed, template, and guide for starting new services with security hardening standards, and codify the code review loop in governance.
- **In Scope**: I1 (`examples/sample-web-service/` seed, `service.template.md`, onboarding guide, 4-file registration), I2 (`workflows.md` and `git-workflow.md` review loop).

## Non-Goals & Out-of-Scope

- **Non-goals**: Introducing a Node build system (R1=current state retained), or promoting service onboarding to a workflow (R2=one-off template).
- **Out of Scope**: I3 (humanizer boundary), I4 (proactive QA comments), I5 (duplicate Related Documents guard), and I6 (RTK convention) are deferred to a later round.

## Work Breakdown

| Task    | Description                                                      | Files / Docs Affected                                                                                                                                                                                                                        | Target REQ | Validation Criteria                      |
| ------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------- |
| PLN-001 | Write service seed with built-in security hardening | `examples/sample-web-service/` | I1 | `docker compose config` parses and YAML is valid |
| PLN-002 | Create service scaffold template and register it in 4 files | `docs/99.templates/service.template.md`, `scripts/validation/check-repo-contracts.sh`, `docs/99.templates/README.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md` | I1 | Contract check has `failures=0` |
| PLN-003 | Write new service onboarding guide | `docs/05.operations/guides/00-workspace/new-service-onboarding.md` | I1 | Guide profile headings are satisfied and normalization passes |
| PLN-004 | Codify code review request/acceptance loop | `docs/00.agent-governance/rules/workflows.md`, `docs/00.agent-governance/rules/git-workflow.md` | I2 | Contract check has `failures=0` |
| PLN-005 | Add generated-artifact freshness contract (LLM Wiki index regeneration) to QA scope | `docs/00.agent-governance/scopes/qa.md` | QA | Contract check has `failures=0` |

## Verification Plan

| ID          | Level      | Description         | Command / How to Run                                                                               | Pass Criteria |
| ----------- | ---------- | ------------------- | -------------------------------------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | Repository contract synchronization | `bash scripts/validation/check-repo-contracts.sh` | `failures=0` |
| VAL-PLN-002 | Structural | Document traceability | `bash scripts/validation/check-doc-traceability.sh` | `failures=0` |
| VAL-PLN-003 | Structural | Seed compose validity | `python3 -c "import yaml; yaml.safe_load(open('examples/sample-web-service/docker-compose.yml'))"` | No exception |

## Risks & Mitigations

| Risk                                       | Impact | Mitigation                                                              |
| ------------------------------------------ | ------ | ----------------------------------------------------------------------- |
| New template type violates the 4-file coupling contract | High | Rerun contract checks immediately after registration and verify step by step |
| Seed compose is caught by infra gates | Medium | Confirm discovery scope: gates scan only `infra/`, not `examples/` |
| Guide placeholder remains and breaks normalization | Medium | Remove placeholder patterns and reverify |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A because this is a governance/documentation change, not a model evaluation target.
- **Sandbox / Canary Rollout**: N/A.
- **Human Approval Gate**: Plan mode approval plus implementation decision confirmation (R1/R2/D3 and I1 landing surface).
- **Rollback Trigger**: Revert changes if contract checks regress.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Task**: [Governance optimization task](../tasks/2026-06-02-governance-optimization.md)
- **Service template**: [Service scaffold template](../../99.templates/service.template.md)
- **Workflow rule**: [Workflows](../../00.agent-governance/rules/workflows.md)
- **Operations**: [New-service onboarding guide](../../05.operations/guides/00-workspace/new-service-onboarding.md)
