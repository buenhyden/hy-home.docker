---
status: active
---
<!-- Target: docs/05.operations/guides/harness-agent-first-engineering.md -->

# Harness / Agent-first Engineering Usage Guide

## Overview (KR)

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Usage Type

How-to / audit guide.

## Target Audience

- AI Agents
- Documentation Writers
- Infra Operators
- Repository Maintainers

## Purpose

반복 가능한 방식으로 workspace purpose, rules, runtime surface, governance contracts, validation gates를 조사하고, 필요한 경우 stage 문서와 README를 템플릿에 맞춰 갱신한다.

## Prerequisites

- Read `AGENTS.md`.
- Read `graphify-out/GRAPH_REPORT.md` before architecture or codebase answers.
- Run `bash scripts/knowledge/report-graphify-health.sh` when `graphify-out/` exists.
- Confirm the active scope from `docs/00.agent-governance/scopes/`.
- Do not inspect secrets or credential files.

## Step-by-step Instructions

1. Read root entry files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
2. Read environment and docs maps: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. Check Graphify health with `bash scripts/knowledge/report-graphify-health.sh`; if it reports `status=advisory`, use Graphify only for navigation and corroborate claims against tracked files and canonical docs.
4. Read governance rules: `docs/00.agent-governance/README.md`, `rules/agentic.md`, `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `scopes/agentic.md`.
5. Inspect runtime surfaces: `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/skill.md`, `.codex/README.md`, `.codex/hooks.json`, `scripts/hooks/agent-event-hook.sh`.
6. Compare runtime mirror against `docs/00.agent-governance/agents/**` and `subagent-protocol.md`.
7. Review validators: `scripts/validation/check-repo-contracts.sh`, `scripts/validation/check-doc-traceability.sh`, `scripts/validation/validate-docker-compose.sh`.
8. Simulate hook payloads when `.claude/hooks/*.sh`, `.codex/hooks.json`, or `scripts/hooks/post-tool-validate.sh` changes; syntax checks alone do not prove `tool_input` parsing.
9. If new stage docs are needed, start from `docs/99.templates/` and update the parent README in the same change.
10. Run the validation commands listed in the runbook before declaring completion.

## Common Pitfalls

- Treating `.codex` as a delegated-agent catalog. It is only a hook/context surface in this repository.
- Editing root shims instead of the governance hub.
- Treating contaminated Graphify output as authoritative architecture evidence.
- Treating `status=advisory` Graphify health as a failure or as architecture authority; it is downgraded navigation context only.
- Claiming full workspace Docker validation when only default/core profile and supported hardening tiers were checked.
- Treating catalog parity checks as semantic parity across all agent/skill content.
- Pulling `10-communication` Compose remediation into a Harness / Agent-first pass without a separate infra scope.
- Skipping hook event and payload simulation after hook quoting, event dispatch, or parsing changes.
- Adding stage documents without updating the parent README.
- Claiming graph refresh when the `graphify` CLI is unavailable.
- Running `pre-commit` manually despite repository guidance.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Operations index](../README.md)
- [Operations policy](../policies/harness-agent-first-engineering.md)
