---
status: enforced
---

# Harness / Agent-first Engineering Operations Policy

## Overview (KR)

이 운영 정책은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약을 유지하기 위한 통제 기준을 정의한다.

## Policy Scope

- Agent entry shims.
- Governance rules and scopes.
- Claude runtime mirror.
- Codex hook/context surface.
- Stage documentation and validators.

## Applies To

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- `.claude/**`
- `.codex/**`
- `docs/00.agent-governance/**`
- `docs/03.specs`, `docs/04.execution/plans`, `docs/04.execution/tasks`, `docs/05.operations`, `docs/05.operations`, `docs/05.operations`
- `scripts/check-*.sh`, `scripts/validate-docker-compose.sh`

## Controls

| Control | Requirement |
| --- | --- |
| Thin root shims | Root files delegate detailed policy to `docs/00.agent-governance/` and runtime overlays. |
| Runtime mirror parity | `.claude/agents` and `.claude/skills` stay synchronized with governance catalog files. |
| Runtime parity scope | Repository checks prove catalog, model, scope import, and protocol-reference parity; they do not prove semantic parity of every runtime document. |
| Model hierarchy | `workflow-supervisor` remains `opus`; worker agents remain `sonnet`. |
| Scope imports | Each runtime agent imports exactly one primary scope. |
| Hook safety | Runtime hooks must parse real payload shapes without shell command substitution side effects. |
| Codex boundary | `.codex` remains hooks/context only unless governance explicitly adopts a Codex catalog. |
| Template-first docs | New stage docs use `docs/99.templates/` and update parent README files. |
| Source-label prevention | Active runtime/governance files must not reference external harness source labels. |
| Graph context health | Graphify is a navigation aid only when health is clean; contaminated output remains advisory and must be corroborated against tracked source and canonical docs. |
| Infra validation scope | HAFE completion may rely on default/core Compose and supported hardening tiers; non-included profiles such as `10-communication` require separate infra remediation. |

## Exceptions

- Historical notes under `docs/00.agent-governance/memory/` may mention prior source labels for audit context.
- `bash scripts/report-graphify-health.sh` may report `status=advisory`; that is evidence for downgraded confidence, not a repository validation failure.
- `graphify` refresh may be skipped when the CLI is unavailable, but the skip must be reported.
- `rtk` may be bypassed when it is unavailable in the active shell.
- `10-communication` compose/include/IP remediation is outside HAFE unless explicitly scoped into an infra change.

## Verification

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
bash -n .claude/hooks/*.sh scripts/*.sh
printf '{"tool_input":{"file_path":"infra/10-communication/mail/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/post-tool-validate.sh
bash scripts/report-graphify-health.sh
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
bash scripts/validate-docker-compose.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-quickwin-baseline.sh
bash scripts/check-all-hardening.sh
```

## Review Cadence

- Run repository contract checks after any root, governance, runtime, provider, script, or stage documentation change.
- Re-run the full verification bundle before declaring a broad harness or Agent-first migration complete.
- Review this policy when `.claude`, `.codex`, or `docs/00.agent-governance/agents` changes.
- Record out-of-scope infra profile failures separately instead of expanding HAFE acceptance criteria silently.

## AI Agent Policy Section (If Applicable)

- Agents must start with non-mutating discovery.
- Agents must not invent runtime teams or untracked roles.
- Agents must document gap findings before making runtime changes.
- Agents must report changed files, checks run, and residual risks.
- Agents must describe Graphify advisory output as navigation context, not architecture authority.

## Related Documents

- [Specification](../../03.specs/harness-agent-first-engineering/spec.md)
- [Plan](../../04.execution/plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../../04.execution/tasks/2026-05-09-harness-agent-first-engineering.md)
- [Usage](./harness-agent-first-engineering.md)
- [Validation Procedure](../runbooks/harness-agent-first-engineering-validation.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)

## Usage

> Migrated from `docs/05.operations/harness-agent-first-engineering.md` during the 2026-05-10 operations taxonomy consolidation.

### Harness / Agent-first Engineering Usage

#### Overview (KR)

이 가이드는 `hy-home.docker`에서 하네스 엔지니어링과 Agent-first Engineering 상태를 다시 조사하거나 보완할 때 따라야 할 절차를 설명한다.

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
- Run `bash scripts/report-graphify-health.sh` when `graphify-out/` exists.
- Confirm the active scope from `docs/00.agent-governance/scopes/`.
- Do not inspect secrets or credential files.

#### Step-by-step Instructions

1. Read root entry files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
2. Read environment and docs maps: `docs/README.md`, `infra/README.md`, `scripts/README.md`.
3. Check Graphify health with `bash scripts/report-graphify-health.sh`; if it reports `status=advisory`, use Graphify only for navigation and corroborate claims against tracked files and canonical docs.
4. Read governance rules: `docs/00.agent-governance/README.md`, `rules/agentic.md`, `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `scopes/agentic.md`.
5. Inspect runtime surfaces: `.claude/CLAUDE.md`, `.claude/settings.json`, `.claude/agents/*.md`, `.claude/skills/*/skill.md`, `.codex/README.md`, `.codex/hooks.json`.
6. Compare runtime mirror against `docs/00.agent-governance/agents/**` and `subagent-protocol.md`.
7. Review validators: `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh`, `scripts/validate-docker-compose.sh`.
8. Simulate hook payloads when `.claude/hooks/*.sh`, `.codex/hooks.json`, or `scripts/post-tool-validate.sh` changes; syntax checks alone do not prove `tool_input` parsing.
9. If new stage docs are needed, start from `docs/99.templates/` and update the parent README in the same change.
10. Run the validation commands listed in the runbook before declaring completion.

#### Common Pitfalls

- Treating `.codex` as a delegated-agent catalog. It is only a hook/context surface in this repository.
- Editing root shims instead of the governance hub.
- Treating contaminated Graphify output as authoritative architecture evidence.
- Treating `status=advisory` Graphify health as a failure or as architecture authority; it is downgraded navigation context only.
- Claiming full workspace Docker validation when only default/core profile and supported hardening tiers were checked.
- Treating catalog parity checks as semantic parity across all agent/skill content.
- Pulling `10-communication` Compose remediation into a Harness / Agent-first pass without a separate infra scope.
- Skipping hook payload simulation after hook quoting or parsing changes.
- Adding stage documents without updating the parent README.
- Claiming graph refresh when the `graphify` CLI is unavailable.
- Running `pre-commit` manually despite repository guidance.

#### Related Documents

- [Specification](../../03.specs/harness-agent-first-engineering/spec.md)
- [Plan](../../04.execution/plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../../04.execution/tasks/2026-05-09-harness-agent-first-engineering.md)
- [Operations Policy](./harness-agent-first-engineering.md)
- [Validation Procedure](../runbooks/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
