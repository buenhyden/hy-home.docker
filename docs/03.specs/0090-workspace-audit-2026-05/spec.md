---
profile_id: spec
status: retired
artifact_id: SPEC-0090
artifact_type: spec
parent_ids:
  - AD-0027
created: 2026-07-05
updated: 2026-08-28
---
# Workspace Audit 2026-05 Technical Specification

## Overview

This completed session is retired. Its original body below is historical
execution evidence, not current authority or permission to repeat its commands.
The original content is recoverable at Git commit
`494065806794980080b081439298d7b534d10803`. Physical cleanup and terminal
Migration mappings remain pending PhaseB.

This document is the technical specification for the May 2026 workspace-wide audit and improvement session. It covers governance rules, documentation lifecycle, scripts, Docker Compose infrastructure, env/secrets contracts, QA/CI/CD, hooks, and skills; it implements low-risk changes and records medium/high-risk changes as deferred items.

## Strategic Boundaries & Non-goals

**Scope:** Audit governance rules, strengthen documentation-lifecycle stage READMEs, verify root/infra README state, generate env/secrets key comparison reports, create seven workspace-specific AI Agent skill stubs, create session Spec/Plan/Task documents, and update `progress.md`.

**Non-goals:** Actual Docker Compose healthcheck/restart policy implementation (deferred), CI workflow changes (deferred), OPA/Conftest policy-code implementation (deferred), secret value changes, and actual `.env` value changes.

## Related Inputs

- **PRD**: No matching PRD; this is an iterative workspace governance audit session.
- **ARD**: [../../02.architecture/descriptions/README.md](../../02.architecture/descriptions/README.md)
- **Related ADRs**: No matching ADRs.

## Contracts

- **Config Contract**: `.env.example` and `.env` keep the same key set. Key comparison reports are created under `docs/05.operations/catalog/*/*/guide.md`.
- **Data / Interface Contract**: skill stubs include the `name`, `description`, `version`, `purpose`, `trigger`, `inputs`, `outputs`, `constraints`, and `related-skills` fields.
- **Governance Contract**: all changes must satisfy the completion criteria in `task-checklists.md`. Only low-risk changes are implemented; medium/high-risk changes are recorded as deferred.

## Core Design

- **Component Boundary**: this specification applies only to the workspace governance layer. It does not change infrastructure runtime behavior, CI/CD deployment behavior, or secret values.
- **Key Dependencies**: `docs/99.templates/templates/sdlc/spec.template.md`, `docs/99.templates/templates/sdlc/plan.template.md`, `docs/99.templates/templates/sdlc/task.template.md`, `docs/00.agent-governance/policies/stage-authoring-matrix.md`
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

- **Plan**: ../../04.execution/plans/2026-05-26-workspace-audit.md
- **Task**: ../../04.execution/tasks/2026-05-26-workspace-audit.md
- **Env Key Comparison**: [../../05.operations/guides/00-workspace/env-key-comparison.md](../../05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md)
- **Secrets Key Comparison**: [../../05.operations/guides/00-workspace/sensitive-env-vars-comparison.md](../../05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/policies/stage-authoring-matrix.md)
- **Progress Log**: [../../00.agent-governance/memory/progress.md](../0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md)

## Boundaries and Inputs

The preceding session boundaries and dated inputs are historical. Current
authoring authority belongs to Stage 00 policies and the Stage 99 Registry.

## Behavior Contract

The session obligations have ended; obsolete stub, progress, R4/R5 and checker
requirements are not current behavior contracts.

## Technical Approach

The preceding implementation approach describes only the completed session.

## Interfaces and Data

Current document fields and shapes are owned by the Stage 99 Registry.

## Failure Modes and Guardrails

Current approval and credential boundaries are owned by Stage 00 policies;
operational responsibilities belong to the Stage 05 catalog.

## Acceptance Contract

The dated verification criteria above are historical session evidence, not
current completion gates. Stage 00 completion policy governs new work.

## Traceability

Historical identity and original content remain recoverable at the commit
above. Current owners are [Stage 00](../../00.agent-governance/README.md),
[Stage 99 Registry](../../99.templates/registry.json), and the
[Operations catalog](../../05.operations/catalog/README.md).
