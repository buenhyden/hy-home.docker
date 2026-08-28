---
profile_id: task
status: active
artifact_id: task-0137-0004
artifact_type: task
parent_ids:
  - SPEC-0137
  - plan-0137
created: 2026-08-23
updated: 2026-08-28
---

# Task: Canonical Agentic Engineering Research Refresh

## Objective

Author and check the approved pre-acceptance `RES-0002` draft on the research
branch only. Final acceptance and integration remain deferred until SPEC-0153
Task 9 has independently established and merged its Stage 90 structure into
`main` and the unchanged final gates pass.
This Task owns research content and its evidence only; it never owns Task 9,
Stage 90 migration mechanics, protected runtime or remote observation, or the
cleanup of another worktree.

## Current Draft State

On 2026-08-28 the user approved the Spec/Plan/Task exception to create README
and the twenty listed leaves before Task 9 acceptance, without accepting,
editing, or merging Task 9, and with `SDLCDOC-ADR-002` and `SDLCDOC-ADR-003`
remaining `UNVERIFIED`. SPEC-0137's Approved Pre-Acceptance Draft Exception
and the Plan's Current Draft Execution section are the current authority.
The earlier blocked-content instructions and retry sequence retained below
describe their pre-exception publication points, not the current draft gate.
The source observations remain evidence; their dates and failure states are
not rewritten by this exception.

Task 1C is published at `2e1dc25935728c7d26388db72bc8b20e42cf2fe7`, the draft
entry commit. Its six VERIFIED and two UNVERIFIED page records are retained;
no more network requests or retries are authorized. The 2026-08-23 roster is
not proof of per-claim observation. Historical source-backed synthesis retains
its actual dates, including Task 0001's 2026-08-08 source ledger and
2026-08-09 V&V evidence. Diataxis retains its 2026-08-08 access and pin
`957c09ca40b4a1edc23874f713e01937d50d54d5`. Roster-only assertions remain
`UNVERIFIED`; local facts require read-only tracked-source corroboration.
Older ADR material and synthesis must not repair the two unresolved claims.

The only content target is the Spec's exact 21-file set under
`docs/90.references/research/0002-agentic-engineering-research-pack/` in
`codex/0137-agentic-research-refresh`. README keeps `RES-0002` as a draft
research document. Each new generic-reference leaf uses the exact
`reference:agentic-engineering-research-draft:<filename-stem>` artifact ID to
avoid the twenty existing protected dated-pack IDs. This is not Task 9
identity acceptance or a new RES allocation; final identity reconciliation
is deferred. Metadata dates measure actual local draft work, never refetch.
No parent routing, generator, dated pack, other worktree, script, test, memory,
runtime, remote, or protected authority is changed.

| Current unit | State at this publication point |
| --- | --- |
| D0 — Spec/Plan/Task exception | Previous published unit at `264a6d1d64a41c329cd86b5978fb47f38503673f` — `docs(plan): permit isolated research draft authoring`; its original in-tree Not Run record is historical. External rules/specification and documentation-quality reviews were C0/I0/M0, with controller approval. |
| D1 — foundation: README, workspace baseline, scope matrix | Previous published unit at `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` — `docs(research): establish isolated draft foundation`. Its corrected external rules/specification (`/root/draft_d1_rules_review`) and documentation-quality (`/root/draft_d1_quality_review`) reviews were C0/I0/M0, with controller approval; original in-tree Not Run terminal rows are historical. |
| D2 — four harness/provider/instruction leaves | Previous published unit at `4481e73d433f6738e0e09b9e94977d4a2ac127cf` — `docs(research): analyze harness and provider controls`. Corrected external rules/specification (`/root/draft_d2_rules_review`) and documentation-quality (`/root/draft_d2_quality_review`) reviews were C0/I0/M0, with controller C0/I0/M0; its original in-tree Not Run terminal row is historical. |
| D3 — four model/catalog/memory leaves | Previous published unit at `29d947b4bec58bec35d8555c27f2b3550634fe43` — `docs(research): analyze models agents and memory`; corrected `/root/draft_d3_rules_review`, `/root/draft_d3_quality_review`, and controller reviews were all C0/I0/M0. |
| D4 — five SDLC/docs/wiki leaves and composition reconciliation | The initial work and its sole correction are exhausted historical attempts with nonauthorizing terminal reviews; one user-approved additional narrow correction is in progress against Plan-only publication `63fb97f20fdbeb5474873fd19b97a32104938288`. It edits only README, matrix, metadata lifecycle, SDLC roles, and this Task. Both unresolved ADR claims remain `UNVERIFIED`; D4 terminal review is Not Run in-tree/external. |
| D5 — three delivery/quality leaves | Not Run. |
| D6 — two infrastructure/security leaves | Not Run. |
| D7 — complete draft reconciliation | Not Run; passing means draft checks only, not readiness or final acceptance. |

Use a fresh doc-writer for every content unit, independent rules/specification
and quality review at C0/I0/M0, and controller final review before each logical
commit. The ordinary maximum is two attempts: initial work and one narrower
correction, then stop. The Plan's current exception permits only D4 extra
correction 1; the user approved that same correction on 2026-08-28 and no
further retry. Publish only actual unit evidence; terminal verdicts remain
`Not Run` in-tree and are bound externally to the reviewed tree. No file
mutation follows terminal review before commit. The Plan's exact scoped
metadata, local-link, census, aggregate, eight-scope, citation, ADR-gap, and
six-edge checks replace no final acceptance gate.

The retained all-pages-VERIFIED `DELTA_AUDIT` is `Not Run` for this approved
draft, not relabeled PASS. Task 9 acceptance/synchronization, the full
manifest-backed six-suite freeze and ladder, readiness, final integration,
finishing, and cleanup are deferred and `Not Run`. This Task remains active;
the old final-acceptance prerequisites are unchanged.

## Inputs

The following inputs describe the Task 1C publication baseline. Current draft
permission is the explicit exception above, not a change to those observations.

| Input | Observed state on 2026-08-28 Asia/Seoul |
| --- | --- |
| Approved specification | `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` at `68354fc8e92658a53043a9a8242397d48c4f6caf`; explicit user approval and independent rules/specification and documentation-quality final C0/I0/M0. Original Spec evidence remains below. |
| Active execution plan | `docs/03.specs/0137-agentic-research-pack-rebuild/plan.md` at approved retry-plan commit `c501ee371547540b3e7368b0d9f76e6811b08b16`; Task 1A is committed at `5b3fdaf7d3cfa9742e77efe4b8c1dc018b5ef072`, and Task 1B remains the historical publication. Task 1C governs this separate five-page reobservation. |
| Structural dependency | `docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0009-references.md`; owner-branch implementation `49522aa1d782838706bd558b8e139b107918ffee` is bound by completed Task evidence at frozen snapshot `2b5fa6f7b4299e23972717204cc6b678eb688be4` (last Task-path touch `9ef889b516dd03fc32ff850f7bec33fb59d760bc`). Neither owner-branch completion nor its C0/I0/M0 implementation reviews prove acceptance on `main`; no dirty owner worktree was inspected or absorbed. |
| Content destination | `docs/90.references/research/0002-agentic-engineering-research-pack/`; absent at literal main `d6cac43d77653e833732ec589f333db333222e07` and retry-plan commit `c501ee371547540b3e7368b0d9f76e6811b08b16`. Content and synchronization remain `BLOCKED`. |
| Branch and main snapshots | Research branch `codex/0137-agentic-research-refresh` was clean at Task 1A entry, HEAD `5cb154a00173088011dad15eb5f50bb87bde57c9`. Newly observed `task1a_main_snapshot_commit` is `d6cac43d77653e833732ec589f333db333222e07`; it happens to equal the Plan's historical comparison. Preserved Task-8-derived baseline remains `0c841b086cd1e6adc2c1ca53ce14eec309fe8f47`. |
| Graph evidence | `graphify-out/GRAPH_REPORT.md` was built from `f8a72211`; it is stale and advisory and requires corroboration against tracked sources and current governance. |
| Preserved external-source baseline | 2026-08-23 observations and fixed pins remain unchanged. External research was read-only and did not observe secrets, provider entitlement, live runtime state, or remote enforcement. `DOCARCH-DIATAXIS-BASE-001` is preserved, outside the seven delta claims, and grants no refetch. |
| Architecture-practice delta observation | The first three C4 observations are retained from Task 1B. Under the approved narrow correction, the remaining five roster URLs were each reobserved exactly once on 2026-08-28 Asia/Seoul after date/origin preflight: six active pages are `VERIFIED` and two are `UNVERIFIED`. Source-backed claims C4, arc42, and ADR role are `VERIFIED`; ADR lifecycle and relationships remain `UNVERIFIED`; synthesis remains `Not Run`. No research content was authored. |

## Work Log

