---
title: "Hermes Report Source Contract"
version: "0.2.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0060"
parent_ids:
- "AD-0004"
- "AD-0031"
created: "2026-11-06"
---

# ADR-0060: Hermes Report Source Contract

## Context

### Problem and Drivers

The Hermes `research-report` plugin (0.3.0) sends the Gateway an `ingestion-v1`
request whose `source_text` is the canonical JSON of the collector receipt rows
(`hermes-plugin/tools.py`, `_submit`), `source_sha256` is the SHA-256 of that
string, and `source_ref` is `hermes-source-set:<that digest>`. The receipt set
is evidence for the Attester, but it is not the daily report.

Blog-data ADR-0097 (branch `dev`, an external repository) defines the opposite
meaning. The Gateway keeps the whole original report in `reports.source_text`,
exports it unchanged in a `blog-data-report-record/1`, the receiver recomputes
its SHA-256 against the signed `source_sha256`, and the note renders it
verbatim under `## 원본 보고서` in a fence. Nothing parses it. A receipt-set
JSON therefore lands in the vault as "the daily report". The read-only Gateway
observation on 2026-11-06 (schema 4, image `c05e5b88`) found 16 stored reports
whose `source_text` is model-supplied fragments of 5 to 7069 characters; none
hash-matches a cron output file or its `## Response` section.

Host findings (read-only, 2026-11-06, Hermes Agent 0.23.0):

- The run's final response is only the Telegram digest. The email is a longer
  HTML text the agent writes and sends itself through the Google Workspace
  script; Hermes keeps it only inside tool-call arguments in the session
  transcript. The email and Telegram texts differ by design.
- `cron/output/<job>/<ts>.md` is written atomically after the agent loop, holds
  the digest plus wrapper frame, is pruned by retention, and its file name has
  no execution id.
- The `post_llm_call` hook sees the final text and the cron identity, but not
  the email.
- Every job reuses one shared scratch path, `~/.hermes/cache/scratch/email_body.html`.
  The file-mutation verifier refuses a whole-file overwrite of an existing file
  the task has not read, and appends a failure footer to the final response.
  This recurred on 2026-10-28 and 2026-11-02 to 2026-11-05.
- The agent sometimes submits before the email work is final.

The Hermes operator drafted a contract change request on 2026-11-06 (an
untracked draft, treated as data). On 2026-11-06 the owner answered "초안 작성
(권장)" to drafting this contract.

- `source_text` must be the report a reader receives, so the vault note and the
  `source_sha256` signature refer to the real original (ADR-0097).
- `ingestion-v1` and attestation/2 must not change; the Gateway rejects extra
  fields.
- Source Receipt verification and its evidence must survive.
- The email, the Telegram text and the Gateway bytes must provably derive from
  one stored byte string.
- A mutable or shared file must not be the source of truth.
- Collector receipts are same-UID audit bindings, not producer authentication or
  independent Attestation, and the Attester verifies items by independent fetch
  without reading `source_text`. These trust boundaries stay distinct.

### Decision Scope

This decision covers the meaning of `source_text`, `source_sha256` and
`source_ref` in the Hermes `research-report` plugin's `ingestion-v1` request,
and how the plugin stores the report. `ingestion-v1`, attestation/2 and the
export contract do not change. The sidecar `84d3f689378b` failure streak is out
of scope here.

## Decision

### Chosen Option

1. `source_text` is the finalized full daily report Markdown, exact UTF-8 bytes.
   `source_sha256` is the SHA-256 of those bytes. `ingestion-v1` fields,
   attestation/2 and the export contract do not change.
2. `source_ref` stays `hermes-source-set:<sha256 of the canonical receipt-set
   JSON>`. The plugin keeps that receipt-set JSON as an immutable private audit
   record through the existing `publisher/private_records.py` path, so Source
   Receipt verification and its evidence remain.
3. `submit_research_report` gets a versioned argument that carries the report
   once. This bumps the tool contract version; it adds no `ingestion-v1` field.
4. The plugin writes the report as a per-execution immutable file (mode 0600, no
   overwrite) bound to `job_id`, `execution_id` and the scheduled instant. The
   email HTML and the Telegram text are derived from that stored file.
