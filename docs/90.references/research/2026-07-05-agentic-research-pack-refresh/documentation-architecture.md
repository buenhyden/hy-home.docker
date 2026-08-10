---
status: active
artifact_id: reference:agentic-research:documentation-architecture
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
---

# Reference: Documentation Architecture and Diataxis Alignment

## Overview

Diataxis separates documentation by the user need it serves rather than by the
product feature it describes. It derives exactly four types from two axes:
whether content informs **action** or **cognition**, and whether it serves the
**acquisition** or the **application** of skill. Tutorial, how-to guide,
reference, and explanation are the four resulting quadrants.

This reference maps that framework onto the tracked documentation corpus of
`hy-home.docker`. It was first written against baseline `867a8146` and every
count and template claim was re-derived at `HEAD` on 2026-08-07; corrected rows
are labeled inline. The repository already names Diataxis as a design input at
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

Counts were re-derived from the tracked corpus at `HEAD` on 2026-08-07,
excluding `README.md` files unless stated. Where a count differs from the
earlier `867a8146` baseline the current value is used; the corpus has grown and
the template set has changed since that baseline, so several figures below are
corrections rather than restatements.

| Criterion | Quadrant         | Repository document type                                                    | Template path                                              | Stage owner          | Tracked count                                          | Status                | Gap / caveat                                                                                               | Confidence |
| --------- | ---------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------- | ------------------------------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------- | ---------- |
| DOC-05    | Tutorial         | None                                                                        | None                                                       | Unassigned           | 0                                                      | Missing               | No template produces a learning-oriented artifact; the stage authoring matrix has no learning-oriented row | High       |
| DOC-06    | How-to           | Operations runbook                                                          | `operations/runbook.template.md`                           | Stage 05             | 62                                                     | Implemented           | Cleanly shaped; explanation-mode headings are validator-forbidden                                          | High       |
| DOC-07    | How-to           | Operations guide, procedural portion                                        | `operations/guide.template.md`                             | Stage 05             | 66 guides total                                        | Partially Implemented | Same artifact also carries explanation and reference sections; see DOC-12                                  | High       |
| DOC-08    | Reference        | Stage 90 reference                                                          | `common/reference.template.md`                             | Stage 90             | 72                                                     | Implemented           | Strongest quadrant in the corpus                                                                           | High       |
| DOC-09    | Reference        | Spec and contract set                                                       | `sdlc/spec.template.md` plus 8 `spec-contracts/` templates | Stage 03             | 59 specs                                               | Implemented           | Machine-readable contract templates extend the reference mode correctly                                    | High       |
| DOC-10    | Reference        | Operations policy, control portion                                          | `operations/policy.template.md`                            | Stage 05             | 64                                                     | Partially Implemented | `## Verification` adds a how-to section to a reference artifact; see DOC-13                                | High       |
| DOC-11    | Reference        | PRD and ARD                                                                 | `sdlc/prd.template.md`, `sdlc/ard.template.md`             | Stage 01, Stage 02   | 25 each                                                | Implemented           | Requirement and architecture description are austere reference                                             | Medium     |
| DOC-12    | Explanation      | ADR, bounded to decisions                                                   | `sdlc/adr.template.md`                                     | Stage 02             | 25                                                     | Partially Implemented | Genuine discursive explanation, but only for decision records; no home for non-decision explanation        | High       |
| DOC-13    | Explanation      | Scattered subsections                                                       | No dedicated template                                      | Distributed          | 65 guides carry `### Overview`; 63 carry `### Purpose` | Partially Implemented | This is the exact scattering pathology Diataxis names                                                      | High       |
| DOC-14    | Outside Diataxis | Plan, task, incident, postmortem, release, archive, audit, memory, progress | 9 templates                                                | Stage 04, 05, 98, 00 | 101 plans, 130 tasks                                   | Not Applicable        | Evidence and provenance records are not user-need documentation; the four quadrants do not apply           | High       |

## Mode-Mixing Findings

