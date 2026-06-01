---
status: draft
---
<!-- Target: docs/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md -->

# Agent Governance Phase 2 Alignment Plan

## Overview (KR)

이 문서는 Phase 1 조사 결과를 바탕으로 `hy-home.docker`의 공유 AI Agent 거버넌스(Stage 00), 문서 체계, Codex 하네스, Docker/Compose 운영 규칙, QA/CI/CD 규칙, Skill 전략을 Phase 3에서 안전하게 개선하기 위한 Phase 2 계획서다.

Phase 2는 계획만 작성한다. Stage 00, template, provider harness, validator, Docker runtime, CI 설정, `.codex/agents/*.toml` 값은 이 단계에서 변경하지 않는다. 구현은 사용자가 이 계획을 승인한 뒤 Phase 3에서만 수행한다.

## Context

### Current Workspace Purpose

`hy-home.docker`는 Docker Compose 기반 홈/개발 인프라와 agent-first engineering workflow를 함께 관리하는 저장소다. 루트 `docker-compose.yml`, `infra/**`, `secrets/**`, `.github/**`, `scripts/**`, stage-gated docs가 하나의 운영/거버넌스 표면을 이룬다.

### Current Evidence

- Stage 00 already defines shared governance, provider adapters, Template Contract, QA/CI/CD policy, Model Policy, and clarification duty.
- Codex currently has `.codex/agents/*.toml`; `workflow-supervisor` uses `gpt-5.5` with `model_reasoning_effort = "xhigh"`, and workers use `gpt-5.4-mini` with `model_reasoning_effort = "medium"`.
- `.codex/agents/*.md` also exists as a legacy/compatibility prompt surface.
- Repository validators currently pass, including provider surface sync, repo contracts, doc traceability, LLM Wiki freshness, `.codex/hooks.json` JSON syntax, and `git diff --check`.
- Graphify is advisory because `report-graphify-health.sh` reports `surprising_cross_root_inferred_edges`; architecture claims must be corroborated against tracked source files and stage docs.
- HADS block tags and AI manifest conventions are not currently integrated into `docs/99.templates/**` or Stage 00.
- Superpowers process skills and IMP documentation/Docker/QA/DevOps/architecture/data skills are partially represented by existing policies, but not mapped as a coherent Stage 00 workflow and skill-adapter policy.

### Existing Historical Artifacts

The prior Phase 2 and Phase 3 artifacts remain historical evidence:

- `docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md`
- `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md`
- `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md`

This plan supersedes stale assumptions in earlier Phase 2 text where the current worktree now proves a different state, especially the existence of `.codex/agents/*.toml`.

## Goals & In-Scope

- **Goals**:
  - Convert Phase 1 findings into an approval-gated Phase 3 roadmap.
  - Preserve Stage 00 as the single source of truth for shared governance.
  - Plan how to integrate HADS, Superpowers, IMP documentation, Docker, QA, DevOps, architecture, and data-engineering strategies without creating a second governance layer.
  - Plan Codex harness alignment around existing `.codex/agents/*.toml`, legacy `.md` compatibility handling, `.codex/skills/**`, hooks, model fields, and QA/CI/CD participation.
  - Plan how to close semantic gaps that current green validators do not prove.
- **In Scope**:
  - `docs/00.agent-governance/**`
  - `docs/99.templates/**`
  - Target-stage docs under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, and `docs/90.references`
  - `AGENTS.md`, `.codex/README.md`, `.codex/agents/**`, `.codex/skills/**`, `.codex/hooks.json`
  - Provider adapter docs and surfaces for Claude, Codex, and Gemini when required to preserve shared governance parity
  - `scripts/operations/sync-provider-surfaces.sh`, `scripts/validation/**`, and `scripts/knowledge/**` where Phase 3 needs validation coverage
  - Docker/Compose policy surfaces and documentation, not live runtime changes

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not implement any Stage 00, template, validator, Codex harness, Docker, CI, or runtime changes during Phase 2.
  - Do not migrate, delete, or rewrite legacy `.codex/agents/*.md` during Phase 2.
  - Do not treat current passing checks as proof that HADS, Superpowers, or IMP strategies are fully integrated.
  - Do not create non-canonical active docs paths such as `docs/superpowers/**`; repository stage taxonomy remains canonical.
- **Out of Scope**:
  - User-global Codex settings under `/home/hy/.codex`
  - Secrets, credentials, private tokens, shell history, or deployment state
  - Docker service start/stop/recreate, image rebuilds, migrations, or live network changes
  - Remote GitHub branch protection mutation
  - Direct Phase 3 implementation before user approval

