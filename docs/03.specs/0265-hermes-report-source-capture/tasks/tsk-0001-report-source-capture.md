---
title: "Hermes Report Source Capture Task"
version: "0.12.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-12"
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

### First run and plugin 0.4.2 (2026-11-07)

The first scheduled 0.4.0 runs (08:00 KST, all three jobs; Hermes read-only
check, controller digest check) stored, rendered and sent every report: Store,
Email, Order and Verifier PASS for all three, recipient header PASS, Telegram
FAIL for `6eabd835f969` only. No report reached the Gateway:

- `25674fbc0bf3`: its outbox record has `source_text` byte-identical to
  `report.md`, `source_sha256` and `source_ref` correct, and `source_text` is
  not JSON, but it stayed `pending` with 0 attempts on `missing_address_policy`:
  `~/.hermes/config/research-webhook-allowed-cidrs` was never created on
  server A (required since `6853286db`, 2026-11-02). The owner chose to create
  it in the W7 window after the schema 5 switch, and not to retry this record.
- `6eabd835f969` (3 of 19 items, `number_not_found`) and `8d0925bc571d` (1 of 6,
  `quote_not_found` and `number_not_found`): `resolve()` stopped at the first
  failing item and the agent got only `source_quality`.
- The `6eabd835f969` run patched its own skill to write Telegram text itself,
  and Hermes reverted it at the owner's request. Its report was already cut off
  mid-sentence in the model's tool-call argument, not by a limit.

Owner decision (2026-11-07), plugin 0.4.2: `resolve()` checks every item and
raises `SourceQuality` with each failing `item_id` and its codes. The result is
`source_quality` with `failed_items`, returned before any source set or outbox
record exists. The prompt lets the agent remove exactly those items, unedited,
and submit once more with the same report, never a third time. The stored
report is reused unchanged on that second call.

### Switch window (2026-11-07)

The owner approved the window on 2026-11-07 ("Now"), after #778 merged. All
steps ran from outside `hermes-gateway.service`, in this order:

1. W9 install, 09:29 KST: a `UMask=0077` drop-in for `hermes-gateway.service`
   and `daemon-reload`, then plugin 0.4.2 from `82b117685` via
   `update-hermes-plugin.sh` (9/9 files match, doctor OK, backup
   `~/.hermes/plugins/.research-report-backup-20261107T002914Z`), a restart,
   and `update-cron-prompts.sh` (3 jobs updated, backup
   `~/.hermes/cron/jobs.json.pre-prompt-20261107T002931Z`, marker and rule
   checks pass). After the restart: `UMask=0077`, `__pycache__` 0700.
2. W7 backup, 09:31 KST, with the running `c05e5b88` image:
   `/data/backup-pre-schema5-20261107T003121Z.sqlite3`, integrity ok, 16
   reports, 121 candidates.
3. W7 restore test on that backup: copied to a private volume (no network,
   uid 10001) and opened with the new image. `user_version` 4→5; reports,
   candidates, attestations, exports, export files and request keys 16, 121,
   16, 121, 63 and 16 before and after; item exports acknowledged 53, held
   `SOURCE_UNVERIFIED` 60 and `KIND_MISMATCH` 8; export hash `221634a8…`
   unchanged; 0 foreign-key violations; integrity ok. Same result as the
   2026-11-06 copy.
