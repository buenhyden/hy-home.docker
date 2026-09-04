---
title: "Reference: Documentation Architecture and Diataxis Reader Modes"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0002-m0007"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: Documentation Architecture and Diataxis Reader Modes

## Overview

Diataxis distinguishes four documentation modes by the reader need being served:
tutorial for learning, how-to for completing a goal, reference for retrieving
information, and explanation for building understanding. This is a content and
reader-intent lens. It is not a replacement for this repository's normative
Stage 00-99 lifecycle taxonomy, artifact profiles, or approval gates.

The rendered `https://diataxis.fr/` site was reopened on 2026-08-08 and
returned HTTP 429 with `cf-mitigated: challenge`. On re-attempt on 2026-08-14
the same rendered site returned successfully: the landing page states the
framework covers "tutorials, how-to guides, technical reference and
explanation" and that Diátaxis "places them in a systematic relationship."
This is a direct verification, not an inference from the previously
inaccessible page. The four-mode model and detailed per-mode guidance remain
independently verified from the pinned upstream source repository at commit
`957c09ca40b4a1edc23874f713e01937d50d54d5`, and this revision additionally
verified the site's own `/how-to-use-diataxis/` page live. Both routes now
agree: no discrepancy between the rendered site and the pinned source was
found. The prior revision's inability to reach the rendered site is retained
below as **Historical retained** evidence of host volatility, not deleted.

## Purpose

Satisfy REQ-22 with a current, source-bounded reader-mode architecture and a
workspace mapping that helps authors choose what a document must do without
inventing empty folders, changing lifecycle ownership, or treating a Stage 90
recommendation as policy.

## Repository Role

This Stage 90 reference is advisory analysis. The
[stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md),
[documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md),
metadata profiles (retired path: `../../../99.templates/support/document-metadata-profiles.yaml`),
and mapped templates remain authoritative. Reader mode can refine content
inside an approved artifact; it cannot select a stage, authorize a mutation,
change an artifact's evidence role, or prove that the reader need was met.

## Scope

### In scope

- The four Diataxis reader needs and their distinct authoring intent.
- Current workspace surfaces that can serve each need.
- The boundary between a reader-mode lens and normative lifecycle taxonomy.
- Adoption rules, evidence limits, gaps, risks, owners, and all fourteen
  persona scopes.

### Out of scope

