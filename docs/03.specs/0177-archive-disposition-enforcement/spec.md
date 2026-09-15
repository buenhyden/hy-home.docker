---
title: "Archive Disposition Enforcement Specification"
version: "1.0.1"
type: "sdlc/spec"
status: "approved"
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
model, and `ADR-0035` records the choice as `proposed`. The executable contracts
predate it in six places. This package moves five of them and registers no
Git-history-only profile, so the sixth stays. Until the package adopts the
model, the registered checks keep enforcing their current subset, which the
policy names explicitly.

## Boundaries and Inputs

- Inputs: the Stage 98 dispositions section of
  `.agents/governance/documentation-protocol.md`, `ADR-0035`, the Stage 98 README,
  and the measured link graph recorded in the Task.
- In scope:
  - `scripts/lib/document_governance/links.py`: `_CITABLE_ARCHIVE_PREFIX`, and
    `_PRESERVED_LINK_PREFIXES`, which skips the outbound links of a preserved
    record.
  - `scripts/lib/document_governance/archive.py`: `_parse_tombstone_text` and
    `TombstoneRecord`, `validate_preservation_boundary` and its literal
    disposition set, the `load_archive` root allowlist, and
    `load_task10_recovery_references`.
  - `scripts/lib/document_governance/registry.py`: `PRESERVED_DISPOSITIONS` and
    `preserved_origin_path`, and the loading of the new profile fields.
  - `scripts/lib/document_governance/spec_packages.py`: `_recorded_retirements`,
    which treats a Tombstone as the only record of a retirement.
  - `scripts/lib/document_governance/lifecycle/recovery.py`, whose `run` takes no
    comparison base and whose preserved count names the three dispositions
    literally, and `scripts/validation/check-document-corpus-lifecycle.py`,
    which calls it.
  - `scripts/lib/document_governance/metadata/heading.py`, whose
    `_registered_section_findings` does not receive the base that
    `scripts/validation/check-document-metadata.py --mode check-changed`
    resolves.
  - `docs/99.templates/registry.json`: the `tombstone` and `migration` profiles,
    a new `archive-record-resolved` profile, and the
    `common.archive_disposition_model` switch.
  - `docs/99.templates/templates/archive/tombstone.template.md` and
    `migration.template.md`.
  - The Retention Catalog section of the Stage 98 README.
  - The tests under `tests/lib/document_governance/` that cover each of these.
  - The acceptance of `ADR-0035`, which supersedes `ADR-0033`, and the clauses of
    the policy, `REQ-0026`, `AD-0030`, and the Stage 98 README that state the
    transition or the Tombstone pairing.
- Out of scope: rewriting any sealed Tombstone or Migration; editing any frozen
  body; creating a `resolved/` directory before a closed Incident exists, and the
  `.markdownlint-cli2.yaml` exclusion that the creating change owns; registering
  any profile as Git-history-only; and a trigger that moves a closed Incident into
  `resolved/`. `TERMINAL_DOCUMENT_STATUSES` in `archive.py` excludes `resolved` and
  `published`, so nothing yet requires that move, and the gap is recorded here
  rather than closed.
- Authorization: local edits, commits, integration into `main`, and push, as the
  operator directed for the change that opened this package.
  `.agents/governance/github-governance.md` makes a pull request the default
  route to `main`, so a direct push under that direction is reported as a rule
  bypass rather than presented as the policy route. Each later integration
  records its own authorization in the Task.

## Behavior Contract

1. `common.archive_disposition_model` in the Registry is `transition` until the
   package adopts the model. While it is `transition`, every check behaves as it
   does before this package. Setting it to `adopted` is the acceptance of
   `ADR-0035` and happens in the result tree that makes that transition. Items 2
   to 10 describe the `adopted` state.
2. A document outside Stage 98 links only to the Stage 98 index, `completed/`,
   and `resolved/`. An `operation/incident` record and its `operation/postmortem`
   are the only profiles that may link to any archive path. A `resolved/` body's
   outbound links are not checked, like every other preserved body's.
