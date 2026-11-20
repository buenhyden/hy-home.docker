---
title: "Agent Governance Standardization Requirements"
version: "2.0.0"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "requirements"
artifact_id: "REQ-0024"
created: "2026-06-01"
---

# Agent Governance Standardization Requirements

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the requirement payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Overview

##### Problem and Outcome

The AI agents in this repository must follow one governance model and one
SDLC even when their execution format differs by provider. The goal is to
separate the owners of policy, provider translation, document format, and
execution evidence, and to keep `.claude/` and `.codex/` from degrading into
independent policy sources.

##### Stakeholders

- The maintainer must be able to immediately tell which document is
  canonical in case of a conflict.
- An AI agent must load only the minimum policy, role, skill, Spec, and Task
  needed for the request.
- A reviewer must be able to reproduce the difference between provider
  projection and the canonical source, the approval boundary, and the
  verification result.
- An operator needs an explicit approval boundary so agent work does not
  expand into secrets, runtime, deployment, or remote state.

The owner, @buenhyden, writes, reviews and accepts this package.

#### Scope

##### In Scope

This package covers the governance model, canonical ownership, provider adapters and SDLC flow of the AI agents in this repository, as stated in the Overview.

##### Constraints and Exclusions

- Shared agent governance policy changes are made only within the approved
  repository scope.
- Provider adapters do not use user-global settings or credentials as
  canonical input.
- Historical body clones, compatibility redirects, and separate progress
  documents are not created.
- Runtime, deployment, secret, and remote GitHub state changes require
  separate explicit approval.

