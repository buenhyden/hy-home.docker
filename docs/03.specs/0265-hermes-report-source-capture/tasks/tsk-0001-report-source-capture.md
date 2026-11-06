---
title: "Hermes Report Source Capture Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
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

Record the execution and evidence of work units W1 to W9 of the Plan. W1 to
W4 and W6 are implemented in the repository (plugin 0.4.0); W5 is partial; no
runtime operation (W7 to W9) has run.

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
| SPEC-0265-TSK-0001 | ready | in-progress | #implementation-w1-w6 |

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

### Implementation W1-W6

Plugin 0.4.0 (`hermes-plugin/plugin.yaml`), on the worktree of `6378597d9`
before the controller's commit:

- W1: `submit_research_report` contract v2 (`SUBMIT_CONTRACT_VERSION = 2`)
  takes exactly `payload`, `source_receipts` and `report_markdown`; any other
  argument is `invalid_submission_fields`. A missing, empty, placeholder,
  malformed (lone surrogate, control character other than tab, newline and
  carriage return) or over-limit report is refused before any write or network
  call with a stable code and `state: "BLOCKED"`; nothing is truncated or
  substituted. `source_text` is the report, `source_sha256` its UTF-8 digest.
  The Source Receipt checks are unchanged.
- W2: the canonical receipt-set JSON (the bytes 0.3.0 sent as `source_text`)
  is `source-set.json`, created once through the new
  `PrivateRecords.create` (complete temporary linked into place, 0600, no
  replacement, `record_conflict` on different bytes); `source_ref` is
  `hermes-source-set:` plus its digest.
- W3: `report.md`, `email.html`, `telegram.txt` and `manifest.json` (job,
  execution, scheduled instant, digests, `derived_from_sha256`) live in
  `research-report-store/<job_id>-<execution_id>/` (0700). The stdlib
  renderers read only the stored bytes. The tool result carries the paths and
  digest whatever the Gateway answered; the outbox record and `response.id`
  are unchanged.
- W4: the prompt orders finalize, collect, submit once, then send from the
  returned files; it forbids the shared `email_body.html`, uses `mktemp -d`
  for any other temporary directory, keeps the email, Telegram and Gateway
  results apart and never resends an email; the statement that the full report
  is not preserved is gone. `update-cron-prompts.sh` requires exactly one
  marker per prompt (else it names the job and count before any edit), checks
  that the head is kept and leaves a job already on the current block
  unchanged. `update-hermes-plugin.sh` refusals name the path, octal mode, uid
  and link count. The umask-dependent fixtures (seven update-script tests and
  the address policy test) set their modes explicitly.
- W5 (partial): `tools.metric_lines` builds Pushgateway lines whose labels are
  only job kind, outcome, a fixed reason enumeration and a size bucket. The
  workload has no Pushgateway push path, so nothing is pushed; the push
  wiring, the Alertmanager rule and the Grafana panel remain open.
- W6: the workload README states the new `source_text` meaning, the report
  store, the trust boundaries and the rollback order.

Criterion 9 mapping: H (item identity, titles, quotes, numbers and dates),
D-03, G-02 and G-03 are prompt text, checked by
`test_prompt_carries_the_owner_item_rules`. D-01 is the existing
`source_check.check_item` quote check; the Attester byte comparison is an
investigation, not code here. D-02 (business-evidence gate), D-04 (publish
date in the signed set) and D-05 (historical fetch-failure classification)
need their own evaluation or Blog-data contract and are not implemented here.
G-01's producer dedupe is prompt text; Export and ACK are untouched.

Design deviations: the pinned `ingestion-v1` fixture predates
`source_quotes`, so the schema test validates the request with the quotes
removed and checks the item field set separately (as 0.3.0 did implicitly).
The Telegram text records its origin in `manifest.json`, not in its visible
body. The 0.3.0 bound of 524288 characters on the receipt-set JSON is replaced
by the 4 MiB private-record limit (`source_set_too_large`, `BLOCKED`).
`tests/e2e_collect_harness.py` passes a synthetic report; the owned-ingress E2E
was not run.

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
| E1 | 1, 2, 4, 6 | W1 | `python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`ReportSourceContractTests`, `ToolSchemaTests`, `PrivateRecordCreateTests`); new tests fail on `6378597d9` sources | worktree on `6378597d9`, uncommitted | PASS | 430 tests, OK under both umasks | required | - |
| E2 | 3 | W2 | same suite: `test_source_ref_digest_is_the_private_receipt_set_record` | worktree on `6378597d9`, uncommitted | PASS | 430 tests, OK | required | - |
| E3 | 5 | W3 | same suite: `test_gateway_email_and_telegram_share_one_stored_digest`, `test_renderers_escape_and_flatten_markdown` | worktree on `6378597d9`, uncommitted | PASS | 430 tests, OK | required | - |
| E4 | 7, 8, 9 | W4 | same suite: `test_deploy_scripts.py` prompt, marker-count and rerun tests; `test_plugin_bundle.py` message tests; `bash -n` and `shellcheck` on both deploy scripts | worktree on `6378597d9`, uncommitted | PASS | 430 tests, OK; shellcheck clean | required | - |
| E5 | 10 | W5 | metric label test `test_metric_labels_are_fixed_low_cardinality_values` | worktree on `6378597d9`, uncommitted | PASS | label test only; push path, Alertmanager rule and Grafana panel not built | required | - |
| E5b | 10 | W5 | Pushgateway push, Alertmanager rule and Grafana panel lint | not built | NOT_RUN | - | required | - |
| E6 | 11 | W6 | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`; `python3 scripts/validation/check-document-links.py --mode alignment` | worktree on `6378597d9`, uncommitted | PASS | metadata: 0 violations; links: 898 documents, 0 failures; `check-document-corpus-lifecycle.py`: 0 violations | required | - |
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

Open. W1 to W4 and W6 have passing repository evidence; W5 is partial
(E5b NOT_RUN); W7 to W9 are operations and stay NOT_RUN until the owner's
approved run and direct evidence.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0060](../../../02.architecture/decisions/0060-hermes-report-source-contract.md)