| Date | Unit | Observed result |
| --- | --- | --- |
| 2026-08-23 | External research | Five read-only research clusters completed for harness/loop/providers, agents/models/memory, SDLC/docs/wiki, delivery/QA/V&V, and Compose/infra/security. No research file was authored or modified. |
| 2026-08-23 | Spec correction | Commit `11fda02484c78df957156bfd27228851e764116d` aligned SPEC-0137 with `RES-0002`, the eight-scope axis, Stage 03 ownership, and the independent Task 9 boundary. |
| 2026-08-23 | Spec review | Independent rules/specification and documentation-quality reviews both returned C0/I0/M0. |
| 2026-08-23 | Dependency check | The Task 9 worktree remained uncommitted and independently owned; `RES-0002` was absent from this branch. Content authoring is `BLOCKED` pending an accepted Task 9 merge to `main`. |
| 2026-08-23 | User scheduling ruling | The user approved eventual research integration and cleanup, but scheduled main-branch integration and cleanup only after the Task 9 worktree is completed and merged to `main`. No merge or cleanup was performed. |
| 2026-08-23 | Authority-correction validation | Focused metadata and diff check passed. Traceability remained FAIL on one inherited over-size historical Task finding; no PASS claim was made. |
| 2026-08-23 | Plan/Task review R1 — initial | Rules C0/I2/M0; quality C0/I4/M0. Failed, did not authorize commit, and its findings were corrected before R2. |
| 2026-08-23 | Plan/Task review R2 — corrected | Rules C0/I1/M0; quality C0/I2/M0. Failed, did not authorize commit, and its findings were corrected before R3. |
| 2026-08-23 | Plan/Task review R3 — next | Rules C0/I1/M0; quality C0/I0/M0. Failed because the pair was nonzero, did not authorize commit, and its findings were corrected before R4. |
| 2026-08-23 | Plan/Task review R4 — acceptance | Rules C0/I0/M0; quality C0/I1/M0. The round label did not make the nonzero pair approved; it failed, did not authorize commit, and its findings were corrected before R5. |
| 2026-08-23 | Plan/Task review R5 — absolute-final preliminary | Rules C0/I0/M0; quality C0/I3/M0. Failed, did not authorize commit, and its findings were corrected before R6. |
| 2026-08-23 | Plan/Task review R6 — terminal attempt | Rules C0/I1/M0; quality C0/I0/M0. Failed and did not authorize commit. Its then-current correction and next-review wording is superseded historical context, not the verdict for this Task 1A unit. |
| 2026-08-28 | Historical authority identity | Original Plan/Task authority-correction commit resolved to `796f92f58d1c491a804d600fd90a65f858267d06`. Git identity alone does not establish its terminal verdict; R1–R6 remain failed historical reviews. |
| 2026-08-28 | Approved architecture Spec | `68354fc8e92658a53043a9a8242397d48c4f6caf` — `docs(spec): extend architecture research scope`; explicit user approval and final independent dual C0/I0/M0. |
| 2026-08-28 | Plan correction | `5cb154a00173088011dad15eb5f50bb87bde57c9` committed exactly `plan.md` after the review sequence below closed all findings. Preserved baseline and conditional delta remain separate. |
| 2026-08-28 | Task 1A dependency observation | Literal main snapshot `d6cac43d77653e833732ec589f333db333222e07`, Spec base, and Plan HEAD have no canonical pack. Task 9 completion is owner-branch-only; main acceptance, synchronization, content, integration, and cleanup remain blocked. |
| 2026-08-28 | Task-only ledger alignment — historical Task 1A | This unit records already observed evidence and binds future execution to the committed Plan. No Spec/Plan, historical Task, Task 9, source content, runtime, or external system was changed; no delta request occurred. Executed Task 1A validation and reruns passed metadata and diff checks; traceability/alignment remained inherited FAIL/non-PASS with zero attributable findings, as recorded below. The external exact-tree execution report binds these recorded outcomes after the mandatory final-text rerun without another self-recording edit; terminal review remains external. |
| 2026-08-28 | Task 1A publication completed | `5b3fdaf7d3cfa9742e77efe4b8c1dc018b5ef072` — `docs(task): align canonical research delta ledger`; final full reviews plus scoped closure left both independent seats C0/I0/M0, with no edit after terminal review before commit. This is the Task 1B entry HEAD. |
| 2026-08-28 | Task 1B closed-roster invocation | Controller issued eight sequential no-shell curl GETs in one Python process, once per literal Plan row, after eight closed-environment `date +%F` results of `2026-08-28` and exact mapping/origin/descendant checks. Process exit 0 is executor completion only. No redirects, retries, substitute URLs, browser, second HTTP client, or linked-page requests occurred. Per-page outcomes and digests are below. |
| 2026-08-28 | Task 1B capture limitation | Tool output was truncated (28,219 original tokens against a 22,000-token output limit), losing the ADR-LIFECYCLE JSON record/body. Its request and date preflight occurred between ADR-ROLE and ADR-RELATIONSHIPS, but its exact timestamp, status, exit, headers and digests were not retained. It is `UNVERIFIED`; no retry was made. The other seven raw records remained only in transient controller memory for analysis/review; no raw bytes are committed. |
| 2026-08-28 | Task 1B source sufficiency | C4's notation page and ADR-ROLE returned 404; arc42 returned an unfollowed 301; ADR-LIFECYCLE evidence was lost; ADR-RELATIONSHIPS returned a decision index insufficient for its required relationship boundary. All five source-backed claims remain `UNVERIFIED`. Task 6 remains blocked by page verification and the separate structural dependency. |
| 2026-08-28 | Task 1B focused validation | Metadata PASS (`selected=1 violations=0`); traceability FAIL (1 inherited finding) and alignment FAIL (42 inherited findings), attributable 0. Diff/whitespace and exact-path exclusion checks passed. The final-text rerun is bound externally without another evidence edit; terminal review remains Not Run in-tree. |
| 2026-08-28 | Task 1C approved reobservation | The approved retry Plan at `c501ee371547540b3e7368b0d9f76e6811b08b16` authorized exactly five corrected URLs. Controller completed each once, in roster order, after the required 2026-08-28 preflight and closed-environment identity checks. No retry, redirect follow, linked-page request, or alternative source occurred. |
| 2026-08-28 | Task 1C dependency recheck | `main` resolved to `d6cac43d77653e833732ec589f333db333222e07`; the canonical destination census was empty on that commit and on the retry Plan commit. Task 9 implementation `49522aa1d782838706bd558b8e139b107918ffee` is not an ancestor of main (exit 1), which is expected non-ancestry rather than a PASS. |
| 2026-08-28 | Task 1C focused validation | Exact stable draft check: metadata PASS (`selected=1 violations=0`); traceability FAIL (1 inherited finding) and alignment FAIL (42 inherited findings), attributable 0. Scoped whitespace, exact-path, clean-exclusion, and memory-only record-consistency checks passed. Terminal review remains external. |
| 2026-08-28 | Task 1C publication completed | Published as `2e1dc25935728c7d26388db72bc8b20e42cf2fe7` — `docs(task): record architecture delta reobservations`. The earlier in-tree Not Run terminal-review row preserves that publication point; no new verdict is inferred from the commit identity. |
| 2026-08-28 | Approved branch-only draft exception | The user approved Spec/Plan/Task correction and subsequent creation of only README plus twenty research leaves before Task 9 acceptance, retaining both unresolved ADR claims as `UNVERIFIED`. No Task 9 acceptance, change, synchronization, merge, or new external request is authorized. This D0 unit changes only the three authority/evidence files. Initial checks are recorded below; final-tree rerun and terminal review remain Not Run. |
| 2026-08-28 | D4 SDLC/docs draft | Five D4 leaves, README aggregates, and the scope matrix were authored from retained evidence and tracked local files at `29d947b4bec58bec35d8555c27f2b3550634fe43`. Six architecture-practice pages remain VERIFIED and ADR-LIFECYCLE plus ADR-RELATIONSHIPS remain `UNVERIFIED`; composition is evidence-limited advisory synthesis. No source request, generator, runtime, or protected authority was used. The initial work and sole correction's terminal reviews are historical and nonauthorizing. |
| 2026-08-28 | Plan-only D4 correction authority | User approval was repeated for the same one additional narrow D4 correction, with no further retry. The Plan-only publication `63fb97f20fdbeb5474873fd19b97a32104938288` — `docs(plan): authorize one additional D4 correction` — records that authority; current D4 extra correction 1 is in progress and its terminal review remains Not Run in-tree/external. |

## Architecture Practice Delta Observations

| Page key | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams/notation` | 2026-08-28 | VERIFIED |
| `ARC42-OVERVIEW` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview/` | 2026-08-28 | VERIFIED |
| `ADR-ROLE` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | 2026-08-28 | VERIFIED |
| `ADR-LIFECYCLE` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |

## Architecture Practice Delta Evidence Records

The first three retained records below are unchanged historical observations from
`2643d9b9008f21d472e998039cd37b8ceb421109`. Their old missing-notation wording
in the separately preserved Task 1B evidence is historical observation context,
not the current combined C4 conclusion.

### C4-INTRODUCTION

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/introduction`
- Page title: Introduction | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 supports software-architecture communication during up-front design and retrospective documentation through progressively detailed views. Its uses include onboarding, architecture review, and risk or threat analysis.
- Supported page-level propositions:

  1. C4 helps teams communicate software architecture during design and documentation.
  2. Its progressive views are system context, container (applications/data stores), component, and code.

- Limitations and caveats: Mutable page observed only on the recorded date; no revision is stated. The page does not establish a lifecycle or approval contract, local adoption, entitlement, or runtime execution. Page-level sufficiency does not settle the four-page C4 claim.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-ABSTRACTIONS

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/abstractions`
- Page title: Abstractions | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 models static structure through nested abstractions, starting with people using software systems and progressing through containers, components, and code elements.
- Supported page-level propositions:

  1. People use software systems; systems contain containers, and containers contain components.
  2. Containers represent applications or data stores; components comprise code elements such as classes, interfaces, objects, or functions.

- Limitations and caveats: Mutable page; no revision is stated. A C4 container is not automatically a Docker container. Mapping these abstractions to this workspace is local interpretation, not proof of adoption or runtime behavior. No notation-page evidence is supplied here.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-DIAGRAMS

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/diagrams`
- Page title: Diagrams | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 uses four static diagram levels and supplementary views. Teams select useful levels rather than drawing every level; system-context and container diagrams are often sufficient.
- Supported page-level propositions:

  1. The static levels are system context, container, component, and code.
  2. Supporting diagram types include system landscape, dynamic, and deployment views.
  3. Teams need only the levels useful for their communication needs.

- Limitations and caveats: Mutable page; no revision is stated. It mandates neither every level nor a local review gate. This view taxonomy does not substitute for the missing required notation-page guidance; navigation links were not requested.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-NOTATION

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/diagrams/notation`
- Page title: Notation | C4 model
- Publisher: C4 model
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 notation is notation-independent. A standalone diagram should state its type and scope, include a legend, expand abbreviations, identify elements and responsibilities, show relevant technology, and label directed relationships and inter-container protocols. Consistent colour use and accessibility matter; UML is possible but has text and tool limitations.
- Supported page-level propositions:

  1. C4 diagrams should be understandable in isolation through type/scope context, a legend, and expanded abbreviations.
  2. Containers and components should identify their technology, while directed relationships convey labels and relevant protocol detail.

