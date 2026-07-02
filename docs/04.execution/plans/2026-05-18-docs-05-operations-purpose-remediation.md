---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md -->

# docs/05.operations Purpose Remediation Plan

## Overview

This document is the implementation plan for organizing `docs/05.operations` around guide, policy, and runbook purposes, and for preventing the same drift through repository contracts.

## Context

`docs/05.operations` is the canonical operations stage that manages guides, policies, runbooks, and incidents separately. The 2026-05-18 audit found that some leaf documents still had wrong-bucket headings or were missing required headings for policy/runbook profiles.

## Goals & In-Scope

- **Goals**:
  - Align operations leaf documents with guide/policy/runbook purpose profiles.
  - Move DAG deployment policy from the guide bucket to the policy bucket.
  - Split LLM Wiki maintenance guide/policy/runbook documents by purpose profile.
  - Add operations purpose profile validation to repo contracts.
  - Refresh the generated LLM Wiki index.
- **In Scope**:
  - `docs/05.operations/**`
  - `scripts/validation/check-repo-contracts.sh`
  - `docs/90.references/data/llm-wiki/index.md`
  - `docs/04.execution/plans/README.md`
  - `docs/04.execution/tasks/README.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not create new PRD, ARD, ADR, or Spec documents.
  - Do not change Docker Compose, service runtime, secrets, or infrastructure behavior.
  - Do not rewrite historical operations content beyond purpose-profile alignment.
- **Out of Scope**:
  - `projects/storybook/mcp/`
  - Deployment, PR creation, publishing, or incident/postmortem creation

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| OPS-001 | Move DAG deployment policy into policy bucket and fix references | `docs/05.operations/{guides,policies,runbooks}/07-workflow/**` | OPS-PURPOSE-001 | No references to `guides/07-workflow/01.dag-deployment.md` remain outside regenerated indexes |
| OPS-002 | Normalize LLM Wiki maintenance guide/policy/runbook profiles | `docs/05.operations/*/llm-wiki-maintenance.md` | OPS-PURPOSE-002 | Guide has `## Usage`; policy has controls and verification; runbook has procedure and evidence |
| OPS-003 | Add missing policy and runbook profile headings | `docs/05.operations/policies/**`, `docs/05.operations/runbooks/**` | OPS-PURPOSE-003 | Purpose profile scan reports `guides=0`, `policies=0`, `runbooks=0` |
| OPS-004 | Remove nested duplicate Related Documents sections | `docs/05.operations/guides/**` | OPS-PURPOSE-004 | `#### Related Documents` scan returns no matches |
| OPS-006 | Refresh generated indexes and evidence | `docs/90.references/data/llm-wiki/index.md`, progress log | OPS-PURPOSE-006 | LLM Wiki check and repo validators pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-OPS-001 | Structural | Check operations profile headings | Custom Python scan over `docs/05.operations/{guides,policies,runbooks}` | `guides=0`, `policies=0`, `runbooks=0` flagged |
| VAL-OPS-002 | References | Check moved DAG policy references | `rg -n "guides/07-workflow/01\\.dag-deployment\|01\\.dag-deployment\\.md" docs/05.operations README.md AGENTS.md CLAUDE.md GEMINI.md infra scripts` | No stale active references |
| VAL-OPS-003 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-OPS-004 | LLM Wiki | Verify generated index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS |
| VAL-OPS-005 | Repository Contract | Verify repo contracts including new operations profile gate | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-OPS-006 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Mechanical heading insertion changes operational meaning | Medium | Only add scope, verification, and escalation scaffolding; preserve existing controls and procedures |
| Moved DAG policy leaves stale links | Medium | Run targeted `rg` and regenerate LLM Wiki index |
| Validator becomes too broad and flags templates or README files | High | Limit profile gate to leaf Markdown under `guides`, `policies`, and `runbooks`; exclude README and incidents |
| Untracked Storybook MCP files are touched | High | Do not edit or stage `projects/storybook/mcp/`; verify with `git status` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Structural profile scan and stale reference scan must pass before full repository validators.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: The user approved the remediation plan in conversation.
- **Rollback Trigger**: Revert only scoped operations/template/validator/index/progress changes if validators cannot pass without broad runtime edits.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Operations purpose profile scan reports zero flagged guide, policy, and runbook files.
- [x] DAG deployment policy lives under `docs/05.operations/policies/07-workflow/`.
- [x] Parent READMEs and direct references use the new DAG policy path.
- [x] Operation template documents the profile contract.
- [x] Repo contract enforces the profile contract.
- [x] LLM Wiki generated index is fresh.
- [x] Progress log records final evidence.

## Related Documents

- **Operations index**: [../../05.operations/README.md](../../05.operations/README.md)
- **Task record**: [../tasks/2026-05-18-docs-05-operations-purpose-remediation.md](../tasks/2026-05-18-docs-05-operations-purpose-remediation.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage authoring matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
