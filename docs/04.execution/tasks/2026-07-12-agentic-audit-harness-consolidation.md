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
| T-AHC-001 | Clarify canonical, snapshot, and superseded lifecycle routes. | doc | Audit Lifecycle | Task 1 | Snapshot preservation, contracts, review | Documentation Specialist | Done |
| T-AHC-002 | Reassess all 161 criteria and canonical overview. | doc/eval | Criterion Contract | Task 2 | State distribution, 11/161, review | Agentic Workflow Specialist | Done |
| T-AHC-003 | Implement semantic closure contract and adversarial tests. | impl/test | Semantic Freshness | Task 3 | RED/GREEN, CLI PASS, review | QA Engineer | Todo |
| T-AHC-004 | Split scoped and broad security readiness signals. | impl/test | Security Readiness | Task 4 | 13 controls, negative test, review | Security Auditor | Todo |
| T-AHC-005 | Wire semantic freshness into generator, contracts, and CI. | impl/ci | QA and CI | Task 5 | Unit/matrix/workflow/contracts, review | CI/CD Engineer | Todo |
| T-AHC-006 | Regenerate, run full QA/wrapper, and close evidence. | test/doc | Verification | Task 6 | Full bundle, wrapper, branch review | QA / Documentation | Todo |

## Phase View

### Phase 1 — Evidence Organization

- [x] T-AHC-001 Audit lifecycle organization
- [x] T-AHC-002 Canonical current-state reassessment

### Phase 2 — Enforced Precision

- [ ] T-AHC-003 Semantic freshness validator
- [ ] T-AHC-004 Security readiness precision
- [ ] T-AHC-005 QA and CI integration

### Phase 3 — Closure

- [ ] T-AHC-006 Generated evidence, controlled QA, and branch review

## Review Ledger

| Task | Implementation Commit(s) | Spec Verdict | Quality Verdict | Findings / Resolution | Review Package |
| --- | --- | --- | --- | --- | --- |
| T-AHC-001 | `2579560b..38ead5f3` | PASS | APPROVED | C0/I0/M0; no findings | `.superpowers/sdd/task-1-review.md` |
| T-AHC-002 | `ee64b3a7..699eda00` | PASS | APPROVED | Initial I1/M1 resolved by `699eda00`; re-review C0/I0/M0 | `.superpowers/sdd/task-2-rereview.md` |
| T-AHC-003 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-004 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-005 | Pending | Pending | Pending | Pending | Pending |
| T-AHC-006 | Pending | Pending | Pending | Pending | Pending |

### T-AHC-001 Audit Lifecycle Organization Evidence

- **Implementation commit / base**: This Task 1 logical commit is based on
  `2579560b` (`docs(plan): correct historical evidence checks`).
- **Changed scope**: Replaced the root audit lifecycle routes, added one dated
  evidence boundary to each of the eighteen 2026-07-03/04 Markdown reports,
  and renamed the 2026-07-03 pack's `Planned References` heading to
  `Included Reports`.
- **Historical preservation**: The corrected
  `rg --files-without-match '^## Evidence Snapshot Boundary$' ...` check and
  sorted before/after historical-literal `diff -u` produced no output. The
  before and after captures each contain seven preserved payloads.
- **Validation**: `bash scripts/validation/check-repo-contracts.sh` passed with
  `failures=0`; `git diff --check` passed.
- **Approved command corrections**: The original `rg -L` used ripgrep's
  follow-symlink option rather than a files-without-match check, and the
  original `rg -n` comparison included shifted line numbers and nondeterministic
  file order. Human-approved corrections are recorded in plan-fix commit
  `2579560b`; both corrected checks pass.
- **Protected surfaces**: No runtime, remote, secret, provider, model, CI,
  validator, generated artifact, or infrastructure surface changed.
- **Independent review**: Spec compliance PASS and task quality APPROVED with
  Critical 0, Important 0, and Minor 0. The reviewer confirmed 18/18 snapshot
  boundaries, canonical/snapshot/supersession routing, historical preservation,
  pending-before-review lifecycle discipline, and the docs-only boundary.

### T-AHC-002 Canonical Current-State Reassessment Evidence

