---
title: "Hermes Report Source Capture Task"
version: "0.5.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-07"
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
W6 are implemented in the repository: W1 to W4 and W6 in plugin 0.4.0, W5 in
plugin 0.4.1; no runtime operation (W7 to W9) has run.

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
  marker per prompt (else it names the job and count before any edit) and
  leaves a job already on the current block unchanged.
  `update-hermes-plugin.sh` refusals name the path, octal mode, uid and link
  count. The umask-dependent fixtures (seven update-script tests and
  the address policy test) set their modes explicitly.
- W5: done in the W5 round below. The unused `metric_lines` of the first round
  was deleted in fix round 1.
- W6: the workload README states the new `source_text` meaning, the report
  store, the trust boundaries and the rollback order.

Criterion 9 mapping: H (item identity, titles, quotes, numbers and dates),
D-03, G-02 and G-03 are prompt text, checked by
`test_prompt_carries_the_owner_item_rules`. D-01 is the existing
`source_check.check_item` quote check; the Attester byte comparison is an
investigation, not code here. G-01's producer dedupe is prompt text; Export
and ACK are untouched. D-02 (business-evidence gate), D-04 (publish date in
the signed set) and D-05 (historical fetch-failure classification) are
rejected for this change: each needs its own evaluation or a Blog-data
contract.

### Fix round 1

Owner decision (2026-11-06), "Store and render in the plugin": on a day with
no source-backed item the plugin still stores the report and renders the
email and Telegram text; only the Gateway submission is skipped. Changes, in
the fix round 1 working tree, after the independent security and code review:

- `_submit` is store-first: argument names, then `report_markdown`, then the
  cron identity, then `report.md`, `email.html`, `telegram.txt` and
  `manifest.json`; only then the Gateway path (receipts, items, `_validate`,
  size, `source-set.json`, send). Every result after the store carries the
  report paths and digest. `items: []` with `source_receipts: []` returns
  `status: "stored"` and `gateway: "skipped_no_items"` (also in the manifest)
  and sends nothing; `source-set.json` is written only with receipts. A
  report-level error (`report_required`, `report_not_final`,
  `report_malformed`, `report_bidi_control`, or `request_too_large` when the
  report alone exceeds 524288 code points or the 1 MiB request) is BLOCKED
  with no paths.
- The link pattern is `\[([^\[\]\n]*)\]\(([^()\s]+)\)`; headings and bullets
  are parsed without regexes, so rendering is linear. A test renders
  200000-character pathological lines under 2 s; the old patterns took about
  2 to 3 s at 20000 characters.
- A replay compares only `report.md` and returns the stored outputs without
  re-rendering; an output missing after an interrupted call is rendered from
  the stored bytes. Under the lock, `PrivateRecords.remove_temporaries` first
  drops this execution directory's stale `.tmp-*` entries, so a crash between
  `link()` and `unlink()` (a record with two links) recovers.
- U+202A to U+202E and U+2066 to U+2069 are refused as
  `report_bidi_control`; zero-width joiners stay allowed.
- `update-cron-prompts.sh` refuses, naming the job, when the job text before
  the marker contains `email_body.html` (host rule 8). Criterion 8 is met in
  the repository by that guard plus the prompt text; the live prompts are
  verified at W9. The never-firing head check and its README claim are gone.
- The prompt submits once even with no items, sends the email and Telegram
  only from the returned files, makes a Telegram final response exactly the
  `telegram.txt` text, and on a report-level BLOCKED fixes the report and
  calls once more; if still BLOCKED it renders the email in a `mktemp -d`
  directory, sends it and states that the report was not preserved.
- `metric_lines` and its test are deleted (W5 above).
- `tests/fixtures/ingestion-v1.schema.json` is now the Blog-data `dev` file
  `scripts/lib/ingestion/contracts/ingestion-v1.schema.json` at `ecc6c6518a`,
  copied byte for byte from a local clone, SHA-256
  `820333eee0d816d1194e6b091e0a221300d755513dda1e75b1e9302e3de65271`. The
  previous `a6d0957` file lacked `source_quotes`, its only difference. The
  pinned digest in `test_gateway_adapter.py` follows, and the schema test
  validates the real request including `source_quotes`.

### Fix round 2

