---
status: active
artifact_id: reference:agentic-research:documentation-architecture
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

# Reference: Documentation Architecture and Diataxis Alignment

## Overview

Diataxis separates documentation by the user need it serves rather than by the
product feature it describes. It derives exactly four types from two axes:
whether content informs **action** or **cognition**, and whether it serves the
**acquisition** or the **application** of skill. Tutorial, how-to guide,
reference, and explanation are the four resulting quadrants.

This reference maps that framework onto the tracked documentation corpus of
`hy-home.docker` at baseline `867a8146`. The repository already
names Diataxis as a design input at
`docs/99.templates/support/external-source-rationale.md:22`, so this is an
alignment check against a declared input, not the introduction of a new
framework.

This document does not change any template, validator, or authoring rule. Every
divergence it finds is recorded as a gap with a canonical owner.

## Purpose

Establish which Diataxis quadrant each repository document type actually serves,
identify quadrants that are unserved or served only by scattered fragments, and
name the templates that mix modes inside one artifact.

## Repository Role

`docs/00.agent-governance/rules/documentation-protocol.md` and
`docs/00.agent-governance/rules/stage-authoring-matrix.md` remain the canonical
authoring rules. `docs/99.templates/templates/` remains the canonical template
set, and `scripts/validation/check-repo-contracts.sh` remains the enforcement
boundary. This Stage 90 document is a comparison and routing aid only.

## Scope

### In Scope

- The four Diataxis types, their two derivation axes, and their stated
  prohibitions
- The compass heuristic for assigning content to a type
- Quadrant mapping for every tracked repository document family
- Mode-mixing inside single templates, and quadrants with no owner

### Out of Scope

- Rewriting, splitting, or creating any template
- Changing validator-enforced heading contracts
- Authoring tutorial content
- Semantic assessment of Korean prose bodies beyond structural headings and
  declared usage metadata

## Definitions / Facts

- **Diataxis** derives four documentation types from two axes. The upstream
  source states the completeness claim directly: "there are necessarily four
  quarters to it, and there could not be three, or five. It is not an arbitrary
  number."
- **Action versus cognition** separates practical knowledge, knowing how, from
  theoretical knowledge, knowing that.
- **Acquisition versus application** separates being at study from being at
  work.
- **Blur** is the named failure mode where adjacent quadrants bleed into each
  other. The upstream source states that in the worst case there is "a complete
  or partial collapse of tutorials and how-to guides into each other, making it
  impossible to meet the needs served by either."
- Diataxis explicitly rejects top-down restructuring as an adoption method:
  "It certainly does not mean that you should create empty structures for
  tutorials/howto guides/reference/explanation with nothing in them. Don't do
  that." The prescribed method is small in-place iteration.
- Diataxis states its own limit: "Diataxis cannot address functional quality in
  documentation," though it works "to expose lapses in functional quality." Its
  use here is therefore diagnostic, not corrective.

## The Compass

The upstream compass reduces type assignment to two questions.

| If the content informs | And serves the user's | Then it belongs to |
| ---------------------- | --------------------- | ------------------ |
| Action                 | Acquisition of skill  | A tutorial         |
| Action                 | Application of skill  | A how-to guide     |
| Cognition              | Application of skill  | Reference          |
| Cognition              | Acquisition of skill  | Explanation        |

## Type Criteria and Prohibitions

| Criterion | Type         | Orientation            | Governing question        | Stated prohibition                                                                                                                                           |
| --------- | ------------ | ---------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| DOC-01    | Tutorial     | Learning-oriented      | "Can you teach me to...?" | "A tutorial is not the place for explanation." Ignore options and alternatives; do not try to teach.                                                         |
| DOC-02    | How-to guide | Goal-oriented          | "How do I...?"            | "Action and only action / no digression, explanation, teaching." Write from the user's perspective, not the machinery's.                                     |
| DOC-03    | Reference    | Information-oriented   | "What is...?"             | "Neutral description is the key imperative." Reference "should not attempt to show how to perform tasks"; its structure must mirror the product's structure. |
| DOC-04    | Explanation  | Understanding-oriented | "Why...?"                 | "Keep explanation closely bounded." Do not absorb instruction or technical description that already has a home.                                              |

## Quadrant Mapping Matrix

Counts are derived from the tracked corpus at baseline `867a8146`,
excluding `README.md` files unless stated.

