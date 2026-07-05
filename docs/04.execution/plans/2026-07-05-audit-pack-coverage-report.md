---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-audit-pack-coverage-report.md -->

# Audit Pack Coverage Report Implementation Plan

## Overview

This plan implements the audit-pack implementation-status coverage output
follow-up from the agentic engineering automation candidates reference.

## Context

The Stage 90 agentic engineering audit pack contains multiple implementation
status matrices. Maintainers can read them manually, but repository contracts
did not yet expose a compact coverage report or check that required overview
categories remain present.

## Goals & In-Scope

- **Goals**:
  - Add a read-only audit-pack coverage report.
  - Check required audit reports and overview categories through repo contracts.
  - Keep raw and normalized implementation statuses visible for audit readers.
  - Add Stage 03/04 evidence and update automation-candidate closure text.
- **In Scope**:
  - `scripts/validation/report-audit-pack-coverage.sh`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 evidence, indexes, audit references, generated navigation, and
    progress memory.

## Non-Goals & Out-of-Scope

- No audit report rewrite or automatic conclusion refresh.
- No CI workflow behavior change or new required job.
- No provider adapter, runtime, Docker Compose, deployment, remote GitHub,
  credential, secret, token, raw-log, shell-history, or `.env` mutation.
- No SBOM, vulnerability gate, provenance, attestation, or executable eval
  runner adoption.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-APC-001 | Add audit-pack coverage parser. | `scripts/validation/report-audit-pack-coverage.sh` | VAL-APC-001, VAL-APC-002 | `--check` passes against the current audit pack. |
| PLN-APC-002 | Wire repo-contract gate and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-APC-003 | Full repo contracts pass. |
| PLN-APC-003 | Add Stage evidence and update audit references. | Spec, plan, task, indexes, audit docs | VAL-APC-004 | Links and documentation validation pass. |
| PLN-APC-004 | Refresh generated navigation and close memory. | LLM Wiki, Graphify, progress | VAL-APC-004 | Freshness and graph health are recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-APC-001 | CLI | Check audit-pack coverage output. | `bash scripts/validation/report-audit-pack-coverage.sh --check` | Required reports and overview categories pass. |
| VAL-PLN-APC-002 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/report-audit-pack-coverage.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-APC-003 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-APC-004 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-APC-005 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Report output is mistaken for refreshed implementation truth | Medium | Label it as coverage output and keep audit conclusions in Stage 90 reports. |
| Parser breaks on provider comparison tables | Medium | Treat Claude, Codex, and Gemini columns as status columns. |
| Category list drifts silently | Medium | Repo contracts fail when required overview categories disappear. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Current audit pack parser fixture and repo-contract
  pass.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before publishing report output to CI,
  rewriting audit reports, or changing category taxonomy.
- **Rollback Trigger**: Revert the script/validator/evidence commit if the
  parser creates false failures.

## Completion Criteria

- Audit-pack coverage report exists and passes `--check`.
- Repo contracts run and guard the report.
- Scripts README and Stage 03/04 evidence reference the new script.
- Audit candidate text records the follow-up as implemented.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/112-audit-pack-coverage-report/spec.md](../../03.specs/112-audit-pack-coverage-report/spec.md)
- **Task**: [../tasks/2026-07-05-audit-pack-coverage-report.md](../tasks/2026-07-05-audit-pack-coverage-report.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
