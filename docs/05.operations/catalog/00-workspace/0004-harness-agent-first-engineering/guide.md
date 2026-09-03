---
title: Harness / Agent-first Engineering Usage Guide
version: 1.0.0
type: operation/guide
layer: operations
status: active
owner: "@buenhyden"
artifact_id: GDE-0004
parent_ids:
  - SPEC-0094
created: 2026-06-04
updated: 2026-08-21
---

# Harness / Agent-first Engineering Usage Guide

## Overview

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Usage

1. Read root entry files: `README.md`, `AGENTS.md`, and `CLAUDE.md`.
2. Read environment and docs maps: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. Check Graphify health with `bash scripts/knowledge/report-graphify-health.sh`; if it reports `status=advisory`, use Graphify only for navigation and corroborate claims against tracked files and canonical docs.
4. Read governance policy: `docs/00.agent-governance/README.md`, `policies/agentic.md`, `policies/documentation-protocol.md`, and `policies/stage-authoring-matrix.md`.
5. Inspect provider-native runtime surfaces: `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`; `.codex/agents/*.toml`, `.codex/hooks.json`; and `docs/00.agent-governance/providers/README.md`, `docs/00.agent-governance/providers/registry.yaml`, `docs/00.agent-governance/providers/codex.md`, `scripts/hooks/agent-event-hook.sh`. Inspect `.agents/agents/*.md` and `.agents/skills/*/SKILL.md` separately as the provider-neutral compatibility and shared-skill projection.
6. Compare runtime projections against `docs/00.agent-governance/roles/**`, `docs/00.agent-governance/skills/**`, and `providers/registry.yaml`.
7. Review validators: `scripts/validation/run-ci-gate.py`, `scripts/validation/check-document-links.py --mode traceability`, `scripts/validation/validate-docker-compose.sh`.
8. Simulate hook payloads when `.claude/hooks/*.sh`, `.codex/hooks.json`, or `scripts/hooks/post-tool-validate.sh` changes; syntax checks alone do not prove `tool_input` parsing.
9. If new stage docs are needed, start from `docs/99.templates/` and update the parent README in the same change.
10. Run the validation commands listed in the runbook before declaring completion.

### Audience and Prerequisites

#### Usage Type

How-to / audit guide.

#### Target Audience

- AI Agents
- Documentation Writers
- Infra Operators
- Repository Maintainers

#### Purpose

반복 가능한 방식으로 workspace purpose, rules, runtime surface, governance contracts, validation gates를 조사하고, 필요한 경우 stage 문서와 README를 템플릿에 맞춰 갱신한다.

#### Prerequisites

- Read `AGENTS.md`.
- Read `graphify-out/GRAPH_REPORT.md` before architecture or codebase answers.
- Run `bash scripts/knowledge/report-graphify-health.sh` when `graphify-out/` exists.
- Confirm the active role, skill, provider, and policy route from `docs/00.agent-governance/`.
- Do not inspect secrets or credential files.

## Troubleshooting

- Treating `.codex/agents/*.toml` or `.claude/agents/*.md` as canonical role catalogs instead of provider-native adapters to the Stage 00 catalog.
- Treating `.agents/` as a provider-native runtime surface instead of the provider-neutral compatibility and shared-skill projection.
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

- `Routine Usage` steps and the linked validators complete without unresolved failures.

## Runbook Handoff

반복 검증, evidence capture, rollback 또는 escalation 절차는
[Harness / Agent-first Engineering Runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Harness and Agent-first Engineering Outcome](../../../../03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Policy](policy.md) (`POL-0004`), [Runbook](runbook.md) (`RUN-0004`)

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Operations runbook](runbook.md)
