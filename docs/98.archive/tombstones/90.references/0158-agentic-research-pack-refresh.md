---
title: Agentic Research Pack Refresh Tombstone
type: archive/tombstone
layer: archive
status: completed
owner: "@buenhyden"
artifact_id: tomb-RES-0001
parent_ids: [MIG-0003]
created: 2026-08-30
updated: 2026-08-30
---

# Agentic Research Pack Refresh Tombstone

## Retired Path

`docs/90.references/research/0001-agentic-research-pack-refresh/README.md`

## Replacement

`docs/90.references/research/0002-agentic-engineering-research-pack/README.md`

## Reason

RES-0001 declared itself `superseded` by RES-0002, which is present and active.
The pack was retained after SPEC-0137 staged its deletion and then abandoned the
plan, so twenty superseded documents stayed in the active corpus and three
separate mechanisms existed only to route around them: the link gate's path
exemption, the LLM wiki generator's retiring-pack prefix, and the old-path gate
with its allowlist in a cancelled Task. Deleting the pack removes the subject
those mechanisms guarded.

The retired path is the pack's README because a recovery tuple must resolve to a
regular Git blob and a directory resolves to a tree. The README carries RES-0001,
so retiring it retires the package; its nineteen leaves are in the same commit
and need no tombstone of their own.

## Recovery Commit

`88e8e808bcaaf1116f9d3445407b159dcc760f81`

## Traceability

- [Archive index](../../README.md)