## Concept Area Plan

| Concept Area | Current State | Desired State | Phase 3 Change Type |
| --- | --- | --- | --- |
| Agent | Stage 00 agent catalog and `.codex/agents/*.toml` are aligned by validators. | Stage 00 remains canonical; provider adapters are explicitly format-only implementations. | Clarify provider-adapter wording and legacy `.md` role. |
| Skill | Function catalog, `.codex/skills/**`, `.claude/skills/**`, and user/global skill references are not described as one unified skill lifecycle. | Stage 00 defines shared skill triggering, skill metadata, skill-to-stage mapping, and provider-specific loading surfaces. | Add skill lifecycle and adapter rules; update validation/manual gates if needed. |
| Rule | Rules exist across Stage 00 and hooks. | Rules distinguish active policy, advisory memory, provider mechanics, and runtime hooks. | Merge duplicated rule text; remove provider-specific policy forks. |
| Hook | Codex hooks exist via `.codex/hooks.json`; shared semantics live in Stage 00. | Hook behavior is described as guardrail routing, not a second policy store. | Clarify hook parity and validation responsibilities. |
| Sub-agent | `subagent-protocol.md` defines model tiers and provider mapping. | Sub-agent routing explicitly maps role complexity to model and reasoning effort while preserving provider availability caveats. | Refine model/reasoning table and task-complexity mapping. |
| Output Style | Output style rules exist but are not fully tied to humanizer/doc-writing strategies. | Human-facing output rules include concise, non-promotional, evidence-first writing standards. | Incorporate IMP humanizer principles into output style without adding decorative prose rules. |
| Workflow | Stage workflow exists; Superpowers flow is scattered in historical tasks. | Stage 00 maps brainstorming, writing-plans, executing-plans, TDD, debugging, verification, and finishing-branch into canonical stage workflows. | Add workflow mapping table and conflict rule for non-stage Superpowers default paths. |
| Memory | Memory/progress is advisory and mandatory for completion. | Memory updates remain mandatory in implementation phases while Phase 2 plan-only constraints are explicitly documented. | Clarify Phase 2 exception or progress-log timing in plan/task conventions. |
| QA | QA scope has TDD-first and verification guidance. | QA maps TDD, senior-QA coverage, regression, manual gates, and evidence-before-claims into one policy. | Refine QA scope and task checklist. |
| CI/CD | GitHub governance defines local/remote CI boundaries. | CI/CD policy maps Codex-visible commands, CI-only jobs, manual evidence, and non-automatable gates. | Expand policy matrix and provider participation notes. |
| Model Policy | Current policy and TOML fields are aligned. | Policy states allowed model IDs, reasoning-effort values, complexity tiers, and evidence limits as of the accepted baseline. | Add baseline/evidence note and validation boundary wording. |
| Template Contract | Templates are enforced by validators, but HADS is absent. | Template Contract states whether HADS is required, optional, or prohibited per document type. | Add HADS decision and template overlay plan after approval. |

## Template Contract & Document Plan

| Template Type | Template Adjustment Decision | Document Refactor Plan | Notes |
| --- | --- | --- | --- |
| PRD | No structural change planned unless HADS overlay is approved. | Only refactor PRDs if validator or HADS decision reveals required metadata gaps. | Keep requirements testable and downstream-linked. |
| ARD | No immediate change planned. | Preserve existing ARD shape; add HADS only if approved as a non-breaking overlay. | Architecture docs should stay concise and decision-linked. |
| ADR | No immediate change planned. | Avoid rewriting historical decisions except for required frontmatter/template violations. | Historical semantics must be preserved. |
| Spec | Potentially add optional AI-readable block guidance. | Refactor only active specs affected by governance or Docker/Compose policy changes. | Avoid broad speculative spec rewrites. |
| Plan | Add explicit skill-strategy and approval-gate fields only if the repo adopts them. | New or updated plans should show skill mapping and verification strategy. | This plan is the immediate example. |
| Task | Add stronger evidence fields only if required by Phase 3 validation. | Future Phase 3 task must record commands, skipped checks, and user approvals. | Task remains evidence, not new requirements. |
| Guide | Consider Diataxis alignment with existing guide/policy/runbook split. | Update only docs impacted by Docker/Compose or agent workflow changes. | Avoid mixing guide and runbook headings. |
| Policy | Consider HADS `[SPEC]` blocks for active policy only after approval. | Policy docs should remain authoritative and validator-friendly. | Do not introduce ambiguous prose tags. |
| Runbook | Consider `[BUG]` blocks for verified failure/fix patterns only after approval. | Runbooks remain procedure-first; HADS must not disrupt required headings. | Must preserve operations profile contract. |
| Incident/Postmortem | No HADS change planned unless incident docs need AI-readable RCA blocks. | Preserve incident timeline and RCA template requirements. | Avoid retroactive history rewriting. |
| Reference | HADS is most useful here as optional AI-readable facts and caveats. | Candidate pilot area for HADS overlay if user approves. | Lower risk than active policy docs. |

