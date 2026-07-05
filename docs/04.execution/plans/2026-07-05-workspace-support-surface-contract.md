---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-workspace-support-surface-contract.md -->

# Workspace Support Surface Contract Implementation Plan

## Overview

This document plans the implementation of
`docs/03.specs/106-workspace-support-surface-contract/spec.md`. The work
formalizes `_workspace` as an ignored, short-lived repo-support staging surface
with tracked contract README files and validator enforcement.

## Context

Stage 00 currently tells subagents and workflows to write intermediate artifacts
to `_workspace/`, but the repository has no tracked `_workspace` directory and
no `.gitignore` contract for its safe use. The user approved a bounded first
implementation unit: define `_workspace` as repo-support staging, distinguish it
from diagnostics/local logs/auth files/tokens/shell history, and record the
broader repo-wide template/frontmatter cleanup as follow-up rather than doing it
in the same batch.

## Goals & In-Scope

- **Goals**:
  - Define the `_workspace` role and purpose.
  - Add tracked contract README files under `_workspace`.
  - Protect `_workspace` with `.gitignore` default-ignore rules.
  - Update Stage 00 governance references from generic `_workspace/` handoff to
    `_workspace/repo-support/`.
  - Update Stage 99 support contracts so `_workspace` is clearly outside
    target-stage and template-source profiles.
  - Add repository validation for tracked `_workspace` drift.
  - Record implementation evidence and remaining gaps.
- **In Scope**:
  - Stage 03 spec and Stage 04 plan/task evidence.
  - `_workspace/README.md` and `_workspace/repo-support/README.md`.
  - `.gitignore`.
  - Stage 00 governance documents that directly route agent outputs.
  - Stage 99 support documents that define frontmatter/template governance.
  - `scripts/validation/check-repo-contracts.sh`.

## Non-Goals & Out-of-Scope

- No secret value reads, writes, rotations, summaries, or migrations.
- No Docker Compose runtime, provider adapter, hook, model-policy, CI workflow,
  deployment, or remote GitHub mutation.
- No broad repo-wide frontmatter cleanup beyond direct fallout.
- No permanent storage of raw logs, shell history, local diagnostics, or auth
  material.
- No creation of active specs, plans, or tasks outside canonical stage paths.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Spec | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-WSC-001 | Create design and execution evidence | `docs/03.specs/106-workspace-support-surface-contract/**`, this plan, task evidence, Stage 03/04 indexes | `VAL-WSC-006` | Spec, plan, and task are linked and use canonical templates. |
| PLN-WSC-002 | Add tracked `_workspace` contract and ignore boundary | `_workspace/README.md`, `_workspace/repo-support/README.md`, `.gitignore` | `VAL-WSC-001`, `VAL-WSC-002` | Only approved README files are tracked; ignore rules protect runtime artifacts. |
| PLN-WSC-003 | Update governance and support contracts | `docs/00.agent-governance/**`, `docs/99.templates/support/**` | `VAL-WSC-003`, `VAL-WSC-004` | Generic `_workspace` artifact guidance is replaced with `_workspace/repo-support` where applicable. |
| PLN-WSC-004 | Add validator enforcement | `scripts/validation/check-repo-contracts.sh` | `VAL-WSC-005` | Repo contracts fail on unapproved tracked `_workspace` files or missing ignore rules. |
| PLN-WSC-005 | Validate, update progress, and close task evidence | task evidence, `docs/00.agent-governance/memory/progress.md` | `VAL-WSC-006` | Final checks pass or unrelated failures are documented as gaps. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-WSC-001 | Patch hygiene | Check whitespace and conflict markers | `git diff --check` | No output. |
| VAL-PLN-WSC-002 | Traceability | Check documentation traceability after docs/governance edits | `bash scripts/validation/check-doc-traceability.sh` | `failures=0`. |
| VAL-PLN-WSC-003 | Contract | Check repository contracts including `_workspace` protected surface | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |
| VAL-PLN-WSC-004 | Focused search | Confirm no generic handoff guidance still points runtime artifacts to root `_workspace/` | `rg -n "_workspace/" docs/00.agent-governance docs/99.templates _workspace .gitignore scripts/validation/check-repo-contracts.sh` | Remaining hits are approved contract text or `_workspace/repo-support` guidance. |
| VAL-PLN-WSC-005 | Git status | Confirm tracked surface is bounded | `git status --short` | Only expected files are changed or untracked. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| `_workspace` becomes a permanent evidence dumping ground | Medium | State promotion rules and ignore runtime artifacts by default. |
| Agent handoff text still writes to unsafe root `_workspace/` | Medium | Update Stage 00 routing references and run focused search. |
| Secret-like artifacts are accidentally tracked | High | Add validator allowlist and prohibited path segment checks. |
| README files become policy SSoT | Medium | Put durable rules in Stage 00/99 support docs and keep `_workspace` READMEs as local contracts. |
| Broad corpus cleanup expands beyond approved unit | Medium | Record broader template/frontmatter cleanup as follow-up gap only. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A; this is repository contract and documentation work.
- **Sandbox / Canary Rollout**: N/A; no runtime service behavior changes.
- **Human Approval Gate**: User approved Approach A on 2026-07-05.
- **Rollback Trigger**: Revert the logical commits if validator behavior blocks
  approved tracked files or governance wording proves too restrictive.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 03 spec and Stage 04 plan/task evidence exist and are linked.
- [x] `_workspace` contract README files exist and define allowed/prohibited
      surfaces.
- [x] `.gitignore` protects `_workspace` runtime artifacts.
- [x] Stage 00 and Stage 99 contract wording is aligned.
- [x] Repository validator enforces the tracked `_workspace` allowlist and
      prohibited path segments.
- [x] Final verification is recorded in task evidence and progress memory.

## Related Documents

- **Spec**: [Workspace Support Surface Contract Spec](../../03.specs/106-workspace-support-surface-contract/spec.md)
- **Task**: [Workspace Support Surface Contract Task](../tasks/2026-07-05-workspace-support-surface-contract.md)
- **Subagent Protocol**: [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
- **Environment Constraints**: [Environment constraints](../../00.agent-governance/rules/environment-constraints.md)
- **Template Governance**: [Template governance](../../99.templates/support/template-governance.md)