The scoped security re-review of fix round 1 found the placeholder pattern
quadratic: `lorem ipsum.*` stops at a newline, so `\W*` backtracks across it
on input such as `lorem ipsum` + `!`*N + newline + `!`*M + `a`; with the old
pattern 8000 characters took 1.8 s. `(?s:.*)` now consumes to the end in one
step, and a test bounds 250000-character inputs. A `report_conflict` now
returns the paths of the report this execution stored first, and the prompt
tells the agent to send those stored files and never submit again for that
run, so no second, self-rendered email follows. The immutable
manifest no longer records a Gateway outcome; the result carries it.

### Metrics collection approval (criterion 10)

On 2026-11-06, asked how the metrics are collected, the owner chose "textfile
collector (recommended)": the plugin atomically replaces
`~/backups/metrics/hermes_research.prom`, which node-exporter's textfile
collector reads (`infra/06-observability/docker-compose.yml` binds
`${BACKUP_STATE_REPO_DIR}/metrics` to `/textfile`, `create_host_path: false`,
beside the SPEC-0192 `hyhome_backup*.prom` files). Pushgateway is not used: it
has no host port and only a protected Traefik route. The Spec (0.2.0) changes
its In Scope bullet and criterion 10 from the Pushgateway to the textfile
collector with the same label rule, and "report size bucket" to the last
report size in bytes (a numeric gauge, no label). That answer approves the
amendment, so the Spec stays `approved`.

### W5 metrics

On the worktree of `800ebf788`, before the controller's commit:

- `handle_submit_report` records metrics after every outcome through
  `_record_metrics`, which swallows any exception, so the tool result is the
  same with or without metrics. The job kind comes from the cron context
  (`_ALLOWED_JOBS`); without a cron run nothing is recorded.
- State lives in `~/.hermes/data/research-metrics/state.json` through
  `PrivateRecords` (0700 directory, 0600 file, per-key lock), so values
  survive across runs and concurrent jobs serialize.
- If `~/backups/metrics` (module constant `METRICS_DIR`, patched in tests) is
  not a directory, the textfile is skipped and the directory is not created.
  Otherwise `tempfile.mkstemp` in that directory, write, `fchmod` 0644, fsync,
  `os.replace` to `hermes_research.prom`.
- Gauges per `job_kind`: `hermes_research_last_outcome_timestamp_seconds`
  by `outcome` (`submitted`, `stored_no_items`, `gateway_error`, `blocked`,
  `conflict`, `store_failed`), `hermes_research_last_success_timestamp_seconds`
  (`submitted` or `stored_no_items`, else the kind's `first_seen`; emitted
  for all three kinds),
  `hermes_research_last_report_bytes`; counter
  `hermes_research_blocked_total` by `blocked_reason` (the BLOCKED codes plus
  `other`). The text is rendered by iterating the enums, so no other label
  value can appear.
- Alerts in `alert_rules.local.infra.yml` group `hermes_research_alerts`:
  `HermesResearchNoSuccess` (`time() - last_success > 26h`, for 30m) and
  `HermesResearchBlocked` (`blocked` or `store_failed` newer than the last
  success, for 5m), both `severity: warning`, `domain: apps`, runbook RUN-0053;
  the existing default Slack route takes them, no new receiver.
- Dashboard `Applications/hermes-research` (`hyhome-hermes-research`), listed
  in the Grafana README coverage and source tables.
- `tests/e2e_collect_harness.py` points both metrics paths into its work
  directory.

### W5 fix round

The independent review of the W5 commits (`e98dafde0`..`94530091a`) found
seven items; the controller ruled on each, and all are fixed:

- Medium: `HermesResearchNoSuccess` would fire about 30 m after install for a
  kind that had not run yet. Each kind now carries `first_seen` (set for all
  three kinds on the first recorded outcome), and the success gauge is the
  last success or else `first_seen`.
- Low: invalid nested state stopped metrics for good. Under the lock each
  kind entry is validated and only a bad one is reset; an unreadable or
  non-object file restarts the state, and a state file the records layer
  refuses (mode, links, symlink, size) is unlinked and rewritten.
- Low: the metrics lock was unbounded. `PrivateRecords.lock` takes an
  optional `timeout`; metrics use 1 s of `LOCK_NB` retries, then skip.
