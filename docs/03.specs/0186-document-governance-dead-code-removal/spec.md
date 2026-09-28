---
title: "Document Governance Dead Code Removal Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0186"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0030"
created: "2026-09-28"
---

# Document Governance Dead Code Removal Specification

## Overview

SPEC-0184 deferred three pieces of validator code that no current input
reaches, or that exist only to bridge a base older than today's `main`. This
package removes each one after proving it is unreachable, so the validators
carry only rules that still apply.

## Boundaries and Inputs

In scope:

1. `load_artifact_contract` in
   `scripts/lib/agent_governance/agent_governance_contract.py`. It is a
   "compatibility loader for explicitly supplied legacy transition fixtures",
   and nothing tracked calls it.
2. The Stage 98 README base read in
   `scripts/lib/document_governance/archive.py`. It is marked `ponytail:`
   for removal "once no supported base predates SPEC-0179 Archive 3.0.0".
   `main` at `7d46c4e56` and every later base carry
   `docs/98.archive/retention-catalog.md`.
3. The reviewed Foundation evidence wave in
   `scripts/lib/document_governance/lifecycle/contract.py`:
   `REVIEWED_EVIDENCE_WAVES`, `FOUNDATION_EVIDENCE_OWNER_PATHS`, the
   `ACTIVE_CONSUMER_EXCLUSIONS` rows, and the `docs/04.execution/**` consumer
   glob. They name Stage 04 paths that no longer exist.

Out of scope:

- Any change to a validator's accepted inputs or findings for current
  documents.
- Frozen Stage 98 bodies and migration manifests. They are read, not edited.
- Language migration (SPEC-0184 P2) and README content.

## Behavior Contract

1. Every removed symbol has zero tracked callers, shown by `git grep` over the
   whole repository, including tests and `.agents/`.
2. A removal that some tracked migration manifest, archive record, or test
   fixture still reaches is not made. The Task records it as kept, with the
   caller that reaches it.
3. Validator output on the current tree is unchanged: the same findings and
   the same counts from every changed-profile member.
4. Tests that exist only to exercise removed code are removed with it. No
   test that guards current behavior is deleted.

## Technical Approach

For each candidate, work in this order:

1. Search for callers and inputs. For item 3, also check whether any tracked
   migration manifest declares the `foundation` wave and whether any path in
   `FOUNDATION_EVIDENCE_OWNER_PATHS` resolves at `HEAD`.
2. If nothing reaches the code, delete it together with its dedicated tests,
   one candidate per commit.
3. Run the affected suites and the changed-profile members. Compare the
   validator summaries with the pre-change summaries recorded in the Task.

## Interfaces and Data

No CLI, Registry, schema, or document contract changes. Public functions that
are removed are listed in the Task with the `git grep` evidence.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| A caller exists outside `scripts/` | Behavior rule 1 searches the whole repository |
| A base older than the catalog record is still validated | Item 2 is removed only after confirming `origin/main` and the local `main` both carry `docs/98.archive/retention-catalog.md` |
| A frozen migration manifest still needs the Foundation wave | Behavior rule 2 keeps the code and records why |
| Output drifts unnoticed | Behavior rule 3 compares validator summaries before and after |

## Acceptance Contract

1. `load_artifact_contract` is removed, or the Task records the tracked caller
   that keeps it.
2. The Stage 98 README base read is removed, or the Task records the base that
   still needs it.
3. The Foundation evidence wave and its Stage 04 path constants are removed,
   or the Task records the manifest or fixture that reaches them.
4. Changed-profile members, except the blocked `check-conftest-policy.sh`,
   return 0, and their summaries match the pre-change run.
5. `tests/lib` and `tests/validation` pass.

## Traceability

- REQ-0024: canonical agent governance contract loading.
- REQ-0026: document retention and retirement validation.
- AD-0030: document lifecycle governance.
- SPEC-0184 Task, Deferred Items: the source of this package.

## Open Questions

None. Each candidate's outcome is decided by the evidence rules above.

## Operational Impact

None. The change touches validator code only. No service, Compose file, or
runtime surface changes.