#### Requirements

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0024-FR-0001 | `.agents/` must be the sole normative owner of AI agent policy, workflow, canonical role, canonical skill, and provider boundary. | Agents must follow one governance model, and the maintainer must be able to tell immediately which document is canonical in a conflict. | Each agent policy, workflow, canonical role, canonical skill and provider-boundary rule has one owner under `.agents/`, and no file under `.claude/` or `.codex/` defines one. | must |
| REQ-0024-FR-0002 | The shared agent governance Provider Registry must own only provider identity, projection route, model/permission translation, and hook binding, and must not intrude on Stage 99's document profile/path/ template authority. | The goal is to separate the owners of policy, provider translation, document format and execution evidence. | Provider Registry entries hold only provider identity, projection route, model and permission translation, and hook binding; none sets a document profile, path or template. | must |
| REQ-0024-FR-0003 | `.claude/` and `.codex/` must be adapters that project the shared agent governance canonical source into provider or runtime format, and must not define separate policy, lifecycle, or completion criteria. `.agents/` is the actual repository-owned canonical source and holds only registered canonical categories. Native provider documents remain the authored originals for each of `.claude/` and `.codex/`, and generated README files or adapters must not overwrite the canonical source. Codex discovers and explicitly reads canonical skills, while Claude uses thin generated adapters that link to the canonical source. Skills for both providers are invoked explicitly, and discovery, loading, invocation, and runtime acceptance must not be claimed as the same evidence. Unknown or unsafe content is preserved fail closed and is not deleted automatically. | The goal is to keep `.claude/` and `.codex/` from degrading into independent policy sources. | Tracked files under `.claude/` and `.codex/` are classified as authored provider adapters, generated projections, or native runtime mechanics that the Provider Registry allows. | must |
| REQ-0024-FR-0004 | Canonical roles and skills must be defined exactly once in `.agents/`, and generated/tracked provider surfaces must preserve name, role, scope, and source relationships. | A reviewer must be able to reproduce the difference between provider projection and the canonical source. | There is no name, source or scope drift between shared agent governance and provider surfaces, and a canonical skill's native entry and nested governance metadata preserve the same ID, owner and scope. | must |
| REQ-0024-FR-0005 | An agent performing repository changes must load the relevant Requirement, Architecture, active Spec, and current Task through the bootstrap policy and provider adapter. | An AI agent must load only the minimum policy, role, skill, Spec and Task needed for the request. | The bootstrap policy and both provider adapters route an agent that changes the repository to the relevant Requirement, Architecture, active Spec and current Task. | must |
| REQ-0024-FR-0006 | The SDLC must use a single flow of Requirement -> Architecture/ADR -> Spec -> implementation -> Operations, and the current Spec Package's Task must own execution state and evidence. | Agents must follow one SDLC even when their execution format differs by provider. | Spec and Plan states express approval authority and Task and item states express execution; executing Tasks have approved parents, and a cancelled Spec requires a terminal Plan and terminal Tasks under the registered lifecycle. | must |
| REQ-0024-FR-0007 | General completion judgment must rely on reviewed diffs, registered verification results, and current Task evidence, and must not require branch SHA pinning, corpus snapshots, or a parallel handoff ledger as separate completion conditions. | The goal is to separate the owners of policy, provider translation, document format and execution evidence. | The current authority does not use deleted execution ledgers as input, and no completion check requires a branch SHA pin, a corpus snapshot or a parallel handoff ledger. | must |
| REQ-0024-FR-0008 | Governance gates and fixtures must check only the current contract declared by the Stage 99 Registry, script manifest, and workflow contract, and must not reproduce retired paths, document bodies, or fixed file counts. | This package records no rationale for this requirement. | Registered governance and document suites pass without dependence on historical fixtures, and the current authority does not use Stage 98 documents as input. | must |
| REQ-0024-FR-0014 | `.agents/`'s canonical categories are limited to governance, role, invocable skill, verified navigational knowledge, and reusable prompt contract, and paired Skill evaluation evidence; evaluation data is not loaded as execution instructions. Markdown instruction categories have a registered Stage 99 profile and canonical root inventory. Retired evaluator code, fixtures and event proofs must not remain recurring QA prerequisites. Knowledge and prompt content must not duplicate mandatory rules, detailed design, specifications, or runbook bodies, and must instead route to the canonical owner. No category owns execution progress state, and the current Spec Package Task remains the sole progress/handoff authority. Verified knowledge may preserve reusable durable domain facts with source, owner, validity, sensitivity, and invalidation; it remains navigation, not workflow authority. `.agents/evaluations/README.md` routes paired baseline/Skill task, raw output, scoring and aggregate evidence; representative results never imply all Skill membership or runtime acceptance. Current quality policy owns QA admission, agentic policy owns evaluation authority, and the active Task owns execution and acceptance. New evidence paths require bounded Stage 99 classification and canonical registration. | This package records no rationale for this requirement. | Every `.agents/` canonical category is one of the listed categories with a registered Stage 99 profile and root inventory for each Markdown instruction category; evaluation data is not loaded as execution instructions, and no category holds execution progress state. | must |
| REQ-0024-FR-0015 | Claude and Codex must share one repository-local agent memory store that every worktree of a checkout reaches, in place of separate native provider memories. Updates must name the expected revision and never overwrite silently, and limits must be stated as what actually enforces them. What a record may hold is owned by the environment constraints policy, section 5. | This package records no rationale for this requirement. | Both providers read and revise the same memory record from different worktrees, and a stale revision changes nothing. | must |
| REQ-0024-NFR-0009 | Rule interpretation and provider projection verification must be deterministic and fail closed, with no conflicting fallback; measure: the same tree yields the same projection verdict on every run. | The maintainer must be able to tell which document is canonical in a conflict, and a reviewer must be able to reproduce the projection difference and verification result. | The same tree yields the same projection verdict on every run, and an unknown or conflicting input fails instead of falling back. | must |
| REQ-0024-NFR-0010 | Governance, role, skill, knowledge and prompt documents and the authored provider guidance are English, and every `README.md` is Korean; native keys, required headings, commands, quotations and preserved evidence retain their original syntax. Profile languages follow the [document language rule](../00.workspace/03.process/documentation-protocol.md#document-language). Provider adapters must not lose meaning; measure: registered metadata checks report no language-rule violation. | This package records no rationale for this requirement. | Registered metadata checks report no language-rule violation. | must |
| REQ-0024-NFR-0011 | Agent permissions must be minimum scope and must not expose or change secrets, credentials, private keys, tokens, or unapproved external state; measure: no tracked permission grants a write outside the approved scope. | An operator needs an explicit approval boundary so agent work does not expand into secrets, runtime, deployment or remote state. | No tracked permission grants a write outside the approved scope, and explicit skill invocation configuration does not expand permissions. | must |
| REQ-0024-NFR-0012 | A verification failure must be able to identify its owner and the target to fix, and a duplicate aggregate gate must not own the same predicate more than once; measure: each failing check names one owner. | A reviewer must be able to reproduce the verification result. | Each failing check names one owner, and no predicate is owned by more than one aggregate gate. | must |
| REQ-0024-NFR-0013 | The current document must match the tracked implementation, and legacy, deprecated, or conflicting rules must be removed from the current surface; measure: registered governance suites pass on the current tree. | The maintainer must be able to tell immediately which document is canonical in case of a conflict. | Registered governance suites pass on the current tree. | must |

| Requirement ID | Attribute | Measure | Unit | Environment | Criterion |
| --- | --- | --- | --- | --- | --- |
| REQ-0024-NFR-0009 | Determinism | The same tree yields the same projection verdict on every run. | The package records no unit for this measure. | The same tree, on every run. | The same projection verdict on every run, and an unknown or conflicting input fails instead of falling back. |
| REQ-0024-NFR-0010 | Language consistency | Registered metadata checks report no language-rule violation. | The package records no unit for this measure. | The package records no measurement environment. | No language-rule violation reported by the registered metadata checks. |
| REQ-0024-NFR-0011 | Least privilege | No tracked permission grants a write outside the approved scope. | The package records no unit for this measure. | The package records no measurement environment. | No tracked permission grants a write outside the approved scope, and explicit skill invocation configuration does not expand permissions. |
| REQ-0024-NFR-0012 | Diagnosability | Each failing check names one owner. | The package records no unit for this measure. | The package records no measurement environment. | Each failing check names one owner, and no predicate is owned by more than one aggregate gate. |
| REQ-0024-NFR-0013 | Currency | Registered governance suites pass on the current tree. | The package records no unit for this measure. | The current tree. | Registered governance suites pass. |

##### Functional Requirements

- **REQ-0024-FR-0001**: `.agents/` must be the sole normative owner of AI agent
  policy, workflow, canonical role, canonical skill, and provider boundary.
- **REQ-0024-FR-0002**: The shared agent governance Provider Registry must own
  only provider identity, projection route, model/permission translation, and
  hook binding, and must not intrude on Stage 99's document profile/path/
  template authority.
- **REQ-0024-FR-0003**: `.claude/` and `.codex/` must be adapters that project
  the shared agent governance canonical source into provider or runtime
  format, and must not define separate policy, lifecycle, or completion
  criteria.
  `.agents/` is the actual repository-owned canonical source and holds only
  registered canonical categories. Native provider documents remain the
  authored originals for each of `.claude/` and `.codex/`, and generated
  README files or adapters must not overwrite the canonical source. Codex
  discovers and explicitly reads canonical skills, while Claude uses thin
  generated adapters that link to the canonical source. Skills for both
  providers are invoked explicitly, and discovery, loading, invocation, and
  runtime acceptance must not be claimed as the same evidence. Unknown or
  unsafe content is preserved fail closed and is not deleted automatically.
- **REQ-0024-FR-0004**: Canonical roles and skills must be defined exactly
  once in `.agents/`, and generated/tracked provider surfaces must preserve
  name, role, scope, and source relationships.
- **REQ-0024-FR-0005**: An agent performing repository changes must load the
  relevant Requirement, Architecture, active Spec, and current Task through
  the bootstrap policy and provider adapter.
- **REQ-0024-FR-0006**: The SDLC must use a single flow of
  Requirement -> Architecture/ADR -> Spec -> implementation -> Operations,
  and the current Spec Package's Task must own execution state and evidence.
- **REQ-0024-FR-0007**: General completion judgment must rely on reviewed
  diffs, registered verification results, and current Task evidence, and
  must not require branch SHA pinning, corpus snapshots, or a parallel
  handoff ledger as separate completion conditions.
- **REQ-0024-FR-0008**: Governance gates and fixtures must check only the
  current contract declared by the Stage 99 Registry, script manifest, and
  workflow contract, and must not reproduce retired paths, document bodies,
  or fixed file counts.
- **REQ-0024-FR-0014**: `.agents/`'s canonical categories are limited to
  governance, role, invocable skill, verified navigational knowledge, and
  reusable prompt contract, and paired Skill evaluation evidence; evaluation
  data is not loaded as execution instructions.
  Markdown instruction categories have a registered Stage 99 profile and
  canonical root inventory. Retired evaluator code, fixtures and event proofs
  must not remain recurring QA prerequisites. Knowledge and prompt content
  must not duplicate mandatory rules, detailed design, specifications, or runbook
  bodies, and must instead route to the canonical owner. No category owns
  execution progress state, and the current Spec Package Task remains the sole
  progress/handoff authority. Verified knowledge may preserve reusable durable
  domain facts with source, owner, validity, sensitivity, and invalidation; it
  remains navigation, not workflow authority. `.agents/evaluations/README.md`
  routes paired baseline/Skill task, raw output, scoring and aggregate evidence;
  representative results never imply all Skill membership or runtime acceptance.
  Current quality policy owns QA admission, agentic policy owns evaluation
  authority, and the active Task owns execution and acceptance. New evidence
  paths require bounded Stage 99 classification and canonical registration.
- **REQ-0024-FR-0015**: Claude and Codex must share one repository-local agent
  memory store that every worktree of a checkout reaches, in place of separate
  native provider memories. Updates must name the expected revision and never
  overwrite silently, and limits must be stated as what actually enforces
  them. What a record may hold is owned by the environment constraints policy,
  section 5.

##### Quality Requirements

- **REQ-0024-NFR-0009 — Determinism**: Rule interpretation and provider
  projection verification must be deterministic and fail closed, with no
  conflicting fallback; measure: the same tree yields the same projection
  verdict on every run.
- **REQ-0024-NFR-0010 — Language consistency**: Governance, role, skill,
  knowledge and prompt documents and the authored provider guidance are
  English, and every `README.md` is Korean; native keys, required headings,
  commands, quotations and preserved evidence retain their original syntax.
  Profile languages follow the
  [document language rule](../00.workspace/03.process/documentation-protocol.md#document-language).
  Provider adapters must not lose meaning; measure: registered metadata
  checks report no language-rule violation.
- **REQ-0024-NFR-0011 — Least privilege**: Agent permissions must be minimum scope and must not
  expose or change secrets, credentials, private keys, tokens, or
  unapproved external state; measure: no tracked
  permission grants a write outside the approved scope.
- **REQ-0024-NFR-0012 — Diagnosability**: A verification failure must be able to identify its
  owner and the target to fix, and a duplicate aggregate gate must not own
  the same predicate more than once; measure: each failing check
  names one owner.
- **REQ-0024-NFR-0013 — Currency**: The current document must match the tracked
  implementation, and legacy, deprecated, or conflicting rules must be
  removed from the current surface; measure: registered governance suites
  pass on the current tree.

#### Traceability

##### Sources

- **Governance entry**: [canonical agent governance](../../.agents/README.md)

##### Verification Links

###### Acceptance Conditions
<!-- core-payload-level:4 -->

- **REQ-0024-FR-0001**: Each agent policy, workflow, canonical role, canonical
  skill and provider-boundary rule has one owner under `.agents/`, and no file
  under `.claude/` or `.codex/` defines one.
- **REQ-0024-FR-0002**: Provider Registry entries hold only provider identity,
  projection route, model and permission translation, and hook binding; none
  sets a document profile, path or template.
- **REQ-0024-FR-0003**: Tracked files under `.claude/` and `.codex/` are
  classified as authored provider adapters, generated projections, or native
  runtime mechanics that the Provider Registry allows.
- **REQ-0024-FR-0004**: There is no name, source or scope drift between shared
  agent governance and provider surfaces, and the native entry of a canonical
  skill and its nested governance metadata preserve the same ID, owner and
  scope.
- **REQ-0024-FR-0005**: The bootstrap policy and both provider adapters route
  an agent that changes the repository to the relevant Requirement,
  Architecture, active Spec and current Task.
- **REQ-0024-FR-0006**: Spec and Plan states express approval authority, while
  Task and item states express execution. Executing Tasks have approved
  parents. A cancelled Spec requires a terminal Plan and terminal Tasks
  under the registered lifecycle.
- **REQ-0024-FR-0007**: The current authority does not use deleted execution
  ledgers as input, and no completion check requires a branch SHA pin, a corpus
  snapshot or a parallel handoff ledger.
- **REQ-0024-FR-0008**: Registered governance and document suites pass without
  dependence on historical fixtures, and the current authority does not use
  Stage 98 documents as input.
- **REQ-0024-FR-0014**: Every `.agents/` canonical category is one of the
  listed categories, and each Markdown instruction category has a registered
  Stage 99 profile and root inventory; evaluation data is not loaded as
  execution instructions, and no category holds execution progress state.
- **REQ-0024-FR-0015**: Both providers read and revise the same memory record
  from different worktrees, and a stale revision changes nothing.
- **REQ-0024-NFR-0009**: The same tree yields the same projection verdict on
  every run, and an unknown or conflicting input fails instead of falling back.
- **REQ-0024-NFR-0010**: Registered metadata checks report no language-rule
  violation.
- **REQ-0024-NFR-0011**: No tracked permission grants a write outside the
  approved scope, and explicit skill invocation configuration does not expand
  permissions.
- **REQ-0024-NFR-0012**: Each failing check names one owner, and no predicate
  is owned by more than one aggregate gate.
- **REQ-0024-NFR-0013**: Registered governance suites pass on the current tree.

###### Verification Method
<!-- core-payload-level:4 -->

Each condition is judged by running the registered governance and document suites on the current tree, as the determinism and currency measures state, and by reviewing the provider surfaces they classify. The condition that both providers revise the same memory record from different worktrees also needs a runtime observation across both providers, not only a suite run. The Spec Packages that list REQ-0024 as a parent, such as SPEC-0212 and SPEC-0244, record the suite results and the observation in their Task evidence rows. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

###### Downstream Links
<!-- core-payload-level:4 -->

- **Architecture Description**: [AD-0027 Agent Governance Canonical Adapter](../00.workspace/02.architecture/01.descriptions/0027-agent-governance-canonical-adapter.md)
- **Historical implementation evidence**: SPEC-0158; SPEC-0264 (retired; version history) delivered folder guides; SPEC-0253 (retired; version history) removed the frozen archive payload boundary and the deleted-Task CI evidence owner from QA and CI; SPEC-0270 (retired; version history) delivered the 1 GiB shared memory capacity ledger, bounded read-only search and memory backup source
- SPEC-0254 (retired; version history) delivered the plain-text stage identities in infra READMEs, the agent-governance suite selection for folder guide edits, the `common/agent-guide` type and the active folder guides.
- SPEC-0251 (retired; version history) split folder README (people) from folder AGENTS.md (agents), added the placement rule and the nine first folder guides.
- **Decision**: [ADR-0032 Canonical Agent Governance Home](../00.workspace/02.architecture/02.decisions/0032-canonical-agent-governance-home.md)
- **Decision**: [ADR-0034 Canonical Knowledge and Prompt Surfaces](../00.workspace/02.architecture/02.decisions/0034-canonical-knowledge-and-prompt-surfaces.md)
- **Decision**: [ADR-0049 Shared Agent Memory Store](../00.workspace/02.architecture/02.decisions/0049-shared-agent-memory-store.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
