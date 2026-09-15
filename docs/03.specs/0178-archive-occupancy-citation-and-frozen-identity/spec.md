---
title: "Archive Occupancy, Route Citation, and Frozen Identity Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0178"
parent_ids:
- "REQ-0026"
- "AD-0030"
- "ADR-0036"
created: "2026-09-15"
---

# Archive Occupancy, Route Citation, and Frozen Identity Specification

## Overview

The archive consistency assessment
[RES-0096](../../90.references/research/0096-archive-disposition-consistency/README.md)
found three places where a rule and the checks or practice that carry it
disagree, and where resolving them changes meaning. A finished Task of an
unfinished package must hold `in-progress` to pass the occupancy check. The
incident and postmortem citation exception admits route records that hold no
body. And "byte-identical at the move" is not verifiable, because the completing
commit changes status, version, and Task evidence in the same commit.

`ADR-0036` proposes the resolution. This package moves the checks and the
governing text onto it, and accepts `ADR-0036`, in one result tree.

On 2026-09-16 the operator also assigned this package the one gap RES-0096 left
without an owner, its item A11: an Incident can reach `resolved` without
recording when it closed.

## Boundaries and Inputs

- Inputs: `ADR-0036`, RES-0096, the Stage 98 sections of
  `.agents/governance/documentation-protocol.md`, `REQ-0026`, and the state
  SPEC-0177 leaves on completion.
- Precondition: SPEC-0177 is completed and preserved, `ADR-0035` is `accepted`,
  and `common.archive_disposition_model` is `adopted`. This package is not
  activated before then.
- In scope:
  - `scripts/lib/document_governance/archive.py`:
    `validate_active_stage_occupancy` and the Retention Catalog source check.
  - `scripts/lib/document_governance/links.py`: the order of the archive
    boundary conditions in `check_alignment`.
  - `docs/99.templates/registry.json` and
    `docs/99.templates/contracts/document-profile.schema.json`: a
    `common.frozen_transition_fields` list.
  - The `incident` profile in `docs/99.templates/registry.json`: a
    `required_frontmatter_by_status` entry for `resolved`.
  - The tests under `tests/lib/document_governance/` that cover each of these.
  - The acceptance of `ADR-0036`, its supersession of `ADR-0035`, and the
    in-place amendment of REQ-0026-FR-0009, REQ-0026-FR-0012,
    REQ-0026-FR-0014, the first `REQ-0026` Constraint, and the Acceptance
    Criterion on archive links; the `AD-0030` statement of the link exception;
    the policy paragraph on a finished Task of an
    unfinished package, its Links into Stage 98 section, and its retirement
    verification sentence; the Stage 98 README boundary section; and
    `.agents/skills/incident-response/SKILL.md`.
- Out of scope: any edit to a frozen body or sealed record; a catalog row or
  identity comparison for a record preserved before the Retention Catalog
  existed; `TERMINAL_DOCUMENT_STATUSES` for `resolved` and `published`; and a
  machine check of the context an incident gives when it cites a
  `superseded/` or `retired/` body.

## Behavior Contract

1. Occupancy in an active Stage 03 is judged per package. A package is terminal
   when its Spec's status is terminal. A terminal Spec or a terminal Plan in an
   active Stage 03 is a finding.
2. Inside a package whose Spec is not terminal, a Task whose status is
   `completed` is admitted, and a Task whose status is `cancelled` is a finding.
   An admitted `completed` Task grants no disposition; the package still moves
   whole, with its Spec's terminal transition, in one result tree. A package
   whose Spec is terminal admits no member in an active Stage 03.
3. A standalone document in Stages 01, 02, 05, or 90 is judged per document, as
   before.
4. A link from outside `docs/98.archive/` to a path under
   `docs/98.archive/tombstones/` or `docs/98.archive/migrations/` is an
   `active-archive-link` finding for every source profile.
5. An `operation/incident` or `operation/postmortem` document may link to a body
   under `completed/`, `superseded/`, `retired/`, or `resolved/`. Every other
   source keeps the adopted boundary: the index, `completed/`, and `resolved/`.
6. For every Retention Catalog row, the frozen unit equals its `Source` object:
   the same member paths, the same Git file modes, and the same bytes after the
   frontmatter, line endings included.
7. Within frontmatter, only the keys `common.frozen_transition_fields` lists may
   differ in value, and `superseded_by` may be added. Any other added, removed,
   or reordered key is a finding. A member without frontmatter must match byte
   for byte.
8. A missing `Source` object is a finding, never a pass.
9. A preserved record with no catalog row is not compared.
10. An `operation/incident` whose status is `resolved` carries a nonempty
    `resolved_at`. A missing key, a null, or an empty string is a
    `status-frontmatter-required` finding, and the value keeps the `date-time`
    format the frontmatter schema declares.

## Technical Approach

The occupancy check reads package membership from the Registry `spec`, `plan`,
and `task` path patterns rather than from a second pattern in the check, and
reads the Spec's status once per package.

The link boundary becomes an ordered decision: a source inside Stage 98 is out
of scope; the index is admitted; a route record is rejected; an incident or
postmortem source is admitted for a retention class; any other source uses the
adopted citable prefixes. The route-record rule comes before the profile
exception, which is the whole behavioral change.

