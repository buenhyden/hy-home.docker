---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md -->

# LLM Wiki Stage Category Coverage Implementation Plan

## Overview

This plan implements the LLM Wiki stage/category grouping follow-up from the
agentic engineering automation candidates reference.

## Context

The generated LLM Wiki index already gives agents a safe path list. Audit
consumers also need a compact view of the same safe-path corpus by source
bucket, category, and role so they can inspect coverage shape without reading
the full index.

## Goals & In-Scope

- **Goals**:
  - Generate a Stage 90 data snapshot for LLM Wiki source-bucket/category
    coverage.
  - Keep the snapshot deterministic and freshness-checked.
  - Preserve existing LLM Wiki safe-source exclusions.
  - Add Stage 03/04 evidence and close the automation-candidate follow-up.
- **In Scope**:
  - `scripts/knowledge/generate-llm-wiki-coverage.sh`
  - `docs/90.references/data/knowledge/**`
  - `scripts/validation/check-repo-contracts.sh`
  - `scripts/README.md`
  - Stage 03/04 evidence, indexes, audit references, generated navigation, and
    progress memory.

## Non-Goals & Out-of-Scope

- No public wiki, website, or full-content export.
- No CI workflow behavior change or new required job.
- No runtime, Docker Compose, deployment, remote GitHub, provider adapter,
  credential, secret, token, raw-log, shell-history, or `.env` mutation.
- No change to Graphify authority; graph output remains advisory.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-LWC-001 | Add coverage generator. | `scripts/knowledge/generate-llm-wiki-coverage.sh` | VAL-LWC-001, VAL-LWC-002 | Generator write and `--check` pass. |
| PLN-LWC-002 | Add generated data category/output. | `docs/90.references/data/knowledge/**` | VAL-LWC-001, VAL-LWC-002 | Output groups by bucket, category, and role. |
| PLN-LWC-003 | Wire repo-contract freshness and script inventory. | `check-repo-contracts.sh`, `scripts/README.md` | VAL-LWC-003 | Full repo contracts pass. |
| PLN-LWC-004 | Add evidence and close candidate. | Stage 03/04 indexes, audit docs, progress | VAL-LWC-004 | Documentation validation passes. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-LWC-001 | Generator | Generate and check snapshot. | `bash scripts/knowledge/generate-llm-wiki-coverage.sh`; `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` | Output is fresh. |
| VAL-PLN-LWC-002 | Syntax | Check changed shell scripts. | `bash -n scripts/knowledge/generate-llm-wiki-coverage.sh scripts/validation/check-repo-contracts.sh` | No syntax errors. |
| VAL-PLN-LWC-003 | Hygiene | Check whitespace and conflict markers. | `git diff --check`; `git diff --cached --check` | No output. |
| VAL-PLN-LWC-004 | Docs | Check generated and docs contracts. | LLM Wiki freshness, doc traceability, doc implementation alignment | All pass. |
| VAL-PLN-LWC-005 | Contracts | Check full repository contracts. | `bash scripts/validation/check-repo-contracts.sh` | `failures=0`. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Snapshot includes generated or secret-bearing paths | High | Reuse LLM Wiki safe-path allowlist and exclusion rules; repo contracts check freshness. |
| Snapshot becomes a replacement for canonical source files | Medium | Label it as coverage/navigation evidence and link canonical sources. |
| New staged paths are missed during implementation | Low | Stage new files before final generation and validation. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Generator write/check and repo-contract pass.
- **Sandbox / Canary Rollout**: N/A; no runtime service changes.
- **Human Approval Gate**: Required before public publishing or CI summary
  publication.
- **Rollback Trigger**: Revert the generator/output/evidence commit if the
  snapshot creates false freshness failures.

## Completion Criteria

- Generated coverage snapshot exists and passes `--check`.
- Repo contracts run and guard the snapshot.
- Scripts README, data indexes, and Stage 03/04 evidence reference the new
  generator.
- Automation candidate text records the follow-up as implemented.
- Generated LLM Wiki and Graphify outputs are refreshed or skip evidence is
  recorded.

## Related Documents

- **Spec**: [../../03.specs/113-llm-wiki-stage-category-coverage/spec.md](../../03.specs/113-llm-wiki-stage-category-coverage/spec.md)
- **Task**: [../tasks/2026-07-06-llm-wiki-stage-category-coverage.md](../tasks/2026-07-06-llm-wiki-stage-category-coverage.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