- Creating `tutorial/`, `how-to/`, `reference/`, or `explanation/` folders.
- Reclassifying or moving existing stage documents.
- Modifying templates, profiles, validators, routes, or generated artifacts.
- Claiming that a path name or heading proves semantic quality.
- Using an inaccessible-at-the-time Diataxis site response, stale Graphify
  output, private state, runtime state, or remote state as evidence. (The
  site is intermittently reachable; a past HTTP 429 does not license
  assuming today's response, and today's HTTP 200 does not license assuming
  tomorrow's.)

## Definitions / Facts

### Verified source boundary

| Observation                      | Evidence                                                                                                        | State                                                                                                                                                                                                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rendered site access, 2026-08-08 | `https://diataxis.fr/`, 2026-08-08T17:14:35+09:00                                                               | **Historical retained — UNVERIFIED page body at that timestamp**: HTTP 429; Cloudflare challenge, 5,338-byte challenge response.                                                                                                                                             |
| Rendered site access, 2026-08-14 | `https://diataxis.fr/` and `https://diataxis.fr/how-to-use-diataxis/`, re-fetched this revision                 | **Verified live**: both pages returned successfully. Content agrees with the pinned upstream source below; no discrepancy found. Host access is confirmed intermittently blocked (429 on one date, 200 on another), so a future re-attempt should not assume either outcome. |
| Upstream source identity         | `evildmp/diataxis-documentation-framework`, default branch `main`                                               | Verified through the GitHub API at commit `957c09ca40b4a1edc23874f713e01937d50d54d5`, authored 2026-08-06; not re-pinned this revision because the live site now independently corroborates it.                                                                              |
| Four-mode model                  | pinned `source/index.rst` and `source/map.rst`; cross-checked against the live 2026-08-14 landing page          | Verified from immutable upstream source and now also from the live rendered page.                                                                                                                                                                                            |
| Mode-specific guidance           | pinned tutorial, how-to, reference, and explanation source files                                                | Verified from immutable upstream source; paraphrased below.                                                                                                                                                                                                                  |
| Adoption method                  | pinned `source/how-to-use-diataxis.rst`; cross-checked against the live 2026-08-14 `/how-to-use-diataxis/` page | Verified on both routes: use the model as a guide, do not create empty quadrant structures, and publish every incremental improvement immediately rather than waiting for a complete rewrite.                                                                                |

Graphify reports `status=advisory` because its manifest is missing and it found
two surprising cross-root inferred edges. It was built from `f8a72211`, not the
Task 6 baseline. No claim below depends on the graph; all workspace mappings
were corroborated against tracked stage rules, profiles, templates, and the
current SDLC research leaves.

### Four reader modes

| Mode         | Reader situation and question                                                            | Authoring job                                                                                                | Boundary that preserves the mode                                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tutorial     | The reader is acquiring a skill: “Can you teach me to do this?”                          | Provide a coherent, guided, achievable learning experience with early visible results and expected outcomes. | Do not turn the lesson into a choice-heavy reference dump or a production task recipe. Success is the learning journey, not merely task completion. |
| How-to guide | The reader has a goal in active work: “How do I achieve this outcome?”                   | Give a practical sequence that starts from stated prerequisites and reaches one concrete goal.               | Keep the path focused on action. Link to background and reference instead of interrupting the procedure with broad teaching or theory.              |
| Reference    | The reader needs accurate information: “What is this, and what are its available parts?” | Describe the machinery neutrally, consistently, and in a structure that reflects the subject.                | Do not make reference carry a lesson or an end-to-end operational procedure. Examples may illustrate facts without replacing them.                  |
| Explanation  | The reader is reflecting: “Why is this designed or behaving this way?”                   | Connect concepts, context, history, constraints, alternatives, and consequences.                             | Bound the topic and avoid absorbing instructions or neutral technical inventory that have other homes.                                              |

The modes are not a mandatory reading sequence. The upstream map explicitly
allows readers to enter wherever their immediate need lies and move between
needs over time. A single subject may therefore need multiple documents, but a
repository does not become better merely by creating four named containers.

### Reader mode is not lifecycle taxonomy

| Axis                   | Reader-mode lens                                          | Repository lifecycle taxonomy                                                                                 |
| ---------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Governing question     | What does this reader need at this moment?                | What artifact owns intent, decision, contract, execution, operations, reference, history, or template source? |
| Authority              | Advisory source-informed content design.                  | Normative Stage 00 governance and Stage 01-99 contracts.                                                      |
| Unit of classification | A page, section, or bounded content need.                 | A typed artifact with path, template, metadata, lifecycle, and approval rules.                                |
| Change effect          | May suggest splitting or linking content after approval.  | Selects canonical owner and validation; controls whether a mutation is allowed.                               |
| Evidence meaning       | Mode fit can be assessed but is not proven by a filename. | Artifact identity and validator results prove tracked contract state, not reader success.                     |

Consequently, a guide is not automatically a Diataxis how-to, a reference
artifact is not automatically neutral technical reference, and an ADR is not
automatically complete explanation. Conversely, Plan, Task, Incident,
Postmortem, Release, Audit, Archive, and Memory artifacts retain essential
lifecycle or evidence roles even when none maps cleanly to a reader mode.

### The compass and iterative adoption

The live 2026-08-14 fetch of the rendered site confirms a fifth concept beyond
the four modes: the site's navigation names a separate "compass" resource for
orienting a reader among the four needs, distinct from the four mode pages
themselves. This reference does not reproduce the compass's content — it was
not the subject of this leaf's pinned-source verification and would need its
own direct fetch to cite precisely — but its existence is a useful boundary
marker: Diataxis itself distinguishes "which mode does this content need" from
"how does a reader find the right mode," and this workspace's own navigation
question (Stage 90 curated map, LLM Wiki, README chain) is the second kind of
problem, not the first. Conflating the two would misapply a content-shape
framework to a discovery/routing problem this workspace already solves
differently (see the companion LLM Wiki reference).

The site's `/how-to-use-diataxis/` page, fetched directly this revision,
states the adoption method in stronger terms than a prior paraphrase captured:
"Don't create empty structures for tutorials/howto guides/reference/
explanation with nothing in them" and "every step in the right direction is
worth publishing immediately," with the framework positioned as "a guide, not
a plan." This is a direct, sourced reason — not merely this reference's
inference — that the `In scope`/`Out of scope` prohibition on creating
`tutorial/`, `how-to/`, `reference/`, or `explanation/` folders in this
workspace tracks Diataxis's own stated adoption method rather than
contradicting it: Diataxis's authors themselves warn against exactly that
move.

### Current workspace mapping

| Reader need                       | Current candidate surfaces                                                                                                                        | Current state and evidence limit                                                                                                                                                        | First owner for a future change                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Learn through a guided experience | No dedicated normative lifecycle artifact. `docs/90.references/learning/` is a category name, not semantic proof of tutorials.                    | **Partial / unverified semantic coverage.** A tutorial may be authored in an approved current surface, but no empty tutorial folder or new artifact type is justified by this analysis. | Product intent, then the applicable Stage 03/04 chain and `doc-writer`.                       |
| Complete an operational goal      | Stage 05 Guides and Runbooks; a Guide owns routine usage, while a Runbook owns repeatable operational procedure and recovery.                     | **Implemented as typed surfaces.** Per-document goal focus and successful execution require content review or execution evidence.                                                       | Operations owner plus `doc-writer`; Runbook execution evidence remains Task/operations-owned. |
| Retrieve precise information      | Stage 03 Specs and child contracts, Stage 05 Policies, Stage 90 References, generated reference data, and canonical runtime/configuration owners. | **Implemented as typed surfaces.** Stage 90 and generated indexes are advisory; runtime truth must be read from its direct owner.                                                       | Artifact's stage owner; generated files use their named generator.                            |
| Understand reasons and trade-offs | Stage 02 ADRs for decisions; bounded explanatory sections in Guides, research References, and other approved artifacts.                           | **Partial.** ADRs explain decisions, not every concept; Stage 90 analysis cannot become policy by explanation alone.                                                                    | Architecture owner for decisions; the owning stage for non-decision explanation.              |

### README-as-folder-index convention and the Related Documents contract

This workspace's README chain and `## Related Documents` contract are its own
navigation layer, structurally distinct from Diataxis's reference mode and
worth re-deriving directly rather than assumed. Two blocking rules govern it,
re-read directly this revision from
[`documentation-protocol.md`](../../../00.agent-governance/policies/documentation-protocol.md):

- **R2 — README Sync:** "Any folder-level change (file added, moved, removed,
  or content-modified) -> the parent `README.md` MUST be updated to reflect
  the current state of the folder," including when "a document's title,
  status, scope, or summary-level content changes in a way that affects how
  the folder README describes that document." An agent is blocked from
  completion until this is satisfied.
