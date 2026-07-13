---
layer: agentic
---

# Frontmatter Contract

## Overview

This document defines frontmatter key ownership for template sources and target
documents. Frontmatter is a Markdown-adjacent preprocessing convention, not core
CommonMark syntax, so the repository treats it as a small structured metadata
surface.

The sole machine-readable application profiles live in
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml). They
define required, optional, forbidden, parent, lifecycle, and exception rules
per artifact type. The exhaustive historical inventory remains advisory; the
approved active chain and safely selected changed/new documents are enforced.

## Surface Interpretation

| Surface | Human authoring boundary |
| --- | --- |
| Typed Markdown template source | Declare the target profile through registered placeholders; copying the source does not preserve template identity or lifecycle evidence. |
| README template source | Remove source frontmatter when copied unless the selected README profile independently permits a field for a declared consumer. |
| Machine-readable template source | Use the native format and comments; do not add Markdown frontmatter. |
| Stage 00 or Stage 99 governance/support document | Use the governance convention, not an active-stage lifecycle profile. |
| Target stage leaf | Select the path-derived registry profile and honest lifecycle state. |
| README | Follow the matched README profile; frontmatter is absent by default. |
| Repo-support README | Follow the explicit workspace/repo-support profile and remain outside active-stage metadata inference. |
| Generated output | Preserve generator-owned metadata and refresh through the canonical generator. |
| Unsupported or native platform surface | Preserve the real consumer's contract; do not add repository metadata for uniformity. |

Human role and authoring boundaries are split between the
[SDLC document contract](./sdlc-document-contract.md),
[common document contract](./common-document-contract.md), and
[README profile contract](./readme-profile-contract.md). This document owns
frontmatter interpretation only. Generic `type` remains forbidden;
`artifact_type` is the stable profiled key introduced only through the approved
metadata rollout.

## Parent Serialization Boundary

`parent_ids` contains direct parent identities with set-like semantic meaning.
The registry's deterministic serialization order makes diffs stable; it does
not assign priority, approval rank, chronology, or dependency strength. The
validator owns profile precedence and ordering behavior. Human-readable
`Related Documents` links continue to express broader traceability.

## Validation Contract

- The registry defines profiles and value semantics; the metadata checker is
  the executable interpreter. Human documents must not substitute their own
  key lists, precedence rules, or transition algorithms.
- Exhaustive reporting remains advisory for historical migration debt. The
  safely selected changed/new boundary fails closed when it cannot establish a
  trustworthy base or working-tree snapshot.
- New documents cannot use a legacy exception. An eligible base-existing legacy
  document may retain only proven pre-existing deficits within the checker's
  approved boundary; partial migration and newly introduced violations block.
- Reverse or otherwise exceptional lifecycle movement requires explicit scoped
  Stage 04 approval evidence consumed by the checker; prose cannot override it.
- Active-record inspection remains advisory unless a later approved gate says
  otherwise.
- Diagnostics expose bounded paths, identities, counts, and finding codes, not
  raw bodies, logs, credentials, or secret values.
- The canonical pre/post-migration snapshot is
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md`.

Registered typed Markdown template sources declare their target `artifact_type` and
use only the placeholder forms registered in the machine-readable profile.
Template validation checks target-required keys without resolving placeholder
IDs. Instantiated non-template documents recursively reject every registered
angle-bracket token even when composed inside a larger scalar or nested list;
non-angle markers such as `YYYY-MM-DD` remain field-specific.
Spec 123 is the sole approved cross-cutting root exception in this rollout; its
empty `parent_ids` is explicit and does not authorize arbitrary root Specs.

Archive tombstones use the archive lifecycle profile and the provenance fields
required by the registry.

## Disposition and Archive Metadata Rules

Restructure dispositions are audit/task decisions, not frontmatter values. Do
not add frontmatter keys such as `disposition`, `document_type`, or
`template_type` to encode archive decisions.

| Decision Surface | Frontmatter Rule |
| --- | --- |
| `active-canonical` | Keep the target's lifecycle `status` and primary document profile. |
| `historical-archive` | Use `status: archived` only on the archive tombstone under `docs/98.archive/**`. |
| `duplicate-remove` | Do not add new metadata to the duplicate solely to delete it; record replacement evidence in task/gap records. |
| `conflict-remove-or-archive` | Use archive provenance keys on the tombstone or record a gap when no replacement exists. |
| `evidence-preserve` | Preserve historical frontmatter unless a future task proves it is active-current guidance drift. |

Archive provenance is limited to archive tombstones and approved archive
profiles. The registry owns the exact field set and value constraints.

## Duplicate-Purpose Key Rules

- Do not use both `type` and path-derived document role for the same purpose.
- Do not use generic `owner`, `updated`, or `links` metadata unless a target
  profile explicitly consumes those keys.
- Do not copy README template metadata examples into final README files.
- Do not add YAML frontmatter to README files just to make them resemble
  target-stage leaf documents. README role is normally derived from path,
  heading, and folder-index profile.
- Do not use template-source `status: draft` as a final target status without
  checking the target lifecycle.

## Legacy Cleanup Rules

- Remove generic metadata snippets that list `title`, `type`, `owner`,
  `updated`, or `links` when they are only illustrative.
- Replace flat template path references with canonical nested template paths.
- If a target document contains copied template instructions instead of
  topic-specific content, record a follow-up gap unless the document is already
  in the approved edit scope.

## Corpus Routing Rules

- Select SDLC and operations leaf roles through the
  [SDLC document contract](./sdlc-document-contract.md).
- Select Reference, Audit, Archive, governance, generated, template,
  repo-support, and native/unsupported surfaces through the
  [common document contract](./common-document-contract.md).
- Select README behavior through the
  [README profile contract](./readme-profile-contract.md).
- Resolve every exact key, value, transition, path, and exception question from
  the registry and checker rather than extending these human routes by analogy.

## Related Documents

- [support README](./README.md)
- [template contract](./template-contract.md)
- [lifecycle status](./lifecycle-status.md)
- [document metadata profiles](./document-metadata-profiles.yaml)
- [external source rationale](./external-source-rationale.md)
- [SDLC document contract](./sdlc-document-contract.md)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
