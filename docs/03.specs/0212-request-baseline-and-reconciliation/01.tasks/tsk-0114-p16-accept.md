---
title: "P16 Acceptance Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-24"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0114"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P16 Acceptance Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion170/W186 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply D16: separate design, code, regression, real environment and owner
acceptance for every R/P step up to P16, record the owner's acceptance where
it was given, keep the cutover not ready while a required boundary is open,
and prepare P17's managed refs.

##### Inputs and Authority

The direct P16-ACCEPT1.2.0 request authorizes this workspace, acceptance
records, read-only observation and normal commit, push, PR and merge. On
2026-11-24 the owner, in this chat, accepted criteria 154 to 161, 163, 165
and 167 to 169 (with E59 superseding E16 for 161; 161 stays pending, see
Blockers), chose to install pasta
before the Codex worker is implemented, approved deleting the merged remote
branches now, and asked for the CodeQL alerts to be reviewed and recorded.
Start was clean `main` 1b7e76aa on branch `codex/p16-accept-1-2-0` in the
linked worktree `.worktrees/p16`; brief p16-accept bound this scope before
the first edit. This Task's forecast was recorded before the start
(revision 1, P30 25, P50 40, P80 70 elapsed minutes). Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

Readiness ledger on 2026-11-24 (design D, code C, regression R, real
environment E, owner acceptance A):

| Criterion | Step | D/C/R | E | A | Open required boundary |
| --- | --- | --- | --- | --- | --- |
| 154 | P00 | done | n/a | accepted | none |
| 155 | P01, R01 | done | hosted CI | accepted | none |
| 156 | P02 | done | hosted CI | accepted | none |
| 157 | P03 | done | hosted CI | accepted | none |
| 158 | P04, R02 | done | hosted CI | accepted | none |
| 159 | P05 | done | hosted CI | accepted | none |
| 160 | P06 | done | two bounded Claude reviews | accepted | none |
| 161 | P07 | done | owned LAB readiness and cleanup | pending | E16 cannot be resolved under the SDLC rule (its CLI version is gone); the owner's acceptance with E59 waits for a decision on that rule |
| 162 | P08 | done | Claude observed; Codex unobserved | pending | Codex native brief run after 2026-11-27 12:53 |
| 163 | P09 | done | shared memory round trip reused | accepted | none |
| 164 | P10 | done | store migration observed | pending | first scheduled run of the renamed unit (2026-11-25 03:00); Codex final-response capture after 2026-11-27 12:53 |
| 165 | P11 | done | real forecast and outcome | accepted | none (calibration needs 20 samples) |
| 166 | P12 | Claude done; Codex refused | two-worker Claude run and cancel | pending | Codex worker: owner installs passt, then implementation and a real run after 2026-11-27 12:53 |
| 167 | P13 | done | read-only real report | accepted | none (effects unobserved by design) |
| 168 | P14 | done | read-only real selection | accepted | none: TSK-0112 E15 (555 tests with the repository venv) and E16 (hosted pass on the fixed head) resolve its open rows; job recreation is seen at the next owner `up` |
| 169 | P15 | done | owned removal (TSK-0113 E05) | accepted | none |
| 138 | W08 | done | removal refused by R2 lock | pending | remove the locked R2 memory copies after 2026-12-10 |
| 148 | W10 | done | daily backup failing | pending | R2 at its 9 GB cap: a remote prune after the lock of snapshot d0f50bdd ends, or an R2 cap decision, then a successful daily backup |
| 153 | W09 follow-up | done | ReDoS re-check PASS; owner dismissed all 10 alerts, 0 open | pending | none; owner acceptance only |

Cutover readiness: **not ready**. Required boundaries stay open for 138,
148, 161, 162, 164 and 166, and 153 has no open required row (the owner dismissed its alerts) and waits
for acceptance only. Hosted CI on
`main` passed for the current heads, so no required CI is cancelled or
failing. Q-01 to Q-04 are settled; no new question affects the cutover
beyond the Codex worker choice already made.

