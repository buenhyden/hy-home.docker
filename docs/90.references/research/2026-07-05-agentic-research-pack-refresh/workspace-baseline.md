---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md -->

# Reference: Agentic Engineering Workspace Baseline

## Overview

This reference summarizes the current `hy-home.docker` workspace purpose, roles, CI/CD, QA, automation, formatting, operating contracts, templates, scripts, integration guidance, SDLC, governance, system structure, and rules from repo-local evidence.

## Purpose

Fix a stable baseline before comparing this repository with external harness engineering and loop engineering sources.

## Repository Role

This reference is a navigation aid for `docs/00.agent-governance/`, the HAFE specification, HAFE operations guide/policy, scripts, and CI workflow. It does not replace current policy, execution plans, task evidence, or runtime truth.

## Scope

### In Scope

- Workspace purpose and roles
- Stage-gated documentation system
- CI/CD and QA gates
- Automation and hook surfaces
- Formatting and template contracts
- Provider adapters and subagent governance
- Follow-up gap recording

### Out of Scope

- Active policy changes
- Runtime configuration changes
- Operational procedure execution
- Secret values, credentials, or tokens

## Definitions / Facts

- **Workspace purpose**: The root README defines this repository as a shared harness-engineering and agent-first engineering workspace that connects Docker Compose home/development infrastructure with stage-gated documentation.
- **Primary runtime surface**: The root `docker-compose.yml` includes `infra/**/docker-compose*.yml` files. Runtime truth lives in `infra/`, `docker-compose.yml`, registry JSON files, and validation scripts.
- **Stage taxonomy**: `docs/00.agent-governance/rules/bootstrap.md` defines the source-of-truth paths from `docs/01.requirements` through `docs/05.operations`, plus `docs/90.references` and `docs/99.templates`.
- **Reference boundary**: `docs/90.references` provides stable context and source-backed facts, not active policy, runbooks, plans, or task evidence.
- **Governance SSOT**: `docs/00.agent-governance/` owns rules, scopes, provider overlays, the agent catalog, memory, and the subagent protocol.
- **Provider adapter model**: Claude uses `.claude/`, Codex uses `.codex/`, and Gemini uses `.agents/` as provider-specific runtime surfaces while Stage 00 remains the policy source.
- **CI/CD**: `.github/workflows/ci-quality.yml` splits docs traceability, implementation alignment, repository contracts, git-flow, Compose validation, hardening, template/security baseline, QuickWin, pre-commit, frontend quality, Storybook coverage, and zizmor into distinct jobs.
- **QA**: `docs/00.agent-governance/scopes/qa.md` separates local checks, CI-only gates, hook/script evidence, and skipped-check rationale by change type.
- **Automation**: `scripts/README.md` defines validation, hardening, hooks, knowledge, operations, and libraries as canonical purpose-folder script surfaces.
- **Formatting**: Formatting is governed through `.pre-commit-config.yaml`, hook-mediated post-tool validation, `git diff --check`, and target-stage template rules.
- **Operating contract**: The HAFE policy uses controls for thin root shims, runtime mirror parity, model hierarchy, scope imports, hook safety, Codex boundary, template-first docs, and Graphify advisory context.
- **Templates**: `docs/99.templates/` provides stage templates, and `documentation-protocol.md` makes template-first authoring, README sync, related links, and status frontmatter part of completion.
- **Integration guide**: The root README and HAFE guide describe the agent work starting sequence, Graphify advisory use, provider/runtime inspection, and validator review flow.
- **SDLC**: The repository SDLC is modeled as requirements -> architecture -> specs -> execution -> operations, supported by reference and template stages.

## Workspace Category Map

