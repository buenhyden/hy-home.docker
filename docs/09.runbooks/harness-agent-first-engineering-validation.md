---
status: draft
---

# Harness / Agent-first Engineering Validation Runbook

## Overview (KR)

이 런북은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약이 계속 유효한지 반복 검증하는 절차를 제공한다.

## Purpose

Root shim, governance, runtime mirror, Codex boundary, stage documentation, validation script drift를 안전하게 확인한다.

## Canonical References

- [Specification](../04.specs/harness-agent-first-engineering/spec.md)
- [Operations Policy](../08.operations/harness-agent-first-engineering.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Subagent Protocol](../00.agent-governance/subagent-protocol.md)

## When to Use

- Root instruction files change.
- `.claude` or `.codex` files change.
- `docs/00.agent-governance/**` changes.
- New stage docs are added.
- A harness or Agent-first audit is requested.

## Procedure or Checklist

### Checklist

- [ ] Confirm `git status --short --branch`.
- [ ] Read `graphify-out/GRAPH_REPORT.md`.
- [ ] Run `bash scripts/report-graphify-health.sh`.
- [ ] Confirm no runtime policy change is needed before editing docs.
- [ ] Confirm new stage docs use templates and parent README files are updated.
- [ ] Run all verification commands below.

### Procedure

1. Inspect workspace state.

   ```bash
   git status --short --branch
   sed -n '1,120p' graphify-out/GRAPH_REPORT.md
   bash scripts/report-graphify-health.sh
   ```

2. Interpret Graphify health.

   - `status=clean`: Graphify may be used as a navigation aid.
   - `status=advisory`: Graphify remains readable, but architecture and codebase claims must be corroborated against tracked source files, `docs/00.agent-governance/`, and active stage docs.
   - The report prints counts and guidance only; it must not print source file contents.

3. Run governance and docs checks.

   ```bash
   bash scripts/check-repo-contracts.sh
   bash scripts/check-doc-traceability.sh
   ```

4. Run infrastructure and baseline checks.

   ```bash
   bash scripts/validate-docker-compose.sh
   bash scripts/check-template-security-baseline.sh
   bash scripts/check-quickwin-baseline.sh
   bash scripts/check-all-hardening.sh
   ```

5. Run source-label scan.

   ```bash
   rg -n "H100|Harness-100|harness-100|h100_pattern|examples/harness-100" AGENTS.md CLAUDE.md GEMINI.md .claude .codex docs/00.agent-governance --glob '!docs/00.agent-governance/memory/**'
   ```

6. Report changed files, command outcomes, Graphify health status, and any residual risk.

## Verification Steps

The runbook is successful when JSON parsing, Graphify health reporting, repository validators, and Docker checks exit with status 0, and the source-label scan returns no active matches. `report-graphify-health.sh` is non-failing advisory evidence; `status=advisory` requires corroboration but does not fail the repository gate.

## Observability and Evidence Sources

- Command output from validation scripts.
- `git diff --stat`.
- `scripts/report-graphify-health.sh` status and contamination counts.
- `scripts/check-repo-contracts.sh` runtime harness catalog section.
- `docs/06.tasks/2026-05-09-harness-agent-first-engineering.md` task evidence.

## Safe Rollback or Recovery Procedure

- For documentation mistakes, revert only the affected stage doc or README hunk.
- For runtime catalog drift, restore parity between `.claude/**` and `docs/00.agent-governance/agents/**`.
- For Compose validation failures, inspect the changed `infra/**/docker-compose*.yml` files before editing unrelated files.

## Agent Operations (If Applicable)

- Use the active runtime's delegated-agent facility only when the user explicitly requests delegation.
- Pass a primary scope path explicitly to delegated agents.
- Do not use memory notes as active policy.
- Do not delete `_workspace/` artifacts without approval.

## Related Operational Documents

- [Operations Policy](../08.operations/harness-agent-first-engineering.md)
- [Guide](../07.guides/harness-agent-first-engineering.md)
- [Plan](../05.plans/2026-05-09-harness-agent-first-engineering.md)
- [Task Evidence](../06.tasks/2026-05-09-harness-agent-first-engineering.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
