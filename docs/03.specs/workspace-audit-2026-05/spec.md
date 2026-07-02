---
status: completed
---

<!-- Target: docs/03.specs/workspace-audit-2026-05/spec.md -->

# Workspace Audit 2026-05 Technical Specification

## Overview

This document is the technical specification for the May 2026 workspace-wide audit and improvement session. It covers governance rules, documentation lifecycle, scripts, Docker Compose infrastructure, env/secrets contracts, QA/CI/CD, hooks, and skills; it implements low-risk changes and records medium/high-risk changes as deferred items.

## Strategic Boundaries & Non-goals

**Scope:** Audit governance rules, strengthen documentation-lifecycle stage READMEs, verify root/infra README state, generate env/secrets key comparison reports, create seven workspace-specific AI Agent skill stubs, create session Spec/Plan/Task documents, and update `progress.md`.

**Non-goals:** Actual Docker Compose healthcheck/restart policy implementation (deferred), CI workflow changes (deferred), OPA/Conftest policy-code implementation (deferred), secret value changes, and actual `.env` value changes.

## Related Inputs

- **PRD**: No matching PRD; this is an iterative workspace governance audit session.
- **ARD**: [../../02.architecture/requirements/README.md](../../02.architecture/requirements/README.md)
- **Related ADRs**: No matching ADRs.

## Contracts

- **Config Contract**: `.env.example` and `.env` keep the same key set. Key comparison reports are created under `docs/05.operations/guides/`.
- **Data / Interface Contract**: skill stubs include the `name`, `description`, `version`, `purpose`, `trigger`, `inputs`, `outputs`, `constraints`, and `related-skills` fields.
- **Governance Contract**: all changes must satisfy the completion criteria in `task-checklists.md`. Only low-risk changes are implemented; medium/high-risk changes are recorded as deferred.

## Core Design

- **Component Boundary**: this specification applies only to the workspace governance layer. It does not change infrastructure runtime behavior, CI/CD deployment behavior, or secret values.
- **Key Dependencies**: `docs/99.templates/templates/sdlc/spec.template.md`, `docs/99.templates/templates/sdlc/plan.template.md`, `docs/99.templates/templates/sdlc/task.template.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- **Tech Stack**: Markdown documents, Bash validation scripts, and the Claude `skill.md` format

## Historical Gap Registry Snapshot (2026-05-26)

The rows below preserve the original workspace-audit baseline for this completed
session. They are not current implementation status. For present-day state,
prefer the current QA gates, follow-up task evidence, and progress log entries.

| ID     | Area                | Summary                                     | Risk   | Status       |
| ------ | ------------------- | ------------------------------------------- | ------ | ------------ |
| GAP-01 | Infra               | 46/47 Compose files lack healthcheck/restart policy coverage | Medium | Deferred     |
| GAP-02 | Docs Lifecycle      | Stage README lifecycle sections incomplete | Low    | Implemented  |
| GAP-03 | Docs Operations     | docs/05.operations/ cross-link normalization | Low    | Implemented  |
| GAP-04 | Root README         | Verify whether current state is reflected | Low    | Verified OK  |
| GAP-05 | Skills              | Seven workspace-specific AI Agent skill stubs missing | Low    | Implemented  |
| GAP-06 | Env Contract        | Missing .env.example vs .env key comparison report | Low    | Implemented  |
| GAP-07 | Secrets Contract    | Missing SENSITIVE_ENV_VARS key comparison report | Low    | Implemented  |
| GAP-08 | CI/CD               | CI workflow expansion, including validate-compose | Medium | Deferred     |
| GAP-09 | infra/README        | Verify normalization status | Low    | Verified OK  |
| GAP-10 | Spec/Plan/Task      | Create session Spec/Plan/Task | Low    | Implemented  |
| GAP-11 | Policy Verification | OPA/Conftest policy-code not implemented | Medium | Deferred     |
| GAP-12 | Coverage Ledger     | progress.md lacks audit session entry | Low    | Implemented  |
| GAP-13 | Stage 04 lifecycle  | Verify stage-authoring-matrix consistency | Low    | Verified OK  |
| GAP-14 | Hookify naming      | Explain `.local.md` naming | Low    | Pre-existing |

## Verification

```bash
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `check-repo-contracts.sh` passes, proving docs taxonomy, README, and template inventory contracts.
- **VAL-SPC-002**: `check-doc-traceability.sh` passes, proving execution/operations cross-link integrity.
- **VAL-SPC-003**: seven skill stubs are created under `.claude/skills/`.
- **VAL-SPC-004**: env/secrets key comparison reports do not include secret values.
- **VAL-SPC-005**: the session Plan and Task include required template sections.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-26-workspace-audit.md](../../04.execution/plans/2026-05-26-workspace-audit.md)
- **Task**: [../../04.execution/tasks/2026-05-26-workspace-audit.md](../../04.execution/tasks/2026-05-26-workspace-audit.md)
- **Env Key Comparison**: [../../05.operations/guides/00-workspace/env-key-comparison.md](../../05.operations/guides/00-workspace/env-key-comparison.md)
- **Secrets Key Comparison**: [../../05.operations/guides/00-workspace/sensitive-env-vars-comparison.md](../../05.operations/guides/00-workspace/sensitive-env-vars-comparison.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Progress Log**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