| Category | Repo-local Evidence | Current Interpretation |
| --- | --- | --- |
| Purpose | `README.md`, `AGENTS.md`, `docs/00.agent-governance/README.md` | Workspace for Docker Compose infrastructure and agent-first governance |
| Role | `infra/README.md`, `docs/README.md`, `scripts/README.md` | Operational, documentation, and agent collaboration repository |
| CI/CD | `.github/workflows/ci-quality.yml`, `docs/00.agent-governance/scopes/qa.md` | GitHub Actions pipeline that separates local reproducible checks and remote-only gates |
| QA | `scripts/validation/**`, `scripts/hardening/**`, `check-doc-traceability.sh` | Script-backed validation for docs, Compose, hardening, template/security, QuickWin, and frontend surfaces |
| Security | `.github/SECURITY.md`, `docs/00.agent-governance/scopes/security.md`, `docs/00.agent-governance/rules/github-governance.md`, `scripts/validation/check-template-security-baseline.sh` | Security is handled through disclosure guidance, scope-level enforcement, GitHub Actions security contracts, template/security baseline checks, secret boundaries, and hardening validation. |
| Linting / Syntax | `.pre-commit-config.yaml`, `scripts/hooks/post-tool-validate.sh`, `.github/workflows/ci-quality.yml` | Style and syntax drift are checked through hook-mediated validation, CI pre-commit, frontend quality gates, YAML/security scans, and `git diff --check`. |
| Docker Compose / Infrastructure | `docker-compose.yml`, `infra/README.md`, `scripts/validation/validate-docker-compose.sh`, `scripts/hardening/check-all-hardening.sh` | Runtime truth remains in Compose and infra files; research docs cite it but do not replace it. |
| Automation | `scripts/hooks/**`, `.claude/hooks/**`, `.codex/hooks.json`, `.agents/workflows/**` | Provider hooks and workflows execute Stage 00 policy as adapters |
| Formatting | `.pre-commit-config.yaml`, `post-tool-validate.sh`, `git diff --check` | Completion hygiene for whitespace, shell style, Markdown linting, and generated index freshness |
| Operating Contract | HAFE policy and runbook | Evidence-backed boundaries across root, provider, runtime, script, and stage surfaces |
| Templates | `docs/99.templates/**`, `documentation-protocol.md` | Template-first authoring, README sync, related links, and status frontmatter |
| Scripts | `scripts/README.md` | Purpose-folder paths are canonical entrypoints; duplicate root wrappers are prohibited |
| Integration Guide | root README, HAFE guide | New work starts from root, governance, docs, scripts, and infra entrypoints |
| SDLC | `stage-authoring-matrix.md`, `docs/README.md` | Lifecycle split across requirements, architecture, specs, execution, operations, references, and templates |
| Governance | Stage 00 rules/scopes/providers/subagent protocol | SSOT for agent execution, provider parity, model policy, and approval boundaries |
| System | `harness-implementation-map.md` | Surface map for governance, compose, secrets, scripts, validation, hardening, hooks, evidence, PR/review, and operations |
| Rules | `bootstrap.md`, `agentic.md`, `task-checklists.md`, `documentation-protocol.md` | Non-mutating discovery, persona routing, scope loading, template contract, and verification evidence |

## Analysis

The repository already treats the harness as a multi-surface contract rather than a single tool. `harness-implementation-map.md` links root shims, governance, Docker Compose runtime, secrets, scripts, validation, hardening, hooks, evidence, PR/review, and operations into one routing map. That is broader than a conventional test harness.

From a loop perspective, `agentic.md` creates a discovery -> plan -> execute -> verify -> progress log flow. CI jobs, hooks, and the memory progress log add additional feedback loops. This reference pack records potential improvements as gaps rather than modifying active policy.

Provider-wise, Claude, Codex, and Gemini share policy but expose different mechanics. Claude emphasizes Markdown runtime adapters and hooks; Codex emphasizes TOML agents, hooks, sandbox/approval configuration; Gemini emphasizes `.agents/` reference indexes and Gemini-native context/workflow surfaces.

## Potential Follow-up / Gap

- The new `docs/90.references/research` category may need a dedicated source freshness cadence if more research packs are added.
- Gemini provider notes define `.agents/` as the Gemini runtime surface, but official Gemini CLI sources reviewed for this task do not show first-class subagents comparable to Claude/Codex.
- Improvements discovered through external research should be separated into future approved work under the correct active stage.

## Source Rules

- Repo-local current truth must be checked against the root README, Stage 00 governance, provider notes, scripts, CI workflow, and HAFE documents.
- External provider facts must prefer official vendor docs and be rechecked before operational adoption.
- Reference documents must remain source-backed interpretation rather than active policy.

## Sources

- [Root README](../../../../README.md) - workspace purpose, structure, CI/quality summary
- [Agent governance hub](../../../00.agent-governance/README.md) - governance SSOT, coverage matrix, provider adapter model
- [Bootstrap rules](../../../00.agent-governance/rules/bootstrap.md) - stage taxonomy and bootstrap sequence
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - template, language, stage, README, related-documents contract
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - stage responsibilities and templates
- [QA scope](../../../00.agent-governance/scopes/qa.md) - QA/CI gate model
- [Security scope](../../../00.agent-governance/scopes/security.md) - security enforcement and secret-boundary model
- [GitHub governance](../../../00.agent-governance/rules/github-governance.md) - workflow security, protected-branch, and required-check contracts
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - repo-local harness surface routing
- [HAFE specification](../../../03.specs/harness-agent-first-engineering/spec.md) - existing harness and agent-first engineering contracts
- [HAFE guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md) - workspace audit guide
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) - operations controls
- [Infra README](../../../../infra/README.md) - Docker Compose infrastructure inventory and validation guidance
- [Security disclosure](../../../../.github/SECURITY.md) - vulnerability reporting boundary
- [Scripts README](../../../../scripts/README.md) - purpose-folder script contract
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - GitHub Actions quality gates

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Stage 00 provider model, CI workflow, script inventory, or HAFE docs change
- **Update Trigger**: Update when repo-local governance/runtime surfaces change or when external research pack assumptions are revised

## Related Documents

- [research pack index](./README.md)
- [research references](../README.md)
- [90.references](../../README.md)
- [agent governance hub](../../../00.agent-governance/README.md)
- [HAFE specification](../../../03.specs/harness-agent-first-engineering/spec.md)
