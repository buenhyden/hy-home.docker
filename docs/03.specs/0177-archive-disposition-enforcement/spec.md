---
title: "Archive Disposition Enforcement Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0177"
parent_ids:
- "REQ-0026"
- "AD-0030"
- "ADR-0035"
created: "2026-09-15"
---

# Archive Disposition Enforcement Specification

## Overview

On 2026-09-15 the operator adopted a Stage 98 model of six dispositions in two
kinds. Four retention classes (`completed/`, `superseded/`, `retired/`,
`resolved/`) hold whole bodies. Two route dispositions (`tombstones/`,
`migrations/`) hold no body and name a route for a consumer outside the
repository. Whether an active document may cite a disposition follows from what
the disposition names, and no Stage 98 record carries a second recovery ledger.

The canonical policy, the Stage 98 README, `REQ-0026`, and `AD-0030` state that
model in the same change that opens this package, and `ADR-0035` records the
choice as `proposed`. The executable contracts predate it in six places, and
this package owns moving them. Until it completes, the registered checks keep
enforcing their current subset, which the policy names explicitly.

## Boundaries and Inputs

- Inputs: the Stage 98 dispositions section of
  `.agents/governance/documentation-protocol.md`, `ADR-0035`, the Stage 98 README,
  and the measured link graph recorded in the Task.
- In scope:
  - `scripts/lib/document_governance/links.py`, whose archive boundary admits
    only `completed/` and the index.
  - `scripts/lib/document_governance/archive.py`, which requires a
    `Recovery Commit` section in every Tombstone, pairs every `retired/` body
    with one Tombstone, rejects a Tombstone for a `completed/` or `superseded/`
    record, and admits only the registered preservation subtrees at the Stage 98
    root, which do not include `resolved/`.
  - `docs/99.templates/registry.json`, the Tombstone and Migration templates, and
    `.markdownlint-cli2.yaml`, for the `resolved/` class and the new record
    shapes.
  - The Retention Catalog, a table in the Stage 98 README whose rows are the
    Retention Envelopes of the records created after acceptance.
  - The acceptance of `ADR-0035`, which supersedes `ADR-0033` and restates its
    full-package preservation unit.
- Out of scope: rewriting any sealed Tombstone or Migration, editing any frozen
  body, creating a `resolved/` directory before a closed Incident exists, and
  registering any profile as Git-history-only. `REQ-0026`'s Constraint and
  `ADR-0033` Decision 5 keep excluding that disposition, and a later decision
  owns any registration.
- Authorization: local edits, commits, integration into `main`, and push, as the
  operator directed for the change that opened this package.
  `.agents/governance/github-governance.md` makes a pull request the default
  route to `main`, so a direct push under that direction is reported as a rule
  bypass rather than presented as the policy route. Each later integration
  records its own authorization in the Task.

## Behavior Contract

1. A document outside Stage 98 links only to the Stage 98 index and the
   retention classes whose own body still leads a reader to current authority:
   `completed/` and `resolved/`. An `operation/incident` record and its
   `operation/postmortem` are the only profiles that may link to any archive
   path.
2. A Tombstone or Migration authored after acceptance carries no redirect, path
   ledger, self-designed body digest, branch SHA, or recovery commit. A sealed
   record authored before acceptance keeps its recorded form and still passes.
3. A `retired/` body authored after acceptance does not require a paired
   Tombstone. Its withdrawal reason is named in its Retention Catalog row.
4. A `resolved/` class is registered as a frozen retention profile and admitted
   by the Stage 98 loader and link graph, and its directory appears only with its
   first record.
5. Each record created after acceptance has exactly one Retention Catalog row
   in the Stage 98 README. The row names the record's path, its class, the value
   its class must name, and its source Git object as `commit:path`, once, and a
   registered check reads the table.
6. No profile is registered as Git-history-only, so every disposition keeps a
   frozen body.

## Technical Approach

The package moves each check onto the model in the order that keeps every
integration valid. The link boundary moves first, because it only widens what
is admitted by one class and narrows nothing that exists today. The Retention
Envelope is defined next, since the Tombstone pairing cannot be released until
something else names why a body was withdrawn. The Tombstone and Migration
contracts then drop their ledger fields for new records, keyed on the record's
creation rather than on a list of legacy paths. `ADR-0035` is accepted last, in
the same result tree that removes the transitional clauses from the policy,
`REQ-0026`, and `AD-0030`. It supersedes `ADR-0033` rather than narrowing it,
because supersession here is whole-document and one decision should own Stage 98
disposition; the full-package preservation unit is restated, not changed.

