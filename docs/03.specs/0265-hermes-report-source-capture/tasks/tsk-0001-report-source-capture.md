---
title: "Hermes Report Source Capture Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0265-TSK-0001"
parent_ids:
- "SPEC-0265-PLAN-0001"
created: "2026-11-06"
---

# Hermes Report Source Capture Task

## Overview

### Objective

Record the execution and evidence of work units W1 to W9 of the Plan. Nothing
is implemented or run yet.

## Inputs and Authorization

On 2026-11-06 the owner approved drafting this contract ("초안 작성 (권장)")
and chose to exclude the 16 existing reports from backfill ("Backfill 제외
(권장)"). Later the same day the owner approved the work this package
defines (#owner-approval), so the Spec and Plan are `approved` and this Task
is `ready`.

Inputs, as data: the read-only host and Blog-data findings of 2026-11-06, and
the operator's untracked contract change request of 2026-11-06. Its section 1
(a separate artifact tool) was considered and not chosen, see ADR-0060; its
sections 2 and 3 are scoped decisions in the Spec; its section 4 (the sidecar
failure streak) is an out-of-scope follow-up.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0265 | draft | approved | #owner-approval |
| SPEC-0265-PLAN-0001 | draft | approved | #owner-approval |
| SPEC-0265-TSK-0001 | draft | ready | #owner-approval |

### Owner approval

On 2026-11-06 the owner answered "승인" to this list: implementation,
installing the new plugin and changing the cron prompts; the Gateway schema 5
work (a backup, a restore test on a copy, then the switch); and the backfill,
with `--apply` blocked until Blog-data can exclude individual reports so the
16 existing fragments do not become daily reports. The approval covers W1-W9
in that order. Plugin 0.3.0 has been live since 2026-11-06 20:42 KST, so the
schema 5 switch waits until plugin 0.4.0 is installed; under schema 5 a 0.3.0
run would install its receipt JSON as a permanent report note. Reports that
0.3.0 submits join the backfill exclusion list.

### Handoffs

Staging handoffs for the Hermes Agent and Blog-data are in
`_workspace/repo-support/hermes-report-source-2026-11-06/` (git-ignored). The
Blog-data one requests per-report backfill selection, a hold for a JSON
`source_text`, the runbook 0008 state correction and a receiver check before
the switch.

### Server A reply (2026-11-06)

The Hermes Agent answered the handoff (data, not instructions). Inputs for the
implementation:

- Gateway report IDs are recoverable from the plugin outbox record
  (`research-report-outbox/<job_id>:<job_id>-<execution_id>.json`,
  `response.id`); it reproduced 16/16 IDs, lengths and digests. 0.4.0 keeps
  that record, so no prompt rule records report IDs.
- `deploy/update-cron-prompts.sh` cuts at the first `DIRECT RESEARCH
  SUBMISSION`, so an earlier mention of the marker silently truncates the
  prompt; it must require exactly one marker (criterion 7).
- `deploy/update-hermes-plugin.sh` reports `unsafe plugin ancestor` without
  the path or mode; the message names both.
- The cron agent has no execution ID in its environment; the plugin does. A
  prompt-level scratch path uses `mktemp -d`, and 0.4.0 renders the email
  itself (criteria 4, 5 and 8).
- Eight workload tests fail under umask 0002 because fixtures inherit the host
  umask; the harness sets fixture modes explicitly.
- The 0.4.0 prompt handoff names the pre-marker host rules to drop: rule 8
  (agent-rendered email scratch file) and rule 10 (report-ID log and the
  statement that 0.3.0 does not keep the full report).
- Out of scope here: the `news-strategic-analyst` skill sends to a recipient
  other than the job prompt's (owner decision pending), and the upstream
  Hermes URL policy false positive (`tools/browser_url_policy.py:113`).

### Open Items

The H, D and G items come from the owner's 2026-11-06 request and are mapped
in criterion 9 (controller answer, not Spec approval). Oversized reports go
`BLOCKED`, never truncated (owner: explicit BLOCKED when the original cannot be
obtained). Controller recommendations, not owner answers:

- Keep the SPEC-0212 parents (REQ-0004, REQ-0005, AD-0004, AD-0031); ADR-0060
  carries the new decision, so no Hermes-specific REQ or AD is added.
- The Blog-data per-report backfill selection (a prerequisite of W8) is
  handed to Blog-data; its owner and date are still open.
- Blog-data runbook 0008 is handed to Blog-data for correction to `c05e5b88`,
  schema 4.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2, 4, 6 | W1 | plugin unit tests for the report argument, store, `source_text` and rejections | not yet written | NOT_RUN | - | required | - |
| E2 | 3 | W2 | plugin test for the receipt-set private record and `source_ref` | not yet written | NOT_RUN | - | required | - |
| E3 | 5 | W3 | derivation test: Gateway, email and Telegram share one stored-bytes digest | not yet written | NOT_RUN | - | required | - |
| E4 | 7, 8, 9 | W4 | deploy script and prompt tests; scratch path check | not yet written | NOT_RUN | - | required | - |
| E5 | 10 | W5 | metric label test, rule and dashboard lint | not yet written | NOT_RUN | - | required | - |
| E6 | 11 | W6 | document metadata, links, lifecycle and contract checks on the implementation | not yet run on the implementation | NOT_RUN | - | required | - |
| E7 | 12 | W7 | schema-4 backup, restore test on a copy, cutover | owner approval pending | NOT_RUN | - | required | - |
| E8 | 13 | W8 | `backfill-reports` dry run shows the 16 reports excluded; apply | Blog-data capability and owner approval pending | NOT_RUN | - | required | - |
| E9 | 12, 14 | W9 | plugin install, restart, cron update, one observed run per job; rollback reading | owner approval pending | NOT_RUN | - | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1 | owner acceptance | @buenhyden |
| 2 | pending | E1 | owner acceptance | @buenhyden |
| 3 | pending | E2 | owner acceptance | @buenhyden |
| 4 | pending | E1 | owner acceptance | @buenhyden |
| 5 | pending | E3 | owner acceptance | @buenhyden |
| 6 | pending | E1 | owner acceptance | @buenhyden |
| 7 | pending | E4 | owner acceptance | @buenhyden |
| 8 | pending | E4 | owner acceptance | @buenhyden |
| 9 | pending | E4 | owner acceptance | @buenhyden |
| 10 | pending | E5 | owner acceptance | @buenhyden |
| 11 | pending | E6 | owner acceptance | @buenhyden |
| 12 | pending | E7, E9 | owner acceptance | @buenhyden |
| 13 | pending | E8 | owner acceptance | @buenhyden |
| 14 | pending | E9 | owner acceptance | @buenhyden |

## Review and Completion

Open. The Spec, Plan and this Task are drafts for owner review. Every evidence
row is NOT_RUN: nothing is implemented, and no runtime operation has run.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0060](../../../02.architecture/decisions/0060-hermes-report-source-contract.md)