3. A record's shape is recognized by its headings, never by a date, an identity
   number, or a list of paths. A sealed Tombstone has the headings `Retired Path`,
   `Replacement`, `Reason`, `Recovery Commit`, `Traceability`, keeps a valid
   recovery commit, and pairs with its `retired/` body. A new Tombstone has
   `Retired Path`, `Successor`, `Reason`, `Traceability`. Its `Retired Path` stays
   the repository path an outside consumer followed, so its `tomb-` identity is
   still derived from the retired document. It names its successor or `none` and
   the reason, and it carries no recovery commit and pairs with no body. A sealed
   Migration keeps its registered sections, and a new Migration has `Purpose`,
   `Moved Scope`, `Current Owner`, `Approval`, `Traceability`.
4. A change that adds a Tombstone or Migration absent from its comparison base
   must use the new shape. A comparison base is not a fixed input, so the rule
   keeps REQ-0026-NFR-0006's exclusion, and no identity cutoff or path list takes
   part.
5. Every `retired/` record has exactly one withdrawal record: a sealed Tombstone
   that pairs with it, or a Retention Catalog row. Completion and supersession are
   never recorded as a withdrawal. A new-shape Tombstone records a route for an
   outside consumer and pairs with no body, so it may name the route of a record
   in any retention class; the rule that a `completed/` or `superseded/` record
   carries no Tombstone binds sealed-shape Tombstones.
6. A change that adds a record under `completed/`, `superseded/`, `retired/`, or
   `resolved/` that is absent from its base adds that record's Retention Catalog
   row in the same change.
7. The Retention Catalog is the table under `## Retention Catalog` in the Stage 98
   README, with the header `| Record | Class | Names | Source |`. It holds one
   row per unit, a Spec package directory or a standalone document.
   - `Record` is a code span of the unit's path under `docs/98.archive/`; a
     package path ends with `/`.
   - `Class` is the disposition directory, and equals the class in `Record`.
   - `Names` is the value the class must name: the identifiers a `completed`
     unit promoted to, the successor identifier of a `superseded` unit, the
     withdrawal reason of a `retired` unit, and the corrective-work owner and
     closure evidence of a `resolved` unit. It is never empty, and outside
     `retired` it contains at least one artifact identifier.
   - `Source` is a code span `<commit>:<path>`. The path equals
     `preserved_origin_path` of `Record`, the commit is an ancestor of `HEAD`, and
     the object resolves to a blob for a document or a tree for a package. A
     moving change cannot name its own commit, so it names the base commit its
     source existed at.
   `Source` is the one source Git object the model permits. No Tombstone,
   Migration, or body names another. A byte comparison between the source and
   the frozen body remains Task evidence, because a completing change also sets
   the transition-owned status fields.
8. `resolved` is a registered disposition. `PRESERVED_DISPOSITIONS` names it,
   the Registry holds an unmanaged `archive-record-resolved` profile,
   `load_archive` admits a `resolved/` subtree, and the sites that named the three
   older dispositions literally read the constant instead.
9. `_recorded_retirements` counts a `retired/` record with a Retention Catalog row
   as a recorded retirement. A Stage 03 package retired after adoption passes
   with its preserved body and its row and no Tombstone, and a removal with
   neither still fails, which is REQ-0026-FR-0003 restated for the new record.
10. No profile is registered as Git-history-only, so every disposition keeps a
    frozen body.

## Technical Approach

The model changes behavior in five checks, and the operator's link rule makes
the change conditional on both the acceptance of `ADR-0035` and the validator
move. A single Registry switch keeps that condition true in every integration.
Work units W3 to W6 land with the switch at `transition`, so each new rule is
inert on the real corpus and exercised only by tests that set the switch in a
fixture. W7 sets the switch to `adopted` in the result tree that accepts
`ADR-0035`, supersedes `ADR-0033`, changes the Registry section lists, and
rewrites every text surface that describes the transition. No integration
leaves the policy describing a check that behaves otherwise.

