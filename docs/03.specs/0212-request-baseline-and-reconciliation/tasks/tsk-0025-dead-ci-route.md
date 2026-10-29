---
title: "Dead CI Route Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0025"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Dead CI Route Task

## Overview

### Objective

Execute W41: find active references and routing to files that do not exist,
and remove the dead ones. This Task owns criterion 36 only.

## Inputs and Authorization

The original request asks that no QA or CI path links a deleted or outdated
manifest, and that scripts which do not reflect the current state be fixed.
On 2026-10-29 the owner asked for the request review to continue through to
merge. The input is `main` at merged PR #622. The authorization covers this
change, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0025 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0025 | ready | in-progress | #objective |
| SPEC-0212-TSK-0025 | in-progress | completed | #evidence |

### Scan

Every `scripts/`, `infra/`, `labs/`, `.github/`, and `tests/` path with a file
extension, named by a tracked file outside `docs/03.specs/`,
`docs/98.archive/`, `graphify-out/`, and `tests/`, was compared with the
tracked tree. 56 named paths did not exist.

| Group | Decision |
| --- | --- |
| `.github/workflow-contract.yml` routing prefix `scripts/validation/check-supply-chain.sh` | Removed. Git history has no file at that path, so the prefix never matched anything. |
| Dated research pack files under `docs/90.references/research/` | Kept; dated observations of earlier layouts. |
| Dated security-update ledgers and synthetic resource-optimization fixtures under `infra/09-platform-ops/` | Kept; dated records and synthetic inputs. |
| `ONE_TIME_VERIFIER_PATHS` in `scripts/lib/document_governance/archive.py` | Kept; the archive check asserts these stay absent. |
| Service-local `scripts/...` in READMEs and OpenBao scripts | Kept; relative to the service folder, and each target exists there. |
| `.github/README.md` in `.github/repository-surface.md` | Kept; the sentence is conditional on the file existing. |
| `scripts/ws.sh` in the product-intake README | Kept; a Project-Template script, quoted from that repository. |
| Skill-relative `scripts/` links | Kept; recorded in TSK-0024. |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Path existence scan | 36 | W41 | Named paths in active files against `git ls-files` | `main`@`b9d610170` | PASS | One dead routing prefix removed; the rest classified | required | - |
| Contract parse | 36 | W41 | `yaml.safe_load` of `.github/workflow-contract.yml` | This branch | PASS | Parses | required | - |
| Workflow-contract and gate tests | 36 | W41 | `python3 -m unittest tests.lib.gate.test_github_workflow_contract tests.validation.test_ci_gate_plan tests.validation.test_agent_governance_ci_routing` | This branch | PASS | 182 tests OK | required | - |
| Metadata contracts | 36 | W41 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 36 | accepted | Path existence scan, Contract parse, Workflow-contract and gate tests, Metadata contracts | No CI routing names a file that does not exist; the other missing paths are dated, synthetic, relative, conditional, or intentionally absent. | SPEC-0212 TSK-0025 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
