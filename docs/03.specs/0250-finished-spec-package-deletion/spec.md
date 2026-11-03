---
title: "Completed Spec Package Deletion"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0250"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-03"
---

# Completed Spec Package Deletion

## Overview

SPEC-0249 deleted Stage 98 and moved retired numbers into the Registry
`reserved_history`. The user directed that completed Spec, Plan, and Task
documents in `docs/03.specs/` be deleted too, and chose to keep every package
that still has an unfinished Task, together with its completed Tasks.

## Scope

Delete each package whose Spec, Plan, and every Task are terminal; reserve its
number; turn current links to it into plain text; drop typed references to it;
and let the checks accept the result. Packages with any non-terminal Task stay
whole. The branch-integration receipt handoff and other Stage 98 readers belong
to the PR #723 review fix, not to this Spec.

## Contracts

- A deleted package's Spec number is in the Registry Spec `reserved_history`.
- No current document links into a deleted package or names it in
  `parent_ids`, `supersedes`, or `superseded_by`; prose may name the ID for
  lineage.
- A terminal Task body stays unchanged. Link alignment excuses a missing target
  only for a link from a terminal Task at a registered Task path into a package
  whose number the checked root's Registry reserves.
- Generation 7 historical admission reads only packages still in the tree.
- SPEC-0208, SPEC-0209, and SPEC-0231 stay while current terminal Tasks are
  admitted through the lifecycle generation migration proofs they carry.

## Acceptance Criteria

1. Every fully terminal package except the three proof carriers is deleted and
   its number reserved; every package with a non-terminal Task remains.
2. No current document links into a deleted package or names one in a typed
   reference, and governance describes the deletion rule.
3. Link alignment, corpus lifecycle, and metadata checks pass without editing
   any terminal Task body.
4. The document-governance, lifecycle, gate, and CI plan suites pass locally,
   with actual results in the Task.

## Failure Conditions

An edited terminal Task body, a deleted package with a non-terminal Task, an
unreserved deleted number, or a link exemption that excuses any other missing
target fails this Spec.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-finished-spec-package-deletion.md)
- [Stage 98 archive deletion](../0249-stage98-archive-deletion/spec.md)
- [Document retention requirement](../../01.requirements/0026-document-retention-and-retirement.md)
- [Document lifecycle architecture](../../02.architecture/descriptions/0030-document-lifecycle-governance.md)