Legacy and new records are told apart by shape, because a frozen body's
frontmatter is unmanaged and keeps its original date, and because a date, an
identity cutoff, or a path list would be the fixed input REQ-0026-NFR-0006
excludes. The shape a new record must take is enforced where a check already
sees the comparison base, which is the model the lifecycle checks use. A
full-corpus run therefore admits every tracked record in the shape it was
written in, and a change that adds a record in the sealed shape is rejected when
it is made.

Two checks receive the base for this. Behavior Contracts 4 and 6 run in
`check-document-corpus-lifecycle.py`, which passes the base from
`resolve_lifecycle_base` into `lifecycle/recovery.run`. The sealed-shape base
condition runs in `check-document-metadata.py --mode check-changed`, which passes
its `BaseSelection` to `_registered_section_findings`. Without a base, both admit
every tracked record, which is the full-corpus behavior above.

`ADR-0035` supersedes `ADR-0033` rather than narrowing it, because supersession
here is whole-document. It therefore restates every rule of `ADR-0033` that stays
in force: owner transfer before terminal transition, full-package preservation,
the atomic terminal transition, no Git-only preservation of a body a profile
preserves, and the divergent-branch handoff. Only the Tombstone pairing of its
fourth decision changes.

## Interfaces and Data

`check-document-links.py`, `check-document-corpus-lifecycle.py`, and
`check-document-metadata.py` keep their arguments and exit contract; they change
which inputs they admit. The Registry gains:

- `common.archive_disposition_model`, `transition` or `adopted`.
- A `sealed_section_shapes` list on the `tombstone` and `migration` profiles.
  Before W7 `required_sections` holds the sealed shape and
  `sealed_section_shapes` is empty. W7 moves the new shape into
  `required_sections` and the old list into `sealed_section_shapes`. A document
  matches `required_sections`, or matches a sealed shape and exists at the
  comparison base.
- An `archive-record-resolved` profile with the unmanaged frontmatter policy of
  the other retention classes.

A Retention Envelope is one row of the Retention Catalog, with the columns
Behavior Contract 7 names. The Stage 98 root allowlist does not change for it,
because the catalog lives in the index the loader already admits.

## Failure Modes and Guardrails

| Failure mode | Guardrail |
| --- | --- |
| A sealed Tombstone or Migration is rewritten to the new shape | The sealed shape stays admitted for a record present at base, so nothing forces a rewrite, and the frozen-body check still covers preserved bodies |
| A record in the sealed shape is added after adoption | The change-aware check rejects a sealed-shape record absent from its base |
| The pairing is released with no withdrawal owner | Every `retired/` record needs exactly one of a sealed pairing or a catalog row |
| A catalog row names a commit a rebase or squash orphaned | The ancestor check fails closed and the row must be corrected |
| The switch is set without the decision being accepted | A registered test binds `adopted` to `ADR-0035`, found by identity in Stage 02 or Stage 98, having left `proposed` through `accepted`, in both directions |
| A new rule is live while the policy still describes the transition | Every new rule reads the switch, and W7 changes the switch and the text in one result tree |
| The link boundary admits `superseded/` or `retired/` by widening a prefix list | Tests assert rejection for each non-citable disposition and admission for `completed/`, `resolved/`, and the index |

## Acceptance Contract

1. With the switch at `transition`, the corpus produces the same findings from
   every registered check as before the package, and a test for each new rule
   proves it inert in that state.
2. With the switch at `adopted` in a fixture, `links.py` admits links from outside
   Stage 98 to the index, `completed/`, and `resolved/`, rejects `superseded/`,
   `retired/`, `tombstones/`, and `migrations/`, keeps the incident and postmortem
   exception, and skips a `resolved/` body's outbound links, each proven by a test.
3. `resolved` is registered as Behavior Contract 8 states, the three sites that
   named the older dispositions literally read the constant, and a test builds a
   `resolved/` subtree from a fixture.
