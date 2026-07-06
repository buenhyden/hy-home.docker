---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md -->

# Audit Implementation Matrix Snapshot Implementation Plan

## Overview

This plan implements a generated Stage 90 audit implementation matrix snapshot
and repo-contract freshness check.

## Context

The agentic engineering implementation audit pack already has a coverage
report for implementation-status cells, but the audit overview still names a
remaining need for full automated audit-matrix refresh from repo paths. A
generated advisory matrix can close the local consistency snapshot part without
rewriting audit conclusions or adopting CI/security gates.

## Goals & In-Scope

- **Goals**:
  - Add a local generated audit implementation matrix snapshot.
  - Summarize audit report presence, overview categories, implementation
    status counts, automation candidate closure, and generated evidence
    surfaces.
  - Add repo-contract freshness coverage.
  - Update Stage 90 indexes and audit references.
  - Add Stage 03/04 evidence and progress memory.
- **In Scope**:
  - `scripts/validation/generate-audit-implementation-matrix.sh`
  - `docs/90.references/data/governance/audit-implementation-matrix.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 indexes, Stage 90 audit/index docs, generated LLM Wiki output,
    Graphify output, and progress memory.

## Non-Goals & Out-of-Scope

- No audit finding rewrite or implementation-status conclusion change.
- No CI workflow behavior change, model-call eval gate, vulnerability gate,
  SBOM generation, signing, provenance attestation, Scorecard run, registry
  lookup, remote GitHub query, or runtime state check.
- No branch protection, release artifact, provider runtime, Docker Compose,
  deployment state, secret, credential, token, private key, raw-log,
  shell-history, or `.env` mutation or inspection.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AIM-001 | Add audit implementation matrix generator. | `scripts/validation/generate-audit-implementation-matrix.sh` | VAL-AIM-001, VAL-AIM-002 | Generator write, dry-run, and `--check` pass. |
| PLN-AIM-002 | Add generated governance data reference and indexes. | `docs/90.references/data/governance/**`, Stage 90 indexes | VAL-AIM-001, VAL-AIM-004 | Generated snapshot and indexes route to it. |
| PLN-AIM-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-AIM-003 | Full repo contracts pass. |
| PLN-AIM-004 | Update audit candidate evidence and Stage evidence. | Stage 03/04 indexes, Stage 90 audit docs, progress | VAL-AIM-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-AIM-001 | Generator | Generate and check audit implementation matrix snapshot. | `bash scripts/validation/generate-audit-implementation-matrix.sh`; `bash scripts/validation/generate-audit-implementation-matrix.sh --check` | Snapshot is fresh. |
| VAL-PLN-AIM-002 | Generator | Preview generated output. | `bash scripts/validation/generate-audit-implementation-matrix.sh --dry-run` | Output renders the audit matrix. |
| VAL-PLN-AIM-003 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/generate-audit-implementation-matrix.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-AIM-004 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-AIM-005 | Docs | Check generated docs and traceability. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-AIM-006 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated summary is mistaken for canonical audit conclusion | Medium | The generated reference states it is consistency evidence and links back to source audit reports. |
| Candidate self-reference creates a stale loop | Medium | The generator uses filesystem presence for the generated output while repo-contract `--check` enforces exact freshness after generation. |
| Security or CI gate adoption is implied without approval | High | Keep eval CI gates, vulnerability gates, SBOM, attestation, and Scorecard as residual gap signals routed to separate Stage 03/04 work. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Generator write/check/dry-run and repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime or remote service changes.
- **Human Approval Gate**: Required before adopting CI gates, scanners, SBOM
  tools, signing, attestation, Scorecard, branch-protection updates, or remote
  jobs.
- **Rollback Trigger**: Revert the generator/output/evidence commit if the
  snapshot creates false freshness failures.

## Completion Criteria

- Generated audit implementation matrix snapshot exists and passes `--check`.
- Repo contracts check snapshot freshness.
- Scripts README, Stage 03/04 indexes, Stage 90 data indexes, and audit
  references are synchronized.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/118-audit-implementation-matrix-snapshot/spec.md](../../03.specs/118-audit-implementation-matrix-snapshot/spec.md)
- **Task**: [../tasks/2026-07-06-audit-implementation-matrix-snapshot.md](../tasks/2026-07-06-audit-implementation-matrix-snapshot.md)
- **Generated reference**: [../../90.references/data/governance/audit-implementation-matrix.md](../../90.references/data/governance/audit-implementation-matrix.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