| Criterion | Quadrant         | Repository document type                                                    | Template path                                              | Stage owner          | Tracked count                                         | Status                | Gap / caveat                                                                                               | Confidence |
| --------- | ---------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------- | ----------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- |
| DOC-05    | Tutorial         | None                                                                        | None                                                       | Unassigned           | 0                                                     | Missing               | No template produces a learning-oriented artifact; the stage authoring matrix has no learning-oriented row | High       |
| DOC-06    | How-to           | Operations runbook                                                          | `operations/runbook.template.md`                           | Stage 05             | 62                                                    | Implemented           | Cleanly shaped; explanation-mode headings are validator-forbidden                                          | High       |
| DOC-07    | How-to           | Operations guide, procedural portion                                        | `operations/guide.template.md`                             | Stage 05             | 66 guides total                                       | Partially Implemented | Same artifact also carries explanation and reference sections; see DOC-12                                  | High       |
| DOC-08    | Reference        | Stage 90 reference                                                          | `common/reference.template.md`                             | Stage 90             | 73                                                    | Implemented           | Strongest quadrant in the corpus                                                                           | High       |
| DOC-09    | Reference        | Spec and contract set                                                       | `sdlc/spec.template.md` plus 8 `spec-contracts/` templates | Stage 03             | 57 specs                                              | Implemented           | Machine-readable contract templates extend the reference mode correctly                                    | High       |
| DOC-10    | Reference        | Operations policy, control portion                                          | `operations/policy.template.md`                            | Stage 05             | 64                                                    | Partially Implemented | `## Verification` adds a how-to section to a reference artifact; see DOC-13                                | High       |
| DOC-11    | Reference        | PRD and ARD                                                                 | `sdlc/prd.template.md`, `sdlc/ard.template.md`             | Stage 01, Stage 02   | 25 each                                               | Implemented           | Requirement and architecture description are austere reference                                             | Medium     |
| DOC-12    | Explanation      | ADR, bounded to decisions                                                   | `sdlc/adr.template.md`                                     | Stage 02             | 25                                                    | Partially Implemented | Genuine discursive explanation, but only for decision records; no home for non-decision explanation        | High       |
| DOC-13    | Explanation      | Scattered subsections                                                       | No dedicated template                                      | Distributed          | 69 `### Overview` plus 63 `### Purpose` inside guides | Partially Implemented | This is the exact scattering pathology Diataxis names                                                      | High       |
| DOC-14    | Outside Diataxis | Plan, task, incident, postmortem, release, archive, audit, memory, progress | 9 templates                                                | Stage 04, 05, 98, 00 | 100 plans, 129 tasks                                  | Not Applicable        | Evidence and provenance records are not user-need documentation; the four quadrants do not apply           | High       |

## Mode-Mixing Findings

| Criterion | Artifact                        | Finding                                                                                                                                                                     | Evidence                                                                       | Status                | Canonical owner                                            | Confidence |
| --------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------- | ---------------------------------------------------------- | ---------- |
| DOC-15    | `operations/guide.template.md`  | The template spans three modes in one document: `## Overview` and `### Purpose` are explanation, `### Step-by-step Instructions` is how-to, `## Common Checks` is reference | 35 of 66 guides self-declare two or more modes in their `### Usage Type` field | Partially Implemented | `docs/00.agent-governance/rules/documentation-protocol.md` | High       |
| DOC-16    | `### Usage Type` value space    | The validator enforces that the field appears exactly once but never validates its value, so free text such as `How-to / audit guide.` passes                               | `scripts/validation/check-repo-contracts.sh` guide rules                       | Missing               | `scripts/validation/check-repo-contracts.sh`               | High       |
| DOC-17    | `operations/policy.template.md` | Reference-mode controls and how-to-mode verification steps coexist                                                                                                          | `## Controls` beside `## Verification`                                         | Partially Implemented | Stage 05 policy owner                                      | Medium     |
| DOC-18    | Cross-bucket blur defence       | Guide, runbook, and policy blur into each other is machine-forbidden, which is a correct Diataxis-shaped separation                                                         | Forbidden-heading rules in `check-repo-contracts.sh`                           | Implemented           | `scripts/validation/check-repo-contracts.sh`               | High       |
| DOC-19    | Universal `## Overview`         | Every Markdown template except `adr.template.md` opens with an explanation-mode `## Overview`, including reference and evidence artifacts                                   | 26 of 27 templates                                                             | Partially Implemented | `docs/99.templates/templates/README.md`                    | Medium     |

## Current-State Assessment

| Category                   | Current state                                                                                                                                                     | Primary comparison           | Status                | Gap                                                                                                                                | Recommendation                                                                                                                                                        | Canonical owner                                            | Evidence                                                  | Confidence |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------- | ---------- |
| Documentation architecture | The corpus is a reference-and-evidence system with a strong how-to layer. The Stage 05 tri-split is already a Diataxis-shaped separation and is machine-enforced. | Diataxis four-quadrant model | Partially Implemented | The tutorial quadrant is empty and unstated; explanation is scattered rather than housed; one template actively mixes three modes. | Record the tutorial exclusion as a deliberate decision, or open a Stage 03 item. Do not create empty quadrant sections, which the framework explicitly warns against. | `docs/00.agent-governance/rules/documentation-protocol.md` | Matrices above; template inventory; tracked corpus counts | High       |

## Potential Follow-up / Gap

