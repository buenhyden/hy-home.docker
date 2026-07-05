---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-provider-hook-parity-matrix.md -->

# Provider Hook Parity Matrix Implementation Plan

## Overview

This plan implements the provider hook parity matrix and Gemini behavioral
reminder checklist follow-up from the agentic engineering automation candidates
reference.

## Context

The repository already has a hard repo-contract gate for Claude/Codex hook
parity. Reviewers also need a compact generated reference that shows each hook
event, command provenance, and Gemini's non-native behavioral reminder contract.

## Goals & In-Scope

- **Goals**:
  - Generate a Stage 90 governance data snapshot for provider hook parity.
  - Compare Claude native wrapper hooks and Codex native dispatch hooks.
  - Render Gemini as a behavioral reminder checklist, not a native hook claim.
  - Keep the snapshot deterministic and freshness-checked.
  - Add Stage 03/04 evidence and close the automation-candidate follow-up.
- **In Scope**:
  - `scripts/validation/report-provider-hook-parity.sh`
  - `docs/90.references/data/governance/provider-hook-parity-matrix.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 evidence, governance/Stage 90 indexes, audit references,
    generated navigation, and progress memory.

## Non-Goals & Out-of-Scope

- No provider runtime configuration changes.
- No hook execution, hook log reading, telemetry capture, or shell-history
  inspection.
- No native Gemini hook support claim or provider policy change.
- No CI workflow behavior change or new remote gate.
- No model policy, credential, secret, token, raw-log, `.env`, runtime, remote
  GitHub, or deployment mutation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-PHM-001 | Add provider hook parity generator. | `scripts/validation/report-provider-hook-parity.sh` | VAL-PHM-001, VAL-PHM-002 | Generator write and `--check` pass. |
| PLN-PHM-002 | Add generated governance data output. | `docs/90.references/data/governance/provider-hook-parity-matrix.md` | VAL-PHM-001, VAL-PHM-002 | Output includes event matrix, command provenance, and Gemini checklist. |
| PLN-PHM-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-PHM-003 | Full repo contracts pass. |
| PLN-PHM-004 | Add evidence and close candidate. | Stage 03/04 indexes, Stage 90 indexes, audit docs, progress | VAL-PHM-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-PHM-001 | Generator | Generate and check snapshot. | `bash scripts/validation/report-provider-hook-parity.sh`; `bash scripts/validation/report-provider-hook-parity.sh --check` | Output is fresh. |
| VAL-PLN-PHM-002 | Provider sync | Confirm generated provider adapters remain aligned. | `bash scripts/operations/sync-provider-surfaces.sh --check` | No provider surface drift. |
| VAL-PLN-PHM-003 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/report-provider-hook-parity.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-PHM-004 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-PHM-005 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-PHM-006 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated matrix is mistaken for active provider policy | Medium | Label it generated audit context and link Stage 00 provider sources. |
| Gemini row implies native hook support | High | Render Gemini as `behavioral-reminder` and cite Stage 00 no-native-hook boundary. |
| Personal provider settings are accidentally included | High | Generator reads tracked config only and excludes `.claude/settings.local.json`. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Generator write/check, provider sync check, and
  repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before provider config mutation, CI summary
  publication, or Gemini native hook policy changes.
- **Rollback Trigger**: Revert the generator/output/evidence commit if the
  matrix creates false freshness failures.

## Completion Criteria

- Generated provider hook parity matrix exists and passes `--check`.
- Repo contracts run and guard the snapshot.
- Scripts README, governance-data indexes, and Stage 03/04 evidence reference
  the new generator.
- Automation candidate text records the follow-up as implemented.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/115-provider-hook-parity-matrix/spec.md](../../03.specs/115-provider-hook-parity-matrix/spec.md)
- **Task**: [../tasks/2026-07-06-provider-hook-parity-matrix.md](../tasks/2026-07-06-provider-hook-parity-matrix.md)
- **Generated matrix**: [../../90.references/data/governance/provider-hook-parity-matrix.md](../../90.references/data/governance/provider-hook-parity-matrix.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
