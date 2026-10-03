---
title: "Quality Source Integration and Synthetic Acceptance"
version: "0.1.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-04"
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
scope; HOME service changes, real target traffic, project credentials and
real-data migration are not. Source review publication is separately authorized
by the owner's 2026-10-03 main-integration request.

## Inputs

- Baseline main `5f99e0e51b41b912f128daafb4a3d41539b77560`; feature
  branch `feat/spec-0203-quality-results` in its own worktree.
- Current root quality Compose, dev-pg provisioner, Alloy/Grafana and
  SPEC-0202 TSK-0001 perf_db handoff.
- Prompt 03, official current tool contracts, approved source-only scope.
- No real `.env`, secret value, application data or production log is an input.

**Approved follow-up source ownership:**

The owner's 2026-10-03 request to reconcile implementation conflicts and complete
SPEC-0201–0205 authorizes this source amendment. Reuse the existing Traefik
engine for a separate synthetic exact-path boundary; do not add another HTTP
mock or change HOME gateway/root. The serial Task writer owns these added or
updated files:

- `infra/11-quality/k6/quality_run.py`, `container_executor.py`, `http_guard.py`,
  `result_import.py`, `object_store.py`, and `README.md`;
- `examples/operations/quality-path-guard/docker-compose.yml`, `acceptance.py`,
  and `README.md`;
- `tests/validation/test_k6_results.py`;
- `infra/06-observability/grafana/provisioning/contracts/perf-db.datasource.yml.example`,
  `dashboards/Infrastructure/perf-results.json`, and `README.md`;
- `examples/operations/quality-metrics/acceptance.py`, `docker-compose.yml`,
  and `README.md`;
- `tests/validation/test_quality_observability.py` and
  `tests/validation/test_quality_object_store.py`.

Guard inputs remain synthetic `test`/mock-only. Its separate project, two
internal networks, pinned images, port 0, volume 0 and secret 0 are checked
before isolated execution. HOME deployment, real API load, project writer
issuance and real object uploads remain held. Source rollback reverts only
these files; fixture cleanup targets only the owned rehearsal project/network
and controller-created temporary directory, without volume deletion or prune.

## Work Log

| Unit | Source and result | State |
| --- | --- | --- |
| W1 | SPEC-0203 package, registered IDs and current root/quality inventory | SOURCE_DONE |
| W2 | `dev-perf-provision`, `perf_db.quality`, project RLS, role grants, exact replay/conflict import and v2 upgrade | SOURCE_DONE; isolated PostgreSQL acceptance passed |
| W3 | Manifest/path validation, immutable artifacts, two-network exact-Path Traefik guard, manifest threshold/structured summary wrapper | SOURCE_DONE; mock-only isolated HTTP acceptance passed; real app target remains NOT_RUN |
| W4 | Transactional normalized import, approved storage contract, bounded immutable upload/restore receipt and exact object-ref binding | SOURCE_DONE; synthetic client/integration checks passed; actual SeaweedFS conditional/checksum compatibility and bucket/writer remain NOT_RUN |
| W5 | WireMock function/load override and independent Locust LAB; root no longer includes Locust | SOURCE_DONE; bounded synthetic WireMock checks passed; Locust request-event/OTel runtime unverified |
| W6 | Bounded Alloy OTLP metrics, k6 dashboard filters, opt-in read-only perf_db datasource contract and result dashboard | SOURCE_DONE; isolated metrics delivery passed; live Grafana datasource issuance remains NOT_RUN |
| W7 | Korean package README, operations docs, catalog projection, focused checks and independent review | PARTIAL: changed gate rerun found one stale projection after the perf mount was narrowed; catalog and exact assertion now pass, but the aggregate gate was not repeated again; infra-validate remains BLOCKED |

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
| `python3 scripts/validation/run-ci-gate.py --profile changed` (first) | 1; 67 Compose selections passed, then 3 assertions failed | Missing Grafana service row and two local file modes were corrected. |
| `python3 scripts/validation/run-ci-gate.py --profile changed` (rerun) | 1; document-governance 629 tests with one failure | `dev-perf-provision` mount projection remained stale after its secret-minimizing change; generated row was refreshed. The aggregate was not repeated after that exact correction. |
| `python3 -m unittest tests.validation.test_perf_db_contract tests.validation.test_secret_metadata_sync -q` | 0; 48 tests | Narrow perf-only mount, no unnecessary backup-key grant, root/LAB public key counts and secret metadata. |
| `python3 -m unittest tests.validation.test_k6_results -q` | 0; 18 tests | Malformed peer inspection fails closed with durable interrupted receipt. |
| `python3 scripts/validation/check-operations-catalog.py` and exact `test_operations_checker_is_executable_and_has_one_complete_route` | 0; PASS and 1 test | Current generated service inventory matches the perf-only mount. |
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
| 2–4 | SOURCE/ISOLATED_PASS; LIVE_NOT_RUN | Mock-only HTTP path/threshold/finalization passed; approved object upload/restore/import contract has synthetic checks; real target/store input remains absent |
| 5 | ISOLATED_PASS | Dedicated `perf_db` synthetic PostgreSQL and negative authority checks |
| 6 | ISOLATED_PASS | Function/load render, journal/reset and HTTP admin 403 checks |
| 7 | STATIC_PASS; RUNTIME_NOT_RUN | Root/LAB graph separation and bounded LAB declarations; Locust telemetry runtime not proven |
| 8 | SOURCE/ISOLATED_PASS; LIVE_NOT_RUN | Alloy actual metrics delivery passed; perf_db read-only views/datasource have source contracts; live Grafana reader connection remains unproven |
| 9 | SOURCE_DONE | Operation contracts and explicit evidence boundaries |

