---
title: "README Navigation and Language Contract Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0184"
parent_ids:
- "REQ-0024"
- "REQ-0026"
- "AD-0030"
created: "2026-09-27"
---

# README Navigation and Language Contract Specification

## Overview

This package makes README navigation and README language one enforced
contract, as
[ADR-0044](../../02.architecture/decisions/0044-readme-navigation-and-document-language.md)
records. It then brings every active README into that contract.

The owner requested the change on 2026-09-27 and decomposed it into three
packages. This package (P1) owns the contract and the README corpus. A
follow-up package (P2) migrates non-README documents to their declared
language and switches language enforcement to the full corpus. A third (P3)
removes the dead code and stale references found by the same audit.

The change is documentation, Registry, and validator work only. It authorizes
no service, volume, network, secret, or remote action.

## Boundaries and Inputs

Inputs are the audit of all 186 tracked READMEs at baseline `f30b168e2`:

- 116 active READMEs.
- 65 frozen Stage 98 READMEs.
- 2 generated adapters (`.claude/README.md`, `.codex/README.md`).
- 3 READMEs under `tests/` and `_workspace/`.

Further inputs are the Stage 99 Registry and its schemas, the README and
operations templates, and these governance documents: the bootstrap policy,
`documentation-protocol.md`, `stage-authoring-matrix.md`, `standards.md`,
`quality-standards.md`, and the Korean-in-governance hook rule. The last
inputs are the link, metadata, archive, lifecycle, and recovery validators
and their tests.

In scope:

- Registry `language` field, schema, templates, and the README profile
  registration of the three unclassified READMEs (`tests/lib/README.md`,
  `tests/validation/README.md`, `_workspace/repo-support/README.md`).
- The `navigation` link mode and the declared-language body check, with their
  regression tests.
- Relocation of the Retention Catalog to `docs/98.archive/retention-catalog.md`
  and the switch of every reader.
- Retirement of the Registry `template_catalog` key and its check. Conversion
  of the `docs/03.specs/README.md` Spec index to package-directory links.
- Governance text: bootstrap hard constraint, documentation protocol language
  rules and README navigation rule, removal of the duplicate language table in
  `docs/README.md`, and the hook rule scope.
- Every active README and both generated adapters. Each is rewritten to
  Korean prose where needed, with no descendant enumeration in folder routers.
  Stale counts, version and port copies without a consuming purpose,
  mislabeled links, and retired identifiers found by the audit are corrected
  or routed to their canonical owner.

Out of scope:

- Non-README language migration (P2).
- Script and dead-code removal (P3).
- Frozen Stage 98 bodies and sealed records.
- The lifecycle state of SPEC-0179, SPEC-0182, and SPEC-0183 and ADR-0037 and
  ADR-0043.
- Any Compose, runtime, or remote change.

Where a README contradicts another README and the canonical Compose or config
source does not settle it, the README routes to the source and the
contradiction is recorded in the Task. The runtime is not edited to match a
document.

## Behavior Contract

1. **Folder router.** A README is a folder router when every tracked direct
   child of its directory, other than `README.md` and `.gitkeep`, is a
   directory. The router must satisfy both of the following:
   - Its links whose targets fall inside its own directory resolve only to a
     direct child directory or to that child's `README.md`. This covers
     inline, reference-style, and HTML `href` links.
   - Its fenced tree diagrams name no file below a direct child.

   Links to targets outside its directory are citations and are not limited
   by this rule.
2. **Label honesty.** In any README, a link whose label ends in `/` resolves to
   a directory or to that directory's `README.md`.
3. **Collection README.** A README whose directory holds direct files
   indexes its own direct members. A deeper link from it is a citation: the
   `navigation` mode does not limit it, and a child's own README still owns
   that child's membership.
4. **Declared language.** Every Registry profile that governs prose declares
   `language`:
   - `ko` for README profiles and Stage 05 profiles.
   - `en` for other `docs/` profiles and for `.agents/` and provider source
     profiles.
   - No `language` for Stage 98 records, template sources, and generated
     runtime adapters.

   The body validator judges the prose left after it removes frontmatter,
   headings, fenced and inline code, link targets, URLs, HTML comments, and
   path- and identifier-shaped tokens; a table is judged by its prose cells.
   README profiles are judged on every document.
   Other profiles are judged only on added or changed documents until P2.
5. **Retention Catalog.** `docs/98.archive/retention-catalog.md` holds the
   `## Retention Catalog` section with the unchanged
   `Record | Class | Names | Source` header. The archive, lifecycle, and
   recovery readers read that path. `docs/98.archive/README.md` routes to it
   and holds no catalog row.
6. **Indexes.** `docs/03.specs/README.md` links each current package as
   `./####-slug/` and states no member file, status, or completed package row.
   The 90.references category READMEs link each package as its directory or
   `README.md`. The Registry `indexes` membership accepts a package-directory
   link as membership.
