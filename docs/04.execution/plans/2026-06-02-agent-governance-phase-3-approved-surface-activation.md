---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md -->

# Agent Governance Phase 3 Approved Surface Activation Plan

## Overview

This document is the implementation plan for promoting user-approved high-risk surfaces after Phase 2 strategy integration into Stage 00, template, CI validator, and Stage 04 evidence contracts.

The user approved changes to policy, runtime, CI, templates, secrets, remote GitHub, model policy, and provider adapters that had previously been approval-gated. Phase 3 does not treat this approval as an unlimited exception; it codifies the evidence, redaction, rollback, provider sync, and remote verification boundaries required for each surface.

## Context

Phase 2 recorded that several areas remained behind human approval gates:

- Stage 00 policy rewrite and high-risk governance surface changes.
- Runtime/Docker mutation and new hard validators.
- CI/template changes.
- Secrets access, remote GitHub mutation, model policy changes, and provider adapter redesign.

The user approved those gates on 2026-06-02. This plan implements the approval as a repository-local governance contract and validator-backed template requirement. It does not perform live Docker mutation, secret value mutation, remote GitHub mutation, model value replacement, or provider adapter regeneration unless a concrete target exists.

## Goals & In-Scope

- **Goals**:
  - Add high-risk approved-surface evidence requirements to Stage 00 workflow checklists.
  - Define approved runtime, secrets, remote GitHub, model, and provider adapter protocols.
  - Extend the task template so future tasks can capture approved-surface evidence consistently.
  - Add a repo-contract check that keeps the approved-surface task template section present.
  - Record secrets metadata-only evidence and remote GitHub read-only evidence without exposing values or mutating remote state.
- **In Scope**:
  - Stage 00 policy docs for task checklists, infra, security, QA, GitHub governance, and subagent/model/provider protocol.
  - `docs/99.templates/templates/sdlc/task.template.md` and template catalog wording.
  - `scripts/validation/check-repo-contracts.sh` template contract check.
  - Stage 04 plan/task artifacts, Stage 04 README indexes, progress log, LLM Wiki, and Graphify evidence.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not read, print, commit, or summarize secret values.
  - Do not change live Docker service state without a concrete service target.
  - Do not mutate remote GitHub settings without a concrete setting target.
  - Do not replace model values or regenerate provider adapters without a named model/role/provider target and validator coupling.
  - Do not weaken branch protection, CI gates, provider sync, or Stage 00 authority.
- **Out of Scope**:
  - Secret value rotation, `.env` value edits, private key access, shell history, or token-bearing log inspection.
  - PR merge, branch protection weakening, required-check removal, or remote secret changes.
  - Broad HADS conversion of active historical documents.
  - Runtime service start/stop/rebuild/recreate because no concrete runtime target was provided.

## Approved Surface Activation Matrix

