---
title: "Foundation Tombstone"
version: "1.0.0"
type: "archive/tombstone"
status: "sealed"
owner: "@buenhyden"
updated: "2026-09-10"
layer: "archive"
artifact_id: "tomb-DATA-0067"
parent_ids:
- "SPEC-0173"
created: "2026-09-10"
---

# Foundation Tombstone

## Retired Path

`docs/90.references/data/0067-foundation/README.md`

## Replacement

`docs/98.archive/retired/90.references/data/0067-foundation/README.md`

## Reason

The only consumer this package still had was the lifecycle gate's byte
comparison against the Migration 0003 recovery blob, not a reader. The Migration
row for `DATA-0067` was repointed to the preserved path in the same change and
`data.yaml` is preserved byte for byte, so the comparison still proves the same
equality against the same bytes.

## Recovery Commit

`95f4ed225b0bb648cddda687211d92496f9b315c`

## Traceability

- [Archive index](../../README.md)