- Limitations and caveats: Mutable page with no stated revision. This is notation guidance, not a mandatory local gate, runtime/adoption proof, or a substitute for the C4 diagram taxonomy. Combined with the retained three C4 sub-boundaries, it makes the mapped C4 claim VERIFIED.
- Very short excerpt: Omitted; paraphrase is sufficient

### ARC42-OVERVIEW

- Claim ID: `DOCARCH-ARC42-001`
- Direct URL: `https://arc42.org/overview/`
- Page title: arc42 Template Overview - arc42
- Publisher: arc42
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: arc42 answers what and how to document and communicate architecture through a tailorable twelve-section template: introduction/goals, constraints, context/scope, solution strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality, risks/debt, and glossary. Building blocks refine hierarchically; important decisions belong in section 9 unless described elsewhere, and detailed documents may be linked.
- Supported page-level propositions:

  1. arc42 defines a twelve-section architecture communication template.
  2. The template includes hierarchical building-block refinement and an architectural-decisions section.

- Limitations and caveats: Mutable page with no stated revision. Linked detailed documents were not visited. The tailorable overview does not mandate equal granularity or prove local adoption or complete implementation of every section.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-ROLE

- Claim ID: `SDLCDOC-ADR-001`
- Direct URL: `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html`
- Page title: Use Markdown Architectural Decision Records | MADR
- Publisher: MADR
- Observed version or revision marker: MADR 4.0.0 chosen option; not independently established as the latest release
- Paraphrased evidence summary: MADR records a project decision to use a structured, lean, maintainable Markdown format for architecture, code, and other decisions. It treats explicit assumptions and later understanding as reasons for the choice, and compares MADR with Nygard, Y-statement, and formless alternatives.
- Supported page-level propositions:

  1. MADR is a structured Markdown format for recording architecture and related decisions.
  2. The page presents explicit assumptions and future maintainability as decision-record motivations.

- Limitations and caveats: This is MADR's own decision and does not create a universal mandate or prove local adoption. Its observed version marker is a chosen option, not independently verified release currency.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-LIFECYCLE

- Claim ID: `SDLCDOC-ADR-002`
- Direct URL: `https://adr.github.io/madr/decisions/0008-add-status-field.html`
- Page title: Add Status Field | MADR
- Publisher: MADR
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: The page considers whether and how a status field should be tracked, chooses YAML front matter, and compares several display styles. It shows on-hold and accepted examples and discusses a superseded-by identifier, including its per-ADR maintenance drawback, but does not define a complete lifecycle or supersession rule set.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: HTTP 200 transport and partial status observations are insufficient for this unchanged boundary, which requires lifecycle, status, and supersession. No other page is used to rescue or remap this row.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-RELATIONSHIPS

- Claim ID: `SDLCDOC-ADR-003`
- Direct URL: `https://adr.github.io/madr/`
- Page title: About MADR | MADR
- Publisher: MADR
- Observed version or revision marker: News observes MADR 4.0.0 dated 2024-09-17 and a rendered development template; neither is independently established as current release
- Paraphrased evidence summary: MADR defines an Architectural Decision as a justified design choice addressing an architecturally significant functional or non-functional requirement, and an ADR as its record with rationale. It discusses neighbouring documents, decision categories, Markdown linting, a template, and proposed/rejected/accepted/deprecated/superseded statuses, but does not establish the requested relationship to an Architecture Description or Spec.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: `AD` means Architectural Decision, not Architecture Description. Generic requirements and local `ARD` interpretation do not prove the specified artifact relationship; this page cannot be conflated with it.
- Very short excerpt: Omitted; paraphrase is sufficient

## Historical Task 1B Architecture Practice Delta Evidence Records

The following preserved Task 1B evidence records, outcomes, and transport
observations are historical only and point to
`2643d9b9008f21d472e998039cd37b8ceb421109`; they are not extra active rows.
The active records above supersede only the five corrected roster observations.

| Page key | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- |
| `C4-INTRODUCTION` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/introduction` | 2026-08-28 | VERIFIED |
| `C4-ABSTRACTIONS` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/abstractions` | 2026-08-28 | VERIFIED |
| `C4-DIAGRAMS` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/diagrams` | 2026-08-28 | VERIFIED |
| `C4-NOTATION` | `DOCARCH-C4-001` | `https://c4model.com/` | `https://c4model.com/notation` | 2026-08-28 | UNVERIFIED |
| `ARC42-OVERVIEW` | `DOCARCH-ARC42-001` | `https://arc42.org/` | `https://arc42.org/overview` | 2026-08-28 | UNVERIFIED |
| `ADR-ROLE` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0001-record-architecture-decisions.html` | 2026-08-28 | UNVERIFIED |
| `ADR-LIFECYCLE` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/` | 2026-08-28 | UNVERIFIED |

### C4-INTRODUCTION

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/introduction`
- Page title: Introduction | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 supports software-architecture communication during up-front design and retrospective documentation through progressively detailed views. Its uses include onboarding, architecture review, and risk or threat analysis.
- Supported page-level propositions:

  1. C4 helps teams communicate software architecture during design and documentation.
  2. Its progressive views are system context, container (applications/data stores), component, and code.

- Limitations and caveats: Mutable page observed only on the recorded date; no revision is stated. The page does not establish a lifecycle or approval contract, local adoption, entitlement, or runtime execution. Page-level sufficiency does not settle the four-page C4 claim.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-ABSTRACTIONS

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/abstractions`
- Page title: Abstractions | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 models static structure through nested abstractions, starting with people using software systems and progressing through containers, components, and code elements.
- Supported page-level propositions:

  1. People use software systems; systems contain containers, and containers contain components.
  2. Containers represent applications or data stores; components comprise code elements such as classes, interfaces, objects, or functions.

- Limitations and caveats: Mutable page; no revision is stated. A C4 container is not automatically a Docker container. Mapping these abstractions to this workspace is local interpretation, not proof of adoption or runtime behavior. No notation-page evidence is supplied here.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-DIAGRAMS

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/diagrams`
- Page title: Diagrams | C4 model
- Publisher: C4 model (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: C4 uses four static diagram levels and supplementary views. Teams select useful levels rather than drawing every level; system-context and container diagrams are often sufficient.
- Supported page-level propositions:

  1. The static levels are system context, container, component, and code.
  2. Supporting diagram types include system landscape, dynamic, and deployment views.
  3. Teams need only the levels useful for their communication needs.

- Limitations and caveats: Mutable page; no revision is stated. It mandates neither every level nor a local review gate. This view taxonomy does not substitute for the missing required notation-page guidance; navigation links were not requested.
- Very short excerpt: Omitted; paraphrase is sufficient

### C4-NOTATION

- Claim ID: `DOCARCH-C4-001`
- Direct URL: `https://c4model.com/notation`
- Page title: Not stated
- Publisher: Not stated
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: The sole request returned HTTP 404. No returned content was analyzed as notation evidence.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: Required notation guidance, consistency expectations, and limitations are unavailable from this roster row. No alternative path was requested; the other three C4 pages cannot substitute for it.
- Very short excerpt: Omitted; paraphrase is sufficient

### ARC42-OVERVIEW

- Claim ID: `DOCARCH-ARC42-001`
- Direct URL: `https://arc42.org/overview`
- Page title: Not stated
- Publisher: Not stated
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: HTTP 301 supplied the exact Location value `/overview/`. The redirect was not followed and its body was not used as architecture-template evidence.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: The target resolves locally to `https://arc42.org/overview/`, a same-origin descendant retaining the mapped claim, but is unrostered and was not requested. Purpose, structure, granularity, and limitations remain unverified. A reviewed Plan correction is required before any target request.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-ROLE

- Claim ID: `SDLCDOC-ADR-001`
- Direct URL: `https://adr.github.io/madr/decisions/0001-record-architecture-decisions.html`
- Page title: Not stated
- Publisher: Not stated
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: The sole request returned HTTP 404. No returned content was analyzed as ADR role or decision-scope evidence.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: Neither role nor decision scope is established by this response; no alternative decision page or external link was requested.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-LIFECYCLE

- Claim ID: `SDLCDOC-ADR-002`
- Direct URL: `https://adr.github.io/madr/`
- Page title: Not stated
- Publisher: Not stated
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: The request occurred after its successful 2026-08-28 date preflight, but executor output truncation lost the response record/body. HTTP status, exit, Location, exact timestamp, and all three digests are unavailable; no response or lifecycle claim is inferred.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: This is evidence-capture failure, not an observed HTTP failure or success. Lifecycle, status, and supersession cannot be assessed. The executed no-follow argv establishes no redirect was followed, not what response arrived. No retry was made.
- Very short excerpt: Omitted; paraphrase is sufficient

### ADR-RELATIONSHIPS

- Claim ID: `SDLCDOC-ADR-003`
- Direct URL: `https://adr.github.io/madr/decisions/`
- Page title: Decisions | MADR
- Publisher: MADR (site identification)
- Observed version or revision marker: Not stated
- Paraphrased evidence summary: HTTP 200 returned MADR's own decision index with template and general ADR links. This body does not support the required ADR-to-Architecture Description/Spec relationship, so transport success is insufficient.
- Supported page-level propositions: None; page is UNVERIFIED
- Limitations and caveats: A decision index is not evidence for the mapped relationship. No linked page was followed; links between ADRs would not by themselves establish relationships to Architecture Description or Spec. The historical `ARD` distinction remains local interpretation, not an upstream-standard claim.
- Very short excerpt: Omitted; paraphrase is sufficient

## Historical Task 1B Architecture Practice Delta Transport Evidence

These are observations of the controller's actual requests, not commands to
rerun. The eight-row table above binds each page key to its literal URL, claim,
family, and actual request date. Every request passed that exact mapping and
same-origin descendant check immediately before invocation. Each closed-env
`date +%F` returned `2026-08-28`; its `TZ` was `Asia/Seoul`. Each GET used
`subprocess.run` without a shell, `timeout=30`, `check=False`, and
`capture_output=True`, with this exact replacement environment and no added
or inherited keys:

```json
{"LC_ALL":"C","LANG":"C","TZ":"Asia/Seoul","PATH":"/usr/bin:/bin"}
```

The exact per-page argv follows; each contains one literal URL only:

```text
C4-INTRODUCTION: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://c4model.com/introduction"]
C4-ABSTRACTIONS: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://c4model.com/abstractions"]
C4-DIAGRAMS: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://c4model.com/diagrams"]
C4-NOTATION: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://c4model.com/notation"]
ARC42-OVERVIEW: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://arc42.org/overview"]
ADR-ROLE: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/decisions/0001-record-architecture-decisions.html"]
ADR-LIFECYCLE: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/"]
ADR-RELATIONSHIPS: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/decisions/"]
```

No redirect was followed on any row, including ADR-LIFECYCLE; this follows
from the executed no-follow transport, not a reconstructed response. All seven
retained header parses reported `malformedHeaders=False` with no multiple
response block. `None` below means observed absence; `Unavailable` means lost
evidence and is never an absence claim. Only retained 2xx/no-Location bodies
were analyzed for their approved page sub-boundary.

| Page key | Actual request timestamp (Asia/Seoul) | Curl exit | HTTP status | Exact Location | Returned-body sufficiency |
| --- | --- | --- | --- | --- | --- |
| C4-INTRODUCTION | 2026-08-28T14:22:39.591307+09:00 | 0 | 200 | None | Sufficient for introduction only. |
| C4-ABSTRACTIONS | 2026-08-28T14:22:40.355621+09:00 | 0 | 200 | None | Sufficient for abstractions only. |
| C4-DIAGRAMS | 2026-08-28T14:22:41.163513+09:00 | 0 | 200 | None | Sufficient for diagram/view taxonomy only. |
| C4-NOTATION | 2026-08-28T14:22:41.977048+09:00 | 0 | 404 | None | Ineligible; not analyzed. |
| ARC42-OVERVIEW | 2026-08-28T14:22:42.699928+09:00 | 0 | 301 | `/overview/` | Ineligible; unfollowed same-origin descendant redirect. |
| ADR-ROLE | 2026-08-28T14:22:43.385223+09:00 | 0 | 404 | None | Ineligible; not analyzed. |
| ADR-LIFECYCLE | Unavailable; request date 2026-08-28 established by preflight | Unavailable | Unavailable | Unavailable | Unavailable; response record/body lost to output truncation, including header-parse result. |
| ADR-RELATIONSHIPS | 2026-08-28T14:22:43.944904+09:00 | 0 | 200 | None | Insufficient; decision index does not establish the mapped relationships. |

All digests below are SHA-256 over the exact raw stdout/stderr or separated
returned body bytes, not over the paraphrases. For each of the seven retained
rows, stderr was empty with digest
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
ADR-LIFECYCLE's stderr bytes and digest are unavailable, not presumed empty.

| Page key | Raw stdout SHA-256 | Returned body SHA-256 |
| --- | --- | --- |
| C4-INTRODUCTION | `9ff3a51e1ce4135fc8af634638fe1d18c08426feaffee70239f58a1226673316` | `ce6cdd3c2ad63a43388f1b51e549866d7e22ca53a51bbb0857c443b2c9acca77` |
| C4-ABSTRACTIONS | `ee49e1f73cfc12aa25d9dbef0d8e366d0d043473470b2beb36055c061566b24a` | `055dbc8ccdea26bcd7393e653e67aa0c422c2a67317f80b41c6f191a12b4a561` |
| C4-DIAGRAMS | `2b4b4703afe1f47a8c1d1dc2315a2ad8b306938d0d26882eee3a0d6f8dab6121` | `4741275cee5c2b78ced67bc79554f1dad262fc0b5c444c66f47536e109c20f08` |
| C4-NOTATION | `8a3b6fc8da01a917d0f7feac2813be08b62bc969cb586bc50cd9f113adbd03b5` | `b620507312c5e97566a3c6cfaf99144fefc18a0da7d941401dfa0f5f58fb0368` |
| ARC42-OVERVIEW | `d27e98986a893d65bd73b222451b22a01aa6d414e87b72270a324cdb49d0d99f` | `0528b3e69b69d7f667f14565d3f301c132d74529632ad6d1321ac18d1660f18f` |
| ADR-ROLE | `34cf9bf5387bb7ad65ad1cecdbbbd8df5572f3b75c7cd723d5ac11bca04aadbc` | `b620507312c5e97566a3c6cfaf99144fefc18a0da7d941401dfa0f5f58fb0368` |
| ADR-LIFECYCLE | Unavailable; output truncation | Unavailable; output truncation |
| ADR-RELATIONSHIPS | `e6757d15815b52c03630724070549926790e1e4f649dca1ba2aa268c942f95df` | `4f694bccd0ef8ec89c0f40a1c8daa352dbed01bddf5773074eb6639f7a79d32d` |

User curl configuration and proxy influence were excluded by argv/environment.
The fixed-path curl executable, OS resolver/network stack, system CA/TLS trust,
remote server and network path remain the observation trust boundary. These
observations do not establish local adoption, runtime execution, entitlement,
Task 9 acceptance, or content authority. No raw stdout/stderr, header, or body
bytes are included in this publication.

## Architecture Practice Delta Transport Evidence

These five Task 1C observations used exactly one no-shell `subprocess.run`
curl GET per literal URL, with `timeout=30`, `check=False`, `capture_output=True`,
the closed environment below, and the Plan's no-follow argv. Each preflight,
exact roster mapping, origin, and descendant check passed immediately before
its request. No redirect, second client, follow-up request, alternate source,
or retry occurred. All five had exit 0, HTTP 200, no `Location`, no malformed
or multiple response header block, no transport error, and no capture failure.

```json
{"LC_ALL":"C","LANG":"C","TZ":"Asia/Seoul","PATH":"/usr/bin:/bin"}
```

Each complete ASCII JSON capture envelope was at most 16,000 characters, with
inner and outer output budgets of 20,000 tokens. The controller reconstructed
base64/zlib stdout and stderr, independently compared identity to the roster,
argv, and environment, then checked all lengths and SHA-256 digests plus body
separation/status before the next request. Wire character lengths, in order,
were 8640, 9032, 7042, 8085, and 14433; raw data was not committed.

```text
C4-NOTATION: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://c4model.com/diagrams/notation"]
ARC42-OVERVIEW: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://arc42.org/overview/"]
ADR-ROLE: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html"]
ADR-LIFECYCLE: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/decisions/0008-add-status-field.html"]
ADR-RELATIONSHIPS: ["curl","--disable","--noproxy","*","--silent","--show-error","--include","--max-time","30","--connect-timeout","10","--max-redirs","0","--proto","=https","--no-location","--compressed","--request","GET","https://adr.github.io/madr/"]
```

| Page key | Actual request timestamp (Asia/Seoul) | Curl exit | HTTP status | Exact Location | Returned-body sufficiency |
| --- | --- | --- | --- | --- | --- |
| C4-NOTATION | 2026-08-28T16:51:21.237526+09:00 | 0 | 200 | None | Sufficient for notation guidance and stated limitations. |
| ARC42-OVERVIEW | 2026-08-28T16:52:13.571085+09:00 | 0 | 200 | None | Sufficient for template structure and granularity. |
| ADR-ROLE | 2026-08-28T16:52:36.477843+09:00 | 0 | 200 | None | Sufficient for ADR role and decision scope. |
| ADR-LIFECYCLE | 2026-08-28T16:56:10.230598+09:00 | 0 | 200 | None | Insufficient for full lifecycle, status, and supersession boundary. |
| ADR-RELATIONSHIPS | 2026-08-28T16:56:33.518082+09:00 | 0 | 200 | None | Insufficient for Architecture Description/Spec relationship boundary. |