**Follow-up verification evidence:**

- RED: `python3 -m unittest tests.validation.test_k6_results.K6ResultContractTests.test_manifest_rejects_wiremock_admin_and_noncanonical_paths -q`
  exited 1 with seven unsafe path cases accepted by the old validator.
- GREEN: `python3 -m unittest tests.validation.test_k6_results -q` exited 0,
  22 tests. Synthetic guard checks cover exact routes, modified config,
  unexpected backend peer, extra provider, published port and malformed inspect.
- `python3 -m unittest tests.validation.test_perf_db_contract tests.validation.test_k6_results tests.validation.test_quality_mock_lab tests.validation.test_quality_observability -q`
  exited 0 with 42 tests after the observability source contract was added.
- Observability RED: two new tests exited 1 for absent datasource/dashboard.
  GREEN with the two existing dashboard integrity gates exited 0, 11 tests.
- `python3 -m compileall -q infra/11-quality/k6` exited 0.
- Host Python lacks Ruff, but the existing pre-commit cache contains the repository's
  pinned Ruff 0.15.12. Scoped `ruff check` and `ruff format --check` on the five
  owned Python files both exited 0. No dependency was installed.


The tracked rehearsal controller was executed on Docker context `default`,
Linux/amd64, after checking capacity and subnet collisions. The fixture used a
unique project, internal subnets `10.251.211.0/24` and `10.251.212.0/24`, no
published ports, named volumes or secrets; resource declarations bound CPU,
memory, PID and writable tmpfs. Cached image references were:

- Traefik: `traefik@sha256:f86a2cab1b5c649070c49f883c743dd32d8485a56e3368c5f93b9e91f1e91259`;
- WireMock: `wiremock/wiremock@sha256:f8c42a38dca3f4a1d7219af11c80438740f39eebb1505b0f029aed743c20e147`;
- k6: `grafana/k6@sha256:9bd01d6941fca969cb61bb57d2da5ee9b385fe2aa8881df3798c196564d6ace6`.

`python3 examples/operations/quality-path-guard/acceptance.py --guard-image
<above-Traefik-reference> --mock-image <above-WireMock-reference> --k6-image
<above-k6-reference>` exited 0. Approved `/health` returned 200; a catch-all
backend would return 200 for `/unapproved`, but the guard returned 404;
`/__admin/requests` also returned 404. The first k6 run exited 0 with
`passed/complete`; a second attempt overrode scenario thresholds from the
manifest and exited 99 with `failed_threshold/complete`. Controller cleanup
succeeded using only its project `down --timeout 10`, without volume/prune
options, then removed only its temporary directory.

Initial rehearsal attempts exposed incorrect tmpfs YAML quoting and a journal
CLI spelling in the new fixture, which were corrected from the existing
WireMock load declaration and actual `--help`. Another attempt exited 0 but
was correctly finalized incomplete: legacy `--summary-export` lacked typed
metrics and threshold outcomes. The infra-owned `handleSummary` wrapper fixed
that actual interface mismatch without weakening finalization. The official
image exposes dormant HTTPS metadata, so verification now rejects enabled
HTTPS listener flags rather than treating `EXPOSE` as a running listener.

Independent review's load-journal and optimized-Python findings were fixed:
load peers must supply `--no-request-journal`, and explicit acceptance
exceptions remain effective with `python -O`. The 22 runner tests cover both
negative cases. Subsequent HTTP execution uses the same guard/threshold
contract; these findings do not authorize HOME changes.

The metrics controller's final recorded command was:

```bash
python3 examples/operations/quality-metrics/acceptance.py \
  --alloy-image grafana/alloy@sha256:b8ec653c44235fbe910879145dac3597d66b0aaecf60bcbbe82580767771a839 \
  --prom-image prom/prometheus@sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0 \
  --probe-image python@sha256:79e7a9b9ff1cbceff819f856fb374477792a5967759d94df266de7b7b4120e6f
```

It exited 0 on 2026-10-03 14:07:17 UTC in project
`quality-metrics-faf0004c517c` with only its dedicated internal network,
CPU limit sum 1.25, memory limit sum 832 MiB, and ports/volumes/secrets 0.
Delta/cumulative counters both reached 5; histogram count 5, sum 125 and
bucket 100 value 5 were verified by actual Prometheus queries. Exact delta
replay stayed 5; missing project identity was dropped; stopped Prometheus
followed by bounded queued retry reached 7. After Alloy restart, the same
metric/resource identity with a new source epoch reset to 4, then delta 2
reached 6. This proves epoch reset/next-delta behavior; tmpfs WAL and
preservation/restoration of the prior value 5 are not proven. Exact project
cleanup passed before removal of controller scratch
`/tmp/quality-metrics-faf0004c517c-3c86dz_v`. HOME was not changed.

