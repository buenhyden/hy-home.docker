---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md -->

# Stage 00 and Codex Harness Governance Alignment Plan

> Phase 3 implementation was approved by the user on 2026-05-31 and completed
> against this plan.

## Overview (KR)

이 문서는 `hy-home.docker`의 단일 공유 AI Agent 거버넌스(Stage 00)와 Codex 하네스를 정렬하기 위한 실행 계획서다. Phase 1 조사 결과와 사용자 확인 사항을 바탕으로, Stage 00 개념 정의, QA/CI/CD 정책, Template Contract, Model Policy, Codex runtime mirror를 하나의 거버넌스 아래로 정리한다.

## Context

Phase 1은 읽기 전용으로 수행했다. `docs/00.agent-governance/**`, `docs/99.templates/**`, `docs/01`-`docs/05`, `docs/90`, `AGENTS.md`, `.codex/agents/*.md`, `.codex/skills/**`, `.codex/hooks.json`, validator, GitHub Actions workflow를 확인했다.

현재 기준선은 다음과 같다.

- `bash scripts/validation/check-repo-contracts.sh`: PASS, `target_stage_docs_total=499`, `normalized_target_stage_docs_total=497`, `legacy_target_stage_docs_skipped=2`.
- `bash scripts/validation/check-doc-traceability.sh`: PASS, `catalog_pairs_total=46`.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check`: PASS.
- `bash scripts/knowledge/report-graphify-health.sh`: advisory, `surprising_cross_root_inferred_edges=3`.
- `git status --short`: clean at the end of Phase 1.

User-confirmed decisions for Phase 2 and Phase 3:

- Codex harness target remains the current `.codex/agents/*.md` YAML frontmatter structure. Do not introduce `.codex/agents/*.toml`.
- Codex supervisor model target is `gpt-5.5`.
- Codex worker model targets are `gpt-5.4-mini` by default and `gpt-5.3-codex` where coding-specialized worker behavior is explicitly justified.
- Stage 00 English-only remediation includes `github-governance.md` and Korean hookify messages; do not leave Korean hook message text as an exception.

## Goals & In-Scope

- **Goals**:
  - Add a shared Stage 00 clarification duty: ambiguous requirements, scope, policy interpretation, model selection, or configuration intent must trigger user questions before irreversible planning or implementation.
  - Define shared concepts once: Agent, Skill, Rule, Hook, Sub-agent, Output Style, Workflow, Memory, QA, CI/CD, Model Policy, and Template Contract.
  - Define one workspace-wide QA & CI/CD policy, not separate provider-specific policies.
  - Define one Template Contract mapping `docs/99.templates/**` to `docs/01`-`docs/05`, `docs/90`, and `docs/99`.
  - Update the shared Model Policy and Codex harness policy around `gpt-5.5`, `gpt-5.4-mini`, and `gpt-5.3-codex`.
  - Keep Codex as a provider harness that implements Stage 00 through `AGENTS.md`, `.codex/agents/*.md`, `.codex/skills/**`, and `.codex/hooks.json`.
  - Record Phase 3 changes and verification evidence in the paired task document.
- **In Scope**:
  - `docs/00.agent-governance/**`
  - `docs/99.templates/README.md` and template mapping references
  - Targeted template-compliance fixes under `docs/01`-`docs/05`, `docs/90`, and `docs/99` when needed to close undocumented deviations
  - `AGENTS.md`
  - `.codex/README.md`
  - `.codex/agents/*.md`
  - `.codex/skills/**` only when needed for shared Skill model alignment
  - `.codex/hooks.json` only when needed for hook parity and QA/CI/CD routing
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/operations/sync-provider-surfaces.sh`
  - `.github/workflows/ci-quality.yml` and `.github/rulesets/main-protection.md` only if Stage 00 QA/CI/CD job taxonomy changes require synchronized updates
  - `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not create a separate Codex governance, QA policy, Template Contract, or Model Policy.
  - Do not introduce `.codex/agents/*.toml`.
  - Do not rewrite unrelated infrastructure service behavior.
  - Do not change Docker runtime state, start or stop services, deploy, migrate data, or read secret values.
  - Do not normalize every historical document by style preference alone.
- **Out of Scope**:
  - User-global Codex configuration under `/home/hy/.codex`.
  - Remote GitHub branch protection mutation.
  - `projects/storybook/mcp/` runtime/package behavior unless an existing validator or documented QA gap requires a read-only note.
  - New external model-provider policy beyond the verified Stage 00 provider set.

## Current State to Desired State

| Concept Area | Current State | Desired State |
| --- | --- | --- |
| Agent / Sub-agent | Catalog, provider parity matrix, and subagent protocol define behavior, but concept definitions are distributed. | Stage 00 names one concept definition and links it to catalog and runtime surfaces. |
| Skill / Function | Workspace functions and runtime skills are treated together, but the distinction between catalog function, runtime skill, and external skill is not crisp. | Stage 00 defines the three terms and keeps provider mirrors from becoming separate policy. |
| Rule | `rules/*.md` is the practical SSoT. | Rule definition and precedence are explicit; provider overlays may bind rules but not redefine them. |
| Hook | Hook parity exists, but hook schema and user-facing message language are inconsistent. | Hook definition, parity, message-language policy, and validation routing are explicit and English-only in Stage 00. |
| Output Style | `rules/output-style.md` is the contract; Codex follows behaviorally. | No duplicate provider style policy; Codex references shared contract only. |
| Workflow | `rules/workflows.md` defines workflows, but external skills and provider mechanics are mixed in prose. | Workflow definition separates provider-neutral function chain from runtime adapter mechanics. |
| Memory | Memory policy exists and progress logging is mandatory. | Memory remains advisory, with clear interaction with phase separation and read-only phases. |
| QA | QA scope and test automator exist; some checks are spread across scripts and CI. | One workspace QA policy maps change types to smallest meaningful local checks and CI gates. |
| CI/CD | GitHub governance lists jobs, but the taxonomy mixes local scripts, inline shell, npm scripts, and CI-only jobs. | CI/CD policy names local vs remote responsibility accurately and keeps required-check tables synchronized. |
| Model Policy | Stage 00 and Codex provider disagree on worker model (`gpt-5.5-instant` vs `gpt-5.4-mini`); actual `.codex/agents/*.md` use `gpt-5.5-instant`. | Stage 00 defines `gpt-5.5` supervisor, `gpt-5.4-mini` general workers, and `gpt-5.3-codex` coding-specialized workers where justified; Codex mirror and validators enforce it. |
| Template Contract | `guide.template.md`, `policy.template.md`, and `runbook.template.md` exist, but some docs still reference nonexistent `operation.template.md`. | One mapping table is consistent across documentation protocol, stage matrix, template README, and validators. |
| Clarification Duty | Existing policy says to stop on conflicts, but underspecification handling is not centralized. | Stage 00 requires clarifying questions before high-impact assumptions in planning, policy, model, template, or config work. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add shared concept glossary and clarification duty to Stage 00 without duplicating provider policy. | `docs/00.agent-governance/README.md`, `rules/agentic.md`, `rules/task-checklists.md`, `rules/output-style.md`, related scope/provider docs | GOV-CLARIFY, GOV-CONCEPTS | Stage 00 has one clear clarification rule and no contradictory concept definitions. |
| PLN-002 | Reconcile Template Contract mapping and document exceptions. | `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `docs/99.templates/README.md`, `scripts/validation/check-repo-contracts.sh` | TPL-SSOT | No active reference to nonexistent `operation.template.md`; split guide/policy/runbook templates are consistently mapped. |
| PLN-003 | Plan and apply bounded template-compliance fixes or documented exceptions for known deviations. | `docs/04.execution/plans/*.md`, `docs/04.execution/tasks/*.md`, affected operations docs only when required | TPL-COMPLIANCE | Undocumented legacy skips, duplicate Related Documents sections, status vocabulary drift, or duplicated policy headings are resolved or documented. |
| PLN-004 | Update shared Model Policy and Codex model mapping. | `subagent-protocol.md`, `rules/provider-capability-matrix.md`, `providers/codex.md`, `.codex/agents/*.md`, `scripts/validation/check-repo-contracts.sh`, `scripts/operations/sync-provider-surfaces.sh` | MODEL-CODEX | `.codex/agents/*.md` use allowed Codex model IDs and no `.toml` files are introduced. |
| PLN-005 | Align Codex runtime mirror language and skill references with Stage 00. | `.codex/README.md`, `.codex/agents/*.md`, `.codex/skills/**`, `providers/codex.md` | HARNESS-CODEX | Codex files do not define separate governance and do not carry stale Anthropic-only model wording as Codex policy. |
| PLN-006 | Normalize Stage 00 English-only content, including `github-governance.md` and hookify messages. | `docs/00.agent-governance/rules/github-governance.md`, `docs/00.agent-governance/rules/hooks/*.md`, any related provider docs | GOV-LANG | `docs/00.agent-governance/**` contains no Korean prose after intentional code/path literals are excluded. |
| PLN-007 | Reconcile QA & CI/CD policy with actual commands and CI jobs. | `rules/github-governance.md`, `scopes/qa.md`, `rules/workflows.md`, `scripts/README.md`, `.github/workflows/ci-quality.yml`, `.github/rulesets/main-protection.md` if needed | QA-CICD | Local-vs-remote job taxonomy accurately represents scripts, inline checks, npm checks, and CI-only jobs. |
| PLN-008 | Record execution evidence in the paired task document during Phase 3. | `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md`, `docs/00.agent-governance/memory/progress.md` | TRACE | Task table and verification summary reflect actual files changed and checks run. |

## Execution Sequence

1. Update Stage 00 shared definitions and clarification duty first.
2. Reconcile Template Contract SSoT tables before changing target-stage documents.
3. Update Model Policy and Codex harness mapping, then update validator expectations.
4. Run provider surface sync in verification mode, then write mode only if the approved implementation edits the canonical runtime source that generates Codex/Gemini surfaces.
5. Normalize English-only Stage 00 text after policy content is settled.
6. Apply bounded target-stage template fixes only where the plan explicitly names the deviation or documents an exception.
7. Update the task evidence and progress log.
8. Run the verification plan and record results.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repository contract, model policy, template mapping, hook parity, runtime catalog parity | `bash scripts/validation/check-repo-contracts.sh` | `failures=0` and PASS message. |
| VAL-PLN-002 | Traceability | Execution and operations cross-links | `bash scripts/validation/check-doc-traceability.sh` | `failures=0` and PASS message. |
| VAL-PLN-003 | Knowledge Index | LLM Wiki freshness after governance/docs changes | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Generated index is fresh, or regenerated and committed if stale. |
| VAL-PLN-004 | Graph Advisory | Graphify advisory status after code/doc changes | `bash scripts/knowledge/report-graphify-health.sh` | Report captured; advisory reasons corroborated against tracked source files. |
| VAL-PLN-005 | Codex Surface | Provider mirror consistency | `bash scripts/operations/sync-provider-surfaces.sh` | `sync-provider-surfaces: no drift` or intentional write/update recorded. |
| VAL-PLN-006 | Stage 00 Language | English-only governance scan | `rg -n \"[가-힣]\" docs/00.agent-governance` | No Korean prose remains in Stage 00. Any remaining hits are code literals or documented exceptions. |
| VAL-PLN-007 | Codex Model Config | Codex agent frontmatter model audit | `rg -n "^(model\|model_reasoning_effort):" .codex/agents/*.md` | Supervisor uses `gpt-5.5`; workers use `gpt-5.4-mini` or justified `gpt-5.3-codex`; no disallowed effort values. |
| VAL-PLN-008 | Hook JSON | Codex hook syntax validation | `python3 -m json.tool .codex/hooks.json >/dev/null` | JSON is valid. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Official model availability differs from local assumptions. | High | Use only verified OpenAI model IDs; mark uncertain aliases as blocked or remove them from active policy. |
| `.codex` mirror edits drift from `.claude` canonical runtime content. | High | Update sync script and validator together; run `sync-provider-surfaces.sh` before completion. |
| English-only remediation changes hook user-message intent. | Medium | Translate behavior-preserving text only; do not change hook trigger semantics unless explicitly planned. |
| Template compliance work becomes a broad historical-doc rewrite. | Medium | Fix only known deviations required by this plan or document exceptions. |
| CI/CD policy text overstates local reproducibility. | Medium | Classify jobs accurately as local script, inline shell, npm package script, or GitHub-only. |
| Phase separation is blurred by progress/task updates. | Medium | Treat this plan as Phase 2 only; defer task evidence and progress updates to Phase 3 unless the user explicitly approves them during planning. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Stage 00 and `.codex` changes must pass repository contract checks before completion.
- **Sandbox / Canary Rollout**: N/A for docs/runtime policy changes; no Docker service start/stop is planned.
- **Human Approval Gate**: Required before Phase 3 implementation because this plan changes governance, model policy, template contracts, and runtime harness metadata.
- **Rollback Trigger**: Revert the Phase 3 change set if repository contracts fail due to model-policy, mirror-parity, or template-contract regressions that cannot be fixed within the approved scope.
- **Prompt / Model Promotion Criteria**: Model policy is promoted only when the provider-specific identifier is verified and validator enforcement matches Stage 00 text.

## Completion Criteria

- [x] User approves Phase 3 implementation against this plan.
- [x] Shared clarification duty exists in Stage 00 and Codex provider guidance.
- [x] Stage 00 concept definitions are present and do not create provider-specific duplicate policy.
- [x] Template Contract mapping is consistent across Stage 00, template README, and validators.
- [x] All target-stage document deviations in scope are fixed or documented as explicit exceptions.
- [x] Codex harness remains `.codex/agents/*.md` YAML frontmatter, not `.toml`.
- [x] Codex model policy uses `gpt-5.5` for supervisor and `gpt-5.4-mini` / justified `gpt-5.3-codex` for workers.
- [x] Stage 00 English-only remediation includes `github-governance.md` and hookify messages.
- [x] QA & CI/CD policy accurately maps local commands, CI-only jobs, inline shell checks, and npm checks.
- [x] Paired task document records actual changes and verification evidence.
- [x] Verification plan passes or any skipped check is explicitly recorded with rationale.

## Related Documents

- **Task**: [2026-05-30-standardizing-agent-governance task](../tasks/2026-05-30-standardizing-agent-governance.md)
- **Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Subagent Protocol**: [Subagent Protocol](../../00.agent-governance/subagent-protocol.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Template Catalog**: [99.templates](../../99.templates/README.md)
- **Operations Index**: [Operations index](../../05.operations/README.md)
