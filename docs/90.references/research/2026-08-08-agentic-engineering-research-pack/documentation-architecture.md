---
status: draft
artifact_id: reference:agentic-engineering-research:documentation-architecture
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: Documentation Architecture and Diataxis Reader Modes

## Overview

Diataxis distinguishes four documentation modes by the reader need being served:
tutorial for learning, how-to for completing a goal, reference for retrieving
information, and explanation for building understanding. This is a content and
reader-intent lens. It is not a replacement for this repository's normative
Stage 00-99 lifecycle taxonomy, artifact profiles, or approval gates.

The rendered `https://diataxis.fr/` site was reopened on 2026-08-08 and returned
HTTP 429 with `cf-mitigated: challenge`; no page-body claim in this reference is
attributed to that inaccessible response. The four-mode model and adoption
guidance were instead verified in the directly accessible upstream source at
commit `957c09ca40b4a1edc23874f713e01937d50d54d5`.

## Purpose

Satisfy REQ-22 with a current, source-bounded reader-mode architecture and a
workspace mapping that helps authors choose what a document must do without
inventing empty folders, changing lifecycle ownership, or treating a Stage 90
recommendation as policy.

## Repository Role

This Stage 90 reference is advisory analysis. The
[stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md),
[documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md),
[metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml),
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
- Using the inaccessible Diataxis site body, stale Graphify output, private
  state, runtime state, or remote state as evidence.

## Definitions / Facts

### Verified source boundary

| Observation | Evidence | State |
| --- | --- | --- |
| Rendered site access | `https://diataxis.fr/`, 2026-08-08T17:14:35+09:00 | **UNVERIFIED page body**: HTTP 429; Cloudflare challenge, 5,338-byte challenge response. |
| Upstream source identity | `evildmp/diataxis-documentation-framework`, default branch `main` | Verified through the GitHub API at commit `957c09ca40b4a1edc23874f713e01937d50d54d5`, authored 2026-08-06. |
| Four-mode model | pinned `source/index.rst` and `source/map.rst` | Verified from immutable upstream source. |
| Mode-specific guidance | pinned tutorial, how-to, reference, and explanation source files | Verified from immutable upstream source; paraphrased below. |
| Adoption method | pinned `source/how-to-use-diataxis.rst` | Verified: use the model as a guide, improve iteratively, and do not manufacture empty quadrant structures. |

Graphify reports `status=advisory` because its manifest is missing and it found
two surprising cross-root inferred edges. It was built from `f8a72211`, not the
Task 6 baseline. No claim below depends on the graph; all workspace mappings
were corroborated against tracked stage rules, profiles, templates, and the
current SDLC research leaves.

### Four reader modes

| Mode | Reader situation and question | Authoring job | Boundary that preserves the mode |
| --- | --- | --- | --- |
| Tutorial | The reader is acquiring a skill: “Can you teach me to do this?” | Provide a coherent, guided, achievable learning experience with early visible results and expected outcomes. | Do not turn the lesson into a choice-heavy reference dump or a production task recipe. Success is the learning journey, not merely task completion. |
| How-to guide | The reader has a goal in active work: “How do I achieve this outcome?” | Give a practical sequence that starts from stated prerequisites and reaches one concrete goal. | Keep the path focused on action. Link to background and reference instead of interrupting the procedure with broad teaching or theory. |
| Reference | The reader needs accurate information: “What is this, and what are its available parts?” | Describe the machinery neutrally, consistently, and in a structure that reflects the subject. | Do not make reference carry a lesson or an end-to-end operational procedure. Examples may illustrate facts without replacing them. |
| Explanation | The reader is reflecting: “Why is this designed or behaving this way?” | Connect concepts, context, history, constraints, alternatives, and consequences. | Bound the topic and avoid absorbing instructions or neutral technical inventory that have other homes. |

The modes are not a mandatory reading sequence. The upstream map explicitly
allows readers to enter wherever their immediate need lies and move between
needs over time. A single subject may therefore need multiple documents, but a
repository does not become better merely by creating four named containers.

### Reader mode is not lifecycle taxonomy

| Axis | Reader-mode lens | Repository lifecycle taxonomy |
| --- | --- | --- |
| Governing question | What does this reader need at this moment? | What artifact owns intent, decision, contract, execution, operations, reference, history, or template source? |
| Authority | Advisory source-informed content design. | Normative Stage 00 governance and Stage 01-99 contracts. |
| Unit of classification | A page, section, or bounded content need. | A typed artifact with path, template, metadata, lifecycle, and approval rules. |
| Change effect | May suggest splitting or linking content after approval. | Selects canonical owner and validation; controls whether a mutation is allowed. |
| Evidence meaning | Mode fit can be assessed but is not proven by a filename. | Artifact identity and validator results prove tracked contract state, not reader success. |

Consequently, a guide is not automatically a Diataxis how-to, a reference
artifact is not automatically neutral technical reference, and an ADR is not
automatically complete explanation. Conversely, Plan, Task, Incident,
Postmortem, Release, Audit, Archive, and Memory artifacts retain essential
lifecycle or evidence roles even when none maps cleanly to a reader mode.

