---
profile_id: runbook
status: active
artifact_id: runbook-0004
artifact_type: runbook
parent_ids: []
created: 2026-06-04
updated: 2026-08-21
---
# Harness / Agent-first Engineering Runbook

## Overview

이 런북은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약이 계속 유효한지 반복 검증하는 절차를 제공한다.

## When to Use

- Root instruction files change.
- `.claude` or `.codex` files change.
- `docs/00.agent-governance/**` changes.
- New stage docs are added.
- A harness or Agent-first audit is requested.

## Procedure

#### Checklist

- [ ] Confirm `git status --short --branch`.
- [ ] Read `graphify-out/GRAPH_REPORT.md`.
- [ ] Run `bash scripts/knowledge/report-graphify-health.sh`.
- [ ] Confirm no runtime policy change is needed before editing docs.
- [ ] Confirm new stage docs use templates and parent README files are updated.
- [ ] Run hook payload simulations after any hook quoting or parsing change.
- [ ] Run all verification commands below.

##### Procedure

1. Inspect workspace state.

   ```bash
   git status --short --branch
   sed -n '1,120p' graphify-out/GRAPH_REPORT.md
   bash scripts/knowledge/report-graphify-health.sh
   ```

2. Interpret Graphify health.

   - `status=clean`: Graphify may be used as a navigation aid.
   - `status=advisory`: Graphify remains readable, but architecture and codebase claims must be corroborated against tracked source files, `docs/00.agent-governance/`, and active stage docs.
   - The report prints counts and guidance only; it must not print source file contents.

3. Run governance and docs checks.

   ```bash
   python3 -m json.tool .codex/hooks.json >/dev/null
   python3 -m json.tool .claude/settings.json >/dev/null
   bash -n .claude/hooks/*.sh scripts/**/*.sh
   bash scripts/validation/check-repo-contracts.sh
   python3 scripts/validation/check-document-links.py --mode traceability
   ```

4. Run hook payload simulations.

   ```bash
   printf '{"tool_input":{"file_path":"infra/10-communication/mail/docker-compose.yml"}}' | CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/docker-compose-pre.sh
   CLAUDE_PROJECT_DIR="$PWD" bash .claude/hooks/session-start.sh
   CLAUDE_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh SessionStart
   printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rg hook"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/agent-event-hook.sh PreToolUse
   printf '{"tool_input":{"file_path":".claude/settings.json"}}' | CODEX_PROJECT_DIR="$PWD" bash scripts/hooks/post-tool-validate.sh
   ```

   These commands validate local script behavior and JSON/system-message output. They do not prove external Claude/Codex platform event delivery.

5. Run infrastructure and baseline checks.

   ```bash
   bash scripts/validation/validate-docker-compose.sh
   bash scripts/validation/check-template-security-baseline.sh
   bash scripts/validation/check-quickwin-baseline.sh
   bash scripts/hardening/check-all-hardening.sh
   ```

   Treat these as default/core Compose and supported hardening tier checks. Do not claim full workspace Docker coverage from `services_total=5`.

6. Run source-label scan.

   ```bash
   ! rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md .claude .codex docs/00.agent-governance
   ```

7. Report changed files, command outcomes, Graphify health status, and any residual risk, including out-of-scope infra profile failures such as `10-communication`.

#### Verification Steps

The runbook is successful when JSON parsing, hook payload simulation, Graphify health reporting, repository validators, default/core Docker checks, supported hardening tier checks, and the source-label scan all complete as expected. `report-graphify-health.sh` is non-failing advisory evidence; `status=advisory` requires corroboration but does not fail the repository gate.

#### Observability and Evidence Sources

- Command output from validation scripts.
- `git diff --stat`.
- `scripts/knowledge/report-graphify-health.sh` status and contamination counts.
- `scripts/validation/check-repo-contracts.sh` runtime agent/function catalog section.
- Hook payload simulation output.
- The current co-located Task when a new implementation change is active.

#### Safe Rollback or Recovery Procedure

- For documentation mistakes, revert only the affected stage doc or README hunk.
- For runtime catalog drift, regenerate provider projections from the canonical Stage 00 roles, skills, and provider registry.
- For Compose validation failures, inspect the changed `infra/**/docker-compose*.yml` files before editing unrelated files.
- For `10-communication` failures, open a separate infra remediation path unless that profile is explicitly in scope.

#### Agent Operations (If Applicable)

- Use the active runtime's delegated-agent facility only when the user explicitly requests delegation.
- Pass a primary scope path explicitly to delegated agents.
- Record durable repository guidance in its owning policy, design, runbook, or Task.
- Do not delete `_workspace/` artifacts without approval.

#### Related Operational Documents

- [Operations Policy](../0004-harness-agent-first-engineering/policy.md)
- [Usage Guide](../0004-harness-agent-first-engineering/guide.md)
- Plan
- Task Evidence
- [Agent Governance Hub](../../../../00.agent-governance/README.md)

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../../README.md)
- [Specification](../../../../03.specs/0094-harness-agent-first-engineering/spec.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
- [Agent Governance Hub](../../../../00.agent-governance/README.md)
- [Subagent Protocol](../../../../00.agent-governance/policies/agentic.md)
