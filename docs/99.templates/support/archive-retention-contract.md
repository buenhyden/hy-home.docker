---
layer: agentic
---

# Archive and Retention Contract

## Overview

This document is the sole human owner for archive and retention. It explains
provenance tombstones, approved preservation, lifecycle review signals,
directory budgets, future partition shape, and derived archive evidence.

Exact archive metadata belongs to
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml). Exact
migration enums, thresholds, admission conditions, and planned partitions
belong to
[`document-corpus-migration-contract.yaml`](./document-corpus-migration-contract.yaml).
The metadata and lifecycle validators are their executable interpreters.

## Tombstone Profile and Provenance

The archive profile requires `status`, `artifact_id`, `artifact_type`, `parent_ids`, `archived_from`, `archived_on`, `archive_reason`, `archive_disposition`, `archived_commit`, `archived_blob`, `preservation_class`.
It permits `layer`, `supersedes`, `current_replacement`, `snapshot_path`, `content_sha256`, `snapshot_reason` only under the profile's conditions.

The repository-local archive dispositions are `superseded`, `duplicate`, `conflict`, `withdrawn`, `evidence-preserve`.
The preservation classes are `git-history`, `immutable-snapshot`.

`archived_commit` must resolve to the immutable commit used for provenance;
`archived_blob` must resolve to a blob; and `archived_commit:archived_from` must
resolve to that exact blob. The tombstone remains concise and never presents
the removed body as current truth.

`current_replacement` is required for superseded, duplicate, and conflict,
forbidden for withdrawn, and optional for evidence-preserve. When a verified
withdrawal has no replacement, the key and `## Current Replacement` section
are absent. Sentinel text must not fabricate a replacement. The direction of
`supersedes`, direct parents, identity, and status still comes from the shared
metadata owner.

## Snapshot Admission and Confidentiality

Git history is the default preservation route and forbids `snapshot_path`,
`content_sha256`, and `snapshot_reason`. An immutable snapshot is admitted only
for an evidence-preserve disposition with explicit audit, legal, or approved
evidence need. It requires all three fields and the `## Preserved Evidence`
section.

The snapshot path is content-addressed beneath
`docs/98.archive/evidence/` with suffix `.md.snapshot`. The content hash must
match both the archived blob bytes and snapshot bytes. Before admission, the
payload must pass the confidentiality scan. Secret-, credential-, token-,
private-key-, auth-file-, shell-history-, raw-log-, or diagnostic-payload
material is not committed. A blocked decision records only safe metadata and
does not retain or print the payload.

## Review Signals and Retention

The repository-local review signals are `draft_days: 30`, `active_days: 90`, `completed_execution_days: 180`.
They request human review; they never mutate status, authorize archive, or
infer a review date. Completed Specs, Plans, Tasks, audits, and other evidence
remain in their owning role while they are current inputs or durable evidence.

Age alone is not a retention decision. A superseded artifact becomes an
archive candidate only after current consumers, replacement truth, Git
provenance, confidentiality, preservation, rollback, and review evidence have
all been checked through the migration manifest.

## Directory Budgets and Future Partition Shape

The repository-local navigation budgets are `warning_at: 100` and `block_new_leaf_at: 150`.
The warning is advisory. Adding a new eligible leaf at the blocking boundary
requires a tracked, canonical, reviewed Plan that authorizes the partition;
editing an existing leaf does not count as a new addition.

Stage 01 through Stage 03 use stable domains or bounded contexts. Stage 04's
future approved shape is `docs/04.execution/plans` -> `docs/04.execution/plans/YYYY` and `docs/04.execution/tasks` -> `docs/04.execution/tasks/YYYY`.
Moves preserve artifact identity and historical evidence. Wave C owns the
actual Stage 04 partition; this Foundation contract does not move leaves.

## Derived Ledgers and Evidence Preservation

Tombstone frontmatter is the archive provenance source of truth. The archive
ledger and snapshot manifest are deterministic generated views of validated
tombstones. They are refreshed only through the canonical lifecycle generator,
compared byte-for-byte in check mode, and never hand-edited. Wave D publishes
the first generated Stage 98 outputs after existing tombstones are remediated.

Historical commands, dates, counts, decisions, verdicts, approvals, hashes,
and execution results remain semantically unchanged. Active links must not use
a tombstone as current guidance. An immutable snapshot is append-only,
content-addressed evidence, not Markdown current truth and not an input to
lifecycle inference.

## Related Documents

- [corpus migration contract](./corpus-migration-contract.md)
- [frontmatter contract](./frontmatter-contract.md)
- [lifecycle status](./lifecycle-status.md)
- [common document contract](./common-document-contract.md)
- [archive template](../templates/common/archive.template.md)
- [Stage 98 archive](../../98.archive/README.md)
- [Foundation task evidence](../../04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md)
