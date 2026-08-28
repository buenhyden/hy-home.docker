---
profile_id: spec
status: active
artifact_id: SPEC-0137
artifact_type: spec
parent_ids:
  - ADR-0029
  - SPEC-0136
created: 2026-08-08
updated: 2026-08-28
---

# Agentic Engineering Research Pack Rebuild Specification

## Overview

SPEC-0137 governs research **content** for the canonical Stage 90 pack
`RES-0002`. It is advisory, English-only closed research: it may report
evidence and gaps, but cannot create policy, runtime, remote, security, or
provider truth. The content target is one README and twenty leaves at
`docs/90.references/research/0002-agentic-engineering-research-pack/`.

## Boundaries and Inputs

External evidence follows a two-snapshot provenance contract. The preserved
baseline record has a 2026-08-23 cutoff and workspace baseline
`0c841b086cd1e6adc2c1ca53ce14eec309fe8f47`; that record date does not establish
new source access. Retained evidence keeps its original observation dates.
One preserved, non-delta synthesis input is available:

| Input identity | Owning leaf | Retained evidence binding | Boundary |
| --- | --- | --- | --- |
| `DOCARCH-DIATAXIS-BASE-001` | `documentation-architecture.md` | SPEC-0137 Task 0001 `REQ-22`, `EXT-DIATAXIS`, and `EXT-DIATAXIS-SOURCE`, retained in the 2026-08-23 record; original access 2026-08-08, pin `957c09ca40b4a1edc23874f713e01937d50d54d5`. | Diataxis's four reader modes, incremental/no-empty-structure adoption guidance, and documented access limitations. |

`DOCARCH-DIATAXIS-BASE-001` authorizes no refetch and is excluded from the seven
delta claim IDs. The correction delta was exhaustively limited to this
Spec-owned claim and source-family allowlist. Its 2026-08-28 Asia/Seoul access
authority was consumed by Task 1C, published at
`2e1dc25935728c7d26388db72bc8b20e42cf2fe7`; no further request is authorized.

| Claim ID | Owning leaf | Permitted source family root or inputs | Claim boundary |
| --- | --- | --- | --- |
| `DOCARCH-C4-001` | `documentation-architecture.md` | `https://c4model.com/` | C4 purpose, abstraction/view model, notation/view use, limitations, and the prohibition on treating a C4 view as lifecycle or authority. |
| `DOCARCH-ARC42-001` | `documentation-architecture.md` | `https://arc42.org/` | arc42 purpose, architecture-documentation template/structure and granularity, limitations, and non-ownership of lifecycle or authority. |
| `SDLCDOC-ADR-001` | `sdlc-document-roles.md` | `https://adr.github.io/` | ADR role and decision scope. |
| `SDLCDOC-ADR-002` | `sdlc-document-roles.md` | `https://adr.github.io/` | ADR lifecycle, status, and supersession. |
| `SDLCDOC-ADR-003` | `sdlc-document-roles.md` | `https://adr.github.io/` | ADR relationships to Architecture Description and Spec plus the local historical `ARD` distinction. |
| `DOCARCH-COMP-001` | `documentation-architecture.md` | Only `DOCARCH-DIATAXIS-BASE-001`, the five preceding source-backed delta claims, and tracked workspace evidence. | Genuinely multi-practice comparison/composition; no new ADR-only proposition. |
| `SCOPE-COMP-001` | `scope-application-matrix.md` | Only the six preceding claims plus tracked workspace evidence. | Eight-scope applicability or non-applicability, adoption conditions, limitations, verification, and exact reciprocal cross-links. |

No additional delta claim ID, source family root, or owner is permitted, and no
other subject or existing baseline claim may be refreshed in this delta. A
direct source-page URL is an evidence URL that is a same-origin descendant of
its listed source family root and inherits that family; it is not an additional
source family. Before access, the corrected Plan must map each proposed direct
source-page URL to exactly one of the five source-backed claim IDs and its one
listed source family root. Cross-origin redirects and third-party linked
content are not authorized. The two synthesis inputs are not source families
and authorize no additional external source.