- Nits: the metrics directory is fsynced after `os.replace`; the promtool test
  also runs `promtool check metrics` on the plugin's own text; promtool cases
  cover a kind first seen at 1 h, a kind that never succeeds and a
  `store_failed` outcome newer than the last success; the Objective and list
  spacing above are corrected.

The three new plugin tests were not run against the reviewed commits (that
scratch-copy run was refused); the first-seen case fails there by
construction, because those commits emit 0.

### Design deviations

- Outcome mapping: `report_store_unavailable` and `record_unavailable` are
  `store_failed`; `report_conflict`, `idempotency_conflict` and
  `source_set_conflict` are `conflict`; any other BLOCKED result is `blocked`;
  any other failure is `gateway_error`. A BLOCKED result also counts under
  its `blocked_reason`, so `report_store_unavailable` appears in both.
- A day without items (`stored_no_items`) counts as a success, so
  `HermesResearchNoSuccess` does not fire on such days.
- The metrics follow the Hermes account's home: a Hermes run under another
  account has no `~/backups/metrics` and writes no textfile.
- Plugin version is 0.4.1: 0.4.0 was installed on server A at 2026-11-06
  23:41 KST, so the metrics change ships as its own release.
- Spec Normal Behavior 6 puts the email and Telegram steps before submission;
  they now follow `submit_research_report`, because the plugin renders them
  from the stored report it returns.
- Spec Normal Behavior 7 asks for an `execution_id` scratch path; the agent
  has no execution id, so the plugin's per-execution store holds the outputs
  and any agent temporary directory comes from `mktemp -d`.
- The Telegram text carries no visible digest; its origin is recorded only in
  `manifest.json` (`derived_from_sha256`). The email carries a
  `report-sha256` meta tag.
- Store-first ordering: the report is stored before the Gateway inputs are
  checked, so a Gateway-side rejection still leaves the stored report and its
  outputs.
- On a day without items the report is stored and rendered and the Gateway
  is skipped (owner decision above).
- A conflicting second report for the same execution is not BLOCKED: the
  result carries `report_conflict` and the first stored report's paths.
- The 0.3.0 bound of 524288 characters on the receipt-set JSON is replaced by
  the 4 MiB private-record limit (`source_set_too_large`, BLOCKED).
- `tests/e2e_collect_harness.py` passes a synthetic report; the owned-ingress
  E2E was not run.