- **R3 — Related Documents:** "Every document MUST contain a `## Related
Documents` section with upstream links. A document without this section is
  INCOMPLETE regardless of content quality."

Neither rule is Diataxis-derived; both predate and are independent of this
leaf's reader-mode analysis. Their effect, read together, is that every folder
carries a locally maintained index (the README) and every leaf document
carries an explicit upstream pointer (`Related Documents`) — a bidirectional
navigation mesh that exists whether or not any individual document also has a
clean reader-mode identity. Re-reading
`readme-profile-contract.md` (retired path: `../../../99.templates/support/readme-profile-contract.md`)
directly confirms this navigation layer is itself typed rather than freeform:
"The registry declares 17 README profiles covering repository and stage
entrypoints, governance and provider catalogs, infrastructure and project
levels, script/test/secret/example catalogs, archive and template catalogs,
and the two `_workspace` support contracts." A README's profile is selected
"by its canonical path, not by whichever body or frontmatter it currently
resembles," with zero-match or overlapping-match treated as a classification
error rather than a license to pick the nearest-looking profile — the same
fail-closed posture the companion metadata-lifecycle reference documents for
lifecycle artifacts generally.

Mapped onto Diataxis: a folder README under this contract functions closer to
a wayfinding/reference hybrid than to any single Diataxis mode — it commonly
answers "what is in this folder and where do I go next," which is navigation,
not one of the four content-shape needs. Treating README-writing as
automatically "the reference mode" would be the same category error this
leaf's `Reader mode is not lifecycle taxonomy` table already warns against for
Guides and ADRs; a README's obligations come from R2/R3 and its matched
README profile, not from Diataxis.

### Adoption and maintenance rules

1. Start from a demonstrated reader question, then resolve the canonical stage
   owner. Do not start from a desire to fill a quadrant.
2. Keep one dominant job per bounded page or section. Link to the neighbouring
   mode when a reader need changes rather than blending every need together.
3. Preserve artifact identity. A how-to-shaped Runbook remains a Runbook with
   operational evidence and recovery obligations; a reference-shaped Spec
   remains a Spec with contract and traceability obligations.
4. Improve incrementally in the canonical file after approval. Do not create
   empty mode folders, parallel document trees, or a second stage taxonomy.
5. Validate metadata, required headings, links, and stage contracts. Then use
   human or task evidence to assess semantic reader-mode fit; structural checks
   cannot prove pedagogy, task success, accuracy, or understanding.
6. Keep Stage 90 advice, runtime definition, local execution, remote
   enforcement, and user outcome as separate evidence classes.

### Implementation status, gaps, and risks

- **Implemented:** typed lifecycle roles and templates provide strong current
  homes for goal-oriented operations and information-oriented contracts.
- **Partial:** guided learning and general explanation have no one-to-one
  normative artifact owner. This is an ownership question, not permission to
  add types or folders.
- **Risk:** naming a folder `learning` or a profile `reference` can create false
  confidence about reader-mode quality. Semantic assessment remains necessary.
- **Risk:** mapping the four modes directly onto Stages 01-05 would erase the
  stages' intent/decision/evidence/operations roles and create a competing
  taxonomy.
- **Follow-up route:** if a real reader journey is missing, open the earliest
  applicable Requirement/Spec/Plan/Task chain and name the target reader,
  outcome, validation, maintenance owner, and content mode. This reference
  cannot approve that work.
- **Gap:** the Diataxis "compass" resource that helps a reader find the right
  mode was identified but not directly fetched/cited this revision; a future
  revision that wants to compare it against the LLM Wiki's curated map should
  fetch `https://diataxis.fr/compass/` (or the pinned source's compass file)
  directly rather than reasoning from this leaf's mention alone.

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **The primary documentation-framework site is a standing access boundary.** The site serves an edge bot challenge rather than rate limiting, so no backoff will clear it. The two-axis wording is `UNVERIFIED` at the rendered site and rests on a pinned upstream source alone: the corroborating vendor page confirms the four type names independently but does **not** state the two axes, so no second source carries that half of the claim. The marker belongs with the four-mode and compass claims, not apart from them.