Every external request in the delta must occur on the currently authorized
date. Before the first request on any later date, work stops and both this Spec
and the corrected Plan must state that actual date, even if earlier requests
occurred on 2026-08-28. Each page's source row records its actual observed
access date and is never prefilled. This Spec does not claim that any source was
accessed or that the research is complete; no delta evidence may be relabeled
as 2026-08-23 evidence. Graphify `f8a72211` is stale and advisory; leads require
corroboration in tracked source, Stage 00 governance, and current stage
documents.

Evidence classes are external fixed, external mutable, tracked workspace
configuration, authorized runtime/remote observation, and historical retained
evidence. A claim must distinguish upstream capability, local adoption, and
observed execution. A source row records topic, claim ID, title, publisher,
direct URL, class, version/revision or observation time, access date, applicable
workspace path/target, and caveat. Unavailable evidence is `UNVERIFIED`, not a
substitute inference.

The closed scope axis is exactly the eight general Stage 00 role scopes:
`agentic`, `architecture`, `common`, `docs`, `infra`, `ops`, `qa`, and
`security`. Named agents and functions are owners or consumers, never extra
scope values. The README's aggregate requirement-by-scope matrix must give each
subject/category × scope cell exactly one value: `applies`,
`not-applicable (<reason>)`, or `historical-only (<reason>)`; blanks are invalid.

SPEC-0153 Task 9 is not accepted or owned here. It exclusively owns structural
Stage 90 migration: creation/rename disposition, parent router/index/generator
and cross-corpus route switch, and dated-pack deletion/cleanup. Both dated
packs, all Stage 90 routers/generators, Stage 00/05 authority, runtime/remote
state, and secrets are protected.

Tasks 0001–0003 retain cancelled overall Task status and no prospective
execution authority; their actually completed subunits and reviews remain
historical evidence. The corrected Plan's current draft section
and `tasks/tsk-0004-canonical-research-refresh.md` govern the exception below.
Plan and Task are co-located in Stage 03; Stage 04 has no authority.

### Approved Pre-Acceptance Draft Exception

On 2026-08-28 the user approved correcting Spec/Plan/Task to create the README
and twenty listed research leaves on the research branch before Task 9
acceptance, while retaining the two unresolved ADR claims as `UNVERIFIED`.
This exception permits only pre-acceptance `DRAFT` content in
`docs/90.references/research/0002-agentic-engineering-research-pack/` on
`codex/0137-agentic-research-refresh`. It does not accept, edit, merge, or assume
SPEC-0153 Task 9; its structural ownership and final acceptance remain intact.
No parent route/index/generator, dated pack, other worktree, runtime, script,
test, memory, or protected authority changes are permitted.

For this draft only, the exception supersedes the missing-target and
pre-authoring structural prerequisites in this Spec and the retained
pre-exception Plan/Task instructions. It does not waive the final Acceptance
Contract, authorize synchronization or integration, or make draft completion
Task completion. The Plan defines the bounded draft units and checks; its old
all-pages-VERIFIED `DELTA_AUDIT` is `Not Run` for this draft, never PASS.

Use retained evidence only. A source URL or the 2026-08-23 roster/date alone
does not establish an observed proposition. Retained historical synthesis
keeps its actual original provenance and dates; unavailable support is
`UNVERIFIED`. Current local facts require read-only corroboration in tracked
files. The committed 2026-08-28 Task 1C records retain six VERIFIED pages and
two UNVERIFIED pages. `SDLCDOC-ADR-002` and `SDLCDOC-ADR-003` remain literally
`UNVERIFIED` in Task 0004, their owning leaf, and README aggregates. Composition
may be explicitly evidence-limited; it must not assert missing lifecycle,
supersession, or Architecture Description/Spec relationship facts, including
through a synthesis claim. No refetch or other external request is authorized.

README uses the research profile, `artifact_id: RES-0002`,
`parent_ids: [SPEC-0137]`, and `status: draft`. Its `created`, `updated`, and
`observed_at` values record actual local draft work, not new external access.
Each leaf uses the existing generic-reference contract without `profile_id`,
`artifact_type: reference`, `parent_ids: []`, `status: draft`, actual
`reviewed_at`, and `review_cycle: on-source-change`. Its exact artifact ID is
`reference:agentic-engineering-research-draft:<filename-stem>`. These
collision-free draft IDs preserve the protected dated pack's existing IDs;
they neither allocate another RES number nor transfer Task 9 identities.
Any final identity reconciliation remains deferred to reviewed integration.

