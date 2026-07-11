---
status: active
---

<!-- Target: docs/03.specs/123-agentic-engineering-audit-remediation/spec.md -->

# Agentic Engineering Audit and Remediation Technical Specification

## Overview

This specification defines a staged program for consolidating agentic
engineering research and implementation audits, measuring how deeply each
researched practice is implemented in `hy-home.docker`, and applying approved
governance and development-harness improvements.

The program keeps the existing 2026-07-05 research and implementation-audit
packs as the canonical Stage 90 sources. It merges verified unique content from
the overlapping 2026-07-07 audit pack, converts that pack to a superseded
mapping record, and preserves the 2026-07-03 and 2026-07-04 audit packs as
dated historical evidence rather than current implementation truth.

The assessment covers workspace purpose and roles; harness and loop
engineering; Claude, Codex, and Gemini provider surfaces; model selection;
agent instructions and catalogs; vibe-coding controls; spec-driven SDLC;
document roles, numbering, metadata, and status transitions; CI/CD; QA;
formatting, linting, and syntax checks; controlled pre-commit execution;
automation, pipelines, and workflows; Docker Compose and infrastructure;
security and supply chain; incidents, postmortems, releases, and operations.

The official Claude, OpenAI/Codex, and Gemini model catalog remains bound to
the previously approved 2026-07-10 10:00 KST cutoff. Current retrieval may
verify page availability and workspace implementation, but later announcements
must not be backdated into that catalog.

## Strategic Boundaries & Non-goals

- Stage 90 remains advisory reference context. It does not replace active
  policy, plans, task evidence, operations procedures, or runtime truth.
- No new dated research or implementation-audit pack is created.
- Governance and development-harness remediation may change Stage 00, Stage
  99, provider instruction and adapter surfaces, validation scripts, the
  controlled QA wrapper, and CI workflows only through approved Stage 04
  tasks.
- Docker Compose services, infrastructure runtime, deployment state, secrets,
  credentials, and remote GitHub settings are not mutated by this program.
  Their findings produce independent follow-up specifications and plans.
- Existing stage numbering is not mechanically unified. Stable artifact IDs
  and explicit parent relations provide cross-stage traceability.
- Existing documents are not mass-migrated merely to satisfy a new metadata
  shape. The active agentic chain migrates first; broader blocking enforcement
  requires later evidence and approval.
- New provider model policy is not inferred from the research catalog. An
  exact provider, model ID, role, reasoning control, adapter path, and
  validation path require explicit approval before policy mutation.

## Related Inputs

- **PRD**: No dedicated PRD is required. This is an approved cross-cutting
  governance, documentation, and development-harness improvement program over
  existing requirements and implementation surfaces.
- **ARD**: No dedicated ARD is required for the audit and governance work.
  Runtime findings that change architecture must create independent ARD/ADR
  artifacts before implementation.
- **Related ADRs**: No new architecture decision is introduced by this design.
- **Previous Specification**:
  [../122-agentic-research-pack-consolidation/spec.md](../122-agentic-research-pack-consolidation/spec.md)