## Scope Implications

| Scope          | Documentation-architecture implication                                                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Agents should classify the immediate reader need while continuing to obey Stage 00 authority, provider loading, permissions, and evidence boundaries.                                    |
| `architecture` | ADRs can serve bounded explanation of decisions; architecture requirements and Specs remain lifecycle contracts rather than Diataxis folders.                                            |
| `backend`      | No current backend application surface was established by the foundation baseline; future API tutorials/how-tos/reference/explanation require an approved backend lifecycle chain.       |
| `common`       | Shared naming, links, formatting, review, and diff hygiene apply across all modes; they do not prove semantic mode fit.                                                                  |
| `docs`         | Direct owner of mode-aware authoring. Use mapped templates and canonical paths; do not create empty quadrant directories.                                                                |
| `entry`        | Gateway readers may need task procedures, configuration reference, and rationale, but current routing stays with the declared infra/entry owners.                                        |
| `frontend`     | The current Storybook fixture does not prove a product documentation set; future learning or goal content needs product and accessibility evidence.                                      |
| `infra`        | Compose/config reference, operational how-to, and topology explanation must remain separate from live runtime proof and secret state.                                                    |
| `meta`         | Profiles and headings can encode artifact roles, but a future reader-mode field would need a Stage 00/99 contract and semantic validation design.                                        |
| `mobile`       | No current mobile source surface was established; all four modes are not applicable until an approved mobile product surface exists.                                                     |
| `ops`          | Guides and Runbooks are the clearest goal-oriented surfaces; Policies stay control/reference oriented, and incidents/postmortems retain evidence roles.                                  |
| `product`      | Product owners define the reader, learning or task outcome, and acceptance need before documentation implementation.                                                                     |
| `qa`           | Structural validators check profile conformance; tutorial success, how-to completion, reference accuracy, and explanatory understanding need mode-specific review or execution evidence. |
| `security`     | Keep procedures, control reference, threat rationale, and training content distinct; none authorizes secret-value access or weakens redaction.                                           |