## Behavior Contract

The approved draft exception permits creating the following exact README and
twenty English leaves before canonical routing. Final route acceptance remains
independent:

| Area | Leaves |
| --- | --- |
| Baseline | `workspace-baseline.md`, `scope-application-matrix.md` |
| Agentic | `harness-engineering.md`, `loop-engineering.md`, `provider-implementation-comparison.md`, `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `agent-model-selection.md`, `ai-agent-catalogs.md`, `memory-hierarchy.md` |
| SDLC/docs | `spec-driven-sdlc.md`, `sdlc-document-roles.md`, `document-metadata-lifecycle.md`, `documentation-architecture.md`, `llm-wiki-system.md` |
| Delivery/quality | `automation-pipeline-workflow.md`, `quality-ci-formatting.md`, `verification-validation.md` |
| Infra/security | `docker-compose-infrastructure.md`, `security-governance.md` |

The following inventory is closed: each subject is assigned to a leaf and has
no unassigned successor.

| Leaf | Required subjects |
| --- | --- |
| `harness-engineering.md` | Harness elements; workspace harness/loop systems, environment, and rules. |
| `loop-engineering.md` | Loop elements, feedback, stopping, and escalation. |
| `provider-implementation-comparison.md` | Claude/Codex implementation; common construction: canonical provider-neutral contract → native adapters → parity checks → irreducible native differences → separately authorized runtime proof. |
| `spec-driven-sdlc.md` | Spec-driven development and SDLC. |
| `docker-compose-infrastructure.md` | Docker Compose and infrastructure. |
| `sdlc-document-roles.md` | PRD, Architecture Description, local `ARD` coinage, ADR, Spec, Plan, Task, Guide, Incident, Postmortem, Policy, Release evidence practice, and Runbook. Each receives role, purpose, trigger, owner, consumer, system, evidence, rules, and relationships analysis. This leaf exclusively owns `SDLCDOC-ADR-001` through `SDLCDOC-ADR-003`: ADR role, decision scope, lifecycle, status, supersession, and relationships to Architecture Description, Spec, and the local historical `ARD` coinage. ADR is a durable decision record, not a replacement for Architecture Description; the local coinage is not presumed to be an external standard role. |
| `documentation-architecture.md` | Preserved input `DOCARCH-DIATAXIS-BASE-001`, delta claims `DOCARCH-C4-001` and `DOCARCH-ARC42-001`, and cross-practice synthesis under `DOCARCH-COMP-001`. Diataxis, C4 Model, arc42, and ADR are complementary practices compared by purpose, granularity, artifact or view, and relationship. Each owned synthesis proposition compares or composes at least two practices and cites the relevant canonical inputs. Every ADR comparison cell or proposition cites one or more of `SDLCDOC-ADR-001` through `SDLCDOC-ADR-003`; this leaf neither restates nor owns an ADR-only proposition. |
| `llm-wiki-system.md` | LLM Wiki system, rules, and implementation. |
| `automation-pipeline-workflow.md` | CI/CD and GitHub Actions. |
| `quality-ci-formatting.md` | QA: formatting, linting, testing, and syntax errors. |
| `verification-validation.md` | Verification and validation. |
| `security-governance.md` | Security system, rules, and implementation. |
| `ai-agent-catalogs.md` | `agency-agents` system, rules, and implementation. |
| `agent-model-selection.md` | Work-aware model/configuration selection. |
| `memory-hierarchy.md` | Short-, long-, and domain-memory tiers and management. |
| `scope-application-matrix.md` | `SCOPE-COMP-001`: for the C4/arc42/ADR composition, explicit applicability or reasoned non-applicability, local adoption conditions, limitations, verification evidence, and cross-links across exactly the closed eight scopes. |
| `workspace-baseline.md`, `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `document-metadata-lifecycle.md` | Shared measurement, instruction/model context, and lifecycle evidence required to make the assigned topics actionable. |

The Release subject is externally researched but locally disposed as no
standalone ordinary-delivery profile: Task plus Git/PR owns ordinary delivery;
real release-event evidence may be analyzed without creating a document role.