## Skill Strategy Alignment Plan

| Skill Strategy | Repository Fit | Planned Integration |
| --- | --- | --- |
| `superpowers:using-superpowers` | Matches explicit skill-loading discipline, but Stage 00 must not depend on one plugin implementation. | Add provider-neutral "skill applicability before action" rule and adapter-specific loading notes. |
| `superpowers:brainstorming` | Conflicts with default `docs/superpowers/specs/**` path; repo requires canonical stage paths. | Map brainstorming output to PRD/ARD/Spec/Plan depending on stage; forbid active non-stage specs. |
| `superpowers:writing-plans` | Aligns with `docs/04.execution/plans/**`. | Use plan template as canonical path; require file/path/test/verification specificity scaled to repo docs work. |
| `superpowers:executing-plans` | Aligns with task-by-task execution evidence. | Map execution to `docs/04.execution/tasks/**`; require plan review before implementation. |
| `superpowers:test-driven-development` | Already partially represented by QA scope. | Make red/green/refactor mandatory for code behavior changes, with documented N/A for docs-only work. |
| `superpowers:systematic-debugging` | Fits incident, troubleshooting, and bug-fix workflows. | Add root-cause-before-fix requirement for bugs, CI failures, and runtime incidents. |
| `superpowers:verification-before-completion` | Already matches evidence-first policy. | Promote evidence-before-claims to completion gate across providers. |
| `superpowers:finishing-a-development-branch` | Overlaps with GitHub governance and git workflow rules. | Add branch-finalization checklist: verify, inspect status/diff, stage only scoped changes, commit/PR/cleanup by approval. |
| `imp-humanizer` | Useful for human-facing Korean docs and final responses. | Add concise, specific, non-promotional writing guidance to output style and docs protocol. |
| `documentation-standards:hads` | Not currently integrated. | Add decision gate for HADS overlay mode before editing templates. |
| `imp-doc-coauthoring` | Useful for collaborative docs and reader testing. | Add optional reader-test/subagent-review gate for high-impact docs. |
| `imp-documentation-writer` | Diataxis maps well to guide/how-to/reference/explanation separation. | Align Diataxis terms with existing guide/policy/runbook/reference taxonomy without renaming stages. |
| Docker skill family | Already represented across infra/security scopes and compose validators. | Consolidate into one Docker policy matrix and decide which checks become hard gates. |
| `imp-senior-qa` | Matches QA scope and CI gate planning. | Add coverage/regression/manual-evidence expectations by change type. |
| `imp-senior-devops` | Matches CI/CD and deployment discipline. | Add pipeline/deployment strategy guidance without changing remote protections in Phase 3 unless approved. |
| `imp-senior-architect` | Matches ADR/ARD and provider adapter redesign. | Add architecture-decision triggers for non-trivial governance/runtime changes. |
| `imp-senior-data-engineer` | Relevant to data tier and data docs, less central to Stage 00. | Add data-specific QA/security references only where data-stage docs or services are touched. |

## Codex Harness Alignment Plan

| Surface | Current State | Planned Phase 3 Treatment |
| --- | --- | --- |
| `AGENTS.md` | Thin bootstrap shim referencing Stage 00. | Keep thin; only add or adjust pointers if current wording fails to mention Phase 2-approved policies. |
| `.codex/README.md` | Codex runtime surface and scope are documented. | Clarify TOML adapter role, legacy Markdown prompt role, hooks, and skill adapter surfaces. |
| `.codex/agents/*.toml` | Exists and validates model/reasoning fields. | Preserve unless Phase 3 finds role/model drift; do not introduce Codex-only governance. |
| `.codex/agents/*.md` | Legacy/compatibility prompt files still exist. | Decide whether to mark as compatibility docs, generate from Stage 00, or retire in a separate approved change. |
| `.codex/skills/**` | Runtime skills mirror governance functions unevenly. | Plan catalog-depth rules and skill metadata validation without copying full skill bodies into Stage 00. |
| `.codex/hooks.json` | Valid JSON hook dispatch surface. | Keep as mechanism; policy stays in Stage 00. |