P17 preparation: the owner approved deleting 28 remote branches whose tips
`main` already contains and whose PRs were closed (the P00-P12 `codex/*`
branches, `docs/workspace-maintenance-cutover`, `fix/searxng-engines`,
`refactor/docs-numbered-cutover`); all 28 were deleted. Left on the remote:
`main`, `dev` (merged, kept as a possible role branch) and four open
Renovate branches with their PRs (#1047, #1048, #1140, #1141); one tag,
`0.0.1`. The only local worktree is the primary checkout. P17's plan,
recovery and package removal read D17 from the 1.2.0 package, which stays
until P17's last step (TSK-0113). Template and Blog boundaries do not apply
to this workspace.

##### Blockers and Decisions

The lifecycle check refuses an accepted criterion with an unresolved
required row, so 161 cannot be accepted while E16 stands: a resolving row
must repeat E16's Check text, which names Claude CLI 2.1.329, and that CLI is
gone; recording E59 under it would misstate the tool. The owner decides
whether E16 is retired by an SDLC exception or reviewed again. The CodeQL review reused TSK-0097's 2026-11-19 analysis and re-measured it
(TSK-0097 "ReDoS re-check"): the five ReDoS alerts are false positives and
the five password alerts are synthetic test fixtures; no code changed, and
dismissal stays with the owner. passt is not installed (`pasta`, `passt`
and `slirp4netns` are absent), so the Codex worker is not implemented
blind; its egress namespace is built and observed once the owner installs
passt. Owner acceptance recorded here comes only from the owner's own
answers; a merge or a PASS was not taken as acceptance.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 170 | W186 | method=review; tool=-; command=- | Criterion Decisions and Remaining Conditions of TSK-0082, TSK-0092, TSK-0095 to TSK-0113 on `main` 1b7e76aa | PASS | Ledger above | required | - |
| E02 | 170 | W186 | method=observation; tool=GitHub CLI; command=gh run list --branch main | `main` 1b7e76aa, 2026-11-24 | PASS | CI Quality Gates success on 1b7e76aa, c001d125 and de588ad0 | required | - |
| E03 | 170 | W186 | method=observation; tool=git; command=git ls-remote origin; git merge-base --is-ancestor per branch; gh pr list | Remote refs, 2026-11-24 | PASS | 34 heads and 1 tag; 28 merged non-role branches, 4 open Renovate branches, `dev` merged | required | - |
| E04 | 170 | W186 | method=observation; tool=git; command=git push origin --delete of the 28 merged branches | Owner approval of 2026-11-24 | PASS | 28 deleted; the remote holds `main`, `dev` and 4 Renovate branches | required | - |
| E05 | 170 | W186 | method=observation; tool=which; command=which pasta passt slirp4netns | This host, 2026-11-24 | FAIL | None installed; the Codex worker namespace cannot be built yet | required | - |
| E06 | 170 | W186 | method=automated; tool=Python3.12.3; command=document corpus lifecycle, metadata check-changed | Change | PASS | 0 violations | required | - |
| E07 | 170 | W186 | method=automated; tool=Python3.12.3; command=document corpus lifecycle on the acceptances | Change before 161 and 168 were settled | FAIL | `accepted criterion 161 has an unresolved required observation`, then the same for 168 | required | - |
| E08 | 170 | W186 | method=automated; tool=Python3.12.3; command=document corpus lifecycle on the acceptances | 161 kept pending; TSK-0112 E15 and E16 added | PASS | 0 violations | required | E07 |

##### Resolution Links

E08 resolves E07; E05 stays FAIL until the owner installs passt.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 170 | pending | E01,E02,E03,E04,E06,E08 | The ledger, the recorded acceptances and the ref preparation are complete; the cutover stays not ready while the listed boundaries are open | @buenhyden |

##### Remaining Conditions

P17 starts only when 138, 148, 161, 162, 164 and 166 have closed their required
boundaries: install passt, observe Codex after
2026-11-27 12:53, see the 2026-11-25 03:00 analysis run, clear the R2 cap and
see a successful daily backup, and remove the locked R2 memory copies after
2026-12-10.

#### Handoff

##### Promotion Receipt

Each step's Task keeps its own evidence and acceptance; this Task owns the
readiness ledger only.

##### Next Owner

The owner closes the listed boundaries; this Task's ledger is re-read before
P17-FINAL-CUTOVER, which is not executed automatically. Keep the package
through P17.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
