---
title: "W02 Disposition 3.0.1 Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-15"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0070"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-15"
---

# W02 Disposition 3.0.1 Task

## Scope

### Objective and Parent

#### Objective

Own W131/criterion 126, the W02-DISPOSITION run of the 3.0.1 package for
this workspace. Classify every open Task against the confirmed decisions,
end only the instructions those decisions override, keep every other
obligation with its owner, record the owner's per-item withdrawals, and
prepare, without running, the target list for the final cutover.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [3.0.1 W00 delta](tsk-0066-w00-delta-3-0-1.md)

### Inputs and Authority

On 2026-11-15 the user asked to continue after W01; W02-DISPOSITION needs
only W00-DELTA. Inputs of the git-ignored package
`_workspace/governance/workspace_governance_3_0_1_20261115/`: the W02 prompt
and designs D00, D14 and D15. The same day the owner withdrew, one item at a
time, SPEC-0263 TSK-0001 criterion 5 and TSK-0002 criterion 8 as
not-required (Q04). Remote history removal and renumbering are not run here
(Q01, Q02, Q10); they run only in Q07-CUTOVER after W11.

## Execution Log

### Work Performed

#### Design summary

| Item | Content |
| --- | --- |
| Designs | D00, D14, D15, bundle 3.0.1; sources S03 to S07, S25, S27, S28 |
| Target | Each open obligation stays with one owner or ends by the owner's per-item withdrawal; nothing unfinished is deleted or marked completed; the cutover is prepared, not run |
| Choice | Classify from each Task's own criteria and evidence; change only what a confirmed decision or the owner settles |
| Rejected | Closing Tasks by status edits; deleting the supabase secret or other user data here (secret actions need their own approval); rewriting remote history now (Q01, Q10 run in Q07-CUTOVER) |
| Interface | Criterion Decisions rows, Lifecycle Events tables, Remaining Conditions notes |
| Risk | Low: Task records and one test comment; focused checks and an author check |
| Sources applied | S25: removing managed refs is separate from residues such as PR refs and outside clones, which the cutover list reports. S28: a worktree isolates files only, so it is not counted as an isolated environment |

#### Read scope

Listed: every Task in the eight open Spec packages. Read: frontmatter,
objective, lifecycle, Criterion Decisions, Remaining Conditions and Next
Owner of each open Task (by three read-only agents), and the cited lines
the author re-checked: SPEC-0263 TSK-0001 and TSK-0002 decisions and rows,
SPEC-0212 TSK-0007 lifecycle, the Next Owner headings of five SPEC-0212
Tasks, SPEC-0204 TSK-0022 authority and headings, and tracked references to
`supabase_password`. Not read: the full bodies of the open Tasks.

#### Open Task dispositions

Three read-only agents read every non-terminal Task's frontmatter,
objective, lifecycle, Criterion Decisions, Remaining Conditions and Next
Owner; the author checked the claims that needed a decision or a change
against the files. SPEC-0212 TSK-0007 is terminal (its lifecycle reaches
`completed`, `tsk-0007:93`) and was listed as open only because a multi-item
Task has no frontmatter status.

| Spec | Task | Class | What remains | Owner |
| --- | --- | --- | --- | --- |
| 0204 | 0001, 0007, 0014, 0016 | NOT_RUN | Runtime, egress, custody, HOME and restore evidence; 0007 stays `draft` and authorizes no deletion | Their Tasks |
| 0204 | 0005, 0006, 0010, 0011, 0012, 0015, 0017, 0018, 0020, 0021 | IN_PROGRESS | Native, HOME, review, delivery or remote evidence; facts dated before 2026-11 need re-checking at the new baseline (Q05) | Their Tasks |
| 0204 | 0022 | IN_PROGRESS | Exact API and worker evidence; status lag fixed below | TSK-0022 |
| 0212 | 0041, 0042, 0044, 0046, 0048, 0049, 0050, 0052, 0054 | IN_PROGRESS | Review, runtime, CI or owner-window evidence per Task | Their Tasks |
| 0212 | 0047, 0055 | DONE_AWAITING_ACCEPTANCE | Owner acceptance only (0055 criterion 108) | @buenhyden |
| 0212 | 0066 to 0069 | Current run | Owner acceptance of criteria 122 to 125 | @buenhyden |
| 0218 | 0002 | IN_PROGRESS | Measured workloads, least-privilege runtime, rollout; its draft admission authorizes preparation only | TSK-0002 |
| 0244, 0245 | 0001 | IN_PROGRESS | Observation, boundary, review; October facts re-checked at the new baseline (Q05) | Their Tasks |
| 0255 | 0001 | DONE_AWAITING_ACCEPTANCE | Hosted CI row E7 never resolved; owner acceptance | @buenhyden |
| 0262 | 0001 | IN_PROGRESS | Independent review and hosted CI of the LAB-check follow-up; PR 1034 is a replay, not a new review | TSK-0001 |
| 0263 | 0001 | IN_PROGRESS | Criterion 7; owner items (`LAB_HOST_BUDGET_*`, COMM-003, the unused supabase secret) | TSK-0001 |
| 0263 | 0002 | Withdrawn criterion | Criterion 8 not-required; the Task stays `in-progress` until the owner closes it | @buenhyden |
| 0263 | 0003 | DONE_AWAITING_ACCEPTANCE | Owner acceptance of criterion 3 | @buenhyden |