5. Per-execution unique scratch paths replace the shared `email_body.html`. The
   file-mutation verifier stays enabled.
6. Submission before the report is finalized is rejected. If the original cannot
   be obtained the state is an explicit `BLOCKED`, never a substitute text.
7. Gateway schema 5 (Blog-data #709) rolls out in an owner-approved operation:
   backup on the current schema-4 image first, restore test on a copy, then
   cutover. `backfill-reports --apply` excludes the 16 existing reports (owner
   answer "Backfill 제외 (권장)"), which needs a per-report exclusion or
   selection capability in Blog-data before any apply.
8. Scoped follow-ups from the operator draft: no classification parser is
   added, and body-only classification claims nothing on a dashboard (its
   section 2); a verified page title wins in a source item and coined names go
   in the report body (its section 3); the sidecar `84d3f689378b` failure
   streak is a separate defect, out of scope here (its section 4).

### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. On 2026-11-06 the owner
answered "초안 작성 (권장)" to drafting this contract. The owner approved the SPEC-0265 work on 2026-11-06 ("승인"), and this ADR moved to `accepted` after #774 merged it as `proposed`; an accepted ADR is replaced only by a new ADR.
Effective from 2026-11-06.

## Alternatives

### Considered Options

1. **Receipt JSON as `source_text` (status quo).** No change. Rejected: it
   violates the ADR-0097 meaning of `source_text`, publishes a JSON array as the
   daily report, and cannot preserve the original report.
2. **A separate artifact tool or companion record keyed by `job_id` + `run_id`**
   (the operator's proposal, section 1 of the draft). Rejected: ADR-0097 makes
   `source_text` the whole original report and ties its signed digest to the
   export; a companion record would leave `source_text` meaning something else,
   add a second contract and a second receipt, and the export would still carry
   the wrong text. It also needs a Gateway/receiver change that the chosen
   option avoids.
3. **Capture the final LLM response with `post_llm_call`.** Rejected as the
   source: it sees only the Telegram digest, not the email; the text can change
   afterwards (fallback notice, media repair, `[SILENT]`); the hook is skipped
   when persistence is disabled; and a failed run may already have fired it.
4. **Wrap the Gmail send script to capture the HTML.** Rejected: it captures the
   email only, depends on an upstream skill script, and leaves Telegram
   unbound.
5. **Chosen: the plugin owns the report bytes.** The agent passes the finalized
   report once to `submit_research_report`; the plugin stores it immutably and
   derives the other outputs from the stored file.

### Trade-offs

Each rejected option carries its reason in the list above; the chosen option
keeps one stored byte string as the source of the Gateway, email and Telegram
outputs.

## Consequences

### Impacts

- The vault note shows the real report. Report size is bounded by the Gateway
  limits (524288 code points; the whole request at most 1 MiB), so a larger
  report is rejected and the run is `BLOCKED`.
- The report bytes are sensitive-heuristic scanned by the Blog-data export; a
  held export is possible and is not a producer fault.
- The model no longer supplies `source_text` or its digest, which removes the
  `source_sha_mismatch` failure class.
- The Attester is unaffected: it verifies items from the Gateway-held request
  and independent fetches, not `source_text`.
- A schema-5 database cannot be attached to the old image. A rollback after
  cutover restores the schema-4 backup and loses later records.
- The 16 existing reports keep their fragments and stay out of the vault.

### Follow-up

- Blog-data: a per-report exclusion or selection capability for
  `backfill-reports`, and its runbook correction (server A state is stale).
- Owner-approved operations for the schema 5 rollout, outside this change.

#### Compliance

SPEC-0265 states testable criteria: the same stored bytes feed the Gateway,
the email and the Telegram text; a pre-final or oversized submission is
rejected; a receipt-set record exists beside every submission.

## Traceability

### Sources

- [SPEC-0265](../../03.specs/0265-hermes-report-source-capture/spec.md)
- [Workload README](../../../infra/07-workflow/n8n/workloads/hermes-blog-ingestion/README.md)
- [SPEC-0212 TSK-0050](../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0050-hermes-provenance-trust-export.md)
- [Home and Development Host Architecture](../descriptions/0031-home-development-host.md)
