---
status: active
artifact_id: task:2026-07-13-document-contract-canonicalization
artifact_type: task
parent_ids:
  - plan:2026-07-13-document-contract-canonicalization
---
<!-- Target: docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md -->

# Task: Document Contract Canonicalization

## Overview

This ledger tracks the six dependency-ordered implementation and review tasks
for Spec 129. It is the durable evidence source for registry, template,
contract, research, audit, repository/CI, generated-output, and controlled QA
work. Corpus migration and remote enforcement remain later sub-projects.

## Inputs

- **Parent Spec**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Parent Plan**:
  [Implementation plan](../plans/2026-07-13-document-contract-canonicalization.md)
- **Canonical Audit**:
  [Implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Canonical Research**:
  [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Registry**:
  [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)

## Working Rules

- Execute one task at a time with a fresh implementer and separate reviewer.
- Use RED/GREEN for code, validator, parser, template, and repository-gate
  behavior.
- Mark a task Done only after Spec PASS and Quality APPROVED with Critical 0
  and Important 0.
- Keep ignored briefs, review packages, and transient handoffs under ignored
  repo-support scratch; promote only durable evidence here.
- Preserve historical payloads and keep the 892-record corpus advisory.
- Never read secret values, raw logs, auth files, tokens, credentials, private
  keys, or shell history.
- Do not mutate runtime, Compose, infrastructure, deployment, provider-global,
  model-policy, ruleset, environment, or remote branch-protection state.
- Never run direct all-files pre-commit. Reserve the controlled wrapper for
  T-DCC-006 from an initially clean linked worktree.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 99 contracts and templates | User approval of Spec 129 and this staged foundation design | Registry, support contracts, typed templates, Release routing | Spec 129 baseline and `d900eabd` generated inventory | Per-task diffs, tests, and reviews | Revert the exact logical task commit | No copied secret values, raw logs, auth, tokens, credentials, or shell history |
| Stage 00 authoring governance | User approval permitting governance/contract changes | Documentation protocol and authoring matrix | Current Stage 00 routes at branch base `e2954cc3` | Linked registry/family/profile duties and review verdict | Revert Task 2 or Task 4 commit | No provider-global or user config mutation |
| Canonical Stage 90 research/audit | User approval to consolidate related documents into canonical packs | 2026-07-05 research and current implementation audit only | 892-record inventory; 11 reports/161 rows | Source-backed research and current evidence wording | Revert logical commit; regenerate owner outputs | Preserve historical commands, dates, counts, verdicts, and results |
| Validation and tracked CI | User approval of non-runtime harness improvement | Metadata parser/tests, repository contracts, existing read-only CI route | Existing changed/new metadata and `repo-contracts` job | RED/GREEN evidence and `failures=0` | Revert Task 1/5 commit | No remote run or protection claim |
| `_workspace` evidence | User-approved repo-support distinction and existing contract | Two tracked READMEs and independent repository enforcement | Existing allowlist and ignored repo-support scratch | Audit coverage only; no docs metadata inclusion | Revert audit wording | Do not inspect diagnostics, logs, auth, tokens, secret values, or shell history |
| Controlled pre-commit | User-approved wrapper design | Final clean linked-worktree QA gate | Clean Git status and wrapper contract | Command/path evidence in this ledger | Stop on unexpected paths; do not clean/hide output | Git-visible, non-ignored repository paths only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DCC-001 | Extend registry/parser with families, key order, README profiles, and parent serialization. | impl/test | Registry Model; VAL-129-001/004/005 | Task 1 | RED/GREEN metadata tests and independent review | Documentation Metadata Engineer | Todo |
| T-DCC-002 | Complete typed Markdown templates and Release routing. | impl/test/doc | Template/Release Contracts; VAL-129-002/003 | Task 2 | Instantiation fixtures, route checks, review | Documentation Template Engineer | Todo |
| T-DCC-003 | Align human contracts and canonical external research. | doc/research | Canonical Ownership; External Source Basis | Task 3 | Source verification, ownership scan, review | Documentation Specialist | Todo |
| T-DCC-004 | Align Stage 00 authoring and canonical audit truth, including `_workspace`. | doc/eval | Guardrails; VAL-129-002/005/006 | Task 4 | 11/161, semantic freshness, review | Agentic Workflow Specialist | Todo |
| T-DCC-005 | Integrate fail-closed repository and CI enforcement. | impl/test/ci | Validator Interfaces; VAL-129-007 | Task 5 | Adversarial tests, repo contracts, workflow security, review | QA / CI Engineer | Todo |
| T-DCC-006 | Regenerate evidence, run full QA/wrapper, review the branch, and close. | test/doc/eval | Verification; VAL-129-007/008 | Task 6 | Full bundle, wrapper, final review | QA / Documentation Lead | Todo |

## Phase View

### Phase 1 — Executable Foundation

- [ ] T-DCC-001 Registry, parser, README profiles, and parent serialization
- [ ] T-DCC-002 Typed templates and Release routing

### Phase 2 — Human and Evidence Alignment

- [ ] T-DCC-003 Human contracts and canonical external research
- [ ] T-DCC-004 Stage 00 authoring and canonical audit reconciliation

### Phase 3 — Enforcement and Closure

- [ ] T-DCC-005 Repository and CI contract enforcement
- [ ] T-DCC-006 Generated evidence, full QA, reviews, and closure

## Review Ledger

| Task | Implementation Commit(s) | Spec Compliance | Quality | Findings / Resolution | Reviewer Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-DCC-001 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-002 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-003 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-004 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-005 | Pending | Pending | Pending | Pending | Ignored SDD report promoted here after approval | Pending |
| T-DCC-006 | Pending | Pending | Pending | Pending | Whole-branch review evidence promoted here | Pending |

## Verification Summary

- **Focused Test Commands**: Pending T-DCC-001 through T-DCC-005.
- **Full Test Commands**: Pending T-DCC-006.
- **Generated Freshness**: Pending T-DCC-006.
- **Graphify**: Required after code changes when available; advisory result and
  corroboration will be recorded per applicable task.
- **Logs / Evidence Location**: Durable concise results live in this task;
  ignored briefs/review packages live under repo-support scratch. Raw logs,
  secret-bearing output, and shell history are not evidence artifacts.

## Controlled Agent Pre-commit Evidence

Evidence covers only Git-visible, non-ignored repository paths. It does not
claim that the wrapper observes ignored/outside-repository writes or provides a
process/filesystem sandbox.

| Command | Allowed Prefixes | Exit Status | Modified Paths | Review Disposition | Skipped Rationale |
| --- | --- | ---: | --- | --- | --- |
| `bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md --allow-prefix docs/ --allow-prefix scripts/validation/ --allow-prefix tests/validation/ --allow-prefix .github/ --allow-prefix .pre-commit-config.yaml` | `docs/`, `scripts/validation/`, `tests/validation/`, `.github/`, `.pre-commit-config.yaml` | Pending | Pending | Pending | N/A; reserved for T-DCC-006 from an initially clean worktree |

## Deviation Notes

- **2026-07-13 preflight resolution**: The user approved resolving the conflict
  between the original one-commit-per-task wording and Task 6's clean-wrapper
  plus post-review closure requirements. Tasks 1-5 use at least one logical
  commit each. Task 6 uses a generated/pre-closure commit, pre-closure review,
  lifecycle-closure commit, and fresh post-closure whole-branch review. Review
  fixes remain separate logical commits. This changes commit/review sequencing
  only; scope, validation, rollback, and protected-surface boundaries remain
  unchanged.

## Program Follow-up Boundary

Completion of this task authorizes no automatic continuation. Later sub-project
Specs must independently own README/instruction migration, SDLC definition
chain, execution evidence, operations/release documents, reference/archive and
remaining corpus migration, corpus-wide blocking, and classic GitHub
branch-protection synchronization. Docker Compose services and deployment
runtime remain separate approval-gated work.

## Related Documents

- **Parent Spec**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Parent Plan**:
  [Implementation plan](../plans/2026-07-13-document-contract-canonicalization.md)
- **Stage 00 Governance**:
  [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage 99 Support**:
  [Template support](../../99.templates/support/README.md)
- **Canonical Audit**:
  [Implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Canonical Research**:
  [Research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Workspace Contract**:
  [`_workspace` contract](../../../_workspace/README.md)