## Technical Approach

Spec/Plan/Task corrections and the approved pre-acceptance draft may proceed
now. Outside that exact exception, content authoring requires an independently
completed and accepted Task 9 result establishing `RES-0002`, or a separate
user-approved migration-row disposition. This branch may create only the
listed draft files in the absent target; it must never accept Task 9 or
establish its parent route.

The README uses the current Stage 99 research profile, including required
frontmatter and `Question`, `Scope`, `Method`, `Findings`, `Sources`,
`Implications`, and `Traceability` sections. The 21-file ceiling forbids an
extra register file. Each leaf owns unique stable claim IDs (`<leaf-prefix>-NNN`)
and detailed source rows. README alone owns aggregate claim, source,
requirement, and eight-scope coverage plus navigation; every claim and matrix
cell has exactly one owner, and aggregate totals must reconcile to leaf rows.

Each leaf separates concept, external evidence, tracked workspace state,
adoption conditions, scope application, limitations, and non-normative
follow-up. Mutable facts retain access dates; unapproved runtime/remote claims
remain `UNVERIFIED`. Git and existing Task records retain history; obsolete
Gate2 detail is not copied into this living Spec.

The correction integrates these subjects into the listed leaves and their
cross-links. Only the approved draft exception permits creating those leaves;
no additional leaf or parent route is created. It performs no structural
migration, does not mutate SPEC-0153 Task 9, and neither replaces nor creates an
authority. Stage 90 remains advisory. Diataxis, C4 Model, arc42, and ADR are
composed where useful; their inclusion must not imply mutual exclusion or
authority replacement.

For this composition, the cross-link graph is the closed three-leaf set
`documentation-architecture.md`, `sdlc-document-roles.md`, and
`scope-application-matrix.md`. Each leaf contains exactly one
`## Architecture Practice Composition Links` section. That section contains
exactly two relative Markdown links: one to each sibling, with each normalized
sibling destination present exactly once. Only links in that named section
count. The exact-six rule counts unique `(source leaf, normalized sibling
destination)` pairs; any duplicate, missing, extra, or fourth-leaf destination
fails.

## Interfaces and Data

The interface is Markdown navigation, leaf claim/source rows, and README
aggregates. Source rows and claim IDs form the traceable data contract; tracked
paths prove repository state only. Runtime/remote records additionally require
authorization, target, timestamp, and redaction boundary. No record may contain
credentials, conversation bodies, raw secret values, or private provider state.

## Failure Modes and Guardrails

- Missing `RES-0002`: only the approved draft exception permits creating the
  listed files; all other content execution awaits accepted Task 9 or a
  separately approved migration disposition.
- Stale, secondary, or incomplete evidence: preserve class/caveat or mark
  `UNVERIFIED`; never promote it to current fact.
- Provider differences: preserve native differences rather than asserting false
  parity; runtime proof needs separate authorization.
- Scope, claim, or source-family ownership conflict: fail the
  matrix/reconciliation; do not duplicate ownership or leave a blank cell.
- Delta source or date mismatch: an unlisted family root, ineligible descendant
  URL, cross-origin redirect, or request outside the currently authorized date
  stops access until the Spec and Plan satisfy the source-family and date
  contracts.
- Documentation-practice composition: do not present Diataxis, C4 Model,
  arc42, or ADR as mutually exclusive, or let a view, template, or decision
  record replace the owning Architecture Description or other authority; do
  not duplicate owned ADR facts outside `sdlc-document-roles.md`.
- Terminology collision: the local historical `ARD` coinage is not presumed to
  be an external standard role and must not be conflated with a standardized
  external Architecture Requirements Document.
- Policy, runtime, remote, security, route, or dated-pack discovery: record an
  advisory follow-up only; do not alter the protected surface.

## Acceptance Contract

This final-acceptance contract is unchanged by draft authoring. The future
bounded Task may close only when:

1. An accepted Task 9 result or separately approved migration disposition has
   established the canonical route, without this capability creating it.
