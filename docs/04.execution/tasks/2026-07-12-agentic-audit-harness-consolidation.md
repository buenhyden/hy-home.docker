---
status: active
artifact_id: task:2026-07-12-agentic-audit-harness-consolidation
artifact_type: task
parent_ids:
  - plan:2026-07-12-agentic-audit-harness-consolidation
---

<!-- Target: docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md -->

# Task: Agentic Audit Harness Consolidation

## Overview

This document tracks six reviewed tasks that organize the Stage 90 audit
corpus, reassess canonical implementation state, add semantic freshness
enforcement, correct security readiness scope, integrate local/CI gates, and
close generated evidence.

## Inputs

- **Parent Spec**:
  [Spec 128](../../03.specs/128-agentic-audit-harness-consolidation/spec.md)
- **Parent Plan**:
  [Implementation plan](../plans/2026-07-12-agentic-audit-harness-consolidation.md)
- **Canonical Audit**:
  [Implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Previous Closure Evidence**:
  [Spec 123 task](./2026-07-11-agentic-engineering-audit-remediation.md)

## Working Rules

- Use a fresh implementation subagent and separate reviewer for each task.
- Follow RED/GREEN for validator and generator behavior.
- Mark a task Done only after Spec compliance and quality are approved.
- Keep ignored briefs, reports, and review packages outside canonical docs.
- Do not run implementation agents in parallel.
- Preserve runtime, remote, secret, provider-native, and model boundaries.
- Never run direct all-files pre-commit; reserve the controlled wrapper for
  T-AHC-006.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Stage 90 audit corpus | User approval of Spec 128 | Audit index and 2026-07-03/04/05 packs | `0fca4705`, current 39-report corpus | Per-task diffs, 11/161 contract, review verdict | Revert logical commit; regenerate owned outputs | No raw logs, secrets, credentials, shell history, or `.env` values |
| Validation scripts/tests | User approval of Spec 128 | Semantic validator, security/audit generators, repo contracts | 90-test baseline and `failures=0` | RED/GREEN tests and full suite | Revert exact logical commit | Deterministic local evidence only |
| Tracked CI workflow | User approval of design section 2 and Spec 128 | Existing `repo-contracts` job | Read-only job and current permissions | Named semantic step, actionlint/zizmor | Revert CI integration commit | No remote run/protection claim or mutation |
| Controlled pre-commit | User-approved wrapper design and Spec 128 | Final clean linked-worktree gate | Tracked task path and clean state | Hook/path evidence below | Stop without cleanup on unexpected paths | Git-visible, non-ignored repository paths only |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AHC-001 | Clarify canonical, snapshot, and superseded lifecycle routes. | doc | Audit Lifecycle | Task 1 | Snapshot preservation, contracts, review | Documentation Specialist | Todo |
| T-AHC-002 | Reassess all 161 criteria and canonical overview. | doc/eval | Criterion Contract | Task 2 | State distribution, 11/161, review | Agentic Workflow Specialist | Todo |
| T-AHC-003 | Implement semantic closure contract and adversarial tests. | impl/test | Semantic Freshness | Task 3 | RED/GREEN, CLI PASS, review | QA Engineer | Todo |
| T-AHC-004 | Split scoped and broad security readiness signals. | impl/test | Security Readiness | Task 4 | 13 controls, negative test, review | Security Auditor | Todo |
| T-AHC-005 | Wire semantic freshness into generator, contracts, and CI. | impl/ci | QA and CI | Task 5 | Unit/matrix/workflow/contracts, review | CI/CD Engineer | Todo |
| T-AHC-006 | Regenerate, run full QA/wrapper, and close evidence. | test/doc | Verification | Task 6 | Full bundle, wrapper, branch review | QA / Documentation | Todo |

## Phase View

### Phase 1 — Evidence Organization

- [ ] T-AHC-001 Audit lifecycle organization
- [ ] T-AHC-002 Canonical current-state reassessment

### Phase 2 — Enforced Precision

- [ ] T-AHC-003 Semantic freshness validator
- [ ] T-AHC-004 Security readiness precision
- [ ] T-AHC-005 QA and CI integration

### Phase 3 — Closure

- [ ] T-AHC-006 Generated evidence, controlled QA, and branch review

## Review Ledger

| Task | Implementation Commit(s) | Spec Verdict | Quality Verdict | Findings / Resolution | Review Package |
| --- | --- | --- | --- | --- | --- |
| T-AHC-001 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-002 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-003 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-004 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-005 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-006 | Pending | Pending | Pending | Pending | Pending |

## Verification Summary

- **Baseline**: `codex/audit-harness-consolidation` from
  `8b58abc22abb8f93c5580e7185efa0f6a62c4e7b`; unit tests 90/90; repository
  contracts `failures=0`.
- **Test Commands**: Exact commands are in the parent Plan; results are added
  after execution.
- **Eval Commands**: Structural 11/161, semantic 11-assertion, scoped/broad
  security, metadata, generated freshness, workflow, and branch review.
- **Evidence Location**: This task plus ignored `.superpowers/sdd/` briefs,
  reports, review packages, and progress ledger.

## Controlled Agent Pre-commit Evidence

Evidence covers only Git-visible, non-ignored repository paths. It does not
claim ignored/outside writes, process isolation, filesystem sandboxing, remote
CI execution, or remote enforcement.

| Command | Allowed Prefixes | Exit Status | Modified Paths | Review Disposition | Skipped Rationale |
| --- | --- | ---: | --- | --- | --- |
| Reserved for the exact Task 6 wrapper command in the parent Plan | Exact listed Task 6 prefixes | Pending | Pending | Pending | N/A after execution; intentionally reserved before T-AHC-006 |

## Deviation and Protected-Surface Notes

- No deviation is currently recorded.
- Runtime Compose, infrastructure state, deployment, secrets, credentials,
  remote GitHub, `.gemini`, provider entitlement, and model literals are out
  of scope.
- Remote CI, branch protection, provider entitlement, runtime health, and
  deployment state remain unverified unless separately approved.
- The collaboration tool exposes no per-dispatch model argument. Platform
  selection remains platform-owned; no repository model policy is inferred.

## Related Documents

- [Spec 128](../../03.specs/128-agentic-audit-harness-consolidation/spec.md)
- [Implementation plan](../plans/2026-07-12-agentic-audit-harness-consolidation.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Audit implementation matrix](../../90.references/data/governance/audit-implementation-matrix.md)
- [Security automation readiness](../../90.references/data/security/security-automation-readiness.md)
- [Previous remediation task](./2026-07-11-agentic-engineering-audit-remediation.md)