7. **Template ownership.** The Registry `template_roles` map is the only
   type-to-template owner. `docs/99.templates/templates/README.md` routes to
   the category directories and to the Registry. The `template_catalog` key and
   the `template-catalog-*` findings no longer exist.
8. **Templates project the target language.** Each README and operations
   template tells its author to write body prose in Korean. Other `docs/`
   templates say English. A test fills each template with sample prose in its
   declared language and passes the language check. A test with the opposite
   language fails it.

## Technical Approach

The contract lands before the corpus. Each step first adds a regression test
that fails on the current tree and then implements the change.

The contract steps are the schema field and Registry declarations, the
`navigation` mode beside `check_entrypoint`, the language check beside
`_registered_section_findings`, the catalog relocation, and the index and
template-catalog changes. Each is one closed commit together with the
governance and consumers it changes, so that no intermediate commit fails its
own gates.

The README rewrite follows once the contract is stable. It is split by area:
root and repository, `docs/`, `.agents/` and providers, `infra/` by layer, and
the remaining surfaces. The areas have disjoint files and share no index, so
independent subagents can execute them. Each Korean rewrite gets a
`humanize-korean` pass and keeps structure tokens unchanged.

## Interfaces and Data

- Schema: `document-profile.schema.json` `$defs/profile.language`, an
  optional enum of `ko` or `en`.
- Registry:
  - `language` on every prose profile.
  - A new `archive-retention-catalog` profile.
  - README profile paths for the three unclassified READMEs.
  - `indexes` package-directory membership.
  - Removal of `template_catalog`.
- Link validator: mode `navigation`, with finding codes
  `navigation-descendant-link`, `navigation-descendant-tree`, and
  `navigation-label-mismatch`.
- Metadata validator: finding code `document-language-mismatch`.
- Archive: the constant that names the catalog path moves to the new record.
  The header constant is unchanged.

## Failure Modes and Guardrails

- **A ledger row lost in relocation.** The catalog tests compare the set of
  rows before and after the move, and the coverage and identity checks must
  pass on the new path.
- **A citation misread as enumeration.** Only targets inside the router's own
  subtree are judged, and a direct child's `README.md` is always allowed.
- **Language heuristic error.** The threshold is calibrated against the
  current corpus and recorded in the validator. Mixed identifier-heavy prose
  is covered by fixtures.
- **Frozen or generated file rewritten.** Stage 98 records and generated
  adapters are edited only through their owner. The adapters are edited only
  through the renderer and its template.
- **Runtime drift hidden by a README edit.** Contradictions are routed to the
  canonical source and recorded; the runtime is not changed.

## Acceptance Contract

1. The schema accepts `language` only as `ko` or `en`. Every prose profile
   declares it as rule 4 assigns, and the Registry tests pass.
2. `check-document-links.py --mode navigation` passes on the tree. Regression
   tests prove it fails on each of the following:
   - a folder router linking a child's `spec.md`, `plan.md`, or Task;
   - a fenced tree naming a grandchild file;
   - a folder-labelled link to a leaf.

   The same tests prove it passes on each of the following:
   - a direct child directory or `README.md`;
   - a collection README listing its own files;
   - a citation outside the router's subtree;
   - a directory holding only `.gitkeep`.
3. The language check passes on every README. Regression tests prove it
   passes on Korean README prose with English headings and identifiers, fails
   on an English README, and skips Stage 98 records and generated adapters.
   Filled templates pass in their declared language and fail in the other.
4. The Retention Catalog lives only in `retention-catalog.md` with the same
   rows, and the archive, lifecycle, and recovery checks pass on it. The Stage
   98 README has no catalog row.
5. `docs/03.specs/README.md` links packages as directories, and the index
   membership check passes on that shape and fails on a missing package.
6. No `template_catalog` key or check remains. The templates README lists no
   template file and passes the navigation mode.
7. Governance states the language priority and the navigation rule once, in
   the documentation protocol. The bootstrap constraint, standards,
   quality standards, stage matrix, and `docs/README.md` route to it without a
   second table.
8. Every active README and generated adapter is Korean, and no folder router
   enumerates descendants. The audit's stale counts, version and port copies,
   mislabeled links, and retired identifiers in READMEs are corrected or
   routed, and any remaining contradiction is recorded in the Task.
9. The changed and full CI gate profiles pass locally. Each failure is
   recorded against its baseline status.

## Traceability

- Requirements: [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md),
  [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- Architecture: [AD-0030](../../02.architecture/descriptions/0030-document-lifecycle-governance.md),
  [ADR-0044](../../02.architecture/decisions/0044-readme-navigation-and-document-language.md)

## Open Questions

None blocking. P2 and P3 get their own Spec packages after this one is
approved.

## Operational Impact

Readers reach every document through one route per level, and README prose is
Korean throughout. External links to `docs/98.archive/README.md#retention-catalog`
must use the new record instead. No runtime behavior changes.
