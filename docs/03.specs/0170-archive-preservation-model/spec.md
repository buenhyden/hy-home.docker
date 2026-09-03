---
title: Archive Preservation Model Specification
version: 1.0.0
type: sdlc/spec
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0170
parent_ids: [REQ-0026, AD-0030, ADR-0030]
created: 2026-09-04
updated: 2026-09-04
---

# Archive Preservation Model Specification

## Overview

Retirement currently deletes. `ADR-0030` decided that a Tombstone is a pointer
and Git history is the recovery mechanism, so `docs/98.archive/` holds 104
pointers and no retained content. The workspace now requires the opposite
default: completed, aged, and withdrawn documents are all kept, each under its
own management rule, and none of them sits in an active stage directory.

Two populations violate that today. Twenty-one completed Stage 03 packages and
three `superseded` documents remain in `docs/03.specs`, `docs/02.architecture`,
and `docs/90.references` alongside live work. And 104 retired documents exist
only inside Git objects, so half the retired set is preserved as a file and
half is not.

The declaration for a retained archive already exists and has never been used.
The `migration` profile registers `archive_disposition`, `archive_reason`,
`archived_from`, `archived_commit`, `archived_at`, `archived_blob`, and
`preservation_class` as optional frontmatter, and `common` registers
`archive_source_prefixes`. No document carries any of them. This package makes
the retained archive real rather than declared.

## Boundaries and Inputs

In scope: `docs/98.archive/`, the Stage 99 registry, the retention rules in
`REQ-0026`, `AD-0030`, `ADR-0030`, and `documentation-protocol.md`, and the
registered checks that judge placement.

Out of scope: what any preserved document says. A record is moved, never
rewritten; its frontmatter and body stay exactly as they were when the document
was live.

Inputs: the 104 Tombstones and their `Retired Path` and `Recovery Commit`
fields, the lifecycle status of every tracked document, and the Stage 03
package membership already derived by `spec_packages.py`.

## Behavior Contract

1. A document whose status is terminal is preserved under
   `docs/98.archive/<disposition>/` followed by its path with the leading
   `docs/` removed.
   The mapping is total and deterministic, so no new pointer field is needed
   and the Tombstone contract stays frozen.
2. `<disposition>` is one of `completed`, `superseded`, or `retired`, taken
   from the document's own lifecycle status. Age is never an input, which
   `REQ-0026-FR-0001` already requires.
3. A completed Spec Package is preserved whole: `spec.md`, `plan.md`, and every
   Task move together. A superseded or retired document is preserved alone.
4. A preserved record is not an authoring target. Its section and frontmatter
   contracts were satisfied while it was live, and re-judging it against a
   later contract would force edits to history.
5. Stage directories `01`, `02`, `03`, `05`, and `90` hold no document with a
   terminal status.

## Technical Approach

The registry gains one path token and three profiles. `{archived_subpath}`
accepts the historical filenames the archive must hold — `README`, `01.setup`,
three-digit package numbers — which current authoring patterns forbid; no live
pattern uses it. The three profiles register the disposition subtrees with
`frontmatter_policy: unmanaged`, `identity_relation: none`, and no section
contract, which is what "not an authoring target" means mechanically. The
registry rule reserving `unmanaged` for the `unsupported` fallback is widened
to admit registered preservation profiles.

Supersession resolution reads the archive, so `supersedes: ADR-0027` still
resolves once `ADR-0027` is preserved. Without that, moving a superseded
document raises `supersession-dangling` from the document that replaced it.

The 104 retired documents are restored from the `Recovery Commit` their own
Tombstone names. Restoration is mechanical and verifiable: the recovered blob
must exist at that commit under the recorded `Retired Path`.

## Interfaces and Data

- `docs/99.templates/registry.json` — the token, the three profiles, and the
  widened `unmanaged` rule.
- `scripts/lib/document_governance/registry.py` — `_path_regex` and the
  frontmatter-policy validation.
- `scripts/lib/document_governance/archive.py` — preserved-record discovery
  and the Tombstone-to-record correspondence.
- `docs/98.archive/{completed,superseded,retired}/` — the retained records.

## Failure Modes and Guardrails

- A preserved record whose Tombstone is missing, or a Tombstone whose record is
  missing, fails closed. Neither half is evidence on its own.
- Restoration that cannot read the recorded blob at the recorded commit stops
  rather than writing a reconstructed file. A guessed record is worse than an
  absent one.
- Widening `unmanaged` must not exempt any live profile. The rule admits only
  profiles whose path pattern is inside `docs/98.archive/`.

## Acceptance Contract

1. No document under `docs/01`, `02`, `03`, `05`, or `90` carries a terminal
   status.
2. Every Tombstone's `Retired Path` has a preserved record at the mapped
   archive path, and every preserved retired record has a Tombstone.
3. Every preserved record is byte-identical to the document it preserves, taken
   from the recorded commit for restorations and from the move for relocations.
4. `run-ci-gate.py --profile full` exits `0`.
5. Mutation evidence: deleting a preserved record, and leaving a terminal
   document in an active stage, each fail the gate.

## Traceability

- Parents: REQ-0026 (document retention and retirement), AD-0030 (document
  lifecycle governance), ADR-0030 (tombstone retirement record).
- ADR-0030 decided the pointer-only archive this package replaces; it is
  superseded rather than amended, because its decision is the thing that
  changed.

## Related Documents

- [Documentation protocol](../../00.agent-governance/policies/documentation-protocol.md)
- [Archive index](../../98.archive/README.md)
