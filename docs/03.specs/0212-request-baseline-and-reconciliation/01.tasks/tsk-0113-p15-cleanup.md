---
title: "P15 Cleanup Task"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0113"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-24"
---

# P15 Cleanup Task

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

Own criterion169/W185 in the [Spec](../spec.md) and [Plan](../plan.md).
Apply the D15 delta: a lifecycle rule for one-off work artifacts, the current
classification of the staging surface, and removal of only what this
remediation program owns and nothing reads.

##### Inputs and Authority

The direct P15-CLEANUP1.2.0 request authorizes this workspace, scoped
documentation changes, removal of artifacts this program owns and normal
commit, push, PR and merge. Inputs are the matching package README/P15, D15,
the decisions file and the Docker profile. Start was clean `main` c001d125 on
branch `codex/p15-cleanup-1-2-0` in the linked worktree `.worktrees/p15`;
brief p15-cleanup bound this scope before the first edit. This Task's
forecast was recorded before the start (revision 1, P30 20, P50 35, P80 60
elapsed minutes). Direct user authorization is authority; this record is
not.

#### Execution Log

##### Work Performed

The staging contract (`_workspace/README.md`, ENVIRONMENT-CONSTRAINTS
R1-R3 and the tracking test) and each tool's own cleanup stay: the work
dispatcher removes worker trees and expires run text at 30 days and run
folders at 90, LAB `down`/`reap` stop only their own project, and the
Compose start records and releases its own reservation. Nothing stated when
a one-off artifact ends. ENVIRONMENT-CONSTRAINTS 2.7.0 adds R169-R172 (owner
and end condition per artifact, removal only of owned, unread artifacts, no
symlink or mount escape and no host prune, and owner, resume point and
deletion condition for recovery material and a still-read input package),
and the harness maintenance guide 2.8.0 adds the end-of-work cleanup
procedure.

Staging classification on 2026-11-24, by current consumer:

| Item | Size | Consumer | Disposition |
| --- | --- | --- | --- |
| `workspace_governance_remediation_1_2_0_20261123/` | 3.5 MiB | P16 and P17 read it | Keep; P17 deletes it last |
| `workspace_governance_remediation_1_1_0_20261120/` | 2.7 MiB | None: superseded input of this program; the 1.2.0 package names it only as an audit baseline and P16/P17 do not read it | Remove (owned, finished) |
| `repo-support/task-2026-07-23-security-supply-chain-runtime-closure/` | 3.2 GiB | Grype database cache read by `verify-sample-service-supply-chain.sh` and written by `seed-grype-db-cache.sh` | Keep (tool cache) |
| `repo-support/analysis/` | 98 MiB | Inventory output and plans read by `compose_start.py` and `compose_observation.py` | Keep (TSK-0094) |
| `repo-support/hermes-report-source-2026-11-06/` | 412 KiB | Hermes report work, last written 2026-11-20 | Keep; its owner decides |
| `repo-support/{openbao,valkey}-native-evidence/` | 136 KiB | `infra/09-platform-ops/security-updates/verification.json` names the OpenBao index | Keep (TSK-0094) |
| `diagnostics/`, `repo-support/previews/` | READMEs only | Staging contract | Keep |
| `.worktrees/docs/` | empty | None: leftover of a removed worktree (2026-11-14) | Remove |

No tracked file links into either package. The 2026-11-20 decisions Q-01 to
Q-04 are summarized in TSK-0098 and implemented by their owners
(ENVIRONMENT-CONSTRAINTS for Q-02), and P17 reads D17 from the package before
deleting it last, so no durable dependency has to move out of the package.
This program's other run artifacts already left: the P12 plan, decoy and
report copies, every brief draft and every linked worktree it made.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0113 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0113 | ready | in-progress | #work-performed |
| SPEC-0212-TSK-0113 | in-progress | completed | #criterion-decisions |

##### Blockers and Decisions

No Q01-Q04 question is reopened. The agent's removal of the two owned
targets was refused by the session's permission classifier, so the owner
runs the exact commands in Remaining Conditions. Items another Task owns stay
with that owner; the TSK-0094 table of 2026-11-19 is a dated snapshot, and
its `workspace_governance_4_2_0_20261116/` row no longer exists on disk.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 169 | W185 | method=review; tool=-; command=- | P15 1.2.0 package, D15, decisions file; `_workspace` README, ENVIRONMENT-CONSTRAINTS R1-R3, TSK-0094, tool cleanup paths; tracked references to every staging item | PASS | Classification above; the lifecycle gap listed in Work Performed | required | - |
| E02 | 169 | W185 | method=observation; tool=GNU coreutils; command=rm -r and rmdir of the two exact owned paths | `_workspace/workspace_governance_remediation_1_1_0_20261120/` and `.worktrees/docs/` | NOT_RUN | Refused by the session permission classifier before any deletion; left to the owner | required | - |
| E03 | 169 | W185 | method=automated; tool=Python3.12.3; command=check-agent-governance-contract.py --mode repository --section all | Change | PASS | 0 failures | required | - |
| E04 | 169 | W185 | method=automated; tool=Python3.12.3 unittest; command=python3 -m unittest tests.lib.test_surface_ownership | Change | PASS | Exit0; the staging tracking test included | required | - |
| E05 | 169 | W185 | method=observation; tool=GNU coreutils; command=rm -r and rmdir of the two exact owned paths | Owner run from the repository root, 2026-11-24 | PASS | The owner's `rm -r` removed `_workspace/workspace_governance_remediation_1_1_0_20261120/`; `.worktrees/docs/` was already absent when the owner's `rmdir` ran; `_workspace/` holds `diagnostics/`, `repo-support/`, the 1.2.0 package and its README | required | E02 |

##### Resolution Links

E05 resolves E02.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 169 | accepted | E01,E03,E04 | Owner @buenhyden accepted on 2026-11-24 in this chat during P16 (TSK-0114). | @buenhyden |

##### Remaining Conditions

The two owned targets are gone (E05). The 1.2.0 package stays until P17,
whose last step deletes it; if P17 fails, it stays with its owner until P17
resumes and succeeds.

#### Handoff

##### Promotion Receipt

ENVIRONMENT-CONSTRAINTS R169-R172 and the harness maintenance guide own the
rule; the tools own their cleanup. This Task owns execution evidence only.

##### Next Owner

The owner accepted criterion169 in P16; TSK-0114 owns the readiness
ledger. Keep the package through P17.

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
