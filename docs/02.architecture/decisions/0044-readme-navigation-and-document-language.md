---
title: "README Navigation and Document Language"
version: "0.2.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-28"
layer: "architecture"
artifact_id: "ADR-0044"
parent_ids:
- "AD-0030"
created: "2026-09-27"
---

# ADR-0044: README Navigation and Document Language

## Context

On 2026-09-27 the owner asked for README navigation and document language to be
one enforced contract across the workspace. An audit of the 186 tracked READMEs
at `f30b168e2` found the following:

- Folder routers whose only substantive children are folders still enumerate
  documents inside those children. These include `docs/03.specs/README.md`,
  `docs/90.references/research/README.md`,
  `docs/99.templates/templates/README.md`, `infra/04-data/README.md`, and
  `.agents/README.md`.
- Two validators require that enumeration: the `indexes` Spec membership check
  and the `template_catalog` check.
- The Stage 98 README is also the machine-read Retention Catalog, so its
  navigation cannot change without touching a ledger.

Language had no machine contract. `documentation-protocol.md` declared
`.agents/**` and Stage 99 sources English-only, and it recorded Korean Stage
01/02/05 and English Stage 03/90 only as observations. `docs/README.md`
carried a second language table that partly disagreed with it. Neither matched
the owner's priority:

1. Every managed README is Korean.
2. Every other human-facing document under `docs/05.operations/` is Korean.
3. Every other document under `docs/` is English.

## Decision Drivers

- A README must route readers, not duplicate the membership its children own.
- One owner per fact: the Registry owns type-to-template mapping and each
  profile's language. The tree owns folder membership.
- Rules must be enforced by the existing validators, not left in prose.
- Frozen Stage 98 bodies, template sources, and generated adapters keep their
  own contracts.

## Options Considered

1. **Prose-only correction.** Edit the READMEs and the policy text. This is
   cheap, but nothing stops a regression, and the validators that require
   enumeration would still fail the corrected READMEs.
2. **Role-contract enforcement (chosen).** Derive folder-only status from the
   tracked tree and enforce a `navigation` link mode. Give every Registry
   profile a declared `language` that the body validator reads. Move the
   Retention Catalog into its own registered record. Retire the checks that
   demanded enumeration.
3. **Generated routers.** Render router READMEs from the Registry. This is
   strong, but it replaces authored explanation with generated lists, and the
   request needs purpose and workflow prose.

## Decision

Adopt option 2.

**Navigation.** A README whose substantive children (every tracked child
except the README and `.gitkeep`) are all directories is a folder router.
Inside its own subtree, a folder router may link only a direct child directory
or that child's `README.md`. This applies to Markdown inline, reference-style,
and HTML links, and to file names in fenced tree diagrams. Links outside its
subtree remain ordinary citations. In any README, a link whose label names a
folder must resolve to that folder or to its README. Collection READMEs, which
hold direct files, index their own direct members; a deeper link from one is a
citation that this decision does not limit.

**Language.** Every Registry profile that governs human prose declares
`language` as `ko` or `en`:

- README profiles and Stage 05 profiles are `ko`.
- Other `docs/` profiles are `en`.
- Profiles outside `docs/` declare `en` only when they are canonical
  governance or provider sources.
- Profiles without prose to judge omit the field: Stage 98 records, template
  sources, and generated runtime adapters.

Structure tokens keep their form in every language. These are required
headings, paths, identifiers, commands, and metadata keys. The body validator
judges prose outside those tokens.

**Ledger separation.** The Retention Catalog moves from
`docs/98.archive/README.md` to `docs/98.archive/retention-catalog.md`. It gets
its own profile, and its table header is kept byte-exact. The Stage 98 README
becomes a router.

**Index ownership.** The Stage 03 index links package directories rather than
`spec.md`, `plan.md`, or Tasks. The Registry `template_roles` map is the only
type-to-template owner, and the `template_catalog` key and its check are
retired.

## Consequences

- Positive: routers stop drifting from the members their children own. The
  language rule is testable. One validator run proves both rules.
- Negative: the bootstrap English-only constraint gains a README exception. The
  Stage 01/02 corpus (Korean today) and much of Stage 05 (English today) do not
  yet match their declared language. Until the corpus follow-up lands, the
  validator enforces declared language fully for README profiles and only on
  changed documents for the rest.
- Language judgment is a heuristic over prose characters. Its limits are
  stated in the validator and in the documentation protocol.

## Traceability

- Requirements: [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md),
  [REQ-0026](../../01.requirements/0026-document-retention-and-retirement.md)
- Architecture: [AD-0030](../descriptions/0030-document-lifecycle-governance.md)
- Spec: [SPEC-0184](../../03.specs/0184-readme-navigation-and-language-contract/)

## Compliance

`check-document-links.py --mode all` enforces navigation.
`check-document-metadata.py` enforces declared language and the Retention
Catalog profile. The Registry schema rejects an undeclared `language` value.

## Follow-up

- Corpus language migration for non-README documents, and full enforcement.
- Script and legacy-code cleanup found by the same audit.