All stderr streams were empty (`length=0`, SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
Digests are over exact raw stdout or separated body bytes; raw response bytes,
headers, stdout, and stderr remain transient controller memory only.

| Page key | Stdout length | Raw stdout SHA-256 | Body offset | Body length | Returned body SHA-256 |
| --- | ---: | --- | ---: | ---: | --- |
| C4-NOTATION | 21713 | `48543571dd93a5f7f36bb3792fe09bf56d7dca93c0a51656168270beedd9e454` | 840 | 20873 | `09d636316f7ed85b756e18cc22abd087deb5b0f6c62c3b8f2162de46fd6f9bad` |
| ARC42-OVERVIEW | 18217 | `bd3af4a1ee83c8a54977fc66a16d1c7e6a2e8cf33cdf9ccee6084ea8cb07c31b` | 447 | 17770 | `3ebcee7fd69015054e75251cc2a4f9f432560f4e874c744c3c0ff530bd8bdef8` |
| ADR-ROLE | 15538 | `cd88a12c362ecb4f8b02caf47d768b3fe0780964e486ac7d42ca50584a8b9a72` | 726 | 14812 | `dd861e5916c4126b5044bac19c3ab50137f09fe8c8660c2c6fbb4ff9e5cc8401` |
| ADR-LIFECYCLE | 19502 | `e976ae629099e8aba2f0b0bf536c04920a1873eddaafeb80785357bca915b6e6` | 726 | 18776 | `1c8879c6ba8b37f1f519f10ee34bc12a144ab1b60ef548edcb4e1bb6b6382d53` |
| ADR-RELATIONSHIPS | 36111 | `ace9270ee610bffa65d4afe256d879ecf57bd8535e49fa9b6c46e4dced550f78` | 746 | 35365 | `7165f41f5912be85e4ee1b8aa826b20f016b3225f0fa5f1ec2c44d0b15334edf` |

The fixed-path curl executable, OS resolver/network stack, system CA/TLS trust
store, remote server, and network path remain the observation trust boundary.
These observations establish neither local adoption nor runtime, entitlement,
Task 9 acceptance, or content authority.

## Historical Task 1B Architecture Practice Delta Claim Outcomes

These original outcomes remain historical evidence from
`2643d9b9008f21d472e998039cd37b8ceb421109`; they are not current outcomes.

| Claim ID | State | Combined sufficiency or dependency |
| --- | --- | --- |
| `DOCARCH-C4-001` | UNVERIFIED | All four required pages evaluated together: three page-level successes cannot replace C4-NOTATION's HTTP 404. |
| `DOCARCH-ARC42-001` | UNVERIFIED | Required overview row redirected; target not requested. |
| `SDLCDOC-ADR-001` | UNVERIFIED | Required role row returned HTTP 404. |
| `SDLCDOC-ADR-002` | UNVERIFIED | Required lifecycle response evidence lost; no status or propositions recoverable. |
| `SDLCDOC-ADR-003` | UNVERIFIED | Required relationship row's HTTP 200 body is insufficient. |
| `DOCARCH-COMP-001` | Not Run | Synthesis-only; no request authorized or made, source inputs unverified and content blocked. |
| `SCOPE-COMP-001` | Not Run | Synthesis-only; no request authorized or made, prerequisite claims/content blocked. |

## Architecture Practice Delta Claim Outcomes

| Claim ID | State | Combined sufficiency or dependency |
| --- | --- | --- |
| `DOCARCH-C4-001` | VERIFIED | All four required C4 sub-boundaries are now supported: retained introduction, abstractions, and diagrams plus Task 1C notation. |
| `DOCARCH-ARC42-001` | VERIFIED | The corrected overview page supports its required template, section, granularity, and limitation boundary. |
| `SDLCDOC-ADR-001` | VERIFIED | The corrected MADR decision page supports ADR role and decision scope. |
| `SDLCDOC-ADR-002` | UNVERIFIED | Status observations alone do not establish the required lifecycle and supersession boundary. |
| `SDLCDOC-ADR-003` | UNVERIFIED | The MADR overview does not establish the required Architecture Description/Spec relationship. |
| `DOCARCH-COMP-001` | Not Run | Synthesis-only; no request authorized or made, and content remains blocked. |
| `SCOPE-COMP-001` | Not Run | Synthesis-only; no request authorized or made, and content remains blocked. |

The active roster has six verified pages and two unverified pages. Task 6's
every-page-VERIFIED gate still fails independently of the structural/content
block. No failed observation is promoted to a research source row; no further
source request, content authoring, synchronization, merge, or cleanup is
authorized by this publication.

## Verification Evidence

The controller executed these initial D0 checks before this evidence edit.
They do not claim a pass for the final publication tree. Its required rerun and
terminal review remain Not Run in-tree and must be bound externally after the
evidence is finalized. No external request, scratch file, or other write was
made by these checks.

| D0 initial check | Observed result |
| --- | --- |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 2e1dc25935728c7d26388db72bc8b20e42cf2fe7 --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/spec.md --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/plan.md --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md` | PASS, exit 0; `selected=3 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| `python3 scripts/validation/check-document-links.py --mode traceability` | FAIL/non-PASS, exit 1; `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`. The Task 0001 `document-not-regular` finding is identical to clean entry; inherited 1, attributable 0. |
| `python3 scripts/validation/check-document-links.py --mode alignment` | FAIL/non-PASS, exit 1; the same corpus counters with `failures=42`. The controller compared all 42 exact finding lines with clean entry: no added, changed, or removed finding; inherited 42, attributable 0. |
| Scope, index, and whitespace | `git diff --check` exit 0. Changed-name/status and worktree status contain only the three authorized modified files; the index is empty. The `git diff --quiet HEAD` exclusion check for all paths except those three exits 0. |
| D0 pack census | 0 files; no research content was created, as required for D0. |

The historical rows below retain their observed publication-point results.
Inherited failures remain raw FAIL/non-PASS, not final acceptance.

| Check | Observed result |
| --- | --- |
| Focused corrected-Spec metadata | PASS; zero violations. |
| Corrected-Spec whitespace check | `git diff --check` PASS. |
| Full repository contract on the Task-8-derived branch | FAIL, `failures=13`; this is a pre-existing baseline result and is not called PASS. |
| Research-content file census | No `RES-0002` content exists in this branch; content phase remains `BLOCKED`. |
| Authority-correction focused metadata | PASS, exit 0: base `11fda02484c78df957156bfd27228851e764116d`, `selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Authority-correction traceability | FAIL, exit 1: exactly `document-not-regular` for `tasks/tsk-0001-rebuild.md`; summary `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`. Classified inherited because the base blob was 2,242,358 bytes and already exceeded the 2 MiB checker ceiling; the current file is 2,242,656 bytes after only metadata/Overview disposition edits. This is not PASS. |
| Authority-correction whitespace check | `git diff --check` exit 0. |
| Plan-only metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 68354fc8e92658a53043a9a8242397d48c4f6caf --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/plan.md`: PASS, exit 0, `selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Plan-only traceability | `python3 scripts/validation/check-document-links.py --mode traceability`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`; unchanged Task 0001 `document-not-regular`, attributable 0. |
| Plan-only alignment | `python3 scripts/validation/check-document-links.py --mode alignment`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=42`; every finding path outside changed Plan, attributable 0. |
| Plan-only scope and whitespace | `git diff --quiet HEAD -- . ':(exclude)docs/03.specs/0137-agentic-research-pack-rebuild/plan.md'` exit 0 proved all other files unchanged, supporting inherited classification above; `git diff --check` exit 0. Only Plan was changed, staged, and committed. Inline audit AST parse and relative/absolute URL-guard positive/negative checks passed. |
| Task 1A main census | `git ls-tree -r --name-only d6cac43d77653e833732ec589f333db333222e07 -- docs/90.references/research/0002-agentic-engineering-research-pack`: exit 0, empty output; canonical pack absent. |
| Task 1A Spec-base census | `git ls-tree -r --name-only 68354fc8e92658a53043a9a8242397d48c4f6caf -- docs/90.references/research/0002-agentic-engineering-research-pack`: exit 0, empty output; canonical pack absent. |
| Task 1A Plan-HEAD census | `git ls-tree -r --name-only 5cb154a00173088011dad15eb5f50bb87bde57c9 -- docs/90.references/research/0002-agentic-engineering-research-pack`: exit 0, empty output; canonical pack absent. |
| Task 1A Task 9-to-main ancestry | `git merge-base --is-ancestor 49522aa1d782838706bd558b8e139b107918ffee d6cac43d77653e833732ec589f333db333222e07`: exit 1, empty output; expected non-ancestry, not validator PASS or acceptance. |
| Task 1A Task 9-to-research ancestry | `git merge-base --is-ancestor 49522aa1d782838706bd558b8e139b107918ffee 5cb154a00173088011dad15eb5f50bb87bde57c9`: exit 1, empty output; expected non-ancestry, not validator PASS or acceptance. |
| Task 9 frozen owner-snapshot ancestry | `git merge-base --is-ancestor 49522aa1d782838706bd558b8e139b107918ffee 2b5fa6f7b4299e23972717204cc6b678eb688be4`: exit 0; owner-branch lineage only. Implementation-commit Task metadata was active; the later frozen snapshot carries completed metadata and binds that implementation. |
| Observed Task 1A validation — metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 5cb154a00173088011dad15eb5f50bb87bde57c9 --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md`: PASS, exit 0, `selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Observed Task 1A validation — traceability | `python3 scripts/validation/check-document-links.py --mode traceability`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`; unchanged Task 0001 `document-not-regular`, attributable 0. |
| Observed Task 1A validation — alignment | `python3 scripts/validation/check-document-links.py --mode alignment`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=42`; every finding path outside changed Task 0004, attributable 0. |
| Observed Task 1A validation — scope and whitespace | `git diff --check` exit 0; `git diff --name-only` and `git status --short` exit 0 and list only Task 0004. `git diff --quiet HEAD -- . ':(exclude)docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md'` exit 0 proves all other files unchanged, supporting inherited classification above. |
| Task 1A exact-tree evidence binding | The results above are actual observed validation outcomes, including executed reruns. The final exact-tree execution report binds the recorded outcomes to the mandatory rerun after this text is finalized, without another self-recording edit. Terminal review remains Not Run in-tree and external; no file mutation follows that review before commit. |
| Observed Task 1B validation — metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 5b3fdaf7d3cfa9742e77efe4b8c1dc018b5ef072 --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md`: PASS, exit 0, `selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Observed Task 1B validation — traceability | `python3 scripts/validation/check-document-links.py --mode traceability`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`; unchanged Task 0001 `document-not-regular`, attributable 0. |
| Observed Task 1B validation — alignment | `python3 scripts/validation/check-document-links.py --mode alignment`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=42`; every finding path outside changed Task 0004, attributable 0. |
| Observed Task 1B validation — scope and whitespace | `git diff --check -- docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md` exit 0; `git diff --name-only` and `git status --short` exit 0 and list only Task 0004. `git diff --quiet HEAD -- . ':(exclude)docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md'` exit 0 proves all other files unchanged, supporting inherited classification. |
| Task 1B exact-tree evidence binding | The preceding results are actual observed validation outcomes, including executed reruns. The final exact-tree execution report binds those recorded outcomes to the mandatory final-text rerun without another self-recording edit. Terminal review remains Not Run in-tree/external. |
| Observed Task 1C validation — metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref c501ee371547540b3e7368b0d9f76e6811b08b16 --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md`: PASS, exit 0, `selected=1 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Observed Task 1C validation — traceability | `python3 scripts/validation/check-document-links.py --mode traceability`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1`; only unchanged Task 0001 `document-not-regular`, attributable 0. |
| Observed Task 1C validation — alignment | `python3 scripts/validation/check-document-links.py --mode alignment`: FAIL/non-PASS, exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=42`; all finding paths are outside Task 0004, attributable 0. |
| Observed Task 1C validation — scope and whitespace | `git diff --check -- docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md` exit 0; `git diff --name-only` and `git status --short` list only Task 0004. `git diff --quiet HEAD -- . ':(exclude)docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md'` exit 0 proves all other files unchanged, supporting inherited classification. |
| Observed Task 1C consistency check | Memory-only check exit 0, `failures=0`: active eight-row/evidence cardinality, mappings/states, exact retained first-three rows/subsections, historical failed-five subsections, nine labels, actual timestamps/digests/lengths, and seven claim states. No generated output, files, or network access. |
| Task 1C exact-tree evidence binding | The outcomes above were executed against stable draft blob `1881aa897a6a5788c7d4886bc0bc291649bcb3fa`, with the same blob before and after. The mandatory final-text rerun binds them externally without another evidence edit; terminal review remains Not Run in-tree/external. |
| Task 6 DELTA_AUDIT | Not Run in this Task-only unit; its content-file inputs are blocked, and two page states fail its every-page-VERIFIED precondition. No successful audit or authoring permission is inferred from the complete request count. |
| Post-Task9 synchronization and frozen ladder | Not Run; Task 9 owner-branch completion is observed, but canonical acceptance and the destination remain absent from `main`. |
| D1 initial focused metadata check | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 264a6d1d64a41c329cd86b5978fb47f38503673f --changed-path docs/90.references/research/0002-agentic-engineering-research-pack/README.md --changed-path docs/90.references/research/0002-agentic-engineering-research-pack/workspace-baseline.md --changed-path docs/90.references/research/0002-agentic-engineering-research-pack/scope-application-matrix.md --changed-path docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md`: PASS, exit 0; `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| D1 initial whitespace and scope check | `git diff --check --` on the four D1 paths: PASS, exit 0. `git diff --name-only` showed only the Task among tracked changes; `git status --short` showed the one authorized untracked pack directory. Final regular-file census, local-link, ID, and scope-table checks remain to run after this evidence text is final. |
| D1 initial focused content snapshot | Read-only inline census/identity check: PASS, exit 0; `census=3 regular_non_symlink=3 scope_rows=8+8 leaf_claim_ids=4`. The three regular pack files are exactly README, workspace baseline, and scope matrix. |
| D1 local Markdown path check | Read-only inline Markdown-destination check: PASS, exit 0; `local_markdown_destinations=30 missing=0` across the three pack files and Task. |
| D1 focused final-text pre-rerun | Explicit four-path metadata command: PASS, exit 0; `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0`. Scoped `git diff --check` also passed, exit 0. Terminal review remains Not Run; rerun follows this evidence text without a later mutation. |
| D1 controller post-freeze checks | Explicit four-path metadata with baseline `264a6d1d64a41c329cd86b5978fb47f38503673f`: PASS, exit 0; `selected=4 violations=0 legacy_exceptions=0 transition_overrides=0`. Direct checks: `3` files, `4` claims, `5` sources, `8` scope rows per leaf, `30` local destinations, `0` missing; `git diff --check` exit 0. `python3 scripts/validation/check-document-links.py --mode traceability` and `python3 scripts/validation/check-document-links.py --mode alignment` were FAIL/non-PASS, exit 1, with inherited baselines respectively `failures=1` and `failures=42`, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0`; exact finding sets equal D0, introduced/worsened `0`. No PASS interpretation is made. |
| D2 initial focused metadata check | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` with explicit README, four D2 leaves, and this Task `--changed-path` arguments: PASS, exit 0; `selected=6 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| D2 initial direct content inspection | PASS, exit 0: exactly `7` regular non-symlink pack files; `20` unique claim IDs and `21` unique source IDs across the six leaves; README aggregate has no missing or extra leaf IDs; every leaf has `8` scope rows; local Markdown destinations missing=`0`; scoped `git diff --check` passed. |
| D2 inherited aggregate link checks | `check-document-links.py --mode traceability`: FAIL/non-PASS, exit 1, `documents=359 links=2472 failures=1`; `--mode alignment`: FAIL/non-PASS, exit 1, `documents=359 links=2472 failures=42`. These equal the inherited D1 baseline; introduced/worsened findings=`0`. Neither result is interpreted as PASS. |
| D2 terminal focused rerun and review | Not Run in-tree. Rerun the explicit six-path metadata command and scoped whitespace check after this final evidence text, then bind fresh independent review and controller approval externally without a later mutation. |
| D2 corrected focused checks | Explicit six-path metadata command: PASS, exit 0; `selected=6 violations=0 legacy_exceptions=0 transition_overrides=0`. Direct inspection: `7` regular non-symlink pack files, `26` unique claims, `30` unique sources, README aggregate missing/extra=`0`, eight scope rows per leaf, and local Markdown destinations missing=`0`; scoped `git diff --check` passed. Traceability/alignment remain inherited FAIL/non-PASS, exit 1, at `documents=359 links=2472 failures=1/42`, exact finding sets equal D1 and introduced/worsened=`0`. Initial `20`/`21` counts above remain the pre-correction snapshot. |
| D2 corrected terminal rerun and review | Not Run in-tree. Rerun the explicit six-path metadata command, direct inspection, link commands, and scoped whitespace check after this final evidence text; fresh independent review and controller approval bind the exact frozen tree externally. |
| D3 terminal focused rerun and review | Historical pre-publication Not Run record. The corrected D3 frozen tree was then independently reviewed at C0/I0/M0 and published at `29d947b4bec58bec35d8555c27f2b3550634fe43`; no current D3 review is pending. |
| D3 focused pre-rerun checks | Historical pre-publication record: explicit six-path metadata with baseline `4481e73d433f6738e0e09b9e94977d4a2ac127cf` passed (`selected=6 violations=0 legacy_exceptions=0 transition_overrides=0`); direct inspection counted `11` regular non-symlink pack files, `42` unique claims, `45` unique sources, README aggregate missing/extra=`0`, and eight scope rows per leaf. Scoped `git diff --check` passed; traceability/alignment were inherited FAIL/non-PASS, exit 1, at `documents=359 links=2472 failures=1/42`, introduced/worsened findings=`0`. |
| D3 initial review and sole correction | Historical pre-publication review: `/root/draft_d3_rules_review` was C0/I0/M1, `/root/draft_d3_quality_review` was C0/I0/M0, and controller C0/I0/M1. The sole correction added the MH-004 advisory domain-partition/lifecycle boundary; corrected external rules, quality, and controller reviews were all C0/I0/M0 before publication. |
| D4 initial metadata check | Historical initial-authoring check: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 29d947b4bec58bec35d8555c27f2b3550634fe43` with all eight explicit D4 owned paths passed, `selected=8 violations=0`. It does not consume current extra correction 1; its terminal review remained Not Run in-tree. |
| D4 initial work and sole correction reviews | Historical and nonauthorizing: initial findings were rules C0/I6/M3, quality C0/I4/M2, controller C0/I7/M2; the sole correction's terminal reviews were rules C0/I2/M2 and quality C0/I3/M2. These exhausted the ordinary two attempts. The user-approved Plan-only exception at `63fb97f20fdbeb5474873fd19b97a32104938288` permits exactly current extra correction 1, not another retry. |
| D4 prior sole-correction focused checks | Historical prior sole-correction evidence: metadata with literal base `29d947b4bec58bec35d8555c27f2b3550634fe43` and all eight owned paths passed, `selected=8 violations=0`; traceability and alignment were inherited FAIL/non-PASS, exit 1, at `documents=359 links=2472 failures=1/42`; scoped `git diff --check` passed. Direct inspection confirmed the closed eight scopes, six composition links, eight-row composition projection (six VERIFIED and two UNVERIFIED delta pages), and local Markdown destinations. |
| Plan-only correction checks | Actual Plan-only evidence: metadata against base `29d947b4bec58bec35d8555c27f2b3550634fe43` selected `1` with `violations=0`; `git diff --check` exited 0; traceability/alignment exited 1 with inherited `1`/`42` failures, `documents=359 links=2472`, and no exact old finding added or removed; all eight initial D4 paths were unchanged. These checks did not consume D4 extra correction 1. |
| D4 extra correction 1 controller checks | Actual controller results against base `63fb97f20fdbeb5474873fd19b97a32104938288`: explicit eight-path metadata passed, exit 0, `selected=8 violations=0 legacy_exceptions=0 transition_overrides=0`; direct memory-only inspection passed, exit 0, `files=16 claims=69 sources=68 local_links=255 errors=[]`; composition passed, exit 0, `architecture_scopes=8 composition_edges=6 errors=[]`; direct-page projection passed, exit 0, `pages=8 verified=6 unverified=2 errors=[]`; scoped `git diff --check` passed. Traceability and alignment were inherited FAIL/non-PASS, raw exit 1, `documents=359 links=2472 catalog_pairs_total=46 archive_direct_links_total=15 removed_template_mentions_total=0 failures=1/42`; exact findings had no added, removed, or worsened entry. The three immutable new-leaf hashes were unchanged; status was the exact original eight paths, index empty, and ignored directory entries unchanged. Terminal review remains Not Run in-tree/external. |

Later evidence is appended only after execution. Each result records the exact
command, baseline or range, exit status, selected path count, and attributable
versus inherited findings. A tracked workflow or configuration proves only
repository adoption; it does not prove remote enforcement or a successful run.

## Review Evidence

D0 is the previous published unit at
`264a6d1d64a41c329cd86b5978fb47f38503673f`; its original in-tree Not Run
record is historical, while its external rules/specification and
documentation-quality reviews and controller approval are C0/I0/M0. D1 is
now published at `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f`; its original
in-tree Not Run terminal rows are historical. D2's corrected external rules/
specification and documentation-quality reviews were C0/I0/M0, with controller
C0/I0/M0. D3's original Not Run rows are historical: its corrected tree was
published after external rules/specification, documentation-quality, and
controller reviews all returned C0/I0/M0. D4's ordinary two attempts are
historical and nonauthorizing; the precise current exception is recorded in
the D4 extra-correction row below.

| Review | Verdict |
| --- | --- |
| Corrected SPEC-0137 rules/specification review | C0/I0/M0. |
| Corrected SPEC-0137 documentation-quality review | C0/I0/M0. |
| Plan/Task R1 — initial | Failed pair: rules C0/I2/M0; quality C0/I4/M0. No commit authority; findings corrected before R2. |
| Plan/Task R2 — corrected | Failed pair: rules C0/I1/M0; quality C0/I2/M0. No commit authority; findings corrected before R3. |
| Plan/Task R3 — next | Failed pair: rules C0/I1/M0; quality C0/I0/M0. No commit authority; findings corrected before R4. |
| Plan/Task R4 — acceptance | Failed pair: rules C0/I0/M0; quality C0/I1/M0. Not approved despite the round label; no commit authority; findings corrected before R5. |
| Plan/Task R5 — absolute-final preliminary | Failed pair: rules C0/I0/M0; quality C0/I3/M0. No commit authority; findings corrected before R6. |
| Plan/Task R6 — terminal attempt | Failed pair: rules C0/I1/M0; quality C0/I0/M0. No commit authority; its then-current correction wording is superseded historical context. |
| Historical next fresh Plan/Task terminal publication review | Recorded as Not Run at the 2026-08-23 publication point; superseded as a prospective instruction. No terminal verdict for `796f92f58d1c491a804d600fd90a65f858267d06` is inferred from Git. |
| Architecture Spec correction — final | Rules/specification C0/I0/M0; documentation-quality C0/I0/M0; explicit user approval for `68354fc8e92658a53043a9a8242397d48c4f6caf`. |
| Architecture Plan — initial | Failed pair: rules C0/I3/M1; quality C0/I5/M0. No commit authority. |
| Architecture Plan — fix1 | Failed pair: rules C0/I3/M0; quality C0/I4/M0. No commit authority. |
| Architecture Plan — fix2 | Failed pair: rules C0/I5/M0; quality C0/I5/M1. No commit authority. |
| Architecture Plan — fix3 | Failed pair: rules C0/I0/M0; quality C0/I4/M0. No commit authority. |
| Architecture Plan — fix4 full review | Rules C0/I0/M0 (`/root/plan0137_rules_final_review`); quality C0/I1/M0 (`/root/plan0137_quality_final_review`). Nonzero pair remained nonauthorizing pending closure. |
| Architecture Plan — fix5 scoped closure | Rules C0/I0/M0 (`/root/plan0137_link_fix_rules_review`); quality C0/I0/M0 (`/root/plan0137_link_fix_quality_review`), closing the absolute-path link guard. Combined with the full reviews, no finding remained open before Plan commit `5cb154a00173088011dad15eb5f50bb87bde57c9`. |
| Retry Plan — initial review | Rules/specification C0/I1/M0 and documentation-quality C0/I1/M0. Both seats identified the mandatory capture-limit metadata validation finding; no commit authority before its scoped correction. |
| Retry Plan — final review | Following one scoped correction, fresh rules/specification and documentation-quality reviews both returned C0/I0/M0 for `c501ee371547540b3e7368b0d9f76e6811b08b16`. |
| Task 1A terminal publication review | Not Run in-tree; fresh rules/specification and documentation-quality exact-tree verdicts remain external, with no later file mutation before commit. |
| Task 1A completed external review — previous unit | Final full reviews plus scoped closure: rules/specification C0/I0/M0 and documentation-quality C0/I0/M0 for `5b3fdaf7d3cfa9742e77efe4b8c1dc018b5ef072`. The preceding Not Run row preserves the historical publication point; no edit followed terminal review before that commit. |
| Task 1B delta-observation terminal review | Not Run in-tree; eight actual requests and durable observation records are published above. Fresh independent final-tree reviews remain external, with no later mutation before commit. |
| Task 1C reobservation terminal review | Not Run in-tree; controller must execute validators, obtain fresh independent exact-tree reviews, and commit without a later Task mutation. |
| D0 published-unit review | External rules/specification C0/I0/M0 and documentation-quality C0/I0/M0; controller approved `264a6d1d64a41c329cd86b5978fb47f38503673f`. The original in-tree Not Run row is historical. |
| D1 initial review | Rules/specification C0/I0/M2 and documentation-quality C0/I0/M2. Nonauthorizing; this one narrower correction addresses the two identified items. |
| D1 corrected publication review | External rules/specification C0/I0/M0 (`/root/draft_d1_rules_review`) and documentation-quality C0/I0/M0 (`/root/draft_d1_quality_review`), with controller approval before `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f`. The original Not Run row is historical. |
| D2 initial review | Rules/specification C0/I0/M1 and documentation-quality C0/I1/M1; nonauthorizing. The sole narrower correction adds retained, source-bound mechanics and fixes instruction-source ownership. |
| D2 corrected terminal review | Not Run externally; fresh independent review must bind the corrected frozen D2 tree without a later mutation. |
| D2 corrected publication review | External rules/specification C0/I0/M0 (`/root/draft_d2_rules_review`) and documentation-quality C0/I0/M0 (`/root/draft_d2_quality_review`), with controller C0/I0/M0 before `4481e73d433f6738e0e09b9e94977d4a2ac127cf`. The original Not Run row is historical. |
| D3 corrected publication review | Rules/specification C0/I0/M0 (`/root/draft_d3_rules_review`), documentation-quality C0/I0/M0 (`/root/draft_d3_quality_review`), and controller C0/I0/M0 before `29d947b4bec58bec35d8555c27f2b3550634fe43`; its prior Not Run record is historical. |
| D3 terminal review | Historical pre-publication Not Run record; no current D3 review is pending after the published C0/I0/M0 external and controller reviews. |
| D4 initial and sole-correction reviews | Historical and nonauthorizing: initial rules C0/I6/M3, quality C0/I4/M2, controller C0/I7/M2; sole-correction terminal rules C0/I2/M2 and quality C0/I3/M2. |
| D4 extra correction 1 review | The user approved this one additional narrow correction on 2026-08-28 and repeated approval for the same correction only. Plan publication `63fb97f20fdbeb5474873fd19b97a32104938288` was independently reviewed: initial rules/quality C0/I0/M0, then controller C0/I0/M1 corrected once; final rules `/root/draft_d4_extra_plan_rules`, quality `/root/draft_d4_extra_plan_quality`, and controller C0/I0/M0 bind Plan blob `91dc202a85c65f330b595f3aba7d4ef1d03ea5d8`. Current D4 extra correction 1 terminal review is Not Run in-tree/external; any nonzero terminal finding stops without retry. |
| D4–D7 research unit reviews | D4 extra correction 1 terminal review is Not Run; D5-D7 are Not Run. |
| Final exact-range rules/specification/quality review | Not Run. |
| Branch-readiness terminal publication review | Not Run; the final-tree verdict and resulting readiness commit ID are external handoff evidence. |
| Main-completion terminal publication review | Not Run; the final Task-only verdict is external handoff evidence. |

No implementation unit advances when a Critical, Important, or Minor finding
remains. Review evidence never substitutes for validator evidence.

For every Task 0004 evidence publication, validators rerun after the tracked
evidence is finalized, then fresh reviewers inspect that exact final tree. The
terminal verdict is reported only in the external execution handoff/commit
evidence, and no file mutation follows before commit. A tracked `Not Run` row is
therefore truthful and does not weaken the external C0/I0/M0 commit gate.

Path-scoped validators must exit zero. Repository- and corpus-wide validators
retain raw status: a non-final logical unit may advance only with zero
attributable findings, while inherited findings remain explicitly FAIL/non-PASS.
On the exact readiness commit and on the final merged tree, every applicable
full-ladder command must exit zero. An inherited nonzero blocks main merge,
completion, and cleanup pending its owner or a separately approved boundary
change.

## Commit Ledger

| Logical unit | Commit | State |
| --- | --- | --- |
| Correct canonical research Spec | `11fda02484c78df957156bfd27228851e764116d` — `docs(spec): align canonical agentic research contract` | Committed and dual-reviewed C0/I0/M0. |
| Read-only external research | No commit | Complete as advisory input; no content authored. |
| Reset Plan/Task authority — historical | `796f92f58d1c491a804d600fd90a65f858267d06` | Resolved original authority-correction identity; terminal verdict not established by Git identity. R1–R6 remain failed historical evidence. |
| Extend architecture research Spec | `68354fc8e92658a53043a9a8242397d48c4f6caf` — `docs(spec): extend architecture research scope` | Committed, explicitly approved, and independently dual-reviewed C0/I0/M0. |
| Align architecture research Plan | `5cb154a00173088011dad15eb5f50bb87bde57c9` — `docs(plan): align architecture research delta` | Committed Plan-only unit; full reviews plus scoped closure leave C0/I0/M0 and no open finding. |
| Correct architecture delta retry Plan | `c501ee371547540b3e7368b0d9f76e6811b08b16` — `docs(plan): correct architecture delta source retry` | Committed after initial independent dual C0/I1/M0 identified mandatory capture-limit metadata validation, one scoped correction, and final independent dual C0/I0/M0. |
| Align canonical research Task ledger | `5b3fdaf7d3cfa9742e77efe4b8c1dc018b5ef072` — `docs(task): align canonical research delta ledger` | Previous Task-only unit committed after final full/scoped independent dual C0/I0/M0; no edit after terminal review before commit. |
| Observe closed architecture delta | `2643d9b9008f21d472e998039cd37b8ceb421109` — `docs(task): record architecture delta observations` | Historical Task 1B publication: eight requests observed, three pages VERIFIED and five UNVERIFIED. Its tracked Not Run terminal-review row is a historical publication point; Git identity/published state does not establish a terminal verdict. |
| Reobserve corrected architecture delta | `2e1dc25935728c7d26388db72bc8b20e42cf2fe7` — `docs(task): record architecture delta reobservations` | Published previous Task 1C unit; five corrected URLs were observed once, yielding six active VERIFIED pages and two UNVERIFIED pages. Its original terminal-review record remains external. |
| D0 — permit isolated research draft authoring | `264a6d1d64a41c329cd86b5978fb47f38503673f` — `docs(plan): permit isolated research draft authoring` | Previous published unit. Its original in-tree Not Run terminal row is historical; external dual C0/I0/M0 and controller approval establish its publication review. |
| D1 — establish isolated draft foundation | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` — `docs(research): establish isolated draft foundation` | Previous published unit after corrected independent dual C0/I0/M0 and controller approval; no later mutation is attributed to its terminal review. |
| D2 — analyze harness and provider controls | `4481e73d433f6738e0e09b9e94977d4a2ac127cf` — `docs(research): analyze harness and provider controls` | Previous published unit after corrected independent dual C0/I0/M0 and controller C0/I0/M0; no later mutation is attributed to its terminal review. |
| D3 — analyze models agents and memory | `29d947b4bec58bec35d8555c27f2b3550634fe43` — `docs(research): analyze models agents and memory` | Previous published unit after corrected external rules/specification, documentation-quality, and controller reviews all returned C0/I0/M0; original in-tree Not Run rows are historical. |
| Plan-only — authorize one additional D4 correction | `63fb97f20fdbeb5474873fd19b97a32104938288` — `docs(plan): authorize one additional D4 correction` | Published authority only. Initial independent dual review was C0/I0/M0; controller C0/I0/M1 was corrected once, then final rules, quality, and controller C0/I0/M0 bind Plan blob `91dc202a85c65f330b595f3aba7d4ef1d03ea5d8`. |
| D4 — isolated draft unit | No commit yet | Current extra correction 1 only; its initial work and sole correction are exhausted historical attempts. Terminal review Not Run in-tree/external. D5-D7 remain Not Run; final acceptance/integration are deferred. |
| Bind accepted post-Task9 main baseline | No commit | Blocked pending canonical Task 9 acceptance on `main` and the exact destination census; owner-branch completion alone is insufficient. |
| Research content and integration units | No commits | Blocked pending the baseline gate. |
| Record research-branch readiness | No commit | Not Run; Task remains active; expected title `docs(task): record canonical research readiness`. The resulting self-identity and terminal verdict are recorded externally, not by mutating this Task after review. |
| Readiness-HEAD finishing gate | No commit by design | Not Run; invoke `superpowers:finishing-a-development-branch` and require every applicable full-ladder command to exit zero on the exact readiness commit before main merge. |
| Record post-merge completion on main | No commit | Not Run; only after merged-tree gates; expected title `docs(task): complete canonical research integration`. |
| Terminal completion-HEAD cleanup gate | No commit by design | Not Run; the full applicable ladder must exit zero on the Task completion commit, and results are reported without creating a self-recording evidence commit. |
| Research branch/worktree cleanup | No commit | Explicitly deferred until the terminal completion-HEAD gate is green. |

## Rulings

The following pre-exception rulings remain history or deferred final gates.
Current Draft State overrides only their pre-authoring block; it grants no
Task 9 acceptance, synchronization, retry, final acceptance, or cleanup.

- This Task is active as the sole prospective SPEC-0137 execution ledger, while
  its content phase is `BLOCKED`; active status does not imply executable
  content authority before the dependency gate passes.
- Tasks 0001, 0002, and 0003 are cancelled historical records. Their retained
  bodies do not authorize future work and are not reclassified as completed.
- Future synchronization follows committed Plan Task 2 exclusively: first
  prove canonical Task 9 acceptance and the exact census on a captured literal
  main commit, then prepare its literal-target `--no-commit --no-ff` merge.
  Validate and independently review the uncommitted merge tree before its
  dedicated commit; prove the reviewed tree and ordered literal parents, then
  revalidate and publish the separate baseline-evidence unit. No current
  synchronization is authorized. Rebase, reset, checkout-based restoration,
  history rewriting, and changes to Task 9 are forbidden.
- If the accepted `main` does not contain both the Task 9 acceptance evidence
  and the canonical `RES-0002` destination, stop. Do not create the destination
  from this Task.
- Any conflict while merging post-Task9 `main` is terminal before the research
  baseline is frozen. Do not resolve any conflicted path; request a new
  synchronization Plan and authority. Content edits begin only after a
  conflict-free merge and recorded baseline.
- `RES-0002/README.md` selects the Stage 99 research profile and owns navigation
  plus the aggregate claim, source, requirement, and eight-scope matrices.
  Leaf rows own detail and must reconcile exactly with the README aggregates.
- Research claims distinguish upstream capability, tracked local adoption, and
  observed runtime or remote proof. Documentation availability never proves
  provider entitlement, model availability, execution, or enforcement.
- Stage 90 is advisory. Stage 04 has no authority, Operations paths are
  prefixless, and ordinary delivery evidence belongs to Task plus Git/PR rather
  than a standalone Release document role.
- No container/runtime, provider entitlement, remote enforcement, secret,
  credential, or private state is accessed by this Task. Public source-page
  observations are confined to the preserved baseline and approved delta;
  unavailable evidence is recorded as `UNVERIFIED`.
- Parent Stage 90 routers, generators, dated packs, and Task 9 remain outside
  this Task after synchronization; this Task never absorbs their ownership.
- Each logical content cluster has one implementer, independent rules/spec and
  quality review, exact focused validation, and its own Conventional Commit.
- Evidence publication is finalized before the terminal fresh exact-tree
  review. That verdict and the resulting commit identity stay in the external
  Task 0004 execution handoff; no file mutation occurs between review and
  commit, and this Task never self-records its own commit hash.
- The sole future validator authority is committed Plan Task 2's reviewed
  freeze from the accepted tree's literal `scripts/manifest.yaml` and actually
  available manifest-backed argv, mapped to all six ADR-0029 responsibilities:
  `document-contract`, `document-graph`, `document-lifecycle`, `operations`,
  `agent-governance`, and `repository-integrity`. Freeze command IDs/order,
  exact argv, raw exits/summaries, and deterministic five-field identities
  under the Plan's comparison contract. Missing mapping, entrypoint or argv
  drift, or ambiguous topology requires reviewed Plan correction. Every skip
  remains `Not Run` with rationale. The pre-sync aggregate and its historical
  `FAIL failures=13` are diagnostic only, never a prospective fallback or PASS.
- Task 0004 remains active through research-branch merge. Main integration is
  allowed only after `superpowers:finishing-a-development-branch` verifies the
  exact readiness commit, post-Task9 main ancestry, clean state, and an actually
  green full ladder. An inherited nonzero remains FAIL and blocks before merge
  pending its owner or a separately approved boundary. Main integration is
  followed by merged-tree gates and a separate main-worktree Task evidence
  commit that records the merge and transitions Task 0004 to completed. Only
  after the full ladder also exits zero on that completion commit may the
  finishing-development-branch workflow remove this research worktree/branch.
  The terminal result is reported without another Task evidence commit. A
  terminal nonzero blocks cleanup and requires a separately reviewed lifecycle
  correction or approved revert. Task 9 and the legacy delta worktrees are
  preserved.
- Main integration follows committed Plan Task 10's literal-readiness protocol:
  clean `main`, exact accepted/frozen main identity, and an external literal
  readiness commit that exists and descends from that main identity. The final
  no-shell ancestry check and immediately following merge consume the same
  literal readiness commit, with no intervening observation or moving-ref
  resolution. Any mismatch stops before merge. The frozen ladder applies to
  final uncommitted publication trees and readiness, merged, and completion
  commits as specified there; this Task does not replace that protocol.
- The 2026-08-23 baseline and `DOCARCH-DIATAXIS-BASE-001` remain preserved with
  no refetch. The only delta claims are `DOCARCH-C4-001`, `DOCARCH-ARC42-001`,
  `SDLCDOC-ADR-001`, `SDLCDOC-ADR-002`, `SDLCDOC-ADR-003`, `DOCARCH-COMP-001`,
  and `SCOPE-COMP-001`. The committed retry Plan alone defines eight direct
  pages; the two synthesis-only claims authorize no request. Task 1C preserves
  Task 1B history and records the five approved corrected pages without
  changing the roster. C4, arc42, and ADR role are `VERIFIED`; ADR lifecycle
  and relationships are `UNVERIFIED`; synthesis remains `Not Run`.
- Every Task 1C request passed the authorized Asia/Seoul date and exact roster,
  origin, descendant, and no-follow preflight. The observed request date was
  `2026-08-28`, not inferred from authorization. The single narrower retry is
  consumed. Any further source/date/roster change requires separate reviewed
  authority and user direction; no content unit re-accesses sources.

## Deferred Items

This retained pre-exception list is not a block on the expressly approved
draft units. Structural/final gates and unresolved ADR evidence remain deferred;
only the README-plus-twenty-leaf draft authoring restriction is superseded.

- SPEC-0153 Task 9 is completed only in the frozen owner-branch evidence;
  independent acceptance on `main`, structural integration, parent routing,
  generator updates, and dated-pack disposition remain with its existing owner.
- The accepted post-Task9 `main` commit and new research baseline have not been
  frozen because canonical main acceptance and the exact destination are absent.
  Future synchronization and the manifest-backed six-responsibility freeze
  follow committed Plan Task 2; owner-branch evidence cannot substitute.
- The twenty-one `RES-0002` files are not authored until the dependency gate
  passes.
- Task 1A's prior external verdict is recorded above. Task 1C terminal review
  remains external to the tree it reviews and is currently `Not Run`; a commit
  still requires external C0/I0/M0 and no subsequent file mutation.
- Task 1C leaves two active pages and two source-backed claims `UNVERIFIED`.
  Task 6 is blocked by its every-page-VERIFIED gate and the independent
  structural gate. The narrower retry is consumed; no alternative or retry is
  authorized without separate reviewed authority and user direction.
- Historical Task 1B navigation evidence identified `/diagrams/notation` on
  C4-DIAGRAMS and `/madr/decisions/0000-use-markdown-architectural-decision-records.html`,
  `/madr/decisions/0008-add-status-field.html`, and
  `/madr/decisions/0009-support-links-between-adrs-inside-an-adrs.html` on
  ADR-RELATIONSHIPS. Task 1C subsequently requested the first three candidates:
  C4-NOTATION and ADR-ROLE are now `VERIFIED`; ADR-LIFECYCLE was requested but
  remains `UNVERIFIED` because its body is insufficient. Only the listed
  `0009-support-links-between-adrs-inside-an-adrs.html` candidate remains
  unrequested and unverified. This historical discovery grants no further
  access authority; a reviewed Plan correction must precede any new request.
  ADR-to-ADR links alone would not establish Architecture Description/Spec
  relationships.
- Post-sync validator execution is deferred to Plan Task 2's manifest-backed
  freeze. No historical aggregate or presumed suite runner selects future
  commands. Raw inherited failures remain FAIL/non-PASS; every applicable
  frozen command must actually exit zero before readiness integration,
  merged-main completion, and terminal cleanup.
- Main merge and current research branch/worktree cleanup are deferred exactly
  as scheduled by the user. Main merge first waits for the readiness-HEAD
  finishing gate to exit zero. Cleanup additionally waits for the terminal
  completion-HEAD full ladder to exit zero and never includes the Task 9 or
  legacy delta worktrees.