4. The Retention Catalog check validates the header, one row per unit, the class
   match, the class value, and each `Source` rule, and a test covers each failure,
   including an orphaned commit and a path that differs from the origin.
5. The new Tombstone and Migration shapes parse and validate without a recovery
   commit, path mapping, or recovery section. The sealed shapes pass with their
   existing invariants, a change that adds a sealed-shape record is rejected, a
   test covers each case, and every tracked Tombstone and Migration still passes.
6. Every `retired/` record has exactly one withdrawal record,
   `_recorded_retirements` accepts a catalog row, and a retired package with
   neither fails, each proven by a test.
7. A change that adds a preserved record without its catalog row is rejected,
   proven by a test.
8. In one result tree: the switch is `adopted`; the `tombstone` and `migration`
   `required_sections` hold the new shapes and `sealed_section_shapes` the old;
   the templates carry the new shapes; `ADR-0035` is `accepted` and restates
   `ADR-0033`'s surviving rules; and `ADR-0033` is preserved under
   `docs/98.archive/superseded/` with its body unchanged, its status and
   `superseded_by` set, its Retention Catalog row added, and its inbound links
   repointed to `ADR-0035`.
9. In the same result tree: the policy's Transition list keeps only its sixth
   item, as a standing statement; `REQ-0026` amends in place, with a version
   bump, REQ-0026-FR-0002, REQ-0026-FR-0003, REQ-0026-FR-0008, REQ-0026-FR-0012,
   REQ-0026-NFR-0007, its first two Constraints and the transition Constraint,
   and the Acceptance Criteria on Tombstone removal, the recovery commit, and the
   namespace; the policy rewrites Retirement preconditions item 4, its Tombstone
   scope section, and its "Until SPEC-0177 completes" sentence; and `AD-0030`, the
   Stage 98 README, `.agents/knowledge/repository-map.md`,
   `.agents/skills/incident-response/SKILL.md`,
   `docs/02.architecture/decisions/README.md`, and `docs/README.md` no longer
   describe a lagging check, a mandatory pairing, or a rule conditioned on
   SPEC-0177 or `ADR-0035`.
10. `python3 scripts/validation/run-ci-gate.py --profile changed` exits 0 on the
    final path set, with the command and exit code recorded.
11. An independent exact-diff review reports no finding outside the current
    authorization, and every accepted finding is corrected before completion.

## Traceability

| Governing document | Relation |
| --- | --- |
| [REQ-0026 Document Retention and Retirement](../../01.requirements/0026-document-retention-and-retirement.md) | Owns the retention requirements this package enforces, including REQ-0026-NFR-0006, which rules out a fixed cutoff |
| [AD-0030 Document Lifecycle Governance](../../02.architecture/descriptions/0030-document-lifecycle-governance.md) | Owns the validator structure this package changes |
| [ADR-0035 Stage 98 Retention Classes and Route Dispositions](../../02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md) | The decision this package accepts |
| [ADR-0033 Full Spec Package Preservation](../../02.architecture/decisions/0033-full-spec-package-preservation.md) | Superseded by `ADR-0035` on acceptance, with its surviving rules restated |

## Open Questions

None is open. The operator answered four questions on 2026-09-15:

- The Retention Envelope lives in a Retention Catalog table in the Stage 98
  README rather than a Registry sidecar.
- A withdrawn body's reason is named in the same row.
- No profile is registered as Git-history-only in this package.
- Acceptance supersedes `ADR-0033` and restates its surviving rules.

The approval review then found the Spec underspecified, and the author settled
the rest inside those answers, as the Task records: the Registry switch, shape
and change keying, the catalog columns and row unit, the `Source` validation, and
a `Retired Path` that stays a repository path.

## Operational Impact

None at runtime. Document authors gain the `resolved/` class and the Retention
Catalog, and new route records drop their ledger fields. Existing records and
frozen bodies are unchanged.
