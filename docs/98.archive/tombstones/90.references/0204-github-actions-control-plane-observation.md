---
title: "Github Actions Control Plane Observation Tombstone"
version: "1.0.0"
type: "archive/tombstone"
status: "sealed"
owner: "@buenhyden"
updated: "2026-09-09"
layer: "archive"
artifact_id: "tomb-DATA-0071"
parent_ids:
- "SPEC-0173"
created: "2026-09-09"
---

# Github Actions Control Plane Observation Tombstone

## Retired Path

`docs/90.references/data/0071-github-actions-control-plane-observation/README.md`

## Replacement

`.github/rulesets/main-protection.md`

## Reason

The payload is a 2026-07-26 public-metadata observation that recorded a failed
run and declared itself `authority: non-authoritative-observation`. Two later
authenticated protection read-backs, on 2026-09-05 and 2026-09-08, are recorded
in the replacement file with the applied settings they verified. The July
snapshot is superseded evidence, and citing it beside a current authenticated
read-back invites the older, weaker observation to be read as current state.

## Recovery Commit

`af9f27f6fb0322b69ad67ba7f879ceddd7a3cf0b`

## Traceability

- [Archive index](../../README.md)
