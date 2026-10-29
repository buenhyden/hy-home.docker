---
title: "Absence Test and Workspace Writer Audit Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0016"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Absence Test and Workspace Writer Audit Task

## Overview

### Objective

Execute W32: record the owner's choices for the three items TSK-0013 deferred
or left not run. This Task owns criterion 27 only.

## Inputs and Authorization

On 2026-10-29 the owner chose, per item: audit the absence tests without
deleting any; keep the existing `_workspace` writers and document them; and
keep external acceptance `NOT_RUN`. The input is `main` at merged PR #612. The
authorization covers this branch, its pull request, and merge through the
protected path. It grants no test removal and no script change.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0016 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0016 | ready | in-progress | #objective |
| SPEC-0212-TSK-0016 | in-progress | completed | #evidence |

### Absence tests

An AST scan of `tests/**/test_*.py` found every `assertFalse(ROOT / "…"
.exists())`-style assertion. Assertions on temporary roots (gate-call
markers, generated secrets, fixture TLS files) are excluded; the rows below
use the real repository root.

| Test | Absent path | Class | Reason |
| --- | --- | --- | --- |
| `tests/validation/test_infra_tier_layout.py:89` | `infra/04-data/influxdb` | current rule | ADR-0047 keeps InfluxDB out of the deployable model. |
| `tests/validation/test_tech_stack_version_contract.py:191` | `renovate.json` | current rule | Renovate reads `renovate.json` before the tested config, so a copy would replace it. |
| `tests/validation/test_quality_mock_lab.py:50`, `:52` | `infra/11-quality/locust` | current rule | Locust is a standalone lab under `labs/`; a tier copy would add a second deploy path. |
| `tests/validation/test_service_runtime_compatibility.py:30` | `infra/04-data/supabase` | current rule | Supabase is a standalone lab; same reason. |
| `tests/validation/test_quality_mock_lab.py:18` | `infra/11-quality/wiremock/docker-compose.load.yml` | current rule | Load mode lives in `wiremock.load.yml`; a second Compose file would split the contract. |
| `tests/validation/test_service_wiring_contracts.py:294` | `infra/docker-compose.dedicated-valkey-monitor.yml` | current rule | The monitor is an overlay beside its base; a root copy escapes overlay classification. |
| `tests/lib/document_governance/test_archive.py:657` | `docs/98.archive/changes` | current rule | Stage 98 allows only registered minimal roots. |
| `tests/lib/document_governance/test_spec_packages.py:3980`, `:3984` | `docs/04.execution`, `DESIGN.md` | current rule | The stage layout has no execution stage or root design file. |
| `tests/validation/test_infra_tier_layout.py:148`, `:151`, `:285` | `infra/11-laboratory`, `infra/10-communication/mailpit`, `infra/09-tooling` | past removal | The same tests assert the current placements directly; these lines only guard leftovers of the tier rename. |
| `tests/validation/test_agent_governance_ci_routing.py:200` | `scripts/validation/check-repo-contracts.sh` | past removal | The next line asserts the manifest no longer names it, which is the current rule. |
| `tests/lib/document_governance/test_archive.py:1020` | Prefixed `mig-0003` path | past removal | The SHA-256 check on the current path already fixes the migration's identity. |

No test is deleted. The five past-removal rows are candidates for their
surface owners; each overlaps a positive assertion, so a removal would lose
only the leftover guard. The scan sees only literal `ROOT / "…"` paths;
`tests/validation/test_infra_tier_layout.py:150`, which builds its path from a
loop variable, is classified with its file's other tier-rename lines.

### Workspace writers

These scripts write under `_workspace/repo-support/task-*/`, which the
`repo-support` README already permits. Their paths stay as they are and are
listed in that README.

| Script | Output |
| --- | --- |
| `scripts/security/seed-grype-db-cache.sh` | Grype database seed |
| `scripts/security/verify-sample-service-supply-chain.sh` | Supply-chain verification record |
| `scripts/operations/rehearse-sample-service-delivery.sh` | Delivery rehearsal inputs and record |
| `scripts/operations/rehearse-postgres-logical-upgrade.sh` | Upgrade rehearsal handoff |
| `scripts/lib/ops/compose-core-readiness.sh` | Readiness record |

No script writes to `diagnostics/`. `agent_governance_contract.py`,
`registry.py`, and `metadata/reference.py` only name the tracked READMEs.

### External acceptance

Four-repository adoption, remote protection, runtime, and native-loader
acceptance stay `NOT_RUN` with the owner. Nothing outside this repository was
read or changed.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Absence-test scan | 27 | W32 | AST scan of `tests/**/test_*.py` for negated `exists`/`is_file`/`is_dir` on `ROOT`-relative literals | This branch | PASS | 16 real-root assertions classified | required | - |
| Writer scan | 27 | W32 | `grep -rl _workspace` over `scripts`, `infra`, `labs`, `.github` | This branch | PASS | 5 writers, all under `repo-support/task-*` | required | - |
| Metadata contracts | 27 | W32 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Workspace contract tests | 27 | W32 | `python3 -m unittest tests.lib.document_governance.metadata.test_reference tests.lib.test_surface_ownership` | This branch | PASS | All pass | required | - |
| External acceptance | 27 | W32 | Four-repository, remote, runtime, and native-loader acceptance | - | NOT_RUN | Owner kept these out of scope | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 27 | accepted | Absence-test scan, Writer scan, Metadata contracts, Workspace contract tests | Absence tests classified with none deleted; workspace writers listed without path changes; external acceptance stays not run. | SPEC-0212 TSK-0016 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