| Surface | Phase 3 Action | Evidence Boundary |
| --- | --- | --- |
| Policy | Add high-risk surface checklist requirements. | Stage 00 checklist and task evidence. |
| Runtime | Add approved runtime mutation protocol. | Plan/target/precheck/rollback/postcheck required; no live mutation without target. |
| CI | Add repo-contract check for the task template approved-surface section. | `bash -n` and repo contracts. |
| Templates | Add optional `## Approved Surface Evidence` to task template and catalog wording. | Template contract and changed-doc validation. |
| Secrets | Add metadata-only secrets protocol; collect count-only evidence. | No values read or printed; count-only command output. |
| Remote GitHub | Add remote mutation protocol; run read-only repo verification. | `gh repo view` read-only evidence; no mutation. |
| Model policy | Add model/provider change protocol. | Existing model values unchanged absent concrete target. |
| Provider adapters | Keep sync coupling as required evidence. | Provider sync must pass; no adapter drift introduced. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-P3-001 | Add high-risk approved-surface requirements to Stage 00 policy and scopes. | Task checklists, infra, security, QA, GitHub governance, subagent protocol | REQ-AGG-NFR-01 | Repo contracts pass and no contradictory policy is introduced. |
| PLN-P3-002 | Extend task template and catalog with approved-surface evidence section. | `docs/99.templates/templates/sdlc/task.template.md`, `docs/99.templates/README.md` | REQ-AGG-FUN-05 | Template section exists and catalog explains high-risk usage. |
| PLN-P3-003 | Add a CI-facing repository contract for the approved-surface template section. | `scripts/validation/check-repo-contracts.sh` | REQ-AGG-FUN-07 | `bash -n` and repo contracts pass. |
| PLN-P3-004 | Create Phase 3 Stage 04 plan/task evidence with approval matrix and scope safety. | Phase 3 plan/task, Stage 04 READMEs, progress log | REQ-AGG-MET-04 | Task evidence records changed and verified-only surfaces. |
| PLN-P3-005 | Run local, generated, provider, Graphify, secret-metadata, and remote read-only verification. | Task evidence, LLM Wiki, Graphify | REQ-AGG-MET-02 | Checks pass or advisory status is explicitly recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P3-001 | Hygiene | Confirm diff has no whitespace errors. | `git diff --check` | No output and zero exit status. |
| VAL-P3-002 | Script | Check modified validator syntax. | `bash -n scripts/validation/check-repo-contracts.sh` | Zero exit status. |
| VAL-P3-003 | Structural | Validate repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-P3-004 | Traceability | Validate execution/operations traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-P3-005 | Provider | Confirm provider surfaces remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-P3-006 | Knowledge Index | Refresh and verify LLM Wiki index because docs are added. | `bash scripts/knowledge/generate-llm-wiki-index.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Regeneration completes and freshness check passes. |
| VAL-P3-007 | Graph Boundary | Refresh graph output and record advisory reason. | `/home/hy/.local/bin/graphify update .`; `bash scripts/knowledge/report-graphify-health.sh` | Graph output refreshed; advisory status is corroborated. |
| VAL-P3-008 | Secrets Boundary | Collect metadata-only secrets evidence. | `find secrets -type f -printf '%p\n' \| wc -l` | Count recorded; no values printed. |
| VAL-P3-009 | Remote GitHub | Collect read-only remote repository evidence. | `gh repo view --json nameWithOwner,defaultBranchRef,isPrivate` | Repository identity and default branch recorded; no mutation. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Approval is interpreted as permission to expose secrets. | High | Security scope and task template require redaction boundary; evidence is metadata-only unless target is concrete and redacted. |
| Remote GitHub approval weakens protection. | High | GitHub governance forbids weakening protected-branch rules and requires before/after evidence for mutation. |
| Model/provider approval creates unsupported drift. | High | Subagent protocol requires Stage 00, generator, adapters, validators, and provider sync to change together. |
| Runtime approval mutates services without target. | High | Infra scope requires target, precheck, rollback, and postcheck; no target means verification-only. |
| Template change is not enforced in CI. | Medium | Repo-contract script checks the approved-surface section exists in `task.template.md`. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repo contracts, doc traceability, provider sync, LLM Wiki freshness, Graphify health, and syntax validation.
- **Sandbox / Canary Rollout**: N/A. No live runtime service target was provided.
- **Human Approval Gate**: Already granted for policy, runtime, CI, templates, secrets, remote GitHub, model policy, and provider adapter surfaces. New concrete secret value mutation, live runtime mutation, remote protected-surface mutation, or model replacement still requires target-specific evidence in the task.
- **Rollback Trigger**: Revert Phase 3 changes if they permit secret exposure, weaken protection, bypass provider sync, or fail repo contracts.
- **Prompt / Model Promotion Criteria**: No model promotion in this pass; future promotion must update Stage 00, generator, adapters, validators, and task evidence together.

## Completion Criteria

- [x] High-risk approved-surface protocols added to Stage 00 policy surfaces.
- [x] Task template and template catalog updated.
- [x] Repo-contract script validates approved-surface template presence.
- [x] Phase 3 plan/task/index/progress evidence recorded.
- [x] Secrets and remote GitHub evidence collected without value or remote mutation.
- [x] Validation commands pass or advisory status is recorded.
- [x] No live runtime, secret value, remote GitHub mutation, model value, or provider adapter drift is introduced without concrete target evidence.

## Related Documents

- **Task**: [Agent Governance Phase 3 Approved Surface Activation Task](../tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- **Phase 2 Plan**: [Agent Governance Phase 2 Strategy Integration Plan](./2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Phase 2 Task**: [Agent Governance Phase 2 Strategy Integration Task](../tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Task Checklist**: [Task Checklists](../../00.agent-governance/rules/task-checklists.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Security Scope**: [Security Enforcement Scope](../../00.agent-governance/scopes/security.md)
- **GitHub Governance**: [GitHub Governance Policy](../../00.agent-governance/rules/github-governance.md)
- **Task Template**: [Task template](../../99.templates/templates/sdlc/task.template.md)