No open Task conflicts with Q01 to Q10 or Q-DRAFT: none starts every Docker
service, deletes unfinished work or keeps a recovery backup for the cutover.
SPEC-0204 TSK-0016 and TSK-0020 must run only the selected services (Q07).

#### Changes

| Item | Change | Basis |
| --- | --- | --- |
| SPEC-0263 TSK-0001 criterion 5 | `pending` to `not-required`; E25 and E54 stay as measurements | Owner withdrawal 2026-11-15; decision of 2026-11-06 that no LAB is promoted |
| SPEC-0263 TSK-0002 criterion 8 | `pending` to `not-required`; E21, E24 and E27 stay as measurements | Same |
| SPEC-0204 TSK-0022 | Status `draft` to `in-progress` with a Lifecycle Events table | Its recorded work ran under the owner's 2026-10-30 request; the status follows the work |

#### Closed audit questions and retired packages

KEEP_VERIFIED: OPEN-01 to OPEN-14 appear only in the Historical Audit ID
definition and a test that refuses them as document parents
(`test_lifecycle.py:272`); no check, prompt or policy outputs them as active
or blocking. No retired package (SPEC-0251, 0253, 0254, 0256, 0257, 0259,
0261, 0270) is regenerated. The unmet SPEC-0270 criterion 2 stays handed to
W08-MEMORY (TSK-0067 D-11).

#### Retired package consumers

A search of `scripts/`, `tests/`, `.github/` and `docs/99.templates/` for
the retired Spec numbers found one stale test comment naming SPEC-0270
(`test_compose_baseline_gates.py:2394`); it now names the memory capacity
ledger. No caller, fixture or registration reads a retired package.

#### Final cutover targets

Prepared only; nothing below is changed here. Q07-CUTOVER confirms each
target, permission and concurrent writer before acting, and keeps no
recovery copy (Q10).

| Target | Observed 2026-11-15 | Note |
| --- | --- | --- |
| Remote branches | 2 (`main` and one feature branch) | Feature branches are deleted on merge |
| Tags | 1 | Exact names confirmed at cutover |
| Releases | 1 | Release assets go with the release |
| Actions artifacts | 1,091 | Deletable through the API |
| Actions caches | 192 | Deletable through the API |
| Pull request refs | up to #1039 | `refs/pull/*` cannot be deleted by the owner; reported as a residue |
| Forks | 0 | The repository is public, so outside clones cannot be known; reported as a residue |
| Local worktrees | 1 | `main` only |
| Spec packages | 8 open (0204, 0212, 0218, 0244, 0245, 0255, 0262, 0263) | Close or withdraw each before renumbering (Q02) |
| `_workspace/` | `diagnostics/`, `governance/`, `repo-support/` | Git-ignored; removed after acceptance |

#### Latency

Local: lifecycle and metadata checks finished within a minute each. Hosted
candidate times for this pull request are recorded when its checks finish;
document-only pull requests 1036 and 1037 took 3 to 6 minutes.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0070 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0070 | ready | in-progress | #open-task-dispositions |

### Blockers and Decisions

The owner decided the two withdrawals. Accepting the Tasks classed
DONE_AWAITING_ACCEPTANCE is the owner's decision and is not made here.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Disposition audit | 126 | W131 | source-review | Every open Task in eight Spec packages at `108006595` | PASS | Open Task dispositions | required | - |
| Status corrections | 126 | W131 | document-lifecycle | `check-document-corpus-lifecycle.py` and `check-document-metadata.py --mode check-changed` at `cad0c0389` | PASS | violations 0 | required | - |
| Cutover inventory | 126 | W131 | remote-observation | Read-only `git ls-remote`, `gh release list`, Actions artifacts and caches, repository metadata | PASS | Final cutover targets | required | - |

### Resolution Links

None.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 126 | pending | Disposition audit, Status corrections, Cutover inventory | Awaiting owner acceptance | SPEC-0212 TSK-0070 |

### Remaining Conditions

Owner acceptance of criterion 126, and of the Tasks classed
DONE_AWAITING_ACCEPTANCE. Every other open Task keeps its own owner.

## Handoff

### Promotion Receipt

None; the dispositions change no canonical owner.

### Next Owner

@buenhyden accepts criterion 126. The cutover target list belongs to
Q07-CUTOVER, which runs only after W11.
