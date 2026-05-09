---
status: draft
---

# Harness / Agent-first Engineering Guide

## Overview (KR)

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Guide Type

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
- Confirm the active scope from `docs/00.agent-governance/scopes/`.
- Do not inspect secrets or credential files.

## Step-by-step Instructions

1. Read root entry files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
2. Read environment and docs maps: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. Read governance rules: `docs/00.agent-governance/README.md`, `rules/agentic.md`, `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `scopes/agentic.md`.
4. Inspect runtime surfaces: `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/skill.md`, `.codex/README.md`, `.codex/hooks.json`.
5. Compare runtime mirror against `docs/00.agent-governance/agents/**` and `subagent-protocol.md`.
6. Review validators: `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh`, `scripts/validate-docker-compose.sh`.
7. If new stage docs are needed, start from `docs/99.templates/` and update the parent README in the same change.
8. Run the validation commands listed in the runbook before declaring completion.

## Common Pitfalls

- Treating `.codex` as a delegated-agent catalog. It is only a hook/context surface in this repository.
- Editing root shims instead of the governance hub.
- Adding stage documents without updating the parent README.
- Claiming graph refresh when the `graphify` CLI is unavailable.
- Running `pre-commit` manually despite repository guidance.

## Related Documents

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Plan](../05.plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../06.tasks/2026-05-09-harness-agent-first-engineering.md)
- [Operations Policy](../08.operations/harness-agent-first-engineering.md)
- [Validation Runbook](../09.runbooks/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
