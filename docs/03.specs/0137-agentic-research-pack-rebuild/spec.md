---
profile_id: spec
status: active
artifact_id: SPEC-0137
artifact_type: spec
parent_ids:
  - ADR-0029
  - SPEC-0136
created: 2026-08-08
updated: 2026-08-23
---

# Agentic Engineering Research Pack Rebuild Specification

## Overview

SPEC-0137 governs research **content** for the canonical Stage 90 pack
`RES-0002`. It is advisory, English-only closed research: it may report
evidence and gaps, but cannot create policy, runtime, remote, security, or
provider truth. The content target is one README and twenty leaves at
`docs/90.references/research/0002-agentic-engineering-research-pack/`.

## Boundaries and Inputs

The external-source cutoff/access date is 2026-08-23; the workspace baseline is
`0c841b086cd1e6adc2c1ca53ce14eec309fe8f47`. Graphify `f8a72211` is stale and
advisory; leads require corroboration in tracked source, Stage 00 governance,
and current stage documents.

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

The existing `plan.md` and Task 0001–0003 bodies and commits are retained
historical evidence only; they have no prospective or future-execution authority
under this corrected Spec. Their active metadata is stale and must be truthfully
corrected in a later Plan/Task-only unit before Task 0004 activation; they are
not thereby called completed. Plan and Task are co-located in Stage 03; Stage 04
has no authority. The prospective record is
`tasks/tsk-0004-canonical-research-refresh.md`.

## Behavior Contract

After its canonical route is independently established, `RES-0002` contains a
README and these twenty English leaves:

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
| `sdlc-document-roles.md` | PRD, Architecture Description, local `ARD` coinage, ADR, Spec, Plan, Task, Guide, Incident, Postmortem, Policy, Release evidence practice, and Runbook. Each receives role, purpose, trigger, owner, consumer, system, evidence, rules, and relationships analysis. |
| `documentation-architecture.md` | Diataxis and documentation architecture. |
| `llm-wiki-system.md` | LLM Wiki system, rules, and implementation. |
| `automation-pipeline-workflow.md` | CI/CD and GitHub Actions. |
| `quality-ci-formatting.md` | QA: formatting, linting, testing, and syntax errors. |
| `verification-validation.md` | Verification and validation. |
| `security-governance.md` | Security system, rules, and implementation. |
| `ai-agent-catalogs.md` | `agency-agents` system, rules, and implementation. |
| `agent-model-selection.md` | Work-aware model/configuration selection. |
| `memory-hierarchy.md` | Short-, long-, and domain-memory tiers and management. |
| `workspace-baseline.md`, `scope-application-matrix.md`, `agent-instructions-vibe-coding.md`, `provider-model-landscape.md`, `document-metadata-lifecycle.md` | Shared measurement, instruction/model context, and lifecycle evidence required to make the assigned topics actionable. |

The Release subject is externally researched but locally disposed as no
standalone ordinary-delivery profile: Task plus Git/PR owns ordinary delivery;
real release-event evidence may be analyzed without creating a document role.

## Technical Approach

Spec/Plan/Task corrections may proceed now. Content authoring begins only in a
branch/worktree based on an independently completed and accepted Task 9 result
that establishes `RES-0002`, or after a separate user-approved migration-row
disposition. This branch must never create the absent target or accept Task 9.

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

## Interfaces and Data

The interface is Markdown navigation, leaf claim/source rows, and README
aggregates. Source rows and claim IDs form the traceable data contract; tracked
paths prove repository state only. Runtime/remote records additionally require
authorization, target, timestamp, and redaction boundary. No record may contain
credentials, conversation bodies, raw secret values, or private provider state.

## Failure Modes and Guardrails

- Missing `RES-0002`: stop before creating or authoring content; await accepted
  Task 9 or separately approved migration disposition.
- Stale, secondary, or incomplete evidence: preserve class/caveat or mark
  `UNVERIFIED`; never promote it to current fact.
- Provider differences: preserve native differences rather than asserting false
  parity; runtime proof needs separate authorization.
- Scope, claim, or source ownership conflict: fail the matrix/reconciliation;
  do not duplicate ownership or leave a blank cell.
- Policy, runtime, remote, security, route, or dated-pack discovery: record an
  advisory follow-up only; do not alter the protected surface.

## Acceptance Contract

The future bounded Task may close only when:

1. An accepted Task 9 result or separately approved migration disposition has
   established the canonical route, without this capability creating it.
2. `RES-0002` has exactly the README and twenty listed English leaves, with
   profile-conformant navigation, unique claim IDs, detailed leaf source rows,
   and reconciling README aggregates.
3. The closed inventory and all eight-scope cells are complete, explicit, and
   evidence-bounded; capability, adoption, and execution are not conflated.
4. The pack makes no unauthorized policy, runtime, remote, release, or security
   assertion and reports inherited baseline failures separately from its result.
5. The Task selects every applicable ADR-0029 public suite—`document-contract`,
   `document-graph`, `document-lifecycle`, `operations`, `agent-governance`, and
   `repository-integrity`—and records an explicit rationale for every skipped
   suite. Current baseline suite implementation has not completed, so this Spec
   makes no present-pass claim.
6. Logical changes are reviewed and committed without altering dated packs,
   routers/generators, Task 9, or protected state.

## Traceability

| Authority | Relationship |
| --- | --- |
| [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md) | Stage ownership, Stage 90 advisory boundary, and six public suites. |
| [SPEC-0136](../0136-sdlc-taxonomy-convergence/spec.md) | Current co-located Spec/Plan/Task taxonomy. |
| [SPEC-0153 Task 9](../0153-workspace-governance-simplification/tasks/tsk-0009-references.md) | Exclusive structural owner; not accepted, editable, or executable here. |
| `RES-0002` | Future content destination after independent structural disposition. |

## Operational Impact

This changes documentation intent only; it does not change services, Compose,
infrastructure, CI/CD execution, GitHub settings, provider configuration,
credentials, or external systems.

## Open Questions

- `RES-0002` is absent. Content authoring remains blocked pending the stated
  independent structural disposition.