## Docker, QA, DevOps, Architecture, and Data Plan

| Area | Planned Common Rule | Candidate Evidence |
| --- | --- | --- |
| Dockerfile optimization | Multi-stage builds, pinned base images, `.dockerignore`, non-root users, health checks, no secrets in image layers. | Dockerfile review checklist, `check-repo-contracts.sh`, optional image scan gate if tooling exists. |
| Docker Compose orchestration | Specific image tags, profile-aware configs, health checks, named volumes, network segmentation, resource limits where applicable. | `validate-docker-compose.sh`, compose profile checks, infra README rubric. |
| Docker security | No plaintext secrets, Docker Secrets or mounted secrets, `no-new-privileges`, capability drops/read-only filesystems where compatible. | Hookify secret rules, hardening scripts, security scope, compose validation. |
| QA | TDD for behavior changes, regression evidence for bug fixes, smallest meaningful local checks, manual N/A rationale for docs-only changes. | QA scope, repo contracts, doc traceability, targeted test commands. |
| DevOps | Local-vs-remote boundary, required CI jobs, branch/PR discipline, deployment changes only with explicit approval. | GitHub governance, workflows, rulesets, task evidence. |
| Architecture | Non-trivial trade-offs require ADR/ARD or documented decision gate. | Stage authoring matrix, architecture docs, provider adapter plan. |
| Data engineering | Data pipelines/services require schema, lineage, security, monitoring, and backup/restore evidence where touched. | Data-tier specs, operations docs, data quality checks if available. |

## Decision Gates Before Phase 3

