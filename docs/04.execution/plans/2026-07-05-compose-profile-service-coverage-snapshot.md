---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md -->

# Compose Profile Service Coverage Snapshot Implementation Plan

## Overview

This plan implements a generated Docker Compose profile/service coverage
reference and freshness gate. It closes `AEA-AUTO-005` by moving audit evidence
from manual prose into a deterministic Stage 90 data artifact.

## Context

The agentic engineering implementation audit identified a gap in Compose
profile coverage evidence. The repository already validates Compose behavior
through existing scripts, but audit readers had no generated inventory that
answers which services are default versus profile-gated across the tracked
Compose corpus.

## Goals & In-Scope

- **Goals**:
  - Generate a Stage 90 Docker data reference from tracked Compose files.
  - Record profile, stage, and Compose-file coverage without runtime
    inspection.
  - Add script inventory and repo-contract freshness enforcement.
  - Update audit, indexes, progress, and generated navigation evidence.
- **In Scope**:
  - `scripts/operations/generate-compose-profile-service-coverage.sh`
  - `docs/90.references/data/docker/compose-profile-service-coverage.md`
  - Stage 03/04 evidence, data indexes, script inventory, audit candidate
    status, and repository contracts.

## Non-Goals & Out-of-Scope

- No Compose service, profile, image, network, or volume changes.
- No Docker Compose execution, container lifecycle action, deployment, or
  runtime health inspection.
- No `.env`, secret, credential, token, private-key, shell-history, raw-log, or
  local auth-file reads or writes.
- No CI workflow, provider runtime, or remote-state changes.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-CPC-001 | Create Stage 03/04 evidence for the snapshot contract. | `docs/03.specs/108-compose-profile-service-coverage-snapshot/**`, this plan, task evidence, indexes | VAL-CPC-001 | Spec, plan, and task are linked and indexed. |
| PLN-CPC-002 | Add generator and generated Stage 90 reference. | `scripts/operations/generate-compose-profile-service-coverage.sh`, `docs/90.references/data/docker/compose-profile-service-coverage.md` | VAL-CPC-001, VAL-CPC-002 | Generator write and `--check` pass. |
| PLN-CPC-003 | Wire script inventory and repo-contract freshness gate. | `scripts/README.md`, `scripts/validation/check-repo-contracts.sh` | VAL-CPC-003, VAL-CPC-004 | Repo contracts fail on stale snapshot and pass on current output. |
| PLN-CPC-004 | Update audit/progress/index evidence and close. | Stage 90 indexes, audit candidate, progress memory, generated LLM Wiki, Graphify | VAL-CPC-004 | Final validation summary is recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Generator | Generate Compose coverage reference. | `bash scripts/operations/generate-compose-profile-service-coverage.sh` | Reference is generated from tracked Compose files. |
| VAL-PLN-002 | Generator | Check generated reference freshness. | `bash scripts/operations/generate-compose-profile-service-coverage.sh --check` | Freshness check passes. |
| VAL-PLN-003 | Syntax | Check shell syntax. | `bash -n scripts/operations/generate-compose-profile-service-coverage.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-004 | Contracts | Check full repo contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |
| VAL-PLN-005 | Docs | Check docs and generated indexes. | `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | All pass. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Generated reference is mistaken for runtime truth | Medium | The generated document states that Compose files remain the runtime source of truth. |
| Generator accidentally includes untracked runtime artifacts | Medium | Use `git ls-files` and filter only tracked Compose paths. |
| Snapshot becomes stale after Compose changes | Medium | Add generator `--check` to repository contracts. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: N/A; this is deterministic repository inventory
  generation.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: User continued the broader infra/document contract
  cleanup on 2026-07-05.
- **Rollback Trigger**: Revert the logical commit and rerun repo contracts if
  the generated reference or freshness gate causes false positives.
- **Prompt / Model Promotion Criteria**: N/A.

## Completion Criteria

- [x] Stage 03/04 evidence exists and is indexed.
- [x] Compose profile/service coverage generator exists under Operations.
- [x] Stage 90 generated reference exists and passes generator `--check`.
- [x] Repo contracts enforce generated snapshot freshness.
- [x] Audit/progress evidence and generated indexes are updated.
- [x] Final validation passes.

## Related Documents

- **Spec**: [../../03.specs/108-compose-profile-service-coverage-snapshot/spec.md](../../03.specs/108-compose-profile-service-coverage-snapshot/spec.md)
- **Task**: [../tasks/2026-07-05-compose-profile-service-coverage-snapshot.md](../tasks/2026-07-05-compose-profile-service-coverage-snapshot.md)
- **Generated reference**: [../../90.references/data/docker/compose-profile-service-coverage.md](../../90.references/data/docker/compose-profile-service-coverage.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