Residual: Hermes formats a cron final response as Telegram MarkdownV2
(`scheduler_delivery.py`), so a URL in `telegram.txt` may render as a link
there although the plugin writes plain text.

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
| E1 | 1, 2, 4, 6 | W1 | `python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`ReportSourceContractTests`, `ToolSchemaTests`, `PrivateRecordCreateTests`); new tests fail on `6378597d9` sources; the linear-render test's patterns took 2 to 3 s at 20000 characters with the old regexes | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | 436 tests, OK under both umasks | required | - |
| E2 | 3 | W2 | same suite: `test_source_ref_digest_is_the_private_receipt_set_record`, `test_day_without_items_stores_and_renders_but_sends_nothing` | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | 436 tests, OK | required | - |
| E3 | 5 | W3 | same suite: `test_gateway_email_and_telegram_share_one_stored_digest`, `test_replay_returns_stored_outputs_without_rerendering`, `test_renderers_escape_and_flatten_markdown`, `test_pathological_lines_render_in_linear_time` | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | 436 tests, OK | required | - |
| E4 | 7, 8, 9 | W4 | same suite: `test_deploy_scripts.py` prompt, marker-count, `email_body.html` guard and rerun tests; `test_plugin_bundle.py` message tests; `bash -n` and `shellcheck` on both deploy scripts | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | 436 tests, OK; shellcheck clean; live prompts verified at W9 | required | - |
| E5 | 10 | W5 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`ResearchMetricsTests`: every outcome, persistence across runs, atomic 0644 replace, missing directory skipped, failure isolation, label enums with no URL/UUID/hex, promtool `test rules` on `tests/fixtures/hermes-research-alerts.test.yml` with the cached `prom/prometheus` image under `--network none`); new tests failed on `800ebf788` (`METRICS_DIR` missing); a mutated `HermesResearchBlocked` comparison fails the promtool cases; `promtool check rules`; `tests.validation.test_compose_baseline_gates`, `test_lab_isolation`, `test_quality_observability`, `test_p03_hermes_gate`, `test_p11_hermes_gate`; `check-p03-hermes.py`, `check-p11-hermes.py`, `e2e-cache-contract.sh`, script manifest, workflow contract, ruff; `check-document-metadata.py --mode check-changed --base-ref origin/main`, `check-document-links.py --mode alignment`, `check-document-corpus-lifecycle.py` | W5 working tree on `800ebf788` | PASS | 445 tests OK under both umasks; promtool 10 rules, cases pass; repo suites 142 (31 skipped) and 53 OK; gates PASS; ruff clean; metadata 0 violations, links 898 documents 0 failures, lifecycle 0 violations | required | - |
| E11 | 10 | W5 | live node-exporter scrape of `hermes_research.prom`, alert firing and dashboard rendering | runtime observation after the W9 install | NOT_RUN | - | required | - |
| E12 | 10 | W5 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`test_first_seen_starts_the_success_clock_of_every_kind`, `test_corrupt_state_resets_only_what_is_bad_and_continues`, `test_a_busy_metrics_lock_skips_metrics_promptly`, promtool `test rules` with the first-seen, never-succeeds and `store_failed` cases plus `check metrics`); `e2e-cache-contract.sh`; ruff; `ObservabilityDashboardContractTests`, `test_lab_isolation`, `test_p03_hermes_gate`, `test_p11_hermes_gate`; `check-p03-hermes.py`, `check-p11-hermes.py`; `check-document-metadata.py --mode check-changed --base-ref origin/main`, `check-document-links.py --mode alignment` | W5 fix round working tree above `94530091a` | PASS | 449 tests OK (448 plus the non-finite state test added after the re-review) under both umasks; e2e exit 0; ruff clean; repo tests OK; gates PASS; metadata 0 violations; links 0 failures | required | - |
| E6 | 11 | W6 | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`; `python3 scripts/validation/check-document-links.py --mode alignment`; `python3 scripts/validation/check-document-corpus-lifecycle.py` | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | metadata: 0 violations; links: 898 documents, 0 failures; lifecycle: 0 violations | required | - |
| E7 | 12 | W7 | schema-4 backup, restore test on a copy, cutover | owner approval pending | NOT_RUN | - | required | - |
| E8 | 13 | W8 | `backfill-reports` dry run shows the 16 reports excluded; apply | Blog-data capability and owner approval pending | NOT_RUN | - | required | - |
| E9 | 12, 14 | W9 | plugin install, restart, cron update, one observed run per job; rollback reading | owner approval pending | NOT_RUN | - | required | - |
| E10 | 1, 4, 6 | W1 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022`, `tests/e2e-cache-contract.sh`, ruff; `test_placeholder_check_is_linear_on_long_reports`, the conflict test and `test_prompt_sends_the_stored_report_on_a_conflict` | fix round 2 commits above `b9c016f10` | PASS | 438 tests OK under both umasks; e2e-cache-contract exit 0; ruff clean | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1, E10 | owner acceptance | @buenhyden |
| 2 | pending | E1 | owner acceptance | @buenhyden |
| 3 | pending | E2 | owner acceptance | @buenhyden |
| 4 | pending | E1, E10 | owner acceptance | @buenhyden |
| 5 | pending | E3 | owner acceptance | @buenhyden |
| 6 | pending | E1, E10 | owner acceptance | @buenhyden |
| 7 | pending | E4 | owner acceptance | @buenhyden |
| 8 | pending | E4 | owner acceptance | @buenhyden |
| 9 | pending | E4 | owner acceptance | @buenhyden |
| 10 | pending | E5, E11, E12 | owner acceptance | @buenhyden |
| 11 | pending | E6 | owner acceptance | @buenhyden |
| 12 | pending | E7, E9 | owner acceptance | @buenhyden |
| 13 | pending | E8 | owner acceptance | @buenhyden |
| 14 | pending | E9 | owner acceptance | @buenhyden |

## Review and Completion

Open. W1 to W6 have passing repository evidence; the live metrics observation
(E11) and W7 to W9 are operations and stay NOT_RUN until the owner's approved
run and direct evidence.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0060](../../../02.architecture/decisions/0060-hermes-report-source-contract.md)
