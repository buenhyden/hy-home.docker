---
title: "W00 Delta Gap Closure Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-15"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0067"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-15"
---

# W00 Delta Gap Closure Task

## Scope

### Objective and Parent

#### Objective

Own W128/criterion 123. Audit the completed W00-DELTA record (TSK-0066)
against every step and acceptance test of the 3.0.1 W00-DELTA prompt, close
each item it left unread, unreviewed, unconfirmed or wrongly decided, and
record the corrections here, since TSK-0066 is terminal and its body is not
edited.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [3.0.1 W00 delta](tsk-0066-w00-delta-3-0-1.md)

### Inputs and Authority

On 2026-11-15 the user asked to examine the W00 prompt for remaining,
unverified, unreviewed, unconfirmed, unstarted, conflicting and missing items,
to correct them with the requirement taking priority, and to commit, push,
open a pull request and merge. That request authorizes this Task, the Spec and
Plan rows for criterion 123 and that delivery. It does not authorize product
code, runtime, native-provider or cross-repository actions; the items handed
to other work units stay with them.

Newly read inputs of the package
`_workspace/governance/workspace_governance_3_0_1_20261115/`: the S03, S04,
S05, S06, S07, S10, S20, S21, S22, S24 and S27 rows of `external-research.md`,
`reports/improved-report.md`, `reports/questions.md` and D03 lines 15 to 45.

## Execution Log

### Work Performed

#### Audit of TSK-0066 against the prompt

| Gap | Prompt requirement | TSK-0066 state | Closure |
| --- | --- | --- | --- |
| G-01 | Step 1: mounts | Not checked | Closed in Environment below |
| G-02 | Pre-start check: installed tools | Not recorded | Closed in Environment below |
| G-03 | Step 2: PR state, changed files, diff and checks | Files and checks for 3 of 13 PRs; no diff review | Closed in PR review below |
| G-04 | Read the eleven named external sources | Not read | Closed in External sources below |
| G-05 | Read the integrated report and questions | Not read | Read; RUN-SETTINGS is not triggered by W00, which needs no backend, cost, host permission or deletion target |
| G-06 | Step 4: separate code-complete, acceptance-wait, unrun operation and new-requirement gap | One verdict column only | Closed in Verdict axes below |
| G-07 | Report: real latency comparison | Not reported | Closed in Latency below |
| G-08 | Step 6: apply the confirmed draft rule without over-blocking | D-03 marked CHANGE | Corrected in Verdict corrections below |
| G-09 | Missing obligation hidden by retirement (Q04) | Not found | New D-11 below |
| G-10 | D03 placeholder rule | Not checked | New D-12 below |

#### Environment

| Item | Observation |
| --- | --- |
| Mount | `/` on `/dev/mapper/ubuntu--vg-ubuntu--lv`, ext4, `rw,relatime`; the workspace has no separate mount |
| Symlinks (depth 3) | Only `.venv/` interpreter links; none leaves the workspace |
| Tools | Python 3.12.3, jsonschema 4.10.3, git 2.43.0, gh 2.45.0, Docker 29.9.2, Claude Code 2.1.325, codex-cli 0.169.0, graphify 0.9.91. Versions only; no native provider run |

#### PR review 1023 to 1035

Changed files and the check rollup were read for every PR: `candidate-quality`,
CodeQL and GitGuardian SUCCESS on all thirteen. The diffs below were reviewed.

| PR | Non-docs change | Review result |
| --- | --- | --- |
| 1023 | None | Criterion 6 and 7 text reworded, not removed; nine Tasks moved `draft` to `in-progress` with a note that work had started, under approved parents. No hidden withdrawal |
| 1024 | None | Wording such as `active` to `approved` for AD-0031/0032; no criterion removed |
| 1025 | None | 225 lines removed from SPEC-0204; spot check found no removed criterion number or status change |
| 1026, 1031, 1035 | Tests in 1031 | Fixtures re-pointed from retired SPEC-0256 to SPEC-0212 and the free-number search now skips `reserved_history`; no assertion weakened |
| 1027, 1028, 1030, 1033 | READMEs only | Task completion and reruns; not repeated |
| 1029 | `restic/backup.sh`, `offsite.sh`, `bin/hyhome-backup.sh`, `test_memory_backup_contract.py`, glossary | Comment text only; behavior unchanged. The comments now say snapshot accounting is not admission-gated "yet" with no named owner; see D-11 |
| 1032 | n8n workflow, `test_compose_baseline_gates.py` | Outside W00; SPEC-0204 owns it |
| 1034 | None | Replay record; not promoted (TSK-0066 D-06) |

Diffs of 1025 were spot-checked for criterion and status lines only; the rest
of its prose was not read.

#### External sources