### Current workspace mapping

| Reader need | Current candidate surfaces | Current state and evidence limit | First owner for a future change |
| --- | --- | --- | --- |
| Learn through a guided experience | No dedicated normative lifecycle artifact. `docs/90.references/learning/` is a category name, not semantic proof of tutorials. | **Partial / unverified semantic coverage.** A tutorial may be authored in an approved current surface, but no empty tutorial folder or new artifact type is justified by this analysis. | Product intent, then the applicable Stage 03/04 chain and `doc-writer`. |
| Complete an operational goal | Stage 05 Guides and Runbooks; a Guide owns routine usage, while a Runbook owns repeatable operational procedure and recovery. | **Implemented as typed surfaces.** Per-document goal focus and successful execution require content review or execution evidence. | Operations owner plus `doc-writer`; Runbook execution evidence remains Task/operations-owned. |
| Retrieve precise information | Stage 03 Specs and child contracts, Stage 05 Policies, Stage 90 References, generated reference data, and canonical runtime/configuration owners. | **Implemented as typed surfaces.** Stage 90 and generated indexes are advisory; runtime truth must be read from its direct owner. | Artifact's stage owner; generated files use their named generator. |
| Understand reasons and trade-offs | Stage 02 ADRs for decisions; bounded explanatory sections in Guides, research References, and other approved artifacts. | **Partial.** ADRs explain decisions, not every concept; Stage 90 analysis cannot become policy by explanation alone. | Architecture owner for decisions; the owning stage for non-decision explanation. |

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

## Scope Implications

| Scope | Documentation-architecture implication |
| --- | --- |
| `agentic` | Agents should classify the immediate reader need while continuing to obey Stage 00 authority, provider loading, permissions, and evidence boundaries. |
| `architecture` | ADRs can serve bounded explanation of decisions; architecture requirements and Specs remain lifecycle contracts rather than Diataxis folders. |
| `backend` | No current backend application surface was established by the foundation baseline; future API tutorials/how-tos/reference/explanation require an approved backend lifecycle chain. |
| `common` | Shared naming, links, formatting, review, and diff hygiene apply across all modes; they do not prove semantic mode fit. |
| `docs` | Direct owner of mode-aware authoring. Use mapped templates and canonical paths; do not create empty quadrant directories. |
| `entry` | Gateway readers may need task procedures, configuration reference, and rationale, but current routing stays with the declared infra/entry owners. |
| `frontend` | The current Storybook fixture does not prove a product documentation set; future learning or goal content needs product and accessibility evidence. |
| `infra` | Compose/config reference, operational how-to, and topology explanation must remain separate from live runtime proof and secret state. |
| `meta` | Profiles and headings can encode artifact roles, but a future reader-mode field would need a Stage 00/99 contract and semantic validation design. |
| `mobile` | No current mobile source surface was established; all four modes are not applicable until an approved mobile product surface exists. |
| `ops` | Guides and Runbooks are the clearest goal-oriented surfaces; Policies stay control/reference oriented, and incidents/postmortems retain evidence roles. |
| `product` | Product owners define the reader, learning or task outcome, and acceptance need before documentation implementation. |
| `qa` | Structural validators check profile conformance; tutorial success, how-to completion, reference accuracy, and explanatory understanding need mode-specific review or execution evidence. |
| `security` | Keep procedures, control reference, threat rationale, and training content distinct; none authorizes secret-value access or weakens redaction. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Diataxis rendered site](https://diataxis.fr/) | 2026-08-08T17:14:35+09:00 | External mutable | **UNVERIFIED page body**: HTTP 429, `cf-mitigated: challenge`; no content claims used. |
| [Diataxis upstream source](https://github.com/evildmp/diataxis-documentation-framework/tree/957c09ca40b4a1edc23874f713e01937d50d54d5/source) | 2026-08-08 | External fixed at pinned revision | Verified through GitHub API/raw source; `index.rst`, `map.rst`, four mode files, and `how-to-use-diataxis.rst` read directly. |
| [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) | 2026-08-08 | Workspace tracked | Canonical stage, language, and advisory-reference boundary. |
| [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) | 2026-08-08 | Workspace tracked | Canonical authoring, routing, and validation owner. |
| [SDLC document roles](./sdlc-document-roles.md) | 2026-08-08 | Workspace tracked draft | Current twelve-role lifecycle analysis; does not itself change policy. |
| [Metadata lifecycle](./document-metadata-lifecycle.md) | 2026-08-08 | Workspace tracked draft | Current profile/lifecycle evidence boundary. |
| [Scope application matrix](./scope-application-matrix.md) | 2026-08-08 | Workspace tracked draft | Fourteen-scope applicability and catalog reachability. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace tracked stale/advisory | Built from `f8a72211`; not used as proof. |

## Maintenance

Reopen the rendered Diataxis site and repin the upstream repository when its
model or adoption guidance changes. Re-evaluate the workspace mapping when
stage roles, templates, profiles, guide/runbook contracts, or reader-facing
routes change. Keep access failures explicit and never replace an inaccessible
source with inherited claims.

## Related Documents

- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [LLM Wiki system](./llm-wiki-system.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
