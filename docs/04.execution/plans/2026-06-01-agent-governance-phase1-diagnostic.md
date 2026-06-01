---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md -->

# Agent Governance Phase 1 Diagnostic

## Overview (KR)

이 문서는 `hy-home.docker`의 환경, 체계, 구조, 규칙을 고도화하기 위한 Phase 1 조사·분석 결과다.

Phase 1은 구현 단계가 아니다. 이 문서는 현재 워크스페이스의 문서, 실행 환경, Stage 00 거버넌스, provider adapter, Docker/DevOps/QA 규칙, 전략 skill 반영 상태를 근거 기반으로 진단하고, Phase 2 이후에 무엇을 수정·보완·개선·통합해야 하는지 설계 방향을 정리한다.

## Context

`hy-home.docker`는 Docker Compose 기반 홈/개발 인프라와 agent-first engineering workflow를 함께 관리하는 저장소다. 루트 shim(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`), Stage 00 거버넌스, provider runtime surface(`.claude/`, `.codex/`, `.agents/`), stage-gated docs(`docs/01`-`docs/05`, `docs/90`, `docs/99`), 검증 스크립트, Compose 인프라가 하나의 작업 체계를 이룬다.

이 진단은 다음 근거를 기준으로 했다.

- `AGENTS.md`, `docs/00.agent-governance/rules/bootstrap.md`, `memory/README.md`, `memory/progress.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`, `documentation-protocol.md`, `workflows.md`, `task-checklists.md`
- `docs/00.agent-governance/providers/agents-md.md`, `providers/codex.md`, `.codex/README.md`
- `docs/01.requirements/README.md`, `docs/02.architecture/requirements/README.md`, `docs/02.architecture/decisions/README.md`
- `docs/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md`
- `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md`
- `graphify-out/GRAPH_REPORT.md` as advisory navigation only, corroborated against tracked docs and scripts

## Goals & In-Scope

- **Goals**:
  - 현재 문서, 환경, 체계, 구조, 규칙의 상태와 문제점을 요약한다.
  - 수정, 보완, 개선, 통합이 필요한 구체 항목을 식별한다.
  - 단순 보완으로 충분한 영역과 재설계 후보를 구분한다.
  - Stage 00 canonical adapter model 기준으로 agent/provider/runtime 구조를 진단한다.
  - 사용자가 지정한 Superpowers, HADS, Docker, DevOps, architecture, QA 전략을 어디에 녹여 넣을지 1차 설계를 제공한다.
- **In Scope**:
  - Stage 00 governance and provider adapter docs
  - Stage 01-05 lifecycle documents, references, templates
  - `.claude/`, `.codex/`, `.agents/` runtime adapter surfaces
  - `scripts/validation/**`, `scripts/operations/**`, `scripts/knowledge/**`
  - Docker/Compose policy and documentation surfaces
  - Node/npm/rtk toolchain visibility for future automation design

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not implement governance, template, validator, Docker, CI, or runtime changes in Phase 1.
  - Do not rewrite existing Stage 01-05 documents just because a gap is found.
  - Do not convert templates or stage docs to HADS in this phase.
  - Do not retire `.codex/agents/*.md` compatibility prompt files in this phase.
- **Out of Scope**:
  - Secrets, credential values, private keys, shell history, or token-bearing logs
  - Docker service start/stop/recreate, migrations, deployment, or live runtime mutation
  - Remote GitHub branch protection mutation
  - User-global Codex settings under `/home/hy/.codex`

## Current State Summary

| Axis | Current State | Diagnosis |
| --- | --- | --- |
| Documentation lifecycle | Canonical stages `docs/01`-`docs/05`, `docs/90`, `docs/99` are defined in bootstrap and stage matrix. There are 525 Markdown files under target stage/reference/template paths. | Mature structure exists. The risk is not absence of lifecycle, but accumulated historical plans/tasks and duplicated explanations that need curated consolidation rather than bulk rewrite. |
| Requirements to architecture | PRD inventory has 23 leaf documents. ARD and ADR inventories each have 23 leaf documents. | Broad PRD -> ARD/ADR coverage exists. Gateway and communication hardening PRDs are intentionally deferred, matching README notes. |
| Stage 00 governance | Stage 00 defines bootstrap, scopes, workflows, provider capability, task checklists, documentation protocol, hooks, memory, and provider overlays. | Stage 00 is the correct common policy source. It already contains the canonical adapter model and should remain the integration point for new strategy guidance. |
| Provider adapters | `.claude/`, `.codex/`, and `.agents/` expose aligned agent/skill surfaces. `.codex/agents/*.toml` are active Codex adapters; `.codex/agents/*.md` are compatibility prompt context. | The adapter model is implemented. Remaining work is clarity, drift prevention, and keeping compatibility prompts from becoming a second policy layer. |
| Workflows and skills | `workflows.md` maps stage-gate flow and external strategy adaptation. `.claude/skills`, `.codex/skills`, `.agents/skills` mirror workspace functions. | Strategy integration has started. Skill lifecycle, trigger depth, and external-vs-workspace skill boundaries need a stable review checklist. |
| Documentation standard | Template mapping, frontmatter status, related-documents rules, stage paths, and HADS advisory boundary are documented. | HADS is intentionally advisory. A future rollout needs an explicit pilot or template decision gate to avoid broad churn. |
| Docker/Compose governance | Infra and security scopes define Compose, secrets, network, hardening, and manual review expectations. `validate-docker-compose.sh` is the key static validation entrypoint. | Good policy coverage exists, but manual review vs hard validator boundaries should be kept explicit so best-practice advice does not become unreviewed enforcement. |
| QA/CI/CD | QA scope defines TDD-first behavior, coverage applicability, local-vs-remote boundary, and evidence expectations. GitHub governance and repo contracts enforce many static rules. | The evidence model is sound. Remaining work is mapping each change type to the smallest meaningful local check and the CI-only gates that should not be duplicated locally. |
| Execution environment | `/home/hy/.local/bin/node`, `npm`, and `rtk` exist. Direct `/home/hy/.local/bin/node --version` returns `v24.14.0`; `PATH=/home/hy/.local/bin:$PATH /home/hy/.local/bin/npm --version` returns `11.9.0`; `/home/hy/.local/bin/rtk --version` returns `rtk 0.34.3`. | Node-based automation is feasible, but agent-visible PATH cannot be assumed in every non-interactive shell. Future scripts should either source the repo QA/CI tooling helper or set PATH explicitly. |
| Knowledge graph | Graphify report exists and identifies Stage 00/community hubs, but health is advisory due to surprising inferred cross-root edges. | Use Graphify for navigation, not completion proof. Claims must be corroborated with tracked docs and validators. |

## PRD to ARD/ADR Coverage

| PRD item | ARD/ADR coverage | Gap type |
| --- | --- | --- |
| `2026-03-26-01-gateway.md` | `0001-gateway-architecture.md`; `0001-traefik-nginx-hybrid.md` | Covered |
| `2026-03-26-02-auth.md` | `0002-auth-architecture.md`; `0002-keycloak-oauth2-proxy-choice.md` | Covered |
| `2026-03-26-03-security.md` | `0003-security-architecture.md`; `0003-vault-as-secrets-manager.md` | Covered |
| `2026-03-26-04-data.md` | `0004-data-architecture.md`; `0004-postgresql-ha-patroni.md` | Covered |
| `2026-03-26-04-data-analytics.md` | `0012-data-analytics-architecture.md`; `0015-analytics-engine-selection.md` | Covered |
| `2026-03-26-05-messaging.md` | `0005-messaging-architecture.md`; `0005-kafka-vs-rabbitmq-selection.md` | Covered |
| `2026-03-26-06-observability.md` | `0006-observability-architecture.md`; `0006-lgtm-stack-selection.md` | Covered |
| `2026-03-26-07-workflow.md` | `0007-workflow-architecture.md`; `0007-airflow-n8n-hybrid-workflow.md` | Covered |
| `2026-03-26-08-ai.md` | `0008-ai-architecture.md`; `0008-ollama-openwebui-local-ai.md` | Covered |
| `2026-03-26-09-tooling.md` | `0009-tooling-architecture.md`; `0009-tooling-services.md` | Covered |
| `2026-03-26-10-communication.md` | `0010-communication-architecture.md`; `0010-communication-services.md` | Covered |
| `2026-03-26-11-laboratory.md` | `0011-laboratory-architecture.md`; `0011-laboratory-services.md` | Covered |
| `2026-03-27-08-ai-open-webui.md` | `0013-open-webui-architecture.md`; `0016-open-webui-implementation.md` | Covered |
| `2026-03-28-02-auth-optimization-hardening.md` | `0014-auth-optimization-hardening-architecture.md`; `0017-auth-hardening-runtime-and-fail-closed.md` | Covered |
| `2026-03-28-03-security-optimization-hardening.md` | `0018-security-optimization-hardening-architecture.md`; `0018-vault-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-04-data-optimization-hardening.md` | `0019-data-optimization-hardening-architecture.md`; `0019-04-data-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-05-messaging-optimization-hardening.md` | `0020-messaging-optimization-hardening-architecture.md`; `0020-messaging-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-06-observability-optimization-hardening.md` | `0021-observability-optimization-hardening-architecture.md`; `0021-observability-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-07-workflow-optimization-hardening.md` | `0022-workflow-optimization-hardening-architecture.md`; `0022-workflow-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-08-ai-optimization-hardening.md` | `0023-ai-optimization-hardening-architecture.md`; `0023-ai-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-09-tooling-optimization-hardening.md` | `0024-tooling-optimization-hardening-architecture.md`; `0024-tooling-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-03-28-11-laboratory-optimization-hardening.md` | `0025-laboratory-optimization-hardening-architecture.md`; `0025-laboratory-hardening-and-ha-expansion-strategy.md` | Covered |
| `2026-04-01-standardize-infra-net.md` | `0026-standardize-infra-net.md`; `0026-standardize-infra-net.md` | Covered |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| P1-001 | Load required bootstrap, memory, stage matrix, and requirements-to-design context. | `AGENTS.md`, `docs/00.agent-governance/**`, `.claude/skills/requirements-to-design-agent/skill.md` | Phase 1 discovery | Required source documents are listed in task evidence. |
| P1-002 | Inspect documentation lifecycle, inventories, and PRD -> ARD/ADR coverage. | `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/04.execution/**` | Documentation analysis | Coverage table records each PRD and matching ARD/ADR. |
| P1-003 | Inspect Stage 00 canonical adapter and provider runtime surfaces. | `docs/00.agent-governance/providers/**`, `.claude/**`, `.codex/**`, `.agents/**` | Structure analysis | Adapter model and compatibility boundaries are summarized. |
| P1-004 | Inspect Docker, QA/CI/CD, and Node/npm/rtk environment assumptions. | `docs/00.agent-governance/scopes/**`, `scripts/**`, `/home/hy/.local/bin/*` | Environment analysis | Tool versions and PATH caveat are recorded. |
| P1-005 | Produce Phase 1 output and validation evidence. | This plan, sibling task, Stage 04 READMEs, progress log | Phase 1 deliverables | Repository checks pass or failures are recorded. |

## Improvement Items

| ID | Area | Finding | Recommended Action | Priority |
| --- | --- | --- | --- | --- |
| P1-DOC-001 | Documentation consolidation | Stage docs are structurally mature, but Phase 1 evidence was implicit in later Phase 2/3 artifacts rather than captured as its own diagnostic artifact. | Keep this Phase 1 diagnostic as the upstream evidence source and link later Phase 2/3 artifacts to it when touched. | High |
| P1-DOC-002 | Documentation duplication | Stage 04 contains many historical workspace audit and governance plans/tasks. They are valuable evidence but hard to scan. | Add curated indexes or summaries instead of rewriting historical artifacts. | Medium |
| P1-DOC-003 | HADS | HADS is documented as advisory only. No template rollout mode is selected. | Treat HADS as a future decision gate: advisory, reference-doc pilot, or required template overlay. | Medium |
| P1-ENV-001 | Node toolchain | Node/npm/rtk exist under `/home/hy/.local/bin`, but non-interactive agent PATH may omit them. | Standardize future automation commands through explicit PATH or `scripts/operations/use-qa-ci-tools.sh`. | High |
| P1-GOV-001 | Canonical adapter | Stage 00 canonical adapter model exists and is implemented across provider surfaces. | Preserve Stage 00 as SSoT; avoid provider-specific policy forks. | High |
| P1-GOV-002 | Compatibility prompts | `.codex/agents/*.md` remain compatibility context beside active `.toml` adapters. | Keep compatibility prompts read-only/contextual unless a future approved retirement or generation plan exists. | Medium |
| P1-SKILL-001 | Skill strategy mapping | External strategy skills are partly mapped in `workflows.md`, but not every referenced IMP-style skill exists as a repo-local skill. | Treat unavailable external names as strategic lenses; encode only stable rules into Stage 00 docs or checklists. | Medium |
| P1-DOCKER-001 | Docker hardening | Docker best-practice expectations are documented, but many are manual review boundaries. | Decide case-by-case which become validators; do not silently hard-fail existing services. | High |
| P1-QA-001 | QA evidence | QA/TDD policy is strong, but docs-only/governance-only work needs explicit N/A rationale. | Keep task evidence tables recording command, pass/fail, and skipped-check rationale. | Medium |
| P1-GRAPH-001 | Graphify | Graphify is useful but advisory due to inferred cross-root edges. | Require source-doc and validator corroboration for architecture or completion claims. | Medium |

## Redesign Candidates

| Candidate | Current Shape | Redesign Scope | Recommendation |
| --- | --- | --- | --- |
| Stage 00 canonical adapter model | Already defined in `providers/agents-md.md` and reflected in provider surfaces. | Low redesign, high preservation. | Do not replace. Harden drift checks and documentation clarity only. |
| Skill lifecycle model | Workspace functions and provider skills exist, while external strategy skills are referenced as process lenses. | Medium redesign. | Define a small lifecycle table: discovery, applicability, provider loading, canonical artifact path, validation evidence. |
| Execution evidence index | Many plans/tasks exist, including repeated audits and governance remediation. | Medium redesign. | Add curated summaries or topic indexes over time; avoid bulk historical rewrites. |
| HADS integration | Advisory boundary only. | Optional redesign. | Pilot in `docs/90.references/` or keep advisory until a separate approved rollout. |
| Node automation baseline | Tools exist, PATH differs by shell context. | Small redesign. | Standardize script wrappers and docs around `/home/hy/.local/bin` or `use-qa-ci-tools.sh`. |
| Docker policy enforcement | Manual expectations plus existing static validators. | Selective redesign. | Promote only low-risk, repo-proven checks to hard validators; keep service-specific exceptions documented. |

## Skill Strategy Integration Plan

| Strategy group | Where to integrate | Proposed treatment |
| --- | --- | --- |
| `using-superpowers` | `rules/workflows.md`, `task-checklists.md`, provider notes | Keep as provider-neutral skill-applicability discipline. Canonical outputs remain in repo stage paths. |
| `brainstorming`, `writing-plans`, `executing-plans` | Stage authoring matrix, Stage 04 plan/task templates | Map idea exploration to PRD/ARD/Spec/Plan and execution to Task evidence. Do not create active non-stage `docs/superpowers/**` artifacts. |
| `test-driven-development`, `systematic-debugging`, `verification-before-completion` | `scopes/qa.md`, `rules/task-checklists.md`, task template | Enforce for behavior changes; record docs-only N/A rationale and evidence-before-claims. |
| `finishing-a-development-branch` | `rules/git-workflow.md`, `rules/github-governance.md`, task checklist | Keep branch finalization as verify, inspect diff/status, stage scoped files, commit/PR only when approved. |
| Code review skills | `agents/functions/code-review-dimensions.md`, `scopes/qa.md`, `github-governance.md` | Keep findings-first review format and require issue/evidence/action clarity. |
| HADS and documentation skills | `documentation-protocol.md`, `output-style.md`, templates only after approval | Keep HADS advisory now; use human-readable, concise, evidence-first Korean in human-facing docs. |
| Docker skill family | `scopes/infra.md`, `scopes/security.md`, Compose validators, operations docs | Maintain hard-vs-manual distinction. Promote only validated checks. |
| DevOps/CI/CD | `github-governance.md`, `scopes/qa.md`, `scripts/README.md` | Document local-vs-remote gate ownership and avoid duplicating heavy CI locally. |
| Architecture | `stage-authoring-matrix.md`, ARD/ADR README docs | Require ADR/ARD when non-trivial trade-offs or adapter model changes appear. |
| QA | `scopes/qa.md`, task template, repo validators | Keep TDD-first for behavior changes and verification evidence for docs/governance work. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P1-001 | Discovery | Confirm required bootstrap, memory, stage matrix, PRD/ARD/ADR inventories, Phase 2/3 evidence, Graphify report, provider docs, and toolchain facts were inspected. | Recorded in task evidence. | Evidence paths and commands listed. |
| VAL-P1-002 | Structural | Check repository contract after adding Phase 1 artifacts. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-P1-003 | Traceability | Check document traceability. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-P1-004 | Provider | Confirm provider surfaces remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-P1-005 | LLM Wiki | Confirm generated repository index freshness. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-P1-006 | Hygiene | Check whitespace/diff hygiene. | `git diff --check` | PASS. |
| VAL-P1-007 | Graph | Confirm Graphify is advisory and not used as sole proof. | `bash scripts/knowledge/report-graphify-health.sh` | Advisory status recorded, if present. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Treating Phase 1 as implementation | High | This artifact records diagnostics only; no runtime, validator, policy, or template behavior is changed here. |
| Overwriting historical evidence | High | Historical Stage 04 documents are referenced, not rewritten. |
| Assuming PATH works everywhere | Medium | Record explicit `/home/hy/.local/bin` evidence and require explicit PATH handling in future automation. |
| Overfitting to Graphify | Medium | Treat Graphify as advisory and corroborate against tracked docs/scripts. |
| Creating duplicate governance | High | Stage 00 remains the only canonical policy and adapter catalog. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Phase 1 completion requires repo contracts, doc traceability, provider sync, LLM Wiki freshness, diff hygiene, and Graphify advisory recording.
- **Sandbox / Canary Rollout**: N/A. This phase does not touch Docker runtime, deployments, or remote state.
- **Human Approval Gate**: Required before any future HADS rollout, Docker hard-validator promotion, compatibility prompt retirement, runtime mutation, deployment, or remote GitHub protection change.
- **Rollback Trigger**: Remove this diagnostic artifact if a broader approved discovery artifact supersedes it and all downstream links are updated.
- **Prompt / Model Promotion Criteria**: N/A. No model policy change occurs in Phase 1.

## Completion Criteria

- [x] Current-state evidence inspected.
- [x] Documentation, environment, governance, adapter, Docker, QA/CI/CD, and skill strategy findings summarized.
- [x] Improvement items and redesign candidates listed.
- [x] Skill/strategy integration plan drafted.
- [x] Verification evidence recorded in the sibling task document.

## Related Documents

- **Phase 1 Task**: [Agent Governance Phase 1 Diagnostic Task](../tasks/2026-06-01-agent-governance-phase1-diagnostic.md)
- **Phase 2 Plan**: [Agent Governance Phase 2 Alignment Plan](./2026-06-01-agent-governance-phase2-alignment.md)
- **Phase 3 Strategy Task**: [Agent Governance Phase 3 Strategy Integration Task](../tasks/2026-06-01-agent-governance-phase3-strategy-integration.md)
- **Stage 00 Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Canonical Adapter Model**: [AGENTS.md Provider-Neutral Notes](../../00.agent-governance/providers/agents-md.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
