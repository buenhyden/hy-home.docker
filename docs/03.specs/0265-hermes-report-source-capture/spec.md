---
title: "Hermes Report Source Capture Specification"
version: "0.3.2"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0265"
parent_ids:
- "REQ-0004"
- "REQ-0005"
- "AD-0004"
- "AD-0031"
created: "2026-11-06"
---

# Hermes Report Source Capture Specification

## Overview

### Intent

The Hermes plugin sends the Gateway the canonical JSON of its collector receipts
as `source_text`. Blog-data ADR-0097 defines `source_text` as the whole original
daily report and renders it verbatim in the vault, so today a receipt-set JSON
would be published as the report. This Spec contracts how the plugin captures
the finalized report once, stores it immutably, and derives the email, the
Telegram text and the Gateway request from the same stored bytes. The decision
is [ADR-0060](../../02.architecture/decisions/0060-hermes-report-source-contract.md).

Observed state (read-only, 2026-11-06): plugin 0.3.0 builds `source_text` from
receipt rows; the Gateway is at schema 4 (image `c05e5b88`) with 16 reports
whose stored `source_text` is model-supplied fragments of 5 to 7069 characters,
none matching a cron output; the email HTML exists only in tool-call arguments;
the shared scratch file `~/.hermes/cache/scratch/email_body.html` triggers
file-mutation verifier refusals on recurring runs.

The five trust boundaries of TSK-0050 stay distinct. A collector receipt is a
same-UID audit binding, not producer authentication or independent Attestation.
The Attester verifies items by independent fetch and does not read `source_text`.
The report bytes added here prove sameness of output, not truth of content.

### Owning Requirements

The owner answered "초안 작성 (권장)" on 2026-11-06 to drafting this contract,
and "Backfill 제외 (권장)" for the 16 existing Gateway reports. Predecessor
context, not edited here: SPEC-0212 TSK-0050 (provenance, trust and export;
terminal body untouched), the historical SPEC-0204 TSK-0022 and RUN-0053.

This Spec makes concrete REQ-0004 and REQ-0005 and the Architecture Descriptions AD-0004 and AD-0031, its frontmatter `parent_ids`. The body cites no REQ-####-FR or REQ-####-NFR identifier. It also applies ADR-0060 (the report source contract) and the blog-data ADR-0097 definition of `source_text` named in the Intent.

## Scope

### In Scope

- `hermes-plugin/tools.py` (`submit_research_report`, tool contract version,
  report store, derived outputs), `plugin.yaml`, and the plugin tests.
- `deploy/research-submission-prompt.txt` and `deploy/update-cron-prompts.sh`.
- Per-execution scratch paths in the cron prompts.
- Low-cardinality metrics and alerts on the existing Prometheus, node-exporter
  textfile collector, Alertmanager and Grafana stack.
- The owner's H, D and G items, only as producer prompt or validator changes
  that add no `ingestion-v1` field (criterion 9).
- The workload README description of the new contract.
- Work units for the owner-approved schema 5 rollout and backfill exclusion
  (definition and evidence slots only).

### Non-goals

- Any `ingestion-v1`, attestation/2 or export contract change.
- A classification parser or field; body-only classification claims nothing
  and appears on no dashboard.
- Carrying a producer-asserted display name in a source item. The verified page
  title wins; coined names go in the report body.
- The sidecar `84d3f689378b` failure streak (1324) and its watermark; a
  separate defect needing its own request.
- Disabling the file-mutation verifier.
- Executing the runtime steps: Gateway backup, restore test, schema 5 cutover,
  backfill apply, plugin install, Gateway restart and cron prompt updates.
  These need owner approval and are recorded as NOT_RUN until then.
- Blog-data code, including the per-report exclusion capability; it is a
  prerequisite delivered in that repository.

## Behavior Contract

### Normal Behavior