The source comparison extends the catalog's existing `Source` check. It lists
both trees with `git ls-tree -r` to compare member paths and modes, reads each
blob with `git cat-file blob`, splits a leading YAML frontmatter block, compares
the remaining bytes exactly, and compares the frontmatter key sequence with only
the registered fields free to change. It stores no digest: both sides are Git
objects the tree and its history already hold, which keeps REQ-0026-NFR-0006.

A completing change therefore writes its final evidence in a commit before the
move, while the Task still reads `in-progress`, and the completing commit
changes only lifecycle fields, the move, the Stage 03 index row, the Retention
Catalog row, and consumers. The occupancy rule of Behavior Contract 2 lets that
earlier commit set the Task to `completed` instead.

The gate result a Task records is the run on the tree of that earlier commit,
which holds every content change. The completing tree differs from it only in
what Behavior Contract 7 admits, the move, the two index rows, and consumers.
The pre-commit changed profile gates that tree, and its result is reported in
the integration report rather than written into the frozen Task.

Behavior Contract 10 uses the Registry's existing status-conditional
frontmatter contract, which the `postmortem` profile already applies to
`reviewed_at` at `published`. It adds one Registry entry and no check.

No new Registry switch is added. Every behavior lands in the result tree that
accepts `ADR-0036`.

## Interfaces and Data

`check-document-links.py`, `check-document-corpus-lifecycle.py`, and
`check-document-metadata.py` keep their arguments and exit contract. The
Registry gains `common.frozen_transition_fields`, a list of frontmatter keys
whose initial value is `["status", "version", "updated", "superseded_by"]`,
declared in the schema as a required array of unique strings. New finding codes:
`catalog-source-members-differ`, `catalog-source-mode-differs`,
`catalog-source-body-differs`, and `catalog-source-frontmatter-differs`.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| A Task is marked `completed` to take one member out ahead of its package | Behavior Contract 2 admits the status only while the Spec is not terminal, and a preserved unit is always a whole package |
| A cancelled Task sits silently in an active package | Behavior Contract 2 keeps it a finding |
| An incident cites a route record as evidence | Behavior Contract 4 applies before the profile exception |
| A completing commit rewrites evidence inside a frozen body | Behavior Contract 6 compares body bytes with `Source` |
| A formatter converts line endings in a preserved body | Line endings are part of the compared bytes |
| A shallow clone lacks the `Source` object | Behavior Contract 8 reports it; hosted CI checks out full history |
| A historical body is rewritten to satisfy the comparison | Behavior Contract 9 compares only records with a catalog row, and frozen records are never edited |
| An Incident is closed without a closure date | Behavior Contract 10 requires `resolved_at` at `resolved` |

## Acceptance Contract

1. Tests written first and failing first prove Behavior Contracts 1 to 3: a
   `completed` Task in an active package passes, a `cancelled` Task in an active
   package fails, a terminal Spec or terminal Plan in Stage 03 fails, and a
   superseded standalone decision in Stage 02 still fails.
2. Tests prove Behavior Contracts 4 and 5 for each of `operation/incident`,
   `operation/postmortem`, and `operation/runbook` against each of the six
   dispositions and the index.
3. Git-fixture tests prove Behavior Contracts 6 to 8: a status-and-version-only
   difference passes; an added body line, an added frontmatter key, a mode
   change, a missing or extra member, a line-ending change, and a missing object
   each fail with their code; an added `superseded_by` passes.
4. The Registry and schema declare `common.frozen_transition_fields`, and a
   Registry load fails without it.
5. Every tracked record, and every row the Retention Catalog holds when this
   package activates, passes the registered checks.
6. In one result tree: `ADR-0036` is `accepted` with `supersedes` naming
   `ADR-0035` and the surviving rules of `ADR-0035` restated; `ADR-0035` is
   preserved under `docs/98.archive/superseded/` with `superseded_by` set, its
   catalog row added, and its inbound links repointed; every text surface
   named in scope states the new rules; and a search of active documents finds
   no remaining statement of the replaced occupancy, citation, or byte-identity
   rules.
7. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0 on the
   tree holding every content change, recorded in the Task, and on the
   completing tree, reported in the integration report.
8. An independent exact-diff review reports no finding outside the recorded
   authorization, and every accepted finding is corrected before completion.
9. A test proves Behavior Contract 10: a `resolved` Incident with a valid
   `resolved_at` passes; one with the key absent, null, or empty fails; and an
   Incident at `mitigated` passes without it.

## Traceability

| Governing document | Relation |
| --- | --- |
| [REQ-0026 Document Retention and Retirement](../../01.requirements/0026-document-retention-and-retirement.md) | Owns the requirements this package amends in place |
| [AD-0030 Document Lifecycle Governance](../../02.architecture/descriptions/0030-document-lifecycle-governance.md) | Owns the validator structure this package changes |
| [ADR-0036 Archive Occupancy, Route Citation, and Frozen Identity](../../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md) | The decision this package accepts |
| [SPEC-0177 Archive Disposition Enforcement](../0177-archive-disposition-enforcement/spec.md) | Must complete first; it accepts `ADR-0035`, which this package supersedes |
| [RES-0096 Archive Disposition Consistency Assessment](../../90.references/research/0096-archive-disposition-consistency/README.md) | The dated evidence for each divergence |

## Open Questions

None is open. The draft asked whether any container other than a Stage 03
package needs the `completed`-member admission of Behavior Contract 2. RES-0096
found none, so Behavior Contract 3 keeps every other stage per document.

## Operational Impact

None at runtime. Authors record completion evidence before the completing
commit and may mark a finished Task `completed` while its package is still
active.
