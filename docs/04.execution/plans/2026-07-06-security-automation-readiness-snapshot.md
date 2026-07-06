---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md -->

# Security Automation Readiness Snapshot Implementation Plan

## Overview

This plan implements a generated Stage 90 security automation readiness
snapshot and repo-contract freshness check.

## Context

The security maturity audit already maps SSDF, SLSA, and OpenSSF Scorecard
coverage, but vulnerability gates, SBOM generation, provenance/attestation,
and Scorecard automation remain future work. A generated readiness snapshot can
make these gaps explicit from tracked repository evidence without adopting the
tools yet.

## Goals & In-Scope

- **Goals**:
  - Add a local generated security automation readiness snapshot.
  - Classify repo-local security automation controls as implemented, partial,
    or gap.
  - Add repo-contract freshness coverage.
  - Update Stage 90 indexes and audit references.
  - Add Stage 03/04 evidence and progress memory.
- **In Scope**:
  - `scripts/validation/generate-security-automation-readiness.sh`
  - `docs/90.references/data/security/**`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 indexes, Stage 90 audit/index docs, generated LLM Wiki output,
    Graphify output, and progress memory.

## Non-Goals & Out-of-Scope

- No OSV/SCA/SAST/container scan execution.
- No SBOM generation, signing, provenance attestation, Scorecard run, registry
  lookup, remote GitHub query, or CI workflow behavior change.
- No branch protection, release artifact, runtime Compose, provider runtime,
  secret, credential, token, private key, raw-log, shell-history, or `.env`
  mutation or inspection.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-SAR-001 | Add readiness generator. | `scripts/validation/generate-security-automation-readiness.sh` | VAL-SAR-001, VAL-SAR-002 | Generator write, dry-run, and `--check` pass. |
| PLN-SAR-002 | Add generated security data reference and category README. | `docs/90.references/data/security/**` | VAL-SAR-001, VAL-SAR-004 | Generated snapshot reports 11 controls and indexes route to it. |
| PLN-SAR-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-SAR-003 | Full repo contracts pass. |
| PLN-SAR-004 | Update audit/index evidence and close readiness candidate. | Stage 03/04 indexes, Stage 90 audit docs, progress | VAL-SAR-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-SAR-001 | Generator | Generate and check readiness snapshot. | `bash scripts/validation/generate-security-automation-readiness.sh`; `bash scripts/validation/generate-security-automation-readiness.sh --check` | Snapshot is fresh. |
| VAL-PLN-SAR-002 | Generator | Preview generated output. | `bash scripts/validation/generate-security-automation-readiness.sh --dry-run` | Output renders the readiness matrix. |
| VAL-PLN-SAR-003 | Syntax | Check changed shell scripts. | `bash -n scripts/validation/generate-security-automation-readiness.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-SAR-004 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-SAR-005 | Docs | Check generated docs and traceability. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-SAR-006 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Snapshot is mistaken for a security certification | Medium | The generated reference states it is planning evidence, not a score, vulnerability result, SBOM, signature, or attestation. |
| Generator matches its own explanatory text | Medium | The generator excludes itself from scanned workflow/script surfaces. |
| Security tooling adoption is implied without approval | High | Keep vulnerability/SBOM/attestation/Scorecard items as gaps and route future adoption through Stage 03/04. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Generator write/check/dry-run and repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime or remote service changes.
- **Human Approval Gate**: Required before adopting scanners, SBOM tools,
  signing, attestation, Scorecard, branch-protection updates, or CI gates.
- **Rollback Trigger**: Revert the generator/output/evidence commit if the
  snapshot creates false freshness failures.

## Completion Criteria

- Generated security automation readiness snapshot exists and passes `--check`.
- Repo contracts check snapshot freshness.
- Scripts README, Stage 03/04 indexes, Stage 90 data indexes, and audit
  references are synchronized.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/117-security-automation-readiness-snapshot/spec.md](../../03.specs/117-security-automation-readiness-snapshot/spec.md)
- **Task**: [../tasks/2026-07-06-security-automation-readiness-snapshot.md](../tasks/2026-07-06-security-automation-readiness-snapshot.md)
- **Generated reference**: [../../90.references/data/security/security-automation-readiness.md](../../90.references/data/security/security-automation-readiness.md)
- **Security maturity audit**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