| Source | Applied here | Not applied |
| --- | --- | --- |
| S05 arc42, S27 RFC 8174 | Choices recorded with reasons in the verdict rows | No new ADR for this intake |
| S06, S07 NASA SWE-051/052 | Ambiguous, unimplemented and missing items kept apart (G-06); trace from criterion to owner | No NASA process or tooling |
| S03 CommonMark, S04 Diátaxis | Not used by W00; consumed by W03-FORMS and W04-CONTENT | - |
| S10, S20, S21, S22, S24 | Tool versions only; no claim of native hook delivery, enforcement or runner isolation | Native witnesses belong to W07-ADAPTER and W09-ENV |

#### Verdict corrections

D-03 of TSK-0066 is corrected from CHANGE (latent) to KEEP_VERIFIED. D03
(lines 23, 39 and 41) lets a separate valid approval authorize work in its
own scope, and forbids blocking work because some other draft exists. An
approved Spec and Plan are that approval, and `spec_packages.py:686-696`
already stops a Task under a draft Spec or Plan. A check that refuses an
approved Spec because its Requirement is draft would over-block. W04-LIFECYCLE
receives no D-03 item.

#### New items

| ID | Item | Verdict | Evidence | Receiving owner |
| --- | --- | --- | --- | --- |
| D-11 | Retired SPEC-0270 criterion 2 says every memory-writing, backup and restore entrypoint uses capacity admission, and it was accepted. The daily `backup.sh backup` and `offsite.sh copy` run without admission since `52ef97b83` (2026-11-11), so the memory store is not in daily snapshots. Runbook `0021-backup-and-restore.md:708-712` defers the fix to "a new Spec", and no Spec or Task owns it | CHANGE | `backup.sh:81-86`, `offsite.sh:160-163`, `test_memory_backup_contract.py:29-35` | W08-MEMORY. The requirement is kept; the redesign must restore admission on the daily path or bring an explicit owner withdrawal (Q04) |
| D-12 | D03 forbids approving a document that still holds placeholders. `metadata/heading.py:1512, 1585` rejects them only in registered table cells; prose `{{...}}`, TODO or TBD is not rejected. No current breach: the three matches are quoted in code spans of terminal Tasks | CHANGE (latent) | `heading.py:1512-1585`; repository search | W04-LIFECYCLE |

#### Verdict axes

| ID | Code complete | Waiting acceptance | Operation not run | New requirement gap |
| --- | --- | --- | --- | --- |
| D-01, D-02, D-04 | Yes | No | - | No |
| D-03 | Yes | No | - | No (corrected) |
| D-05 | - | - | Local cost not measured | Yes |
| D-06 | Partly | SPEC-0262/0263 criteria | LAB live input | No |
| D-07 | Store only | SPEC-0244 criteria | Native memory use | Yes (retrieval, capture) |
| D-08 | Role text | - | Native deny test | Yes |
| D-09 | - | - | - | Not assessed |
| D-11 | No | Accepted criterion, not met | Daily memory snapshot | No: existing requirement unmet |
| D-12 | Partly | - | - | Yes |

#### Latency

The PR 1036 document-only candidate took 3 min 45 s (`candidate-core`) and
3 min 12 s (`candidate-documents`) on its first head and 3 min 38 s and
4 min 14 s on its second. TSK-0065 recorded 10 to 16 min and 15 to 29 min for
code-changing W06 candidates. The inputs differ, so this shows the selection
cost of a document-only change, not a speed-up. Locally,
`check-document-links.py --mode commands` exceeded the 600 s tool timeout,
while `--mode alignment` finished well inside it; this is a local feedback
cost for D-05 (W05-GATES), not measured precisely here.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0067 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0067 | ready | in-progress | #audit-of-tsk-0066-against-the-prompt |

### Blockers and Decisions

No user decision is needed. D-11 keeps the accepted requirement; changing it
to a permanent exception would need the owner's explicit withdrawal, which
W08-MEMORY may present with options.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gap audit | 123 | W128 | source-review | TSK-0066 against each W00-DELTA step and acceptance test at `f8a68537d` | PASS | G-01 to G-10 closed above | required | - |
| PR diff review | 123 | W128 | source-review | `git diff <merge>^1 <merge>` of PRs 1023 to 1035 as scoped above | PASS | PR review 1023 to 1035 | required | - |

### Resolution Links

None.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 123 | pending | Gap audit, PR diff review | Awaiting owner acceptance | SPEC-0212 TSK-0067 |

### Remaining Conditions

Owner acceptance of criterion 123. D-05 to D-09, D-11 and D-12 run in their
receiving work units.

## Handoff

### Promotion Receipt

None; this Task changes no canonical owner.

### Next Owner

@buenhyden accepts criterion 123. W01-CONTRACT may start; its only
prerequisite, W00-DELTA, is met.