## Sources

| Source                                                                                                                                       | Accessed                  | Class                             | Verification state                                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Diataxis rendered site, 2026-08-08 attempt](https://diataxis.fr/)                                                                           | 2026-08-08T17:14:35+09:00 | External mutable                  | **Historical retained — UNVERIFIED page body at that timestamp**: HTTP 429, `cf-mitigated: challenge`; no content claims used from that attempt. |
| [Diataxis rendered site, 2026-08-14 re-attempt](https://diataxis.fr/)                                                                        | 2026-08-14                | External mutable                  | Verified live: HTTP success; four-mode statement and compass reference read directly and cross-checked against the pinned source below.          |
| [Diataxis how-to-use page, 2026-08-14](https://diataxis.fr/how-to-use-diataxis/)                                                             | 2026-08-14                | External mutable                  | Verified live: incremental-adoption and no-empty-structures guidance read directly, matching the pinned `how-to-use-diataxis.rst` paraphrase.    |
| [Diataxis upstream source](https://github.com/evildmp/diataxis-documentation-framework/tree/957c09ca40b4a1edc23874f713e01937d50d54d5/source) | 2026-08-08                | External fixed at pinned revision | Verified through GitHub API/raw source; `index.rst`, `map.rst`, four mode files, and `how-to-use-diataxis.rst` read directly.                    |
| [Stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md)                                                       | 2026-08-08                | Workspace tracked                 | Canonical stage, language, and advisory-reference boundary.                                                                                      |
| [Documentation protocol](../../../00.agent-governance/policies/documentation-protocol.md)                                                       | 2026-08-14                | Workspace tracked                 | Re-read directly for R2 (README Sync) and R3 (Related Documents) blocking-rule text quoted above.                                                |
| README profile contract (retired path: `../../../99.templates/support/readme-profile-contract.md`)                                                          | 2026-08-14                | Workspace tracked                 | Re-read directly; confirms 17 registered README profiles and fail-closed profile-selection rule.                                                 |
| [SDLC document roles](./m0016-sdlc-document-roles.md)                                                                                              | 2026-08-08                | Workspace tracked draft           | Current twelve-role lifecycle analysis; does not itself change policy.                                                                           |
| [Metadata lifecycle](./m0006-document-metadata-lifecycle.md)                                                                                       | 2026-08-08                | Workspace tracked draft           | Current profile/lifecycle evidence boundary.                                                                                                     |
| [Scope application matrix](./m0015-scope-application-matrix.md)                                                                                    | 2026-08-08                | Workspace tracked draft           | Fourteen-scope applicability and catalog reachability.                                                                                           |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                                  | 2026-08-08                | Workspace tracked stale/advisory  | Built from `f8a72211`; not used as proof.                                                                                                        |

## Architecture Practice Delta Claims

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `DOCARCH-C4-001` | `documentation-architecture.md` | source-backed | `https://c4model.com/` |
| `DOCARCH-ARC42-001` | `documentation-architecture.md` | source-backed | `https://arc42.org/` |
| `DOCARCH-COMP-001` | `documentation-architecture.md` | synthesis-only | `—` |

## Architecture Practice Direct-Page Evidence

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DA-SRC-001` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DA-SRC-002` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DA-SRC-003` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DA-SRC-004` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams/notation` | 2026-08-28 | VERIFIED |
| `ARC42-OVERVIEW` | `DA-SRC-005` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview/` | 2026-08-28 | VERIFIED |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Present agent boundaries at a useful C4 level. | Review view type and labels. | No system is modelled here. |
| architecture | applies | Combine outline, structural view, and decision record deliberately. | Check typed owner and links. | ADR gaps remain UNVERIFIED. |
| common | applies | Choose reader mode before structure. | Inspect intended audience. | Advisory synthesis. |
| docs | applies | Use Diataxis form and self-contained diagrams where useful. | Check scope, legend, and links. | No mandatory template. |
| infra | applies | Use deployment views only when useful. | Review local infrastructure owner. | C4 container is not Docker proof. |
| ops | applies | Use dynamic/deployment communication for an operational concern. | Confirm operating artifact owner. | No operation observed. |
| qa | applies | Review diagrams for clarity and accessibility. | Inspect labels and abbreviations. | No formal accessibility certification. |
| security | applies | Include threat-relevant relationships when scoped. | Review diagram evidence. | No threat-model execution. |

## Architecture Practice Composition Links

- [SDLC document roles](./m0016-sdlc-document-roles.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)

## 2026-09-05 Revalidation

Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
Official Diátaxis still separates tutorial, how-to, reference, and explanation;
C4 still provides hierarchical system/container/component/code views; arc42
still provides a twelve-section architecture communication structure. The
repository uses these as reader/viewpoint practices inside existing stages,
not as competing directory or lifecycle taxonomies.

| Capability | Repository implementation | Evidence depth | Gap | Verification route |
| --- | --- | --- | --- | --- |
| Reader modes | Guide and reference roles distinguish use from evidence | Defined, Configured | Not every page needs a quadrant label | document-role review |
| Architecture views | Stage 02 descriptions and decisions own current design | Defined, Repository-enforced | C4 view coverage is demand-driven | architecture links and stakeholder review |
| README hierarchy | Repository, stage, category, package, and service routers have distinct profiles | Repository-enforced | Legacy prose can drift | metadata, index, and link checks |

Recommendation: apply only the view needed by the decision and link to the
canonical owner. Official sources re-opened: [Diátaxis](https://diataxis.fr/),
[C4](https://c4model.com/), and [arc42](https://arc42.org/documentation/).

## Maintenance

Reopen the rendered Diataxis site and repin the upstream repository when its
model or adoption guidance changes. Re-evaluate the workspace mapping when
stage roles, templates, profiles, guide/runbook contracts, or reader-facing
routes change. Keep access failures explicit and never replace an inaccessible
source with inherited claims. The site's access outcome has now flipped once
(429 on 2026-08-08, 200 on 2026-08-14) within one week; treat its
availability as genuinely intermittent rather than assuming either state
persists, and always record the actual HTTP outcome observed at fetch time.

## Related Documents

- [Spec-driven SDLC](./m0018-spec-driven-sdlc.md)
- [SDLC document roles](./m0016-sdlc-document-roles.md)
- [Document metadata lifecycle](./m0006-document-metadata-lifecycle.md)
- [LLM Wiki system](./m0009-llm-wiki-system.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