| Criterion | Artifact                                | Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Evidence                                                                                                                                                                                                      | Status                | Canonical owner                                                                 | Confidence |
| --------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------- | ---------- |
| DOC-15    | `operations/guide.template.md`          | **Corrected 2026-08-07.** The template no longer spans three modes; it was shortened since the earlier baseline. Its seven headings are now `## Overview`, `## Audience and Prerequisites`, `## Routine Usage`, `## Common Checks`, `## Runbook Handoff`, `## Troubleshooting`, `## Related Documents`. `### Purpose` and `### Step-by-step Instructions` no longer appear in it at all. Mode mixing has moved from the template into the corpus: the guides themselves still carry explanation subsections the template does not supply | `docs/99.templates/templates/operations/guide.template.md:10-35`; 36 of 66 guides self-declare two or more modes in `### Usage Type`                                                                          | Partially Implemented | `docs/00.agent-governance/rules/documentation-protocol.md`                      | High       |
| DOC-16    | `### Usage Type` value space            | **Corrected 2026-08-07.** The validator does not enforce that the field appears exactly once. It only rejects _duplicates_: `usage_type_count = sum(... == "### Usage Type")` followed by `if usage_type_count > 1`. Zero occurrences pass silently, and 3 of 66 guides have none. The value is never inspected, so free text such as `How-to / audit guide.` passes. Observed values include 26 `` `system-guide` ``, 17 `` `system-guide \| how-to` ``, and one bare `onboarding`                                                      | `scripts/validation/check-repo-contracts.sh:643-647`                                                                                                                                                          | Missing               | `scripts/validation/check-repo-contracts.sh`                                    | High       |
| DOC-17    | `operations/policy.template.md`         | Reference-mode controls and how-to-mode verification steps coexist, and both are validator-required                                                                                                                                                                                                                                                                                                                                                                                                                                      | `## Controls` beside `## Verification` in the template at lines 20 and 28; both are required literals at `check-repo-contracts.sh:603`                                                                        | Partially Implemented | Stage 05 policy owner                                                           | Medium     |
| DOC-18    | Cross-bucket blur defence               | Guide, runbook, and policy blur into each other is machine-forbidden, which is a correct Diataxis-shaped separation. Each bucket forbids the others' signature headings                                                                                                                                                                                                                                                                                                                                                                  | `check-repo-contracts.sh:606-610`; guides forbid `## Controls`/`## Exceptions`/`## Review Cadence`, policies forbid `## Usage`/`## Runbook Handoff`, runbooks forbid `## Usage`/`## Controls`/`## Exceptions` | Implemented           | `scripts/validation/check-repo-contracts.sh`                                    | High       |
| DOC-19    | Universal `## Overview`                 | **Corrected 2026-08-07.** The count and the exception list were both stale. 20 of 24 Markdown templates open with an explanation-mode `## Overview`. The four that do not are `adr.template.md` (`## Context and Decision Drivers`), `ard.template.md` (`## Overview and Context`), `governance/memory.template.md` (`## Problem`), and `governance/progress.template.md` (`## Current Work Log`)                                                                                                                                        | first `^## ` heading of each `*.template.md` under `docs/99.templates/templates/`                                                                                                                             | Partially Implemented | `docs/99.templates/templates/README.md`                                         | Medium     |
| DOC-20    | Template-versus-validator heading drift | **New 2026-08-07.** Two operations buckets ship a template whose headings the validator rejects or does not satisfy. A guide copied verbatim from its template fails, because the validator requires the literal `## Usage` while the template supplies `## Routine Usage`. A runbook copied verbatim also fails, because the validator requires `When to Use` while the template supplies `## Trigger and Preconditions`. The corpus follows the validator, not the template                                                            | required literals at `check-repo-contracts.sh:602` and `:604`; template headings at `guide.template.md:18` and `runbook.template.md:16`                                                                       | Missing               | `docs/99.templates/templates/` and `scripts/validation/check-repo-contracts.sh` | High       |

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
   explanation currently lives as `### Overview` subsections in 65 of 66 guides
   and `### Purpose` subsections in 63 of 66, neither of which the current guide
   template supplies. ADRs carry real explanation but are bounded
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
   This must be resolved before any template-driven Diataxis remediation.
   The 2026-08-07 revalidation pinned the exact pairs; see DOC-20. Owner:
   `docs/99.templates/templates/` and `scripts/validation/check-repo-contracts.sh`.

## Workspace Application: What to Investigate or Change Here

Diataxis prescribes small in-place iteration and explicitly warns against
creating empty quadrant structures, so none of these is a restructuring
proposal. Each is an investigation prompt with a named owner.

1. **Fix DOC-20 before anything else.** Every other item below assumes an
   author can copy a template and produce a valid document. Today that is false
   for guides and runbooks. Determine which side is canonical — the template's
   `## Routine Usage` and `## Trigger and Preconditions`, or the validator's
   `## Usage` and `When to Use` — then change exactly one side. Changing the
   validator is the cheaper direction because the corpus already follows it;
   changing the template would require editing 66 guides and 62 runbooks.
2. **Constrain `### Usage Type` or remove it.** The field is declared in 63 of
   66 guides, absent in 3, and never validated. It has drifted into a free-text
   mode-mixing confession: 36 guides declare two or more modes. Either register
   an enumeration and gate it, which would make DOC-15 measurable, or drop the
   field, since an unvalidated self-declaration that nothing reads is pure
   maintenance cost. Do not leave it half-enforced. Owner:
   `scripts/validation/check-repo-contracts.sh`.