## Interfaces and Data

`check-document-links.py` and `check-document-corpus-lifecycle.py` keep their
arguments and exit contract; they change which inputs they admit. The Stage 99
registry gains one retention profile and changes two template section lists.
A Retention Envelope is one row of the Retention Catalog table in the Stage 98
README, with the columns Behavior Contract 5 names. The Stage 98 root allowlist
does not change, because the catalog lives in the index the loader already
admits.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| A sealed Tombstone or Migration is rewritten to the new shape | The new contract is keyed on creation after acceptance; the corpus check keeps admitting the recorded form |
| The Tombstone pairing is released before a withdrawal reason has another owner | The Envelope work unit precedes the pairing change, and the corpus check fails a new `retired/` body without a Retention Catalog row |
| The link boundary admits `superseded/` or `retired/` by widening a prefix list | Tests assert rejection for each non-citable disposition and admission for `completed/`, `resolved/`, and the index |
| The policy states a rule no check enforces and no transition names | The policy's transition paragraph lists every lagging check until acceptance removes it |

## Acceptance Contract

1. `links.py` admits links from outside Stage 98 to the index, `completed/`, and
   `resolved/`, rejects `superseded/`, `retired/`, `tombstones/`, and
   `migrations/`, and keeps the incident and postmortem exception, each proven
   by a test.
2. The Registry registers a `resolved/` retention profile, `load_archive` and
   the link graph admit a `resolved/` subtree, and a test builds one from a
   fixture. The Stage 98 README names the lint exclusion as an obligation of the
   change that first creates the directory.
3. The Stage 98 README carries a Retention Catalog table whose rows name path,
   class, the class's named value, and the source Git object once, and a
   registered check requires one valid row for every record created after
   acceptance.
4. The Tombstone and Migration templates and `archive.py` no longer require a
   recovery commit, path mapping, or recovery section for records created after
   acceptance, and every existing sealed record still passes.
5. A `retired/` body created after acceptance passes without a Tombstone when
   its Retention Catalog row names the withdrawal reason.
6. `ADR-0035` is `accepted` and supersedes `ADR-0033`, which moves unchanged to
   `docs/98.archive/superseded/` with reciprocal metadata and its inbound links
   repointed to `ADR-0035`, in one result tree.
7. The transition paragraph is removed from the policy, and `REQ-0026`, `AD-0030`,
   and the Stage 98 README no longer describe any lagging check, while the policy
   still states that no profile is registered as Git-history-only.
8. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0 on the
   final path set, with the command and exit code recorded.
9. An independent exact-diff review reports no finding outside the current
   authorization, and every accepted finding is corrected before completion.

## Traceability

| Governing document | Relation |
| --- | --- |
| [REQ-0026 Document Retention and Retirement](../../01.requirements/0026-document-retention-and-retirement.md) | Owns the retention requirements this package enforces |
| [AD-0030 Document Lifecycle Governance](../../02.architecture/descriptions/0030-document-lifecycle-governance.md) | Owns the validator structure this package changes |
| [ADR-0035 Stage 98 Retention Classes and Route Dispositions](../../02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md) | The decision this package accepts |
| [ADR-0033 Full Spec Package Preservation](../../02.architecture/decisions/0033-full-spec-package-preservation.md) | Superseded by `ADR-0035` on acceptance, with its full-package unit restated |

## Open Questions

None is open. The operator answered the four questions on 2026-09-15:

- The Retention Envelope lives in a Retention Catalog table in the Stage 98
  README rather than a Registry sidecar, so it is found through the index a
  frozen record is already reached by.
- A withdrawn body's reason is named in the same row, as the value its class
  must name.
- No profile is registered as Git-history-only in this package.
- Acceptance supersedes `ADR-0033` and restates its full-package unit.

## Operational Impact

None at runtime. Document authors gain the `resolved/` class and lose the ledger
fields for new route records; existing records and frozen bodies are unchanged.