4. The Compose pin moved to `bcefdc0c0bc4fced9c47d0624d6ca815ddbcaf48` first
   (#779, merged `624a4db8a`), so the running image never differs from main.
   W7 switch, 09:52 KST: `docker compose --profile blog-ingestion up -d
   --no-deps blog-ingestion` from main. Image ID `sha256:8ff847c9…`, healthy,
   log `listening` and `export_enabled: true`. The live DB shows
   `user_version` 5 and the same counts, states and hash as the backup.
   `SOURCE_NOT_REPORT` 0. `n8n-worker` reaches the Gateway (401 without a
   token).
5. Producer allowlist `~/.hermes/config/research-webhook-allowed-cidrs` (dir
   0700, file 0600, the webhook host's /32). The plugin's loader reads and
   parses it.
6. W8 dry run with the 16 exclusions: 0 targets, and 0 on rerun. No `--apply`,
   because no 0.4.x report reached the Gateway under schema 4. The 16 reports'
   `source_ref` is 0.2.5 model free text, so the exclusion list stays their
   only guard.

Blog-data, which runs on another server, gets the return information as a self-contained file the owner delivers.
The restore-test volumes are removed by the owner. The first delivered run
(2026-11-08 08:00 KST) completes E9.

### First post-switch runs and plugin 0.4.3 (2026-11-08)

The first scheduled runs after the switch, on plugin 0.4.2, passed
`report_markdown` that was not the finalized report, and `_report_error`,
which refuses only empty, placeholder, malformed, bidirectional-control and
oversize text, accepted each:

- a 160-byte, two-line stub, which the Gateway accepted as the daily report;
- a one-line pointer to a file path instead of the report;
- a long report cut off mid-way inside the tool-call argument.

On the devops run all six items also carried kind `news`, so the Gateway held
every item as `KIND_MISMATCH`.

Owner decisions (2026-11-08): Gateway sends were stopped by renaming the
producer address allowlist; plugin 0.4.3 reads the report from a file and
checks it ("Report from a file + checks"). Controller ruling (2026-11-08): the
item kind is set from the job like the identity fields.

Plugin 0.4.3, contract v3 (`SUBMIT_CONTRACT_VERSION = 3`):

- `submit_research_report` takes exactly `payload`, `source_receipts` and
  `report_path`; `report_markdown` is now `invalid_submission_fields`.
- `report_path` rules (Spec Normal Behavior 1): a normalized absolute path
  whose parent is a direct `tmp.XXXXXX` child of `tempfile.gettempdir()`,
  `HERMES_HOME/cache/scratch` (Hermes exports it as `TMPDIR` to every agent
  shell through `apply_scratch_tmp_env`) or the process `TMPDIR`, read at call
  time, owned by the plugin user with mode 0700, opened with
  `O_NOFOLLOW`; a `.md` file name; the file opened through the directory
  descriptor with `O_NOFOLLOW` and `O_NONBLOCK`, a single-link regular file
  owned by that user (no file-mode check inside the 0700 parent, so a umask
  0002 file is accepted), at most 2 MiB, read
  once with a bound. Codes: `report_path_not_allowed`, `report_unreadable`,
  `report_too_large`, `report_not_utf8`. The file is never changed.
- After the unchanged `_report_error` checks: `report_too_short` (fewer than
  800 characters after trimming, also with no items) and
  `report_missing_item` (an item's `source_url` is not in the report text).
  Both are report-level `BLOCKED` before the store, so the agent fixes the
  file and calls once more.
- `_gateway` sets each item's `kind` from the job (`news`, `devops`,
  `business_idea`); `kind` is optional in the tool schema and still accepted.
- The metrics `bytes` value is the size of the file read; store-first order,
  replay, the `source_quality` resubmission (same `report_path`, file
  unchanged) and every other behavior are unchanged.
- The prompt asks for the report as a file in a new `mktemp -d` directory and
  passes `report_path`; the e2e harness writes its synthetic report the same
  way.

### Retry and redrive (plugin 0.4.4, 2026-11-11)

Outbox records ended `uncertain` when the plugin sent but got no confirmed
answer (client timeout, connection reset, 5xx), and nothing resent them: the
2026-11-10 devops report was lost until an operator resent it (E9). Causes
seen: n8n took 10.7 s to accept the first request of the morning, Traefik
answered 499 after 14.9 s while n8n never read the body, and the n8n JS runner
cold start. Owner decision (2026-11-11): "Retry + later redrive".

Idempotency evidence (2026-11-11, live Gateway): POSTing the same request
bytes with the same idempotency key again returned HTTP 200 with
`duplicate: true` and the same report id, and the report and candidate counts
did not change. A resend therefore never creates a second report.

Plugin 0.4.4, contract v3 unchanged (no new argument):

- Retry inside the call: a DNS rejection, a `timeout`, `network`, `tls`,
  `invalid_response` or `transport_protocol` transport failure, and an answer
  outside 200/201 other than 409, 401/403 and 400/404/413/415/422 are sent
  again with the same bytes while attempts stay at most 3 and the 60 s budget
  remains, with the existing backoff. Each attempt is written to the record
  first. 409 stays `conflict` and the listed 4xx stay `failed`; neither is
  resent. A 401/403 returns `credential_rejected` and leaves the record
  `uncertain` without a resend in the call (owner ruling 2026-11-11: a rejected
  credential says nothing about the report, so a later redrive may deliver it
  once the credential is fixed). A 200/201 answer with an invalid receipt stays `uncertain` and is
  not resent in the call. Other transport failures (`address_not_allowed`,
  local request or credential refusals) are not resent. 200 is treated like
  201.
- Redrive: after the current result is fixed, and only when the current send
  did not end `delivery_uncertain` or `credential_rejected` (independent review:
  resending then would only spend earlier records' attempts), the same call
  resends at most 2
  earlier outbox records of the same job that are `uncertain` (or `sending`
  left by a crash, or `pending` with at least one attempt), have fewer than 5
  attempts and were created within 7 days, one attempt each with the stored
  bytes and key, inside a separate 30 s budget; no attempt starts with less than 10 s left,
  and redrive stops after an attempt ends `delivery_uncertain` or
  `credential_rejected` (scoped re-review). Before a record is resent it must
  pass the gates of a fresh send (`_validate`, the request size limit,
  `collected_at` ≤ `generated_at` ≤ now) and match what the plugin stored for
  that run: `source_text` equal to its `report.md`, `source_sha256` and
  `source_ref` equal to that `report.md` and `source-set.json`, and every item
  still passing `check_item` against its stored page text. A record written by
  anything else, or changed after it was written, is skipped (automated
  security review of the redrive path). The creation time is the
  stored request's `generated_at`, which the plugin sets when it prepares the
  record; no new record field is added and file times are not used. Each
  record is redriven under its `store.lock(key)` with a lock wait of at most
  1 s; a busy lock is skipped. 200/201 with a valid receipt makes the record
  `persisted` with the receipt stored as `_send` stores it; 409 and the
  listed 4xx make it `conflict` or `failed` (401/403 leave it `uncertain`); anything else leaves it
  `uncertain` with the attempt counted. Only records with exactly the
  current-schema fields are considered; legacy records are skipped.
- The current call's result fields never change; when at least one record
  was resent the result gains `redrive` with only `attempted`, `persisted`
  and `still_uncertain` counts. Metrics are unchanged.
- The outbox record check now accepts up to 5 attempts, so a redriven record
  stays readable by its own run's replay.

### Receipt pairing by item_id (plugin 0.4.5, 2026-11-12)

On 2026-11-12, on plugin 0.4.4, one receipt slip lost each of two daily
reports. News submitted 25 items; one carried a receipt id that matched none
of the run's collected receipts (its page had been collected, under a
different receipt id), and `resolve()` refused the whole submission with
`source_mismatch`. Business ideas got `source_quality`, dropped the failed
item but not its receipt, and the resubmission returned
`source_receipts_required` because the lists no longer had equal length.
Owner decision (2026-11-12): "Yes, pair by item_id".

Plugin 0.4.5, contract v3 unchanged (`source_receipts` stays an accepted
argument, now optional in the tool schema):

- `source_collection.resolve()` pairs each item with this run's own
  collection record by `item_id`. The model's `source_receipts` no longer
  decide pairing or order; omitted, shorter, longer or misordered lists give
  the same rows.
- Item-level problems are `source_quality` failed items: no collected record
  for that `item_id` in this run is `source_missing`, an item `source_url`
  other than the record's final URL is `source_url_mismatch`, and the
  `check_item` codes are unchanged. Duplicate `item_id` (`source_identity`),
  a record failing its integrity check (`invalid_record`), a record whose
  index entry does not match (`source_mismatch`), `source_too_large` and
  `source_time` stay hard errors.
- The no-item day is decided by `items == []` alone. The outbox record's
  `input_sha256` is computed from the items and the plugin-derived receipt ids
  in item order, so replaying the same items is idempotent whatever receipts
  the model sends; the stored source set keeps its 0.4.4 fields. The 0.4.4
  redrive gate is unchanged.
- The cron prompt says the tool pairs by `item_id`, that `source_receipts`
  may be sent as collected or omitted, and that `source_missing` and
  `source_url_mismatch` are failed items to drop like any other.

### Owner acceptance of criteria 12 to 14 (2026-11-11)

The owner accepted criteria 12, 13 and 14 on 2026-11-11 ("Accept SPEC-0265
criteria 12–14 수용"). The operations each carry a recorded result: backup,
restore test and switch PASS (E7), backfill dry run with no `--apply` PASS
(E8), and installs PASS (E14, E16). The rollback is written and tested on a
copy (E18). The delivered-run observation E9 is FAIL, because devops has
delivered nothing on 0.4.3; it is recorded here as an open delivery issue
and not as a pass. Because a required observation is open, criterion 12 is
recorded as pending with the owner's decision noted; it becomes accepted when
a later delivered devops run resolves E9. E17 now resolves E11 (same Check,
W5). Criteria 1 to 11 stay pending.

### First scheduled devops delivery (2026-11-12)

On plugin 0.4.4 the 2026-11-12 devops run delivered on its scheduled run (report
`b1c520ab…`, first send attempt 201), so every job has now delivered and E20
resolves E9; criterion 12 is recorded as accepted per the owner's 2026-11-11
decision. The same morning news and business ideas stored complete reports but
sent nothing: news was refused with `source_mismatch` because 1 of 25 items
carried a receipt id matching none of the run's collected receipts, and
business ideas dropped a `source_quality` item without its receipt, so its one
resubmission returned `source_receipts_required`. Both are agent slips that a
single receipt error turns into a lost report; pairing receipts by `item_id`
in the plugin is proposed to the owner as a follow-up.

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
- `source_quality` allows one resubmission with the failed items removed
  (0.4.2); every other result with report paths still ends submission.
- The metrics change shipped as 0.4.1 (0.4.2 adds `failed_items`): 0.4.0 was installed on server A at 2026-11-06
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

Review fixes for 0.4.3 (independent security review 2026-11-08: no path-read
defect; CHANGES_REQUESTED):

- The prompt now has the agent update the report file after collection so it
  names each kept item's final `source_url`. Without that, a redirected URL
  made `report_missing_item` refuse the report.
- The Spec, this Task and the README name all three allowed roots
  (`tempfile.gettempdir()`, `HERMES_HOME/cache/scratch` and the process
  `TMPDIR`) and why: Hermes exports `TMPDIR` to the scratch directory for
  agent shells.
- The file-mode check is removed. Inside an owner-only 0700 directory with
  one link it protected nothing, and a umask 0002 write would have refused
  every report. A test now covers a short read.

### Plugin 0.4.3 install and E11 observation (2026-11-08)

A read-only check at 17:30 KST found plugin 0.4.3 installed on server A (this
host) but not recorded here. The installed `plugin.yaml`, `tools.py`,
`webhook_transport.py` and `__init__.py` equal `main` `c0bcfb511` by SHA-256
(contract v3, `SUBMIT_CONTRACT_VERSION = 3`). File times give the order:
`tools.py` written 09:53:56 KST, `hermes-gateway.service` started 09:54:07
(`UMask=0077`), and the address allowlist renamed back at 09:54:40 (its ctime),
so Gateway sends are open again on 0.4.3. `__pycache__` is 0700 with 0600
files; the plugin loader reads the allowlist as one valid CIDR. The news,
devops and business-ideas cron prompts reference `report_path` and no longer
`report_markdown`. No research run has happened since: the metrics textfile was
last written 08:12 KST by the 0.4.2 runs above, and the next scheduled run is
2026-11-09 08:00 KST. E9 stays NOT_RUN until that run is observed; the owner
chose to wait for it instead of a manual run.

E11 in part: Prometheus scrapes `hermes_research_*` from `node-exporter:9100`
for all three job kinds; `HermesResearchNoSuccess` and
`HermesResearchBlocked` are loaded and inactive, which is right because the
devops `blocked` outcome precedes a later `submitted` one; Grafana serves
"Hermes Research Reports" (`hyhome-hermes-research`). The alert unit test
`tests/fixtures/hermes-research-alerts.test.yml` passed (`SUCCESS`) with the
running Prometheus image's promtool 3.15.1 against
`alert_rules.local.infra.yml`, whose SHA-256 equals the deployed file
(`869383fa…`), in a network-less one-off container. A live alert firing and a
rendered dashboard view were not observed, so E11 stays NOT_RUN.

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
| E13 | 9 | W4 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`test_quality_failures_name_every_failing_item`, `test_source_quality_lists_failed_items_and_allows_one_resubmission`, `test_resubmission_with_surviving_items_sends_them_once`, prompt exception sentence); `e2e-cache-contract.sh`; ruff; independent review APPROVED, its Minor items fixed | plugin 0.4.2 working tree on `688f94f7f` | PASS | 452 tests OK under both umasks; e2e exit 0; ruff clean | required | - |
| E15 | 1, 6 | W1 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`ReportPathTests`: stored byte-identical file, refused paths, secret-like paths, unsafe directory or file, foreign owner, missing, non-UTF-8 and oversize files, bounded read, `report_too_short`, `report_missing_item`, invalid item structure, no-item day, item kind from the job, metrics bytes; adapted `source_quality` resubmission tests; prompt v3 tests); new tests fail on the 0.4.2 sources; `e2e-cache-contract.sh`; ruff check and format; `check-document-metadata.py --mode check-changed --base-ref origin/main`; `check-document-links.py --mode alignment` | plugin 0.4.3 working tree on `6d942a7eb` | PASS | 469 tests OK under both umasks (105 failures and errors on 0.4.2); e2e exit 0; ruff clean; independent security review: no path-read defect, CHANGES_REQUESTED on the redirect-URL prompt gap and the doc boundary, both fixed with the short-read and file-mode tests | required | - |
| E6 | 11 | W6 | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref origin/main`; `python3 scripts/validation/check-document-links.py --mode alignment`; `python3 scripts/validation/check-document-corpus-lifecycle.py` | fix round 1 working tree, committed as `49f439c37`..`b9c016f10` | PASS | metadata: 0 violations; links: 898 documents, 0 failures; lifecycle: 0 violations | required | - |
| E7 | 12 | W7 | online backup with `c05e5b88`, restore test of that backup on a private copy with the new image (`user_version`, row counts, export states and hash, FK, integrity), Compose pin #779 then `docker compose --profile blog-ingestion up -d --no-deps blog-ingestion`, startup log and live DB check | switch window 2026-11-07 09:31-09:52 KST, image `bcefdc0c0b` `sha256:8ff847c9…` | PASS | backup integrity ok 16/121; copy and live DB `user_version` 5, counts, states and hash `221634a8…` unchanged, FK 0; `listening`, `export_enabled: true` | required | - |
| E8 | 13 | W8 | `backfill-reports --config /run/config.json` with the 16 `--exclude-report-id`, dry run and rerun; apply only for 0.4.x reports received under schema 4 | live DB after the switch, 2026-11-07 | PASS | 0 targets, rerun 0; apply not needed (no 0.4.x report reached schema 4); `SOURCE_NOT_REPORT` 0 | required | - |
| E9 | 12 | W9 | one observed delivered run per job (stored report, `sha256(report.md)` = outbox = Gateway hash, attestation, report and item export states, item kind) | scheduled runs 2026-11-09 to 2026-11-11 on plugin 0.4.3, read-only on server A | FAIL | news delivered 11-09 and 11-11, business ideas 11-09, 11-10 and 11-11: 5 reports, all hashes equal, `source_kind` `report`, no `KIND_MISMATCH`, all acknowledged by server B; devops delivered none (11-09 n8n `TimeoutExecutionCancelledError` on runner cold start, 11-10 `uncertain` and absent from the Gateway, 11-11 Hermes run failure); news 11-10 stopped by the Hermes loop guard before submitting; email and Telegram not checked from sent messages | required | - |
| E19 | 1, 6 | W1 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`RetryAndRedriveTests`: current 401/403 kept `uncertain` without redrive, unconfirmed current send skips redrive, redrive eligibility of `pending`, `sending` and an unparseable `generated_at`, timeout then 201, 502 then 201, 200 duplicate, 409 and 422 not resent, exhausted budget, redrive persisted with the receipt, ineligible records untouched, at most 2, current result unchanged, redrive failure, budget, busy lock; adapted `DeliveryBudgetTests` and the restart test); new tests fail on `602656a52`; `e2e-cache-contract.sh`; ruff check and format; `check-document-metadata.py --mode check-changed --base-ref origin/main`; `check-document-links.py --mode alignment` | plugin 0.4.4 working tree on `602656a52` after the independent review fixes | PASS | 497 tests OK under both umasks (15 failures and errors in this file on `602656a52` sources); e2e exit 0; ruff clean; metadata 2 selected, 0 violations; links 914 documents, 0 failures | required | - |
| E20 | 12 | W9 | one observed delivered run per job (stored report, `sha256(report.md)` = outbox = Gateway hash, attestation, report and item export states, item kind) | scheduled runs 2026-11-09 to 2026-11-12, plugins 0.4.3 and 0.4.4, read-only on server A and the Gateway | PASS | every job has an observed delivered scheduled run: news 2026-11-09 (`a3504a6f…`) and 2026-11-11 (`167e2022…`); business ideas 2026-11-09 (`d8edd7f5…`), 2026-11-10 (`20a105c8…`) and 2026-11-11 (`d7c7bce4…`); devops 2026-11-12 (`b1c520ab…`, 7127 characters, 8 `devops` items `ready`, first send attempt 201). In each, `sha256(report.md)` = outbox = Gateway stored hash, `source_kind` `report`, attested, item kinds correct. Undelivered runs (2026-11-12 news `source_mismatch`, business `source_receipts_required`) are producer-side receipt errors recorded in the Task | required | E9 |
| E21 | 1, 6 | W1 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022` (`SourceCollectionTests`: receipts omitted, misordered, shorter, longer or with one wrong id give the same rows, uncollected item `source_missing`, moved URL `source_url_mismatch`, duplicate `item_id` `source_identity`, tampered record `invalid_record`, other run `source_missing`; `ReceiptPairingTests` with real collection: one wrong receipt of 5 delivers all 5, resubmission keeping the dropped item's receipt persists, uncollected item is a failed item, no-item day with stray receipts stores and skips the Gateway, replay with different receipts keeps `input_sha256` and returns `already_persisted`; `test_receipts_never_reach_pairing`; prompt tests); new tests fail on `b885f0e54` sources; `e2e-cache-contract.sh`; ruff check and format; `check-document-metadata.py --mode check-changed --base-ref origin/main`; `check-document-links.py --mode alignment` | plugin 0.4.5 working tree on `b885f0e54` | PASS | 504 tests OK under both umasks; e2e exit 0; ruff clean; metadata 3 selected, 0 violations; links 905 documents, 0 failures | required | - |
| E14 | 12, 14 | W9 | `update-hermes-plugin.sh` (digest match, doctor), restart, `update-cron-prompts.sh` and prompt checks, `UMask` and `__pycache__` mode, address allowlist parsed by the plugin loader | plugin 0.4.2 from `82b117685`, 2026-11-07 09:29 KST | PASS | 9/9 MATCH, doctor OK, 3 prompts OK, `UMask=0077`, `__pycache__` 0700, allowlist parses | required | - |
| E10 | 1, 4, 6 | W1 | `/usr/bin/python3 -m unittest discover -s infra/07-workflow/n8n/workloads/hermes-blog-ingestion/tests -p 'test_*.py'` under `umask 0002` and `umask 022`, `tests/e2e-cache-contract.sh`, ruff; `test_placeholder_check_is_linear_on_long_reports`, the conflict test and `test_prompt_sends_the_stored_report_on_a_conflict` | fix round 2 commits above `b9c016f10` | PASS | 438 tests OK under both umasks; e2e-cache-contract exit 0; ruff clean | required | - |
| E16 | 12, 14 | W9 | installed files against source by SHA-256, gateway start and `UMask`, `__pycache__` modes, allowlist parsed by the plugin loader, cron prompts reference `report_path` | plugin 0.4.3 from `main` `c0bcfb511`, read-only, 2026-11-08 17:30 KST | PASS | 4/4 files match; started 09:54:07 KST, `UMask=0077`; 0700/0600; 1 valid CIDR; 3 prompts on `report_path`, none on `report_markdown` | required | - |
| E17 | 10 | W5 | live node-exporter scrape of `hermes_research.prom`, alert firing and dashboard rendering | live scrape of `hermes_research_*`, loaded alert rules, provisioned dashboard, promtool alert unit test on the deployed rule hash; Prometheus and Grafana on server A, 2026-11-08 | PASS | 3 series from `node-exporter:9100`; 2 rules inactive; dashboard `hyhome-hermes-research`; promtool 3.15.1 `SUCCESS`, rule SHA-256 `869383fa…` equal; no live firing observed (E11 stays NOT_RUN) | required | E11 |
| E18 | 14 | W9 | rollback reading: workload README and runbook 0053 state that a failed cutover restores the pre-switch schema 4 backup with `c05e5b88` and never attaches `c05e5b88` to a schema 5 DB; the restore test showed `c05e5b88` refusing the migrated copy | #779 documents, restore test 2026-11-06 and the 2026-11-07 backup `/data/backup-pre-schema5-20261107T003121Z.sqlite3` | PASS | documented in both; `UNSUPPORTED_SCHEMA` from `c05e5b88` on the schema 5 copy; backup integrity ok | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1, E10, E19, E21 | owner acceptance | @buenhyden |
| 2 | pending | E1 | owner acceptance | @buenhyden |
| 3 | pending | E2 | owner acceptance | @buenhyden |
| 4 | pending | E1, E10 | owner acceptance | @buenhyden |
| 5 | pending | E3 | owner acceptance | @buenhyden |
| 6 | pending | E1, E10, E19, E21 | owner acceptance | @buenhyden |
| 7 | pending | E4 | owner acceptance | @buenhyden |
| 8 | pending | E4 | owner acceptance | @buenhyden |
| 9 | pending | E4 | owner acceptance | @buenhyden |
| 10 | pending | E5, E11, E12 | owner acceptance | @buenhyden |
| 11 | pending | E6 | owner acceptance | @buenhyden |
| 12 | accepted | E7, E9, E14, E16, E20 | owner accepted 2026-11-11; E20 (2026-11-12 devops delivered on its scheduled run) resolves E9 | @buenhyden |
| 13 | accepted | E8 | owner accepted 2026-11-11 | @buenhyden |
| 14 | accepted | E18 | owner accepted 2026-11-11 | @buenhyden |

## Review and Completion

Open. W1 to W6 have passing repository evidence; the live metrics observation
(E11) and W7 to W9 are operations and stay NOT_RUN until the owner's approved
run and direct evidence.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [ADR-0060](../../../02.architecture/decisions/0060-hermes-report-source-contract.md)
