---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-31-claude-harness-governance-verification.md -->

# Claude Harness Governance Verification Implementation Plan

## Overview

This document is the implementation plan for verifying alignment between shared governance (Stage 00) and the Claude harness, then surgically fixing only confirmed real drift. It revalidates model policy on the web and records non-enforced gaps in governance memory.

## Context

The `/plan` request was written as if Stage 00 needed to be built from scratch, but Phase 1 investigation found that the work was already completed by 2026-05-29 and 2026-05-31 work. Model Policy, QA & CI/CD policy, Template Contract, clarification duty, and 15 agent model aliases (`opus`/`sonnet`) all exist, and `check-repo-contracts.sh` passes with `failures=0`. Therefore, this work is scoped to **verification + real drift fixes + gap recording**, not a new build (user-approved decision).

## Goals & In-Scope

- **Goals**: Prove shared governance and Claude harness alignment with evidence, and fix only confirmed drift.
- **In Scope**:
  - Run validation scripts (`check-repo-contracts.sh`, `check-doc-traceability.sh`) and record results.
  - Perform web-based model revalidation (Claude / Codex / Gemini, 2026-05).
  - Fix confirmed text drift: model identifier at `agents/agents/workflow-supervisor.md:31`.
  - Record non-enforced gap (Gemini tier inversion) in governance memory.
  - Write traceability Plan/Task documents and progress log.

## Non-Goals & Out-of-Scope

- **Non-goals**: New definitions or large-scale rewrites of governance, templates, or harnesses.
- **Out of Scope**:
  - Bulk-rewriting about 499 stage documents; keep the read-only default and record gaps only.
  - Rolling Model Policy back to the 2026-05-29 snapshot.
  - Modifying `.codex/**` or `.agents/**` mirrors, Docker runtime, secrets, deployments, or branch protection.

## Work Breakdown

| Task    | Description                           | Files / Docs Affected                                                                        | Target REQ | Validation Criteria                           |
| ------- | ------------------------------------- | -------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------- |
| PLN-001 | Run baseline validation scripts | `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh` | N/A | Both scripts have `failures=0` |
| PLN-002 | Confirm policy authority after web model revalidation | `subagent-protocol.md` (review only) | N/A | Claude/Codex current state confirmed; Gemini tier issue identified |
| PLN-003 | Fix confirmed model identifier drift | `docs/00.agent-governance/agents/agents/workflow-supervisor.md` | N/A | stale-model grep has no results |
| PLN-004 | Record Gemini tier inversion gap in memory | `docs/00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md` | N/A | Memory template complied with; no placeholders |
| PLN-005 | Write traceability Plan/Task/README/progress | this plan, paired task, two READMEs, `progress.md` | N/A | Template/frontmatter/Related Documents complied with |

## Verification Plan

| ID          | Level      | Description                  | Command / How to Run                                                   | Pass Criteria |
| ----------- | ---------- | ---------------------------- | ---------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | Verify repository contract | `bash scripts/validation/check-repo-contracts.sh` | `failures=0` |
| VAL-PLN-002 | Structural | Verify document traceability | `bash scripts/validation/check-doc-traceability.sh` | `failures=0` |
| VAL-PLN-003 | Content | Confirm stale model strings are absent | `grep -rn -E 'gemini-3-pro\|gpt-5.1' docs/00.agent-governance .claude` | No results |
| VAL-PLN-004 | Hygiene | Confirm whitespace drift is absent | `git diff --check` | No results |

## Risks & Mitigations

| Risk                          | Impact | Mitigation                                                          |
| ----------------------------- | ------ | ------------------------------------------------------------------- |
| Churning files that are already correct | Medium | Keep the "verify + fix real drift only" scope and modify only exact grep matches |
| Changing the Gemini tier prematurely | Medium | Preserve the policy table and record only a decision item in memory because 3.5 Pro is not released |
| Traceability pair (plan<->task) becomes unsynchronized | High | Create plan/task together, register both in READMEs, and rerun traceability validation |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A because this is governance documentation/verification work with no domain code changes.
- **Sandbox / Canary Rollout**: N/A.
- **Human Approval Gate**: Plan approval completed in plan mode.
- **Rollback Trigger**: Revert changes if validation scripts report `failures>0`.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed (`check-repo-contracts.sh`, `check-doc-traceability.sh` both have `failures=0`)
- [ ] Required docs updated (plan, task, two READMEs, progress, memory note)

## Related Documents

- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Provider Capability Matrix**: [provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Documentation Protocol**: [documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Task**: [2026-05-31-claude-harness-governance-verification.md](../tasks/2026-05-31-claude-harness-governance-verification.md)
- **Current Governance Plan**: [Agent Governance Decision Items and Attachment-Gap Plan](./2026-06-02-agent-governance-decision-items-plan.md)
