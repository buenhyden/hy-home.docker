---
title: "Summarize-and-Delete Retirement"
version: "0.2.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "ADR-0051"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# ADR-0051: Summarize-and-Delete Retirement

## Context

### Problem and Drivers

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

- Retirement must stay traceable without a second copy of every removed body.
- Number reuse must stay impossible after the bodies are gone.
- Checks must not depend on files that no longer exist.
- The record of a removal must live in one place that current checks already
  read.

### Decision Scope

This decision covers how a document that leaves an active stage is retired: Stage 98 (`docs/98.archive/`) holds no records, and retired numbers are kept in the Registry. It affects Stage 01 and Stage 02 Traceability, Stage 03 removals and the checks that read Stage 98.

## Decision

### Chosen Option

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

### Authority and Effect

Decided by the owner, @buenhyden, who decided on 2026-11-03 to accept this record; status `accepted`, set in change #723 as the Follow-up records. Effective from 2026-11-03.

## Alternatives

### Considered Options

- Keep the Stage 98 preservation model with its catalog and Tombstones:
  rejected; it duplicates version history, and its checks failed unrelated
  changes.
- Delete the archive and read retired lineage from pinned version history at
  check time: rejected; it makes every gate depend on history depth and recovery
  pins.
- Move the full archive metadata into the Registry: rejected; it keeps the
  preservation bookkeeping under a different name.
- Summarize, delete, and keep only retired numbers in the Registry: selected.

### Trade-offs

Each rejected alternative is rejected for the reason stated in its entry above: duplication of version history, dependence on history depth and recovery pins, or preservation bookkeeping under a different name. The selected option keeps retirement traceable without a second copy of every removed body.

## Consequences

### Impacts

- Removed bodies are recovered from version history at the revision that last
  carried them; checks no longer read them.
- Retirement needs one extra edit, the `reserved_history` entry, and checks fail
  without it.
- Lineage moves into owner Traceability, so it is read where the current rule
  lives.
- Reversal restores the archive files and readers from version history; no
  outside state changes.

### Follow-up

The owner decided on 2026-11-03 to accept this record. A new ADR must enter as
`proposed`, so the status changed to `accepted` in the first change after
SPEC-0249 merged (#723), as ADR-0049 did. Completed Spec packages in Stage 03 are retired
under it in the next phase.

#### Compliance

`check-document-corpus-lifecycle.py` enforces the empty Stage 98 and the
reserved-number rule for Stage 03; the Requirement loader enforces it for Stage
01; allocation-transition checks reject dropping a reserved number.

## Traceability

### Sources

- [REQ-0026 Document retention and retirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [AD-0030 Document lifecycle governance](../descriptions/0030-document-lifecycle-governance.md)
- [ADR-0037 Package waiting and Task cancellation](0037-package-disposition-wait-and-task-cancellation.md)
- SPEC-0249 Stage 98 archive deletion (retired; version history)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)

### Supersession

This decision supersedes ADR-0037 decision items 4 to 10 and the last sentence
of its decision 1 ("Whole-package disposition still requires approval and
preserves every member"). ADR-0048 already replaced the rest of decision 1,
so decision 1 is fully replaced. ADR-0037 decisions 2 and 3, covering Task
cancellation and terminality, are not changed by this record; ADR-0048 already
replaced their completion-receipt clauses. It also supersedes the archive and
preservation wording of ADR-0048 decision 4; the readiness conditions there
stay.