1. **Tool contract.** `submit_research_report` takes a versioned argument that
   carries the finalized report Markdown once, beside the existing payload and
   `source_receipts`. The version is bumped in the tool schema. The model no
   longer supplies `source_text` or `source_sha256`. Contract v3 (plugin 0.4.3,
   2026-11-08) carries the report as `report_path`, the absolute path of a
   Markdown file the agent wrote, replacing the inline `report_markdown` of v2:
   the arguments are exactly `payload`, `source_receipts` and `report_path`.
   `report_path` is read only when it is normalized and absolute, its parent is
   a direct child of one of three roots (the plugin process's temporary
   directory, `HERMES_HOME/cache/scratch`, where Hermes points every agent
   shell's `TMPDIR`, and the process `TMPDIR`) named like `mktemp -d` output
   (`tmp.` plus six or more ASCII letters or digits), the parent is owned by
   the plugin user with mode 0700 and is not a link, and the file name matches
   `[A-Za-z0-9._-]{1,64}.md`; the file is opened without following links, must
   be a single-link regular file owned by that user (its mode is not checked:
   the 0700 parent already keeps others out), at most four times the Gateway code point limit in bytes, read
   once with a bound and decoded as strict UTF-8. The plugin never changes or
   removes that file. The stored `report.md` keeps the read bytes unchanged, so
   ADR-0060's meaning (`source_text` is the finalized report bytes) holds.
   The Gateway request also takes each item's `kind` from the job
   (`news`, `devops`, `business_idea`), overwriting the model's value.
   From plugin 0.4.5 (2026-11-12, contract v3 unchanged) `source_receipts` is
   optional and never decides pairing or order: each item is paired with this
   run's own collection record by `item_id`. An item without such a record
   (`source_missing`) or whose `source_url` differs from the record's final URL
   (`source_url_mismatch`) is a `source_quality` failed item, not a refusal of
   the whole submission; a day without items is decided by `items` alone.
2. **Report store.** The plugin writes the report to a per-execution file with
   mode 0600, created exclusively (no overwrite), bound to `job_id`,
   `execution_id` and the scheduled instant (name or sibling manifest). A
   second write for the same binding is refused.
3. **Gateway request.** `source_text` is the stored file decoded as UTF-8 (the
   exact bytes); `source_sha256` is the SHA-256 of those bytes. `source_ref`
   stays `hermes-source-set:<sha256 of the canonical receipt-set JSON>`. All
   other `ingestion-v1` fields are unchanged.
4. **Receipt-set record.** The canonical receipt-set JSON is stored as an
   immutable private audit record through `publisher/private_records.py`, so
   its digest equals the one in `source_ref` and Source Receipt verification
   and evidence remain.
5. **Derived outputs.** The email HTML and the Telegram text are produced from
   the stored file, so each output records the digest of the stored bytes it
   came from. The email and Telegram texts may differ in form but not in
   origin.
6. **Order.** Submission is accepted only after the report is final, that is,
   after the stored file exists and the prompt's email and Telegram steps are
   done from it.
7. **Scratch paths.** Each execution uses a unique scratch path (including
   `execution_id`) in place of `email_body.html`.

- The report file and the receipt-set record are private (0600, owner only) and
  hold no secret values; the plugin does not copy environment values into them.
- Metric labels are limited to low-cardinality values (job kind, outcome,
  reason). No URL, run, execution or report ID is a label or a metric name.
- The Gateway rollout order is fixed: backup on the schema-4 image, restore
  test on a copy, then cutover. After cutover the old image is never attached
  to a schema-5 database.

### Failure and Edge Cases

- A submission whose report argument is missing, empty, not well-formed UTF-8,
  or sent before the report is final is rejected with a stable error code and
  nothing is sent.
- If the original report cannot be obtained, the state is an explicit
  `BLOCKED`, including a report over the size limit, which is never truncated; the plugin never substitutes a receipt-set text, a digest or a
  model-written fragment as `source_text`.
- An existing report file for the binding is never overwritten; a differing
  second submission is a conflict that needs review.
- A report that exceeds the Gateway limits (524288 code points, 1 MiB whole
  request) is rejected as `request_too_large`.
- Contract v3 refuses, as report-level `BLOCKED` before anything is stored:
  `report_path_not_allowed` (path shape, ownership, mode, file type, link or
  link count), `report_unreadable` (missing or unreadable file),
  `report_too_large` (file over the byte bound), `report_not_utf8`,
  `report_too_short` (fewer than 800 characters after trimming, also on a day
  without items) and `report_missing_item` (an item's `source_url` does not
  appear verbatim in the report). Item entries with an invalid structure are
  left to the existing field validation.
- Gateway persistence is not final delivery; the email, Telegram and Gateway
  results are recorded separately.

The report is stored and hashed as bytes; the plugin applies no newline or
Unicode normalization (the Gateway applies none to `source_text`). The stored
file survives cron output retention because the plugin owns it, not Hermes.

**Observable failures.**

- `source_text` that is not the stored report bytes, or a digest that differs
  from them.
- A receipt-set record missing, overwritten or not matching `source_ref`.
- An email or Telegram text not derived from the stored file.
- A report file overwritten, world-readable, or not bound to its execution.
- A new field in the `ingestion-v1` request.
- A metric label carrying a URL or an ID.
- Backfill applied while the 16 existing reports are not excluded.
- An operation step reported PASS without direct evidence.

**Stop boundaries.**

Stop and route to the owner when the report cannot be obtained, the Gateway
size limits cannot hold the report, Blog-data cannot exclude reports before
apply, or any runtime step lacks owner approval. A runtime step that is not run
stays NOT_RUN.

## Acceptance Criteria

### Criteria

1. `submit_research_report` exposes a bumped tool contract version with one
   report argument, and its schema rejects any extra field. A plugin test shows
   the `ingestion-v1` request still validates against the unchanged schema.
2. In a test, the request `source_text` equals the stored report file bytes
   decoded as UTF-8, and `source_sha256` equals the SHA-256 of the file bytes.
3. In a test, `source_ref` equals `hermes-source-set:` plus the SHA-256 of the
   canonical receipt-set JSON, and an immutable private record with that exact
   JSON exists with mode 0600.
4. The report file is mode 0600, bound to `job_id`, `execution_id` and the
   scheduled instant, and a second write for the same binding fails without
   changing the file.
5. A test derives the email HTML and the Telegram text from the stored file and
   shows that the Gateway request, the email input and the Telegram input
   record the same digest of the stored bytes.
6. A submission before finalization, with an empty or malformed report, or
   above the size limits, is rejected with a stable error code and no network
   call; an unobtainable original yields `BLOCKED`, not a substitute text.
7. `deploy/research-submission-prompt.txt` instructs the agent to finalize the
   report and unique scratch path before submitting once, and
   `deploy/update-cron-prompts.sh` installs it idempotently; their tests pass.
   No prompt asks to disable the file-mutation verifier.
8. No cron prompt writes to the shared `email_body.html`; each uses a path
   including `execution_id`.
9. The owner's H, D and G items (2026-11-06) are producer prompt or validator
   work only and add no `ingestion-v1` field, with each sub-item checked by a
   prompt text check or a validator test, or listed in the Task as rejected:
   - H, item identity: semantic stable item IDs (not `item-1`, `D6`, `G7`);
     one event, change or article per item; dedupe by product, version,
     CVE/GHSA and final URL; the same content on an earlier date is a duplicate,
     while a real new version, event or official correction is an update;
     reports and prior ACKs are never deleted and item IDs of existing runs are
     never rewritten.
   - H, titles: only verifiable names, versions and events; a coined
     business-idea name (for example `I9Verify US` against `Home | E-Verify`)
     goes in the report body, never the item title. A Target Title field needs
     a versioned Blog-data contract first.
   - H, quotes, numbers and dates: every quote is found in the collected bytes
     and corresponds directly to its claim; numbers, dates, durations and proper
     nouns absent from the source are rejected; a relative date is never source
     time; a quote stitched from separate sentences is rejected; publish date
     and fetch date are kept apart; several changes are not merged into one
     release-note item.
   - D-01: all quotes are checked (`source_check.check_item` already flags any
     missing quote); a miss is verified against the Attester's fetched bytes,
     final URL, fetch time and normalization to tell an external page change
     from a defect, and a regression fixture is added only for a real gap.
   - D-02: business-evidence fitness is a separate producer quality gate
     (official regulation, public statistics, competitor pricing, market or
     customer evidence preferred; Wikipedia is not blocked by domain). Any
     validator policy change needs its own evaluation, distinct from
     Attestation and contract approval.
   - D-03: warn on repeated list or portal page titles; an article page title
     equal to the item title is not an error.
   - D-04: the Source Evidence signature meaning is unchanged; a publish date
     joins the signed set only with a new Blog-data Attestation contract, and
     until then is recorded only when confirmed in the source.
   - D-05: historical fetch failures (HTTP, DNS, redirect, block, dynamic
     render, timeout) are classified from logs; a failure on server B today
     does not invalidate server A's past Attestation.
   - G-01: the producer reduces same-target, same-version and same-quote
     duplicates; Gateway immutable Export and ACK never change.
   - G-02: warn on list, changelog and release-list pages unless the specific
     version or paragraph is identified.
   - G-03: no `scope`, `field`, `country`, `industry` or `stack` JSON field;
     body classification lines claim no automatic classification until
     Blog-data agrees a parser contract and tests (rule 7 of
     `30_PARA/33_Resources/README.md`).
10. Metrics (submission outcome, blocked reason, last report size, and
    report-store failures) are written by the plugin as an atomically replaced
    `hermes_research.prom` file in the existing node-exporter textfile
    collector directory (`~/backups/metrics`), with only low-cardinality labels;
    an Alertmanager rule and a Grafana panel exist; a test or lint shows no
    label carries a URL or an ID.
11. The workload README states the new `source_text` meaning, the trust
    boundaries and the rollback rule, and the document checks pass.
12. Operation work units for the Gateway schema 5 backup, restore test, cutover
    and plugin install each have a recorded result of PASS or an honest NOT_RUN;
    no step is reported complete without owner approval and direct evidence.
13. `backfill-reports --apply` is not run until Blog-data provides a per-report
    exclusion or selection capability, and a dry run shows the 16 existing
    report IDs excluded; until then the evidence is NOT_RUN.
14. The rollback is written and tested on paper: a failed cutover restores the
    schema-4 backup and reattaches `c05e5b88`; the old image is never attached
    to a schema-5 database.

### Evidence Requirements

- Criteria 1 to 6 are verified by the plugin test suite run with `python3 -m unittest discover` in the `hermes-blog-ingestion` workload, naming the schema, `source_text` and digest, `source_ref`, report-file binding, shared-digest and rejection tests (TSK-0001 rows for W1 to W3).
- Criteria 7 to 9 are verified by `test_deploy_scripts.py` prompt, marker-count and `email_body.html` guard tests and the validator tests; criterion 10 by the same suite plus a live node-exporter scrape, alert and dashboard check that stays `NOT_RUN` until observed.
- Criterion 11 is verified by the document checks that TSK-0001 row E6 records: `check-document-metadata.py` in `check-changed` mode, `check-document-links.py` in `alignment` mode and the corpus lifecycle check.
- Criteria 12 to 14 are operations rows (W7 to W9): the online backup and restore test, the `backfill-reports` dry run with the 16 excluded report IDs, the delivered-run observation, the installed-file SHA-256 comparison and the rollback reading; each stays `NOT_RUN` until the owner approves and direct evidence is recorded.
- The frontmatter owner (`@buenhyden`) judges each criterion and records the decision in the Task's Criterion Acceptance table; a failed, blocked or skipped check is reported as such and does not count as met.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-report-source-capture.md)
- [ADR-0060](../../02.architecture/decisions/0060-hermes-report-source-contract.md)
- [SPEC-0212 TSK-0050](../0212-request-baseline-and-reconciliation/tasks/tsk-0050-hermes-provenance-trust-export.md)

### Historical and Navigation

No retired, superseded or purely navigational link applies to this Spec.