- **Implementation base**: The Task 2 implementation starts from reviewed Task
  1 base `ee64b3a7`; T-AHC-002 remains `Todo`, its Phase 1 checkbox remains
  unchecked, and its Review Ledger row remains `Pending` until independent Spec
  compliance and quality review approve the implementation commit.
- **Complete reassessment**: All eleven criterion reports and all 161 unique
  ten-field rows were reviewed against current tracked source and completed
  T-AER-008 through T-AER-012 evidence. Structural baseline was already green at
  11 reports / 161 rows while the required semantic stale-phrase scan identified
  the pre-implementation metadata, wrapper, provider-task, and lifecycle wording.
- **Evidence-backed state changes**: `DML-01`, `DML-02`, `DML-03`, `DML-04`,
  `DML-05`, `DML-07`, `DML-08`, `DML-11`, `DML-14`, `QAF-12`, and `AUT-09`
  changed to `Implemented`, depth `3`, disposition `Retain`. Each row now cites
  the tracked profile/checker/wrapper source, focused tests, and T-AER review
  evidence; no other criterion state changed.
- **Metadata boundary**: T-AER-008 supplies typed profiles, stable IDs, direct
  relations, freshness, transitions, explicit reverse overrides, active-chain
  migration, and changed/new enforcement. T-AER-012 supplies deletion,
  identity-change, explicit-base, and impacted-dependent referential-integrity
  hardening. The full historical inventory remains advisory; `DML-09` and
  `DML-12` remain `Partial`, and no corpus-wide migration is claimed.
- **Wrapper boundary**: T-AER-009 supplies the controlled wrapper and its
  independently approved 29-case fake-hook suite. Direct agent all-files
  execution remains prohibited, and wrapper evidence covers only Git-visible,
  non-ignored repository paths; ignored/outside writes and process/filesystem
  sandboxing are not claimed.
- **Conservative provider/eval/live scope**: Completed provider synchronization,
  semantic lifecycle parity, 7/7/7 hook parity, and existing CI metadata-step
  evidence replace stale Task 10 future tense. Native acceptance, `.gemini`
  adoption, general semantic scoring, live execution, remote enforcement, model
  entitlement, runtime/CD, and broad supply-chain gaps retain their prior
  `Partial`, `Missing`, or `Needs Revalidation` states.
- **Exact final distribution**: `Implemented=67`, `Partial=69`, `Missing=14`,
  `Not Applicable=2`, `Needs Revalidation=9`; total `161`.
- **Validation**: Matrix write/check passed; audit coverage check passed with
  11/11 reports, 161/161 unique rows, and 15/15 overview categories; criterion
  contract passed at 11/161; the exact five distribution rows were found; the
  required stale-phrase scan returned no matches; the full validation suite
  passed 90/90; the fake-hook wrapper suite passed 29/29; changed-document
  metadata selected 12 paths with zero violations; provider sync and hook-parity
  freshness passed; traceability passed at 46 pairs / zero failures;
  implementation alignment passed at 640 stage docs / 5,041 links / zero
  failures; repository contracts passed with `failures=0`; `git diff --check`
  passed.
- **Protected surfaces**: Documentation and the generator-owned matrix only.
  No 2026-07-03, 2026-07-04, or 2026-07-07 audit file, runtime, Compose,
  infrastructure, secret, credential, remote GitHub, CI workflow, provider/model
  policy, `.gemini` adoption, or deployment state changed. Direct pre-commit was
  not run, and docs-only changes do not trigger the code-file Graphify refresh.
- **Independent review**: The initial review returned Critical 0, Important 1,
  Minor 1: scoped metadata summaries contradicted the implemented rows and the
  reassessed documents retained `reviewed_at: 2026-07-11`. Fix commit
  `699eda00` aligned all affected summaries, set the overview and eleven
  criterion leaves to `reviewed_at: 2026-07-12`, preserved 67/69/14/2/9, and
  passed metadata 15/0 plus repository contracts. A fresh full-diff re-review
  returned Spec PASS, Quality APPROVED, C0/I0/M0. The original reviewer thread
  could not be re-triggered because of the collaboration thread limit, so the
  approved subagent workflow used a new independent reviewer and recorded the
  platform constraint.

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
