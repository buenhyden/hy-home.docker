---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md -->

# Harness / Agent-first Engineering Plan

## Overview

This plan analyzes the harness engineering and Agent-first Engineering contracts currently implemented in `hy-home.docker` based on file contents, then fills actual gaps with minimal changes.

## Context

Recent repository contracts already verify the `.claude` runtime mirror, Codex boundary, source-label leak prevention, Graphify fallback, and `rg` discovery permission. Three gaps were then confirmed: double-quoted Python blocks in Claude hooks can trigger markdown backtick command substitution, HAFE evidence can read as if the `core` profile and supported hardening tiers cover the entire workspace, and Graphify advisory output can be mistaken for architecture authority.

## Goals & In-Scope

- Summarize the workspace purpose, rules, and environment based on related files.
- Analyze harness engineering components.
- Analyze Agent-first Engineering components.
- Explicitly mark the agent/catalog contract as no-agent-catalog-change because no current gap exists there.
- Fill the Claude hook quoting gap with a heredoc/argv approach.
- Preserve existing stage docs and parent README traceability, and apply this Graphify improvement in place in existing stage docs.
- Add rules and evidence commands that downgrade Graphify health to advisory context when it is not clean.
- Split the `10-communication` Compose include/IP/network issue into separate infra remediation.
- Prove completion with the specified verification commands.

## Non-Goals & Out-of-Scope

- Creating a new agent catalog or Codex delegated-agent catalog.
- Changing the agent catalog, root shim, provider policy, or `.codex` delegated-agent behavior.
- Creating new artifacts under `docs/01.requirements`, `docs/02.architecture/requirements`, `docs/02.architecture/decisions`, or `docs/05.operations/incidents`.
- Hand-editing or regenerating the `graphify-out` generated artifact.
- Promoting the Graphify health report to a hard validation gate.
- `10-communication` root compose include, network, IP allocation, or hardening tier remediation.
- Manually running `pre-commit`.
- Running, deploying, stopping, or deleting the Docker stack.

## Work Breakdown

| Phase | Work | Output |
| --- | --- | --- |
| P1 | Analyze root, docs, infra, and scripts READMEs | Workspace purpose/environment summary |
| P2 | Analyze `AGENTS.md`, provider shims, and governance rules | Agent entry/rule contract summary |
| P3 | Analyze `.claude`, `.codex`, and governance agent catalog | Harness component and runtime mirror summary |
| P4 | Analyze templates and validators | Agent-first guardrail and verification map summary |
| P5 | Write/update stage docs | Spec, Plan, Task, Guide, Policy, Runbook |
| P6 | Confirm parent README traceability | Keep document links and structure synchronized |
| P7 | Fill Claude hook quoting gap | heredoc/argv-based JSON output and payload simulation |
| P8 | Improve Graphify/context-quality and evidence scope | advisory health wording, scoped infra evidence, residual risk |
| P9 | Run verification | Command evidence and residual risk report |

## Verification Plan

```bash
python3 -m json.tool .codex/hooks.json >/dev/null
python3 -m json.tool .claude/settings.json >/dev/null
bash -n .claude/hooks/*.sh scripts/*.sh
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
! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
```

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Stage doc churn duplicates existing governance | Keep active policy in `docs/00.agent-governance/`; stage docs describe analysis and operation only. |
| README sync drift | Update each parent README in the same change as the new document. |
| Source-label regression | Run explicit source-label scan and rely on `check-repo-contracts.sh`. |
| Over-expanding runtime | Do not change agent catalogs, `.codex`, or root shims unless a validator proves a specific gap. |
| Polluted Graphify output is over-trusted | Keep Graphify readable but advisory when health reports contamination; corroborate with tracked source and canonical docs. |
| Hook payload breaks despite syntax checks | Add real `tool_input` payload simulation for Claude and Codex hook entrypoints. |
| `10-communication` validation gap expands scope | Record it as separate infra remediation; do not block HAFE completion. |

## Agent Rollout & Evaluation Gates (If Applicable)

- Agent persona: Agentic Workflow Specialist with Documentation Specialist behavior for stage artifacts.
- Evaluation gate: all commands in the verification plan pass.
- Runtime rollout: limited to shell-safe Claude hook invocation; no agent catalog or provider policy rollout is needed.

## Completion Criteria

- Stage docs exist and contain `## Related Documents`.
- Parent README files keep references to the stage docs.
- Claude hook payload simulations return JSON/system-message output without command substitution side effects.
- `bash scripts/knowledge/report-graphify-health.sh` exits 0 and reports clean or advisory without being treated as architecture authority when advisory.
- Repository contract, docs traceability, default/core Compose, template/security, QuickWin, and supported hardening checks pass.
- Source-label scan returns no active runtime/governance matches.
- `10-communication` remediation remains documented as out of scope for this pass.

## Related Documents

- [Specification](../../03.specs/harness-agent-first-engineering/spec.md)
- [Task Evidence](../tasks/2026-05-09-harness-agent-first-engineering.md)
- [Guide](../../05.operations/guides/00-workspace/harness-agent-first-engineering.md)
- [Operations Policy](../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)
- [Validation Runbook](../../05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
