---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md -->

# Targeted Documentation Precision Remediation Plan

## Overview

This document is the targeted documentation precision remediation plan for `README.md`, `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, and `docs/90.references`. Scope is limited to discoverability, target-relative link, stage ownership, and current evidence drift that can remain after validators pass.

## Context

Recent stage-specific remediation and the bounded consistency audit make `check-repo-contracts.sh` and `check-doc-traceability.sh` pass. This work is precision remediation, not a broad rewrite: each edit is tied to a concrete failing condition to prevent unnecessary template churn.

## Goals & In-Scope

- **Goals**:
  - Tie each edit to an evidence gate.
  - Fix target-relative link mismatches and reader-facing discoverability issues.
  - Leave new execution plan/task evidence in the canonical `docs/04.execution` stage.
  - Synchronize changed parent READMEs and the generated path index only when needed.
- **In Scope**:
  - `README.md`
  - `docs/01.requirements/**`
  - `docs/02.architecture/**`
  - `docs/03.specs/**`
  - `docs/04.execution/**`
  - `docs/05.operations/**`
  - `docs/90.references/**`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not bulk-rewrite historical leaf documents into the current template shape.
  - Do not perform style-only prose rewrites.
  - Do not change runtime Docker Compose, service config, API behavior, or secret structure.
  - Do not use Graphify inferred edges as new remediation scope.
- **Out of Scope**:
  - Reading secret values, credentials, tokens, certificate bodies, shell history, or raw logs.
  - Existing untracked `projects/storybook/mcp/`.
  - branch history cleanup, deployment, external publishing.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Record current precision remediation plan/task evidence | `docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md`, `docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md` | DOC-PRECISION-001 | Plan/task use canonical paths, Target comments, and valid Related Documents |
| PLN-002 | Run evidence-gated drift scans | target docs set | DOC-PRECISION-002 | Missing Related Documents, placeholder, stale taxonomy, pseudo-link, and operations profile scans are classified |
| PLN-003 | Fix only concrete drift | affected docs only | DOC-PRECISION-003 | Every edit cites a failing condition in task evidence |
| PLN-004 | Sync parent README/index docs | `docs/04.execution/README.md`, plans/tasks README, generated LLM Wiki index if path set changes | DOC-PRECISION-004 | New plan/task paths are discoverable |
| PLN-005 | Verify reader smoke flows and validators | validation commands | DOC-PRECISION-005 | Focused scans, smoke flows, validators, and diff hygiene pass or have documented intentional exceptions |
| PLN-006 | Record final progress evidence | `docs/00.agent-governance/memory/progress.md` | DOC-PRECISION-006 | Progress log records concise final status and evidence only |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PRECISION-001 | Coverage | Check required related-doc sections | `rg --files-without-match "^## Related Documents$" README.md docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references -g '*.md'` | No actionable missing files |
| VAL-PRECISION-002 | Placeholder | Check real placeholders in non-template docs | focused `rg` placeholder scan | No actionable non-template placeholder remains |
| VAL-PRECISION-003 | Link hygiene | Check pseudo-links, stale taxonomy, absolute links, and `file://` usage | focused `rg` scans | Findings are fixed or documented as intentional command payloads |
| VAL-PRECISION-004 | Operations purpose | Check guide/policy/runbook heading separation | focused operations heading scan | No cross-profile heading drift in edited docs |
| VAL-PRECISION-005 | Smoke Flow | Validate root and operations navigation | manual README link path walk | Root README -> docs README -> stage README -> leaf doc works; operations README -> guide/policy/runbook works |
| VAL-PRECISION-006 | Repository Contract | Verify repository docs contracts | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-PRECISION-007 | Traceability | Verify execution/operations traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-PRECISION-008 | LLM Wiki | Verify generated index freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS, regenerating only if tracked path set changed |
| VAL-PRECISION-009 | Diff Hygiene | Check whitespace and conflict markers | `git diff --check` | PASS |
| VAL-PRECISION-010 | Graphify | Refresh/report graph navigation after approved docs edits | `graphify update .` if available, then `bash scripts/knowledge/report-graphify-health.sh` | Clean or advisory-only for known inferred edges |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Precision pass becomes bulk rewrite | High | Require a failing condition before each edit |
| Historical task evidence meaning changes | High | Do not rewrite historical leaf plan/task content unless the failing condition is current and concrete |
| Secret data exposure | High | Count paths only; never open secret values or credential files |
| Generated index churn | Medium | Regenerate LLM Wiki only when tracked path inventory changes |
| Graphify inferred edges mislead remediation | Medium | Use Graphify as navigation/reporting evidence only |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Focused scans and repository validators must pass before completion.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: User approved the plan before implementation.
- **Rollback Trigger**: Revert scoped docs changes only if validators cannot pass without broader rewrite.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] Plan/task evidence is present and linked.
- [x] Each edited file maps to a failing condition.
- [x] Parent README/index files are synchronized for new paths.
- [x] Reader smoke flows pass.
- [x] Repository validators and diff hygiene pass.
- [x] Progress log records final evidence.

## Related Documents

- **Execution README**: [../README.md](../README.md)
- **Execution Task**: [../tasks/2026-05-18-targeted-docs-precision-remediation.md](../tasks/2026-05-18-targeted-docs-precision-remediation.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Root README**: [../../../README.md](../../../README.md)