1. **The tutorial quadrant is empty and the exclusion is unstated.** Zero of 27
   templates produce a learning-oriented artifact. This is defensible: the
   audience is operators, contributors, and agents assumed competent, and
   Diataxis itself warns that tutorials consume disproportionate maintenance
   effort. The gap is that `external-source-rationale.md:22` claims "learning"
   is among the mapped concerns while no artifact serves it. Either the
   rationale text or the corpus should change. Owner:
   `docs/99.templates/support/external-source-rationale.md`.
2. **Explanation has no home.** There is no explanation template, and
   explanation currently lives as 69 `### Overview` and 63 `### Purpose`
   subsections inside how-to guides. ADRs carry real explanation but are bounded
   to decisions, leaving no place for subject-level explanation independent of a
   decision. Owner: Stage 05 and Stage 99 template owners.
3. **`### Usage Type` is declared but not constrained.** Because the validator
   checks cardinality and not value, mode mixing is recorded in metadata but
   never gated. A registered enumeration would make DOC-15 measurable. Owner:
   `scripts/validation/check-repo-contracts.sh`.
4. **Resolved. Two validators previously required conflicting headings for a new
   Stage 90 reference.**
   `scripts/validation/check-repo-contracts.sh` hard-requires the literal
   `## Definitions / Facts` in every non-README Stage 90 reference, while the
   reference role in `docs/99.templates/support/document-metadata-profiles.yaml`
   requires the H2 `## Facts and Definitions`. Both were run against the three
   references added alongside this document: using one heading fails the
   repository contract check with three findings, and using the other fails the
   changed-document metadata check with three findings. Pre-existing leaves are
   unaffected because the metadata check only reports newly introduced
   deficits, so the conflict is invisible until a new reference is authored.
   The conflict was resolved on 2026-08-07 by aligning the two outliers to the
   corpus. No document in `docs/90.references` had ever used
   `## Facts and Definitions`, while 69 used `## Definitions / Facts`, so the
   reference template, the reference role in the metadata profiles, and the
   template-source heading list in the repository contract check were changed
   to the heading the corpus actually uses. The audit role's forbidden-heading
   entry was deliberately left unchanged, because 34 existing audit documents
   already carry `## Definitions / Facts` and retargeting that rule would break
   them. That residual inconsistency is recorded here rather than fixed.
5. **Template-versus-validator drift affects any remediation.** In the guides
   and runbooks buckets the shipped template heading and the validator-required
   heading differ, and the corpus follows the validator. Because
   `documentation-protocol.md` declares template-first a blocking condition, an
   author following the template literally would produce a rejected document.
   This must be resolved before any template-driven Diataxis remediation. Owner:
   `docs/99.templates/templates/` and `scripts/validation/check-repo-contracts.sh`.

## Source Rules

- Prefer the upstream Diataxis source repository when the rendered site is
  unavailable, and record which one was read.
- Treat Diataxis as a diagnostic lens, not a restructuring plan; the framework
  states that adoption proceeds by small in-place iteration.
- Keep repository authoring authority with the Stage 00 rules and the validator,
  not with this reference.

## Sources

- [Diataxis site](https://diataxis.fr/)
- [Diataxis upstream source repository](https://github.com/evildmp/diataxis-documentation-framework)
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template index](../../../99.templates/templates/README.md)
- [External source rationale](../../../99.templates/support/external-source-rationale.md)

## Source Retrieval Boundary

The rendered site at `https://diataxis.fr/` served no content on 2026-08-07.
The HTTP 429 it returns is not rate limiting: response headers carry
`cf-mitigated: challenge` and a Cloudflare bot-challenge body, returned before
the origin is reached. Retrying later does not clear it from an automated
client, so this is a standing access boundary rather than a transient failure.

All quoted framework text in this document was therefore read from the
canonical upstream source repository that builds that site,
`evildmp/diataxis-documentation-framework`, at commit
`957c09ca40b4a1edc23874f713e01937d50d54d5`, specifically the files
`source/index.rst`, `source/foundations.rst`, `source/compass.rst`,
`source/map.rst`, `source/tutorials.rst`, `source/how-to-guides.rst`,
`source/reference.rst`, `source/explanation.rst`,
`source/how-to-use-diataxis.rst`, and `source/quality.rst`.

A 2026-08-07 re-check confirmed that this pinned commit is the current head of
the upstream default branch, and that no later commit touches `source/`. The
pinned source is therefore current, and every quotation above was re-verified
against it, including the four types, both axes, the compass table, the blur
failure modes, the completeness claim, and the guidance against creating empty
quadrant structures.

The rendered site itself was still not retrieved, so the deploy state of
`diataxis.fr` against that commit remains unobserved. Note also that `source/`
was restructured upstream on 2026-08-03; references to pre-restructure file
paths would be stale.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when template or authoring contracts change
- **Update Trigger**: Template set changes, validator heading contracts change,
  or the Diataxis upstream source changes

## Related Documents

- [research pack index](./README.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [document metadata lifecycle](./document-metadata-lifecycle.md)
- [LLM-WIKI system](./llm-wiki-system.md)
- [workspace baseline](./workspace-baseline.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
