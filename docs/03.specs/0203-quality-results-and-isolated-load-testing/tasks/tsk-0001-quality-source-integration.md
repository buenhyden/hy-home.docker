---
title: "Quality Source Integration and Synthetic Acceptance"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0203-TSK-0001"
parent_ids:
- "SPEC-0203"
- "SPEC-0203-PLAN-0001"
created: "2026-10-03"
---

# Quality Source Integration and Synthetic Acceptance

## Objective

Implement W1–W7 of SPEC-0203-PLAN-0001 under the user's Prompt 03 source
request, after Prompt 02 landed locally. Source and synthetic tests are in
scope; HOME service changes, real target traffic, project credentials,
real-data migration and remote actions are not.

## Inputs

- Baseline main `5f99e0e51b41b912f128daafb4a3d41539b77560`; feature
  branch `feat/spec-0203-quality-results` in its own worktree.
- Current root quality Compose, dev-pg provisioner, Alloy/Grafana and
  SPEC-0202 TSK-0001 perf_db handoff.
- Prompt 03, official current tool contracts, approved source-only scope.
- No real `.env`, secret value, application data or production log is an input.

## Work Log

| Unit | Source and result | State |
| --- | --- | --- |
| W1 | SPEC-0203 package, registered IDs and current root/quality inventory | SOURCE_DONE |
| W2 | `dev-perf-provision`, `perf_db.quality`, project RLS, role grants, exact replay/conflict import and v2 upgrade | SOURCE_DONE; isolated PostgreSQL acceptance passed |
| W3 | Versioned manifest, budget/origin/path validation, immutable local artifacts and explicit failure states | PARTIAL: k6 traffic remains fail closed with `path_confinement_unavailable` until an enforceable HTTP path boundary exists |
| W4 | Transactional normalized import, SHA256 identity, bounded input and failure receipts | PARTIAL: SeaweedFS upload/restore and non-null `object_ref` await an approved bucket, writer scope and runnable path boundary |
| W5 | WireMock function/load override and independent Locust LAB; root no longer includes Locust | SOURCE_DONE; bounded synthetic WireMock checks passed; Locust request-event/OTel runtime unverified |
| W6 | Bounded Alloy OTLP metrics source and existing k6 dashboard filters | PARTIAL: perf_db read-only Grafana datasource/views and metrics end-to-end delivery remain unimplemented/unverified |
| W7 | Korean package README, operations docs, catalog projection, focused checks and independent review | PARTIAL: changed gate exposed three failures; each corrected and targeted retest passed, but the aggregate gate was not repeated; infra-validate remains BLOCKED |

The user approved two historical Locust link corrections and the seven current
service inventory projections in the Stage 90 research document. Historical
narrative and archived SPEC-0199/0200 authority were not reused. Shared root,
Alloy, environment, registry and projection files had one serial writer.

## Verification Evidence

| Command or check | Exit / finding | Scope |
| --- | --- | --- |
| `python3 -m unittest tests.validation.test_perf_db_contract tests.validation.test_k6_results tests.validation.test_quality_mock_lab tests.validation.test_quality_observability -q` | 0; 35 tests | Source contract and regressions |
| `python3 scripts/validation/check-operations-catalog.py` | 0; PASS | Generated current service projection |
| `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref main` | 0; 32 selected, 0 violations | Changed document metadata |
| `python3 scripts/validation/check-document-links.py --mode all` | 0; 1054 documents, 10735 links, 0 failures, 1 historical archive warning | Link graph |
| `git diff --cached --check` | 0 | Staged whitespace |
| `bash .agents/skills/infra-validate/scripts/static-checks.sh` | 2; PASS 9, BLOCKED 6, NOT_RUN 2 | Unsupported input graph; `yamllint`/`shellcheck` unavailable; dependent Compose checks blocked. No runtime or secret access. |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | 1; 67 Compose selections passed, then 3 assertions failed | Repository path-aware gate. Missing Grafana service row and two local file modes were corrected. Aggregate was not repeated. |
| `python3 -m unittest tests.validation.test_compose_baseline_gates.ObservabilityDashboardContractTests.test_readme_covers_every_service_every_job_and_every_dashboard tests.validation.test_openwebui_oidc_entrypoint.OpenWebUiOidcEntrypointTests.test_script_is_executable_and_not_group_or_world_writable tests.validation.test_gatus_oidc.GatusOidcEntrypointTests.test_script_is_not_group_or_world_writable -q` | 0; 3 tests | Exact failing assertions after correction |
| `bash scripts/operations/sync-tech-stack-versions.sh --check` | 0; 91 tracked image repositories in sync | Version projection |

Bounded isolated checks used Docker context `default`, dedicated project/network,
port 0, synthetic secret where required, bounded CPU/memory and exact owned
cleanup. Fresh/rerun/legacy upgrade and A/B SQL authority checks passed for
`perf_db`; concurrent provision returned exit 75. WireMock function stub and
journal reset passed; no-journal load stub passed and HTTP admin returned 403
with `--admin-api-require-https`. An initial assertion that a disabled journal
would return an empty admin response failed because that endpoint returned 500;
the check and documentation were corrected. Network-free k6 `run --help` passed;
a synthetic threshold-failure script exited 99 as expected. The first k6
synthetic attempt could not read a 0700 temp directory (exit 255); after
fixture permissions were corrected, the expected threshold failure was observed.
Owned test containers, networks and temporary files were removed. Neither
result is evidence of real target traffic, HOME health or k6 remote write.

| Acceptance criterion | Result | Evidence/limit |
| --- | --- | --- |
| 1 | SOURCE_DONE | Current tool roles/licenses in quality Guide and Policy |
| 2–4 | PARTIAL/BLOCKED | Manifest/finalization/import checks pass; actual HTTP path restriction, traffic and durable object handoff unavailable |
| 5 | ISOLATED_PASS | Dedicated `perf_db` synthetic PostgreSQL and negative authority checks |
| 6 | ISOLATED_PASS | Function/load render, journal/reset and HTTP admin 403 checks |
| 7 | STATIC_PASS; RUNTIME_NOT_RUN | Root/LAB graph separation and bounded LAB declarations; Locust telemetry runtime not proven |
| 8 | PARTIAL/BLOCKED | Alloy config validated; actual metrics delivery and perf_db Grafana views not proven |
| 9 | SOURCE_DONE | Operation contracts and explicit evidence boundaries |

## Review Evidence

Independent code review found no open CRITICAL/HIGH/MEDIUM implementation
defect in the current source diff; security and approval boundary review passed.
Reviewers require SPEC-0203 to remain partial/BLOCKED for live k6 path
confinement, SeaweedFS handoff, Grafana perf_db views and Alloy end-to-end
metrics. These are not acceptance PASS claims.

## Commit Ledger

The reviewed source is committed on `feat/spec-0203-quality-results`; the exact
feature SHA is recorded in the final report. No local main merge, push or PR
has been made. The branch and worktree remain available for the deferred
SPEC-0203 requirements.

## Rulings

The user authorized Prompt 03 source implementation by supplying the direct
implementation request after requiring Prompt 02 local integration. Earlier
HOME hold remains effective. Prompt 04's prior shared Alloy ownership is
superseded for this serial Prompt 03 file edit only; Prompt 04 consumes it.

## Deferred Items

Live application load, real credentials/bucket, HOME activation, external
app E2E, operational recovery and data migration await separate specific
approvals and concrete project inputs.