| Gate | Status | Decision Needed | Default if Not Approved |
| --- | --- | --- | --- |
| DG-006 | Open | Should HADS become a required template overlay, an optional reference-doc overlay, or advisory guidance only? | Advisory only; no template conversion. |
| DG-007 | Planned | Keep Superpowers outputs inside canonical stage paths rather than `docs/superpowers/**`. | Use canonical stage paths. |
| DG-008 | Open | Should `.codex/agents/*.md` be retained as compatibility prompts, generated from Stage 00, or retired after TOML adoption? | Retain as compatibility prompts. |
| DG-009 | Open | Which Docker best-practice items become hard validators versus manual review checklist items? | Manual checklist only for new hardening rules. |
| DG-010 | Open | Should Phase 3 create a new task document for this continuation or append to the prior Phase 3 task? | Create a new task document to preserve historical evidence. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Preserve Phase separation and record that Phase 2 is planning-only. | This plan | PHASE-2 | Plan contains no implementation change instructions for this phase. |
| PLN-002 | Plan Stage 00 concept and workflow consolidation. | `docs/00.agent-governance/README.md`, `rules/workflows.md`, `rules/output-style.md`, `rules/task-checklists.md` | GOV-CONCEPTS | Concept/workflow table maps every requested strategy to a canonical stage rule. |
| PLN-003 | Plan Template Contract and HADS decision path. | `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `docs/99.templates/**` | TPL-HADS | HADS integration mode is approved or remains advisory; no silent conversion. |
| PLN-004 | Plan Skill model and runtime skill alignment. | `agents/functions/**`, `.codex/skills/**`, `.claude/skills/**`, `.agents/**`, sync/validation scripts | SKILL-ALIGN | Skill metadata, trigger, catalog depth, and provider adapter expectations are defined. |
| PLN-005 | Plan Codex harness clarification. | `AGENTS.md`, `.codex/README.md`, `.codex/agents/**`, `.codex/hooks.json` | HARNESS-CODEX | Codex harness implements Stage 00 without separate governance. |
| PLN-006 | Plan Model Policy and reasoning-effort guardrails. | `subagent-protocol.md`, `provider-capability-matrix.md`, `providers/codex.md`, validators | MODEL-POLICY | Allowed models/effort values and evidence boundary are explicit. |
| PLN-007 | Plan Docker/Compose policy matrix. | `scopes/infra.md`, `scopes/security.md`, Docker function catalog, `infra/README.md`, validation scripts | DOCKER-POLICY | Build/runtime/security/compose rules are mapped to hard checks or manual gates. |
| PLN-008 | Plan QA/CI/CD evidence model. | `scopes/qa.md`, `rules/github-governance.md`, `.github/**`, `scripts/**`, task template if approved | QA-CICD | Each change type maps to smallest local check, CI gate, and manual evidence. |
| PLN-009 | Plan architecture/data-specialist integration. | Stage authoring matrix, ARD/ADR docs, data-tier specs/operations docs | ARCH-DATA | Specialist rules trigger only when relevant files/domains are touched. |
| PLN-010 | Plan Phase 3 traceability. | Future task doc, progress log, LLM Wiki index if new tracked paths are added | TRACE | Phase 3 has a paired task with commands, results, skipped checks, approvals, and open issues. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Scope | Confirm Phase 2 changed only allowed plan artifacts. | `git diff --name-only` | Only this plan file changes, unless user approves additional plan artifacts. |
| VAL-PLN-002 | Structural | Repository contract check after plan update. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`, or any plan-only failure is recorded. |
| VAL-PLN-003 | Traceability | Document traceability check. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-PLN-004 | Hygiene | Markdown/trailing whitespace diff hygiene. | `git diff --check` | No whitespace errors. |
| VAL-PLN-005 | Provider Surface | Confirm current provider adapters are still synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-PLN-006 | LLM Wiki | Confirm generated LLM Wiki index is fresh. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-PLN-007 | Advisory Graph | Keep Graphify advisory status from driving uncorroborated claims. | `bash scripts/knowledge/report-graphify-health.sh` | Advisory reasons recorded; source docs remain authoritative. |
| VAL-PLN-008 | Runtime Safety | Confirm no Docker runtime, secrets, deployment, or remote GitHub state changed. | `git status --short --branch` plus command audit | No runtime/state-changing commands were run. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| HADS conversion creates broad churn in hundreds of docs. | High | Start with advisory or reference-doc pilot unless the user approves required overlay mode. |
| Superpowers default paths conflict with repository stage taxonomy. | Medium | Map outputs to canonical `docs/01`-`docs/05`, `docs/90`, and `docs/99`; do not create active `docs/superpowers/**`. |
| Docker best-practice advice becomes too generic or incompatible with existing services. | High | Convert only repo-compatible rules into hard gates; keep the rest as review checklist items. |
| Legacy Codex Markdown prompts are removed too early. | Medium | Retain as compatibility prompts until adapter generation/retirement is explicitly approved. |
| Existing completed Phase 3 evidence is overwritten. | High | Preserve historical task docs; create new Phase 3 task for this continuation if implementation proceeds. |
| Model policy overclaims provider availability. | High | Keep local validators limited to repository policy shape; require official/provider evidence before model promotion. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Phase 3 must pass repo contracts, doc traceability, provider sync, LLM Wiki freshness, diff hygiene, and any new manual checks approved from this plan.
- **Sandbox / Canary Rollout**: N/A for plan-only work. Runtime Docker canary is out of scope unless a later approved implementation changes runtime behavior.
- **Human Approval Gate**: Required before Phase 3 implementation, especially for DG-006, DG-008, DG-009, and DG-010.
- **Rollback Trigger**: Revert Phase 3 changes if they create separate governance, break provider parity, or enforce unapproved template/Docker/model rules.
- **Prompt / Model Promotion Criteria**: No new model, model alias, or reasoning-effort value is promoted unless Stage 00 and official/provider evidence agree.

## Completion Criteria

- [x] Phase 2 scope is limited to plan content.
- [x] Current worktree facts replace stale Phase 2 assumptions.
- [x] Stage 00, Template Contract, Skill strategy, Codex harness, Docker/Compose, QA/CI/CD, architecture, and data concerns are mapped to concrete Phase 3 planning tasks.
- [x] Open high-impact decisions are isolated as decision gates rather than silently implemented.
- [x] Phase 2 verification commands pass after this plan update.
- [ ] User approves or amends the decision gates before Phase 3 implementation.

## Related Documents

- **Prior Plan**: [2026-05-30-standardizing-agent-governance](./2026-05-30-standardizing-agent-governance.md)
- **Prior Claude Verification Plan**: [2026-05-31-claude-harness-governance-verification](./2026-05-31-claude-harness-governance-verification.md)
- **Prior Phase 3 Task**: [2026-06-01-agent-governance-phase3-implementation](../tasks/2026-06-01-agent-governance-phase3-implementation.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)
- **Operations Index**: [Operations index](../../05.operations/README.md)
