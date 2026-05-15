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
- `docs/03.specs/**`
- `docs/04.execution/plans/**`
- `docs/04.execution/tasks/**`
- `docs/05.operations/guides/**`
- `docs/05.operations/policies/**`
- `docs/05.operations/runbooks/**`
- `scripts/check-*.sh`, `scripts/validation/validate-docker-compose.sh`

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
- `bash scripts/knowledge/report-graphify-health.sh` may report `status=advisory`; that is evidence for downgraded confidence, not a repository validation failure.
- `graphify` refresh may be skipped when the CLI is unavailable, but the skip must be reported.
- `rtk` may be bypassed when it is unavailable in the active shell.
- `10-communication` compose/include/IP remediation is outside HAFE unless explicitly scoped into an infra change.

## Verification

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
bash -n .claude/hooks/*.sh scripts/*.sh scripts/lib/*.sh
CLAUDE_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh SessionStart
printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh PreToolUse
printf '{"tool_input":{"file_path":"infra/10-communication/mail/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/post-tool-validate.sh
bash scripts/knowledge/report-graphify-health.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-quickwin-baseline.sh
bash scripts/hardening/check-all-hardening.sh
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
- [Usage Guide](../guides/harness-agent-first-engineering.md)
- [Validation Procedure](../runbooks/harness-agent-first-engineering-validation.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
