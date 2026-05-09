---
status: draft
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
- `docs/04.specs`, `docs/05.plans`, `docs/06.tasks`, `docs/07.guides`, `docs/08.operations`, `docs/09.runbooks`
- `scripts/check-*.sh`, `scripts/validate-docker-compose.sh`

## Controls

| Control | Requirement |
| --- | --- |
| Thin root shims | Root files delegate detailed policy to `docs/00.agent-governance/` and runtime overlays. |
| Runtime mirror parity | `.claude/agents` and `.claude/skills` stay synchronized with governance catalog files. |
| Model hierarchy | `workflow-supervisor` remains `opus`; worker agents remain `sonnet`. |
| Scope imports | Each runtime agent imports exactly one primary scope. |
| Codex boundary | `.codex` remains hooks/context only unless governance explicitly adopts a Codex catalog. |
| Template-first docs | New stage docs use `docs/99.templates/` and update parent README files. |
| Source-label prevention | Active runtime/governance files must not reference external harness source labels. |
| Graph context health | Graphify is a navigation aid only when health is clean; contaminated output remains advisory and must be corroborated against tracked source and canonical docs. |

## Exceptions

- Historical notes under `docs/00.agent-governance/memory/` may mention prior source labels for audit context.
- `bash scripts/report-graphify-health.sh` may report `status=advisory`; that is evidence for downgraded confidence, not a repository validation failure.
- `graphify` refresh may be skipped when the CLI is unavailable, but the skip must be reported.
- `rtk` may be bypassed when it is unavailable in the active shell.

## Verification

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
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

## AI Agent Policy Section (If Applicable)

- Agents must start with non-mutating discovery.
- Agents must not invent runtime teams or untracked roles.
- Agents must document gap findings before making runtime changes.
- Agents must report changed files, checks run, and residual risks.

## Related Documents

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Plan](../05.plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../06.tasks/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../07.guides/harness-agent-first-engineering.md)
- [Validation Runbook](../09.runbooks/harness-agent-first-engineering-validation.md)
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