The object handoff's first six tests witnessed RED for the missing helper,
then synthetic client and integration checks passed. New import authorization
checks rejected an unapproved bucket/prefix even after payload self-hash was
recomputed; no non-null reference is accepted without the independently
supplied storage contract and endpoint allowlist. Restored raw artifacts were
re-finalized with the same interface, reproducing final SHA and the same
normalized import envelope. AWS CLI lookup requires an explicit trusted
absolute executable before credential files are consumed, and restore failure
rolls back only its owned published inode while preserving unrelated files.
No real AWS credential, bucket or SeaweedFS request was used.

Native distribution amendment assigns existing `infra/11-quality/k6/result_inspection.py`
and new `tests/validation/test_quality_raw_points.py` to this Task writer.
Four new tests first failed (missing native inspector and v2 execution contract),
then passed: immutable byte/precision/digest preservation, missing/truncated
artifact denial, nonfinite/unsafe-tag/time rejection, and concurrent-growing
stream denial (RED exit 1 before cumulative byte quota and inode/mtime/ctime
checks; GREEN exit 0 afterward). Actual executor v2
requires bounded native Metric/Point NDJSON; legacy v1 summary-only fixtures
remain compatible without claiming preserved distributions. Native raw points
join the immutable checksum and object upload/restore artifact set.
The final actual guard rehearsal returned exit 0, passed/complete with 34
native finite identity-safe points, and exit 99, failed_threshold/complete
for the second manifest-controlled attempt. No URL/query/custom tags were
accepted; exact owned fixture cleanup passed. These are synthetic runtime
proofs using the previously recorded pinned image digests, not live API load.

The final combined source command
`python3 -m unittest tests.validation.test_perf_db_contract tests.validation.test_k6_results tests.validation.test_quality_mock_lab tests.validation.test_quality_observability tests.validation.test_quality_object_store tests.validation.test_quality_raw_points -q`
exited 0 with 57 tests. The eight runner/importer/controller Python paths passed
registered Ruff 0.15.12 `check` and `format --check` (exit 0). These are new
source evidence, separate from the earlier original package's runtime checks.

These checks prove synthetic source contracts. The opt-in datasource example
is outside Grafana's runtime provisioning directory; no reader account,
credential or HOME connection was created. Actual SeaweedFS compatibility and live Grafana reader connection remain
NOT_RUN. These source/synthetic checks do not convert absent approvals or
inputs into operational acceptance. W7 source gate stages completed on 2026-10-04 after registered identity,
checkout-mode and test-owner corrections. The original changed command
returned 1 and remains recorded; the existing runner resumed its registered
tail and returned 0. Document regressions 629, integrated regressions 239,
67 Compose selections and final repository regressions 175 passed at their
respective stages. The required-selector expectation was updated with the
new seven modules, preserving all runtime skip boundaries. The root writer
TSK-0004 alone owns the shared workflow contract. Real store, datasource and
perf_db runtime acceptance remain NOT_RUN. The final independent follow-up
review passed as recorded below.

## Review Evidence

Independent code review found no open CRITICAL/HIGH/MEDIUM implementation
defect in the current source diff; security and approval boundary review passed.
The original review required partial/BLOCKED status for path confinement,
SeaweedFS handoff, Grafana perf_db views and Alloy end-to-end metrics.
Follow-up source adds the exact-path guard and opt-in read-only views;
approved object handoff source and isolated end-to-end metrics were added;
actual store compatibility and live Grafana reader connection remain held.
The final independent review on 2026-10-03 found no remaining findings in
the runner, native inspector, finalizer, importer and object handoff. It
reran 15 raw-point/object tests and 36 combined runner/object/raw-point
tests, both exit 0. It confirmed total-byte bounds, EOF file identity,
external object approval and fail-closed native input. No private input,
HOME endpoint or real store was used. Actual perf_db import and store
compatibility remain NOT_RUN.

## Commit Ledger

The original source landed through PR #349 at main
`d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`. Its original partial criteria
remain visible above. Follow-up source work uses `codex/spec-0201-0205-closure`;
publication and final feature SHA are recorded by the serial root controller.
The in-progress lifecycle was reconciled through `dfce5cdae`, `d7ad61617`,
and `ea0c1d224`; these transitions do not convert deferred acceptance to PASS.


## Rulings

The user authorized Prompt 03 source implementation by supplying the direct
implementation request after requiring Prompt 02 local integration. Earlier
HOME hold remains effective. The owner confirmed on 2026-10-03 that the
actual development API target and SeaweedFS result bucket/writer are not yet
selected; this package remains source-contract-only. Prompt 04's prior shared Alloy ownership is
superseded for this serial Prompt 03 file edit only; Prompt 04 consumes it.

## Deferred Items

Live application load, real credentials/bucket, HOME activation, external
app E2E, operational recovery and data migration await separate specific
approvals and concrete project inputs.
