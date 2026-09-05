---
title: "Harness / Agent-first Engineering Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "operations"
artifact_id: "GDE-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---

# Harness / Agent-first Engineering Usage Guide

## Overview

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

## Usage

1. Read root entry files: `README.md`, `AGENTS.md`, and `CLAUDE.md`.
2. Read environment and docs maps: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. Check Graphify health with `bash scripts/knowledge/report-graphify-health.sh`; if it reports `status=advisory`, use Graphify only for navigation and corroborate claims against tracked files and canonical docs.
4. Read governance policy: `.agents/README.md`, `.agents/governance/agentic.md`, `.agents/governance/documentation-protocol.md`, and `.agents/governance/stage-authoring-matrix.md`.
5. Inspect provider-native runtime surfaces: `.claude/provider.md`, `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`; `.codex/agents/*.toml`, `.codex/hooks.json`; and `.agents/governance/providers/README.md`, `.agents/governance/providers/registry.yaml`, `.codex/provider.md`, `scripts/hooks/agent-event-hook.sh`. Codex discovers canonical `.agents/skills/<skill_id>/SKILL.md` packages and explicitly reads role-selected procedures; Claude uses thin generated pointers. Invocation is explicit and grants no runtime authority.
6. Compare runtime projections against `.agents/roles/**`, `.agents/skills/**`, and `.agents/governance/providers/registry.yaml`.
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
- Confirm the active role, skill, provider, and policy route from `.agents/`.
- Do not inspect secrets or credential files.

## Troubleshooting

- Treating `.codex/agents/*.toml` or `.claude/agents/*.md` as canonical role catalogs instead of provider-native adapters to the canonical agent governance catalog.
- Treating authored `.agents` sources as stale generated files, copying canonical bodies into native skill adapters, or inferring live picker/invocation acceptance from static discovery configuration.
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

- Declared parent: [Harness and Agent-first Engineering Outcome](../../../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Policy](policy.md) (`POL-0004`), [Runbook](runbook.md) (`RUN-0004`)

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Operations runbook](runbook.md)