- **Canonical Research Pack**:
  [../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Canonical Audit Pack**:
  [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Overlapping Audit Pack**:
  [../../90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md](../../90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md)
- **Stage Authoring Matrix**:
  [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation Protocol**:
  [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Canonical research | Extend `2026-07-05-agentic-research-pack-refresh` in place. Add focused criteria only when existing responsibility documents would become overloaded. |
| Canonical audit | Extend `2026-07-05-agentic-engineering-implementation-audit-pack` in place and keep it as the only current agentic implementation audit. |
| Audit supersession | Merge verified unique 2026-07-07 audit content, remove unsupported claims, and convert the 2026-07-07 pack to mapping-only `superseded` records. |
| Historical evidence | Preserve the 2026-07-03 and 2026-07-04 packs as dated evidence; indexes must warn that their corpus counts are not current facts. |
| External evidence | Use primary sources: official vendor documentation, standards bodies, original papers, and official repositories. Record checked date and applicability; preserve the approved provider-model cutoff instead of backdating later facts. |
| Workspace evidence | Derive implementation claims from tracked source, Stage 00 governance, stage documents, templates, scripts, workflows, provider surfaces, and Compose configuration. Graphify is advisory and must be corroborated. |
| Assessment | Every criterion records implementation state, enforcement depth, disposition, owner, automation impact, evidence, and verification. |
| Metadata rollout | Introduce typed metadata as advisory first, migrate the approved active chain, then enforce it for changed/new documents before any broader blocking migration. |
| Pre-commit execution | AI agents run `pre-commit run --all-files` only through an approved wrapper in an isolated worktree and record a concise result in Stage 04 task evidence. Direct manual execution remains prohibited. |
| Provider integrity | Stage 00 stays canonical; Claude, Codex, and Gemini surfaces are adapters. Native capability gaps remain explicit and are not normalized into false parity. |
| Runtime boundary | Compose, infrastructure, security runtime, deployment, secret, and remote findings produce later specs/plans only. |
| Commit boundary | Design, research, audit, metadata schema, migration, QA wrapper, provider/workflow synchronization, runtime follow-up artifacts, and review fixes use logical commits. |

## Core Design

### Program Workstreams

| Workstream | Purpose | Primary Outputs | Mutation Boundary |
| --- | --- | --- | --- |
| W1 Research | Revalidate external criteria and close criteria gaps. | Updated canonical research leaves plus focused metadata/lifecycle and agent-instruction/vibe-coding references. | Stage 90 research and required indexes only. |
| W2 Audit | Perform current repository-wide comparison and consolidate audit history. | Canonical category reports, exhaustive metadata inventory, gap/disposition register, 2026-07-07 supersession. | Stage 90 audits/data and required indexes only. |
| W3 SDLC metadata | Define and introduce typed metadata, lifecycle transitions, numbering relations, and semantic traceability. | Stage 00/99 contracts, schemas, advisory validator, active-chain migration. | No runtime, provider model, secret, or remote mutation. |
| W4 Development harness | Add controlled pre-commit execution and synchronize provider, validator, and CI governance. | QA wrapper, instruction updates, provider adapters, validators, CI workflow changes, task evidence. | No Compose service or deployment mutation. |
| W5 Runtime follow-up | Turn audited runtime gaps into implementation-ready independent work. | Separate Compose, infrastructure, security, and deployment specs/plans. | Documentation only; runtime implementation requires later approval. |

Each workstream receives its own Stage 04 plan/task evidence or an explicitly
linked child plan when the implementation plan decomposes it further.

### Canonical Research Responsibilities

Existing research documents retain their current responsibilities. Two focused
criteria documents are added because the current pack lacks complete source-
backed criteria for these areas:

| Document | Responsibility |
| --- | --- |
| `document-metadata-lifecycle.md` | Typed frontmatter, artifact identity, parent relations, numbering, supersession, review metadata, lifecycle transitions, and semantic validation. |
| `agent-instructions-vibe-coding.md` | Instruction anatomy, generated-code accountability, vibe-coding boundaries, review evidence, verification thresholds, and technical-debt controls. |

The existing `sdlc-document-roles.md`, `quality-ci-formatting.md`, and
`automation-pipeline-workflow.md` documents absorb release, deployment,
pre-commit, and CI/CD criteria without creating separate overlapping leaves.

### Canonical Audit Categories

The canonical audit pack provides responsibility-focused reports for:

1. cross-category implementation overview and gap/disposition register;
2. harness engineering;
3. loop and eval engineering;
4. Claude, Codex, Gemini, provider parity, and model policy;
5. workspace governance, environment, and common rules;
6. SDLC, document roles, numbering, status transitions, traceability, and the
   disposition of release records versus changelogs and release runbooks;
7. frontmatter, templates, and README profiles;
8. CI/CD, QA, formatting, linting, syntax, and controlled pre-commit;
9. automation, pipeline, and workflow;
10. Docker Compose, infrastructure, and operations readiness;
11. security, supply chain, and approval boundaries; and
12. agent instructions, catalogs, vibe coding, `agency-agents`, and model
    routing.

Existing canonical audit leaves are updated in place when their responsibility
matches. New leaves are added only for missing responsibilities. Downstream
links and generated matrices are updated rather than leaving parallel current
summaries.

## Data Modeling & Storage Strategy

### Audit Criterion Record

| Field | Meaning |
| --- | --- |
| Criterion ID | Stable category-local identifier. |
| External criterion | Source-backed practice or capability. |
| Workspace evidence | Tracked path, validator, workflow, or configuration evidence. |
| Implementation state | `Implemented`, `Partial`, `Missing`, `Not Applicable`, or `Needs Revalidation`. |
| Enforcement depth | `0` absent, `1` documented, `2` partially applied, `3` automated/enforced, `4` measured with a closed feedback loop. |
| Disposition | `Retain`, `Fix`, `Improve`, `Add`, or `Remove`. |
| Canonical owner | Earliest stage or runtime surface that owns an approved change. |
| Automation impact | Candidate automation, existing automation, or explicit non-automation reason. |
| Verification | Command, generated evidence, or manual acceptance check. |
| Confidence | Evidence directness, freshness, and unresolved uncertainty. |

No composite average replaces individual evidence. Summary counts may group
criterion states and enforcement depths, but must retain links to the complete
rows.

### Typed Document Metadata

The proposed common keys are:

| Key | Requirement | Meaning |
| --- | --- | --- |
| `status` | Required | Existing lifecycle status vocabulary. |
| `artifact_id` | Required after migration | Stable identifier independent of path. |
| `artifact_type` | Required after migration | PRD, ARD, ADR, Spec, Plan, Task, Guide, Policy, Runbook, Incident, Postmortem, Release, Reference, Audit, or README profile. |
| `parent_ids` | Type-dependent | Direct upstream artifact IDs. Empty only when the type contract permits a root artifact. |
| `supersedes` | Conditional | Artifact IDs replaced by this artifact. |
| `reviewed_at` | Type-dependent | Last evidence-backed review date. |
| `review_cycle` | Type-dependent | Review cadence when the artifact type requires freshness management. |

`Related Documents` remains the human-readable link surface. Frontmatter IDs
support machine validation and must not become a second copy of every link.
Ownership remains in canonical catalogs, CODEOWNERS, or document-body
contracts rather than a stale universal `owner` key.

Before any key becomes blocking, W3 must publish a document-type profile matrix
that states which keys are required, optional, forbidden, or not applicable for
every supported artifact type. The umbrella schema does not make every
type-dependent key mandatory on every document.

### Lifecycle State Machine

Default transitions are:

```text
draft -> active -> completed
                -> superseded
completed      -> superseded
```

`superseded` is terminal for active-stage artifacts. `archived` is valid only
for Stage 98 tombstones. Reverse transitions require explicit Stage 04 task
evidence, approval, reason, and validator override. Status vocabulary and
transition history are distinct: a valid word does not prove a valid change.

### Numbering and Parent Relations

- PRD and Spec three-digit identifiers remain valid.
- ARD and ADR four-digit identifiers remain valid.
- Plan and Task dated names remain valid.
- Tier numbers remain domain-routing identifiers and are not reused as a
  universal lifecycle key.
- `parent_ids` links artifacts across differing numbering systems. Validators
  resolve IDs through a generated or deterministic manifest rather than
  requiring equal numeric suffixes.

### Metadata Rollout

1. Publish the schema and advisory semantic inventory without failing existing
   valid documents.
2. Migrate the agentic-engineering active chain and new workstream artifacts.
3. Generate a repository-wide per-document inventory and category summaries.
4. Make the schema blocking for changed/new documents after false-positive
   review.
5. Require separate approval before blocking the entire historical active
   corpus.

## Interfaces & Data Structures

### Controlled Pre-commit Wrapper

The wrapper contract is:

- live under `scripts/validation/` and be listed in `scripts/README.md`;
- verify repository root, isolated worktree context, approved Stage 04 task
  reference, and allowed invocation mode;
- execute the configured `pre-commit run --all-files` command without hidden
  hook skips;
- capture exit status and a concise hook-result summary without persisting raw
  logs or environment values;
- compare changed paths before and after execution;
- stop when unexpected out-of-scope changes appear, without automatic reset or
  deletion;
- require review of hook-managed edits and a separate formatting commit when
  those edits form an independent logical unit; and
- leave direct manual `pre-commit run` prohibited by agent instructions.

CI may keep its existing project-specific skip contract for heavy duplicate
jobs. The local agent wrapper does not replace GitHub-only checks such as SARIF
upload or protected-branch verification.

### Provider Synchronization

- Stage 00 defines shared role, model-policy, approval, lifecycle, and evidence
  semantics.
- Claude, Codex, and Gemini adapters express only capabilities available on
  their provider surface.
- Provider name-set and semantic parity validators remain coupled to generated
  adapters.
- Gemini pointer/reminder behavior is not represented as native hook or
  subagent execution parity.
- A model-policy change must update policy, generation logic, adapters,
  validators, and Stage 04 evidence in one approved task.

## API Contract (If Applicable)

Not applicable. This program introduces repository documentation, metadata,
script, and workflow contracts and exposes no external API.

## Agent Role & IO Contract (If Applicable)

| Role | Inputs | Outputs | Success Definition |
| --- | --- | --- | --- |
| Workflow supervisor | Approved spec/plan, task briefs, worktree state | Sequential routing, scope control, review packages, final synthesis | Each task stays within its owner surfaces and approval boundary. |
| Research implementer | Category brief, current research, primary sources | Source-backed canonical research change and source ledger | Every new claim is supported and applicability is explicit. |
| Audit implementer | Criteria, tracked workspace evidence, inventory tools | Category report, complete criterion rows, gaps, and logical commit | Every requested category maps to evidence and a disposition. |
| Governance implementer | Approved metadata or instruction task | Stage 00/99, validator, provider, or workflow changes | Changes are coupled, backward-compatible by rollout phase, and verified. |
| Spec-compliance reviewer | Task brief, diff, implementation report | Requirement-by-requirement verdict | No required criterion or boundary is omitted. |
| Quality/security reviewer | Diff, tests, sources, security boundary | Quality verdict and severity-ranked findings | No unresolved critical or important findings remain. |
| Whole-branch reviewer | Exact branch range and all task verdicts | Cross-workstream consistency and readiness decision | Canonical ownership, lifecycle, validation, and protected surfaces are coherent. |

Each implementation task uses a fresh implementer and separate reviewers.
Completed subagents are closed. File ownership conflicts stop the task and are
escalated rather than overwritten.

## Tools & Tool Contract (If Applicable)

- Use `rg`, `rg --files`, tracked-file inventories, and read-only Git commands
  for repository discovery.
- Use official web sources for changing external facts and cite direct pages.
- Use `apply_patch` for authored file changes and canonical generators for
  generated artifacts.
- Use repository validators before adding new checks.
- Use the controlled wrapper, not a direct `pre-commit run`, when the approved
  QA task reaches its full-repository gate.
- Do not persist raw web captures, raw logs, credentials, secret values,
  environment dumps, or shell history.

## Prompt / Policy Contract (If Applicable)

- Audit authority does not authorize active policy or runtime mutation.
- Governance remediation authority is limited to the surfaces named by the
  approved Stage 04 task.
- Runtime follow-up specs/plans do not authorize runtime implementation.
- External agent catalogs are pattern sources, not identities to import
  wholesale. Repository roles remain curated and provider-neutral at Stage 00.
- Vibe coding is acceptable only inside explicit scope, review, verification,
  ownership, and evidence boundaries defined by the approved policy work.

## Memory & Context Strategy (If Applicable)

- Stage 04 task evidence records source checks, inventory counts, commands,
  wrapper results, protected surfaces, commits, review outcomes, and
  deviations.
- `docs/00.agent-governance/memory/progress.md` records material milestones and
  durable pointers, not raw transcripts.
- Generated inventories are reproducible snapshots with freshness checks.
- Graphify output is navigation-only when stale or advisory; tracked source
  and canonical stage documents control conclusions.

## Guardrails (If Applicable)

- Do not create parallel current packs or redirect-style active artifacts.
- Do not claim full lifecycle traceability from link-format checks alone.
- Do not treat valid frontmatter syntax as proof of semantically correct state.
- Do not auto-rewrite the historical corpus when enabling typed metadata.
- Do not reset, delete, or silently accept files modified unexpectedly by the
  pre-commit wrapper.
- Do not infer provider capability, model availability, or reasoning parity.
- Do not change Compose services, deployment runtime, secrets, remote GitHub
  settings, or branch protection in this program.
- Do not mark a runtime follow-up task implementation-ready without rollback,
  validation, and approval gates in its independent plan.

## Evaluation (If Applicable)

Evaluation uses deterministic inventories and reviewable evidence rather than
a single maturity score:

- requested-category coverage and criterion ownership;
- source freshness and primary-source ratio;
- implementation-state and enforcement-depth distributions;
- per-document metadata semantic inventory;
- lifecycle and parent-relation resolution;
- provider adapter set and semantic parity;
- controlled wrapper behavior and out-of-scope change detection;
- validator false-positive review before blocking rollout; and
- independent task and whole-branch review outcomes.

## Edge Cases & Error Handling

| Edge Case | Required Handling |
| --- | --- |
| Mutable provider page cannot prove a historical state | Record `Needs Revalidation`; do not infer the cutoff state. |
| Provider announcement postdates the approved model cutoff | Keep it out of the cutoff catalog; record it only as later context when relevant. |
| Audit pack contains a claim sourced only from the superseded research pack | Revalidate against the canonical research pack and tracked evidence before merging. |
| Historical audit count differs from current corpus | Preserve the dated count as history and generate a fresh inventory for current claims. |
| One artifact has multiple legitimate parents | Use ordered or deterministic `parent_ids`; do not duplicate the artifact. |
| Existing active status appears stale | Report the semantic gap; do not change it without lifecycle evidence. |
| New metadata validator produces broad false positives | Keep the gate advisory, refine the schema, and record exceptions before blocking rollout. |
| Pre-commit wrapper modifies unexpected files | Stop, report the path set, and request scope or separate formatting disposition; do not auto-revert. |
| Required local tool is unavailable | Record the skipped check and rely only on approved alternatives; do not claim the missing gate passed. |
| Provider model is documented but unavailable to the workspace | Keep research and policy separate; do not change adapters. |
| Runtime finding needs architecture change | Create independent PRD/ARD/ADR/Spec/Plan artifacts as required and stop before runtime mutation. |

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback | Human Escalation |
| --- | --- | --- |
| Canonical and duplicate packs disagree | Prefer newly verified primary and tracked evidence; preserve unresolved conflict as `Needs Revalidation`. | Required when the disagreement would change active policy or deletion disposition. |
| Metadata migration would touch most of the corpus | Limit migration to the approved active chain and keep the rest advisory. | Required before repository-wide blocking enforcement. |
| Wrapper cannot isolate hook-managed edits | Stop after evidence capture; leave changes uncommitted and visible. | Required before expanding scope or discarding changes. |
| Workflow or provider change requires a new remote permission | Keep the local contract change incomplete or deferred. | Required before any remote mutation or credential change. |
| Model-policy recommendation lacks an exact value or validator support | Keep current policy and record the recommendation only. | Required with exact provider/model/role/reasoning details. |
| Runtime follow-up lacks rollback or recovery evidence | Keep the plan draft and mark it blocked. | Required before implementation approval. |

## Verification

The detailed implementation plan selects the applicable subset for each task.
The final program gate includes all locally applicable checks:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
```

New metadata inventory, semantic lifecycle, audit-matrix, and controlled
pre-commit wrapper checks must be added to this verification set by their
own approved tasks. Workflow changes also require shell/YAML validation and
locally available `actionlint`/`zizmor` checks or an explicit CI-only rationale.

No command in this section authorizes Docker service startup, deployment,
secret access, remote GitHub mutation, or direct manual pre-commit execution.

## Success Criteria & Verification Plan

- **VAL-AER-001**: The existing 2026-07-05 research pack is the only current
  canonical agentic research pack, including source-backed criteria for
  document metadata/lifecycle and agent instructions/vibe coding.
- **VAL-AER-002**: The existing 2026-07-05 audit pack is the only current
  canonical agentic implementation audit, and verified 2026-07-07 content is
  merged before that pack becomes mapping-only superseded history.
- **VAL-AER-003**: Every requested category and subcategory has an audit row
  with evidence, implementation state, enforcement depth, disposition,
  canonical owner, automation impact, and verification.
- **VAL-AER-004**: A reproducible per-document inventory assesses frontmatter
  keys and values semantically, not only syntactically.
- **VAL-AER-005**: Typed metadata and lifecycle rules are implemented
  advisory-first and applied to the approved active chain without a mass
  historical rewrite.
- **VAL-AER-006**: Cross-stage relations work across existing numbering
  systems through stable artifact IDs and parent references.
- **VAL-AER-007**: AI agents can run the full configured pre-commit suite only
  through the controlled wrapper, with Stage 04 evidence and unexpected-change
  detection.
- **VAL-AER-008**: Stage 00, Stage 99, provider surfaces, validators, and CI
  workflow remain synchronized for every approved development-harness change.
- **VAL-AER-009**: Model-policy changes remain unchanged until exact
  provider/model/role/reasoning/validator approval is recorded.
- **VAL-AER-010**: Compose, infrastructure, security runtime, and deployment
  findings have independent follow-up specs/plans, while runtime state remains
  untouched.
- **VAL-AER-011**: Every implementation task has separate implementer,
  spec-compliance, and quality/security review evidence, followed by a final
  whole-branch review.
- **VAL-AER-012**: Logical commits, clean worktree state, generated-artifact
  freshness, repository contracts, and locally applicable QA/security checks
  pass before branch completion.

## Related Documents

- [Specification folder](./README.md)
- [Implementation plan](../../04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md)
- [Previous research consolidation specification](../122-agentic-research-pack-consolidation/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical implementation audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Overlapping implementation audit pack](../../90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md)
- [Research category](../../90.references/research/README.md)
- [Audit category](../../90.references/audits/README.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Lifecycle status contract](../../99.templates/support/lifecycle-status.md)
- [Subagent protocol](../../00.agent-governance/subagent-protocol.md)
