---
title: "Summarize-and-Delete Retirement"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "architecture"
artifact_id: "ADR-0051"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# ADR-0051: Summarize-and-Delete Retirement

## Context

[ADR-0037](0037-package-disposition-wait-and-task-cancellation.md) made Stage 98
(`docs/98.archive/`) a preserved record: the last sentence of decision 1 required
whole-package preservation, and decision items 4 to 10 set Retention Catalog
assessments, history-only removal approvals, legacy capture generations,
snapshot and object verification, an ordered citation policy, frozen outbound
links, and whole-unit preservation.
SPEC-0248 then stopped every gate from validating Stage 98, and the user directed
that the archive files be deleted, that their still-current substance move into
Stage 01 and Stage 02, and that retired numbers be kept as a minimal list. The
preservation model has no records left to govern.

## Decision Drivers

- Retirement must stay traceable without a second copy of every removed body.
- Number reuse must stay impossible after the bodies are gone.
- Checks must not depend on files that no longer exist.
- The record of a removal must live in one place that current checks already
  read.

## Options

### Alternatives

- Keep the Stage 98 preservation model with its catalog and Tombstones:
  rejected; it duplicates version history, and its checks failed unrelated
  changes.
- Delete the archive and read retired lineage from pinned version history at
  check time: rejected; it makes every gate depend on history depth and recovery
  pins.
- Move the full archive metadata into the Registry: rejected; it keeps the
  preservation bookkeeping under a different name.
- Summarize, delete, and keep only retired numbers in the Registry: selected.

## Decision

1. A document that leaves an active stage is summarized into the Traceability
   of its Stage 01 or Stage 02 owner and deleted in the same change.
2. Version history is the record of the removed body. No recovery ledger,
   catalog, Tombstone, or Migration record is kept.
3. Each top-level identity space records retired numbers in the Registry
   `reserved_history`. A reserved number is never issued again, and the list
   only grows.
4. A Stage 01 gap and a Stage 03 removal are legitimate only when their number
   is reserved in the checked tree's own Registry. No archive copy or branch
   receipt substitutes.
5. Stage 98 holds no records. Its README describes the disposition scheme, and
   any other tracked file under `docs/98.archive/` fails the corpus lifecycle
   occupancy check.
6. Current documents do not link into Stage 98 or name a retired identity in a
   typed reference; prose may name it to explain lineage.

This decision supersedes ADR-0037 decision items 4 to 10 and the last sentence
of its decision 1 ("Whole-package disposition still requires approval and
preserves every member"). ADR-0037 items 1 (except that sentence), 2, and 3,
covering package waiting, Task cancellation, and terminality, are not changed
by this record.

## Consequences

- Removed bodies are recovered from version history at the revision that last
  carried them; checks no longer read them.
- Retirement needs one extra edit, the `reserved_history` entry, and checks fail
  without it.
- Lineage moves into owner Traceability, so it is read where the current rule
  lives.
- Reversal restores the archive files and readers from version history; no
  outside state changes.

### Compliance

`check-document-corpus-lifecycle.py` enforces the empty Stage 98 and the
reserved-number rule for Stage 03; the Requirement loader enforces it for Stage
01; allocation-transition checks reject dropping a reserved number.

### Follow-up

The owner accepted this record on 2026-11-03. Completed Spec packages in Stage
03 are retired under it in the next phase.

## Related Documents

- [REQ-0026 Document retention and retirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 Document lifecycle governance](../descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037 Package waiting and Task cancellation](0037-package-disposition-wait-and-task-cancellation.md)
- [SPEC-0249 Stage 98 archive deletion](../../03.specs/0249-stage98-archive-deletion/spec.md)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)
