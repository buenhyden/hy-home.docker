---
name: policy-gate-agent
description: >
  Orchestrate hy-home.docker policy validation scripts: check-quickwin-baseline.sh,
  check-template-security-baseline.sh, check-repo-contracts.sh, and
  check-doc-traceability.sh. Reports pass/fail by policy category and surfaces
  the minimum changes needed to reach compliance.
---

# policy-gate-agent

Runs and interprets workspace policy validation scripts.

## Trigger Examples

- "Run all policy checks and report failures"
- "Check quickwin baseline compliance for infra/"
- "What's failing in check-template-security-baseline.sh?"
- "Gate this PR against repo contracts"

## Purpose

Execute the full validation suite, parse results by category, and recommend
the minimum changes to reach a green gate. Does not auto-fix unless the user
explicitly approves each change.

## Bootstrap

1. Read `AGENTS.md` and `docs/00.agent-governance/scopes/infra.md`.
2. Check which scripts exist under `scripts/validation/`.
3. Run scripts in this order: `check-repo-contracts.sh` → `check-doc-traceability.sh`
   → `check-quickwin-baseline.sh` → `check-template-security-baseline.sh`.

## Working Rules

- Run scripts as `bash scripts/validation/<script>.sh`; never with `sudo`.
- Report failures grouped by script and category.
- For each failure, propose the minimum remediation — do not auto-apply.
- Medium/high risk remediations require explicit user approval.
- `validate-docker-compose.sh --preflight` requires a local `.env` with secrets;
  skip or flag if secrets are unavailable.
- Record deferred failures in `docs/04.execution/tasks/` if they are known
  accepted gaps (e.g., GAP-01 healthchecks).

## Inputs

| Input | Source |
| ----- | ------ |
| Policy scripts | `scripts/validation/` |
| Infra compose files | `infra/` |
| Known deferred gaps | `docs/04.execution/tasks/` and `docs/00.agent-governance/memory/progress.md` |

## Outputs

- Pass/fail report per script and category
- Prioritized remediation list with risk level
- Optional fixes applied after explicit user approval

## Related Skills

- `compose-stack-agent` — fixes QW-001~005 failures in compose files
- `workspace-audit-revalidation` — full workspace audit including policy gates
- `infra-validate` — compose syntax validation