3. **Decide where explanation lives, and say so.** 65 of 66 guides carry an
   `### Overview` subsection and 63 carry `### Purpose`, but the guide template
   supplies neither. That means the corpus invented an explanation slot the
   template does not model. Either add the subsection to the template, which
   legitimizes the pattern, or move subject-level explanation to a new home. Do
   not do both, and do not create an empty explanation folder.
4. **Resolve the tutorial-quadrant claim in the rationale file, not the
   corpus.** `external-source-rationale.md:22` claims learning is a mapped
   concern while zero of 24 templates produce a learning-oriented artifact. The
   cheap and correct fix is to amend that one line to record the exclusion as
   deliberate. Creating a tutorial template to satisfy the claim is the failure
   mode Diataxis names by name.
5. **Leave the cross-bucket forbidden-heading rules alone.** DOC-18 is the
   strongest Diataxis-shaped feature in the repository and it is already
   machine-enforced. Any remediation that weakens the guide/policy/runbook
   separation is a regression regardless of what it improves elsewhere.

## Source Rules

- Prefer the upstream Diataxis source repository when the rendered site is
  unavailable, and record which one was read.
- Treat Diataxis as a diagnostic lens, not a restructuring plan; the framework
  states that adoption proceeds by small in-place iteration.
- Keep repository authoring authority with the Stage 00 rules and the validator,
  not with this reference.

## Sources

- [Diataxis site](https://diataxis.fr/) - **UNVERIFIED.** Re-requested 2026-08-07; returns HTTP 429 with `cf-mitigated: challenge` from Cloudflare and serves no content to automated clients. See `## Source Retrieval Boundary`
- [Diataxis upstream source repository](https://github.com/evildmp/diataxis-documentation-framework) - the canonical source that builds the site; head re-confirmed 2026-08-07 at `957c09ca40b4a1edc23874f713e01937d50d54d5`, and all quoted text read from `source/` at that commit
- [Divio documentation system](https://docs.divio.com/documentation-system/) - HTTP 200 on 2026-08-07; corroborates the four type names independently but does not state the two axes
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template index](../../../99.templates/templates/README.md)
- [External source rationale](../../../99.templates/support/external-source-rationale.md)

## Source Retrieval Boundary

`https://diataxis.fr/` was requested directly again on 2026-08-07 and again
served no content. The result is reproducible and diagnostically specific, so
it is recorded in full rather than summarized:

```text
HTTP/2 429
server: cloudflare
cf-mitigated: challenge
content-type: text/html; charset=UTF-8
content-length: 5551
content-security-policy: ... script-src ... https://challenges.cloudflare.com ...
```

The `cf-mitigated: challenge` header and the `challenges.cloudflare.com` script
source in the CSP show this is a Cloudflare bot challenge served at the edge,
not origin rate limiting. The status code 429 is the challenge's chosen
response code and is misleading: retrying later, with or without a browser
user-agent, does not clear it from an automated client. **This is a standing
access boundary, not a transient failure, and no amount of backoff will fix
it.**

### Corroboration and What Remains Unverified

Two independent corroborations were attempted on 2026-08-07.

| Source                                                                 | Result         | What it establishes                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `https://docs.divio.com/documentation-system/`                         | HTTP 200, read | Confirms the four types by name — tutorials, how-to guides, technical reference, explanation — and states "there isn't one thing called _documentation_, there are four", describing them as "four different purposes or functions". This is the ancestor formulation of the same framework by the same author. |
| `evildmp/diataxis-documentation-framework`, upstream source repository | HTTP 200, read | Supplies the exact axis wording and the completeness claim.                                                                                                                                                                                                                                                     |

The Divio page **does not state the two axes**. It names the four types and
their differing purposes but leaves the derivation to its per-type sections.
Therefore:

> **UNVERIFIED:** the exact axis wording quoted in `## Definitions / Facts` —
> action versus cognition, and acquisition versus application — could not be
> confirmed from either rendered site. It is verified only against the upstream
> source repository. The four type names themselves are corroborated
> independently by Divio and are not at issue.

### Pinned Upstream Source

All quoted framework text in this document was read from the canonical upstream
source repository that builds the site,
`evildmp/diataxis-documentation-framework`, at commit
`957c09ca40b4a1edc23874f713e01937d50d54d5`, specifically the files
`source/index.rst`, `source/foundations.rst`, `source/compass.rst`,
`source/map.rst`, `source/tutorials.rst`, `source/how-to-guides.rst`,
`source/reference.rst`, `source/explanation.rst`,
`source/how-to-use-diataxis.rst`, and `source/quality.rst`.

The 2026-08-07 re-check queried the GitHub API for the head of the default
branch and received the same SHA, `957c09ca40b4a1edc23874f713e01937d50d54d5`,
committed 2026-08-06 with the message "Added discovery for the feed, tests" —
an Atom feed change that does not touch the framework text. The pin is
therefore still the current head. `source/foundations.rst` was re-read at that
commit and returns the axis and completeness wording verbatim as quoted above.

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
