---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-tech-stack-version-provenance.md -->

# Tech-Stack Version Provenance Implementation Plan

## Overview

This plan implements the tech-stack version drift severity and source
provenance follow-up from the agentic engineering automation candidates
reference.

## Context

The repository already checks that curated tech-stack registry images are
declared in listed Compose files. Reviewers also need a compact generated
snapshot that explains severity, exception status, and source line provenance
without re-reading every Compose file.

## Goals & In-Scope

- **Goals**:
  - Generate a Stage 90 Docker data snapshot for tech-stack version
    provenance.
  - Classify registry images by status and severity.
  - Record Compose source paths and line numbers for each registry image.
  - Keep the snapshot deterministic and freshness-checked.
  - Add Stage 03/04 evidence and close the automation-candidate follow-up.
- **In Scope**:
  - `scripts/operations/generate-tech-stack-version-provenance.sh`
  - `docs/90.references/data/docker/tech-stack-version-provenance.md`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 evidence, Docker/Stage 90 indexes, audit references, generated
    navigation, and progress memory.

## Non-Goals & Out-of-Scope

- No Docker Compose image version changes.
- No registry network lookups, vulnerability scanning, SBOM generation, or
  provenance attestation.
- No CI workflow behavior change or new remote gate.
- No runtime, deployment, provider adapter, credential, secret, token, raw-log,
  shell-history, or `.env` mutation.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-TSV-001 | Add provenance generator. | `scripts/operations/generate-tech-stack-version-provenance.sh` | VAL-TSV-001, VAL-TSV-002 | Generator write and `--check` pass. |
| PLN-TSV-002 | Add generated Docker data output. | `docs/90.references/data/docker/tech-stack-version-provenance.md` | VAL-TSV-001, VAL-TSV-002 | Output includes severity/status/source provenance tables. |
| PLN-TSV-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-TSV-003 | Full repo contracts pass. |
| PLN-TSV-004 | Add evidence and close candidate. | Stage 03/04 indexes, Stage 90 indexes, audit docs, progress | VAL-TSV-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-TSV-001 | Generator | Generate and check snapshot. | `bash scripts/operations/generate-tech-stack-version-provenance.sh`; `bash scripts/operations/generate-tech-stack-version-provenance.sh --check` | Output is fresh. |
| VAL-PLN-TSV-002 | Registry | Confirm existing registry-to-Compose drift gate. | `bash scripts/operations/sync-tech-stack-versions.sh --check` | Registry is in sync. |
| VAL-PLN-TSV-003 | Syntax | Check changed shell scripts. | `bash -n scripts/operations/generate-tech-stack-version-provenance.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-TSV-004 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-TSV-005 | Docs | Check generated and docs contracts. | Compose coverage freshness, LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-TSV-006 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Snapshot is mistaken for runtime truth | Medium | Label it generated audit context and link canonical registry/Compose sources. |
| Floating exceptions are treated as success without review | Medium | Classify approved floating tags as `advisory` and preserve owner/review cadence. |
| Source line provenance drifts after Compose changes | Medium | Add generator `--check` to repo contracts. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Generator write/check, registry sync check, and
  repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before CI publication, registry network
  lookups, vulnerability gating, SBOM/provenance attestation, or image updates.
- **Rollback Trigger**: Revert the generator/output/evidence commit if the
  snapshot creates false freshness failures.

## Completion Criteria

- Generated provenance snapshot exists and passes `--check`.
- Repo contracts run and guard the snapshot.
- Scripts README, Docker data indexes, and Stage 03/04 evidence reference the
  new generator.
- Automation candidate text records the follow-up as implemented.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/114-tech-stack-version-provenance/spec.md](../../03.specs/114-tech-stack-version-provenance/spec.md)
- **Task**: [../tasks/2026-07-06-tech-stack-version-provenance.md](../tasks/2026-07-06-tech-stack-version-provenance.md)
- **Generated provenance**: [../../90.references/data/docker/tech-stack-version-provenance.md](../../90.references/data/docker/tech-stack-version-provenance.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
