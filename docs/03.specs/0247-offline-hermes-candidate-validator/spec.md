---
title: "Offline Hermes Candidate Validator"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0247"
parent_ids:
- "REQ-0010"
- "AD-0009"
created: "2026-10-30"
---

# Offline Hermes Candidate Validator

## Overview

A local publisher operator needs a fail-closed preflight for the external Hermes
v1.0.0 candidate JSON contract. This is repository-owned input validation, not
a producer, a publishing decision, or evidence of ingestion.

## Scope

Validate a single JSON candidate and optionally compare staged Cron and idea
Markdown bytes with their declared SHA-256 digests. Synthetic fixtures only.
No Docker service, network, server transfer, Blog-data write, Cron/email change,
or automatic acceptance of source assertions. The external producer's
`README.md` and `export.py` define the candidate shape; this repository does
not adopt or modify their runtime.

## Contracts

The deterministic v1 validator accepts only the four known job-id/report-kind
pairs, a lowercase 32-hex run ID, SHA-256 hex digests, the expected top-level
and item keys/types, timezone-aware generation time, and canonical relative
source references. `state.run_completed` and `state.source_file_ready` must be
true, `email_delivery` is only `reported_sent`, `reported_failed`, or `unknown`,
and `blog_data_ingested` is always `unknown` (never a write claim).
`source_url` is an HTTP(S) URL or null; a URL with `[출처 확인 불가]` or
`[Link Unavailable]` evidence remains `unverified`, not verified. A URL
without this flag is `source_cited_unverified`; a missing URL is `unverified`.
Other status values and approval/idempotent-write fields are rejected.

Infra/GitHub candidates must have no items and exactly
`blocked_private_source` / `internal_restricted`; validation returns a
separate BLOCKED result, never ready for publication. Other kinds need items
and exactly `ready_for_review` / `unreviewed`, which is not approval. Staged
roots are optional; when supplied, missing, symlinked, escaped, or hash-mismatched
source files fail. With no roots, only digest format is checked and the output
explicitly states that source bytes were not checked.

## Acceptance Criteria

1. A synthetic strategy/news or DevOps candidate is accepted only with the
   exact v1 structural, identity, status, URL, and no-approval semantics.
2. Wrong job-kind, malformed run/hash, URL-plus-unverified mismatch, unexpected
   approval/write fields, and missing or mismatched staged source are rejected.
3. An infra candidate remains BLOCKED even when its structure is valid; no
   private item passes or outbound/writing action occurs.
4. The CLI, tests, Script Manifest, and Stage 03 identity/navigation pass their
   applicable local gates, with actual results recorded in the Task.

## Failure Conditions

Invalid JSON, invalid contract assertions, or unsafe staged file paths produce
nonzero failure. BLOCKED is distinct from invalid input and success. No
failure handler retries online, repairs source, or writes derived payloads.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-offline-hermes-candidate-validator.md)
- [Verification requirement](../../01.requirements/0010-tooling.md)
- [Verification architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)