2. Before delta-window source access, the corrected Plan enumerates every
   proposed direct source-page URL and maps it to exactly one of the five
   source-backed claim IDs and one listed source family root. Every evidence URL
   is a same-origin descendant that inherits its listed family; descendant URLs
   are not additional families, and no cross-origin redirect or third-party
   linked content is used. The Plan adds no claim, source family root, owner,
   subject refresh, or baseline refresh beyond the exhaustive table.
   Every external request occurs on the currently authorized date, initially
   2026-08-28 Asia/Seoul. Before the first request on any later date, both this
   Spec and the Plan are corrected to that actual date, even if requests already
   occurred on 2026-08-28. Each page's source row is never prefilled, records
   its actual observed date, and never relabels delta evidence as part of the
   2026-08-23 baseline.
3. `RES-0002` has exactly the README and twenty listed English leaves, with
   profile-conformant navigation, unique claim IDs, detailed leaf source rows,
   and reconciling README aggregates.
4. The closed inventory and all eight-scope cells are complete, explicit, and
   evidence-bounded; capability, adoption, and execution are not conflated.
5. The delta contains exactly the seven listed claim IDs with the listed
   owners. Each of the five source-backed claims has at least one permitted
   direct primary-source row whose evidence URL inherits its listed source
   family root, and each delta claim records an explicit limitation and local
   adoption condition. `DOCARCH-COMP-001` and `SCOPE-COMP-001` use only their
   listed claim inputs and tracked workspace evidence; their inputs are not
   source families, and neither has an additional external source. The preserved
   `DOCARCH-DIATAXIS-BASE-001` input authorizes no refetch and is not counted
   among the seven delta claims.
6. `sdlc-document-roles.md` exclusively owns and contains
   `SDLCDOC-ADR-001` through `SDLCDOC-ADR-003`. Every ADR comparison cell or
   proposition in `documentation-architecture.md` cites one or more of those
   claims and neither restates nor owns an ADR-only proposition. Every
   `DOCARCH-COMP-001` synthesis proposition compares or composes at least two of
   Diataxis, C4 Model, arc42, and ADR. A proposition involving Diataxis cites
   `DOCARCH-DIATAXIS-BASE-001`; every other practice input cites its relevant
   delta claim ID.
7. `scope-application-matrix.md` owns `SCOPE-COMP-001` and reconciles the
   composition across exactly the eight closed scopes with applicability or a
   reasoned non-applicability, adoption conditions, limitations, and
   verification evidence. It, `documentation-architecture.md`, and
   `sdlc-document-roles.md` each contain exactly one
   `## Architecture Practice Composition Links` section with exactly two
   relative Markdown links, one to each sibling normalized destination exactly
   once. Only that section counts. The six links are exactly the six unique
   `(source leaf, normalized sibling destination)` pairs; a duplicate, missing,
   extra, or fourth-leaf destination fails acceptance.
8. The pack makes no unauthorized policy, runtime, remote, release, or security
   assertion and reports inherited baseline failures separately from its result.
9. The Task selects every applicable ADR-0029 public suite—`document-contract`,
   `document-graph`, `document-lifecycle`, `operations`, `agent-governance`, and
   `repository-integrity`—and records an explicit rationale for every skipped
   suite. Current baseline suite implementation has not completed, so this Spec
   makes no present-pass claim.
10. Logical changes are reviewed and committed without altering dated packs,
   routers/generators, Task 9, or protected state.

## Traceability

| Authority | Relationship |
| --- | --- |
| [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md) | Stage ownership, Stage 90 advisory boundary, and six public suites. |
| [SPEC-0136](../0136-sdlc-taxonomy-convergence/spec.md) | Current co-located Spec/Plan/Task taxonomy. |
| [SPEC-0153 Task 9](../0153-workspace-governance-simplification/tasks/tsk-0009-references.md) | Exclusive structural owner; not accepted, editable, or executable here. |
| `RES-0002` | Approved branch-only draft destination; final structural disposition remains independent. |

## Operational Impact

This changes documentation intent only; it does not change services, Compose,
infrastructure, CI/CD execution, GitHub settings, provider configuration,
credentials, or external systems.

## Open Questions

- Final structural acceptance, identity reconciliation, full-suite validation,
  integration, and cleanup remain deferred. A checked draft is not final
  acceptance; the two unresolved ADR claims remain `UNVERIFIED`.
