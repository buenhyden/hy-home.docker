---
title: "Exporter and Observability Contracts Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0046"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-02"
---

# Exporter and Observability Contracts Task

## Overview

### Objective

Implement the approved local P07 companion-start, independently expected
target and observation freshness contracts. Preserve historical datastore and
quality metrics acceptance, and separate source, owned isolation and operational
execution evidence.

## Inputs and Authorization

The direct P07 plan authorizes local implementation, synthetic and bounded
owned isolated checks, the exact declared Prometheus 3.15.1 digest image pull,
independent reviews and a normal local logical commit. Actual HOME services,
host configuration, operating credentials, external notification recipients,
credential rotation and remote integration are excluded. Existing user changes
must be preserved. Missing dependency-package documents prevent claiming a
complete historical crosscheck.

Initial workspace HEAD is clean at
`169c1b62f9a29738dde587b584418f9e93b78029`. Its branch is an observed input,
not an authorization to operate the services. Source declaration counts are
observations and not fixed acceptance constants.

Governing inputs are REQ-0027, AD-0031, SPEC-0212 and its Plan, POL-0078,
SPEC-0224 datastore observation acceptance and SPEC-0214 quality OTLP
acceptance. Historical P07 resource optimization belongs to SPEC-0218 and is
distinct from this request.

## Work Log

### Single-writer leases

Every writer records public existing-path fingerprints or ABSENT new paths
before editing and pauses only the affected path if a concurrent change
conflicts. Acceptance owner, writer, independent reviewer, data owner and
operational accepter are separate. Agent labels grant no human or operational
authority. Data owner and operational accepter remain UNASSIGNED.

| Scope | Single writer | Independent review | Boundary |
| --- | --- | --- | --- |
| Companion selection, guarded operator CLI and directly related tests | `/root/p07_launcher` | independent code/security reviewer | New `compose-start.py`, selection library and direct tests; coordinate expected output interface before edits |
| Shared Compose, Prometheus generated expectation inputs, alert rules and Grafana panels | `/root/p07_observability` | independent IaC/security reviewer | New `scripts/lib/ops/compose_observation.py`, `tests/lib/ops/test_compose_observation.py`, `tests/validation/fixtures/p07-observation.rules.test.yml`, and `infra/06-observability` Prometheus rules/config/start and Grafana dashboard slices; one writer integrates shared Compose if needed |
| Isolated quality-OTLP fixture and related proof | `/root/p07_qa` | independent QA reviewer | `examples/operations/quality-metrics/acceptance.py`, its Compose file and new `tests/validation/test_p07_quality_metrics.py`; synthetic inputs only |
| SPEC-0212, this Task, DATA-0096 and relevant operating docs | `/root/p07_docs` | independent document reviewer | Current Task and owned documents; preserve completed Task bodies |
| CI and script manifest registration | `/root/p07_ci` | independent CI reviewer | `.github/workflow-contract.yml`, `scripts/manifest.yaml` and new `tests/validation/test_p07_ci_routing.py`; no gate or skip weakening |

Public documentation baseline: SPEC
`9241bdfbe34a2a91588a2fe2e991e9da73d09b6917a9c75244569f460c653c12`, Plan
`c9e457e50f834d6015b96800009786915a69b248be3a32935faa11bfd84113d5`, DATA README
`afc4861050f9e387283ea99c72303c26c050745fb353272c4ffe1babddf20131`, and DATA
payload `c1160fb7d492b019676d43b309d28e4293d86668fa7f2a267949dc918b494678`.
This Task was absent at the baseline. Source writers record their own packets.

The launcher's new `scripts/operations/compose-start.py`,
`scripts/lib/ops/compose_start.py` and `tests/lib/ops/test_compose_start.py`
were absent at the baseline. The quality fixture's public baseline is
`acceptance.py` SHA `c33dc16138ed9732510ab25cd9b7b354f68185b4b979d060dd1f56129b88ffe5`
and Compose SHA `acf096ce617ed9456ede2e86e9faede852f4bd2f5059b8e59a3ac3e97dde43e2`;
its new test was absent. CI workflow contract baseline SHA is
`d9041760171b958aafa6dd9e8d32baec80354a327db8ae05a3986db364146ac7`, script
manifest `cb87cd932ec667f82ae5cf1d1fb4a49312897af4ed2444f7c78a097c61860159`,
and its new routing test was absent. These public hashes are not runtime or
credential evidence.

The document writer also owns the P07 consumer instructions in GDE-0045,
RUN-0045 and `infra/06-observability/prometheus/README.md`; their baseline
SHA-256 values, respectively, are
`e897316e99b088c5edea7ec58b76d349b4b6bf53189cf1fd046e8fd33f8cb951`,
`437475e2c36b41ff384d45f2f19bc4f90f0edc75635797021801ffcf05115ecd` and
`973eab93e575e331371877f2ac910568c52189982829cee473a18e4c885e411f`.
Exact instructions will follow the implemented interface; documenting a
consumer does not authorize execution.

The observability writer's new generator, unit test and rule-test fixture were
absent. The same writer owns the new
`infra/06-observability/prometheus/config/alert_rules/alert_rules.local.selection.yml`
(baseline ABSENT). Baseline SHA for both `prometheus.yml` and `prometheus.dev.yml` is
`0fbe5cf591ffb703f33df6a7682e219cb18985b052fae9a9183a590ae88caead`.
Baseline alert rule hashes, in Prometheus, observability and datastore order,
are `1234879f3992378def9718686309e420102fd78f61c781df67e1dbf9118626d4`,
`ff6b4b55f135b2d3cc5fe4f61ed63dafbd72f3a86044167b0a80cb8df381cf7f`, and
`d85b4a16e682702e7493984e6036727a6f909aa3d4f7afb7c2f192122930857c`.
Baseline Grafana hashes, for Prometheus, Alloy, PostgreSQL and Valkey respectively,
are `e63da9ccb8fb74c9955a567a66887bfcff1e237def9c85bf20e4a73c8ab0d391`,
`8f863ae4b622b7242469cb2a9a052e2779f71e3ce04a5d83f6d9d36c9fc9d109`,
`42e0cb7c9ea7f25dfe3e2755e806ab8b61626b012692c49dff91d5e49095b301`, and
`47c101f29ab78d500a04b987d7d064de4698bb5294091ced841eb36d9d492fdc`.
The observability writer also integrates expected-state gating in existing
gateway, auth and OpenBao alert rules; their respective baseline hashes are
`ff9508bb6c1f59b597a827937981c023d79eda8a94b0a0d058d3c9a90e633b5d`,
`ed1b30e0e9c2df62a77581543aaf262605d9400d005dc07bd5f6487d1d005896`, and
`9dc8fdb670ff84f11afd905f42f4365dfdc234051a1f998f75049197b060bc4d`.
The same writer owns the Prometheus startup script (baseline
`8d9aace1b919285f21df4033c2b83b7068014f5bc3b9b9c36733d53354998997`).
Shared observability Compose baseline is
`555bbb09e3e05f1b9de005c2d7210a9931eceb6552f5855a7d524ac14d6d4aa4`;
no Compose edit is currently planned.

### Current dispositions

| Item | Criterion | Work Unit | Initial disposition | Current boundary |
| --- | --- | --- | --- | --- |
| P07.01 | 82 | W87 | IMPLEMENT_GAP | Profile parity exists; an actual shared companion selection API is absent |
| P07.02 | 83 | W88 | IMPLEMENT_GAP | Current `up`-only rules cannot detect an absent expected series or prove backend/freshness |
| P07.03 | 84 | W89 | REUSE_ACCEPTED | Authenticated quality OTLP acceptance exists; current pinned delivery/failure checks are distinct |
| P07.04 | 85 | W90 | IMPLEMENT_GAP | General expected target state is absent; retain DEV on/off and defer unowned workload freshness |

### Safety and evidence boundaries

Use the existing source closure and policy companion authority; do not invent
a second manual inventory, automatic unrelated profile activation, reverse
dependency or unconditional disabled-service alert. A complete selection alone
may create an expected-target inventory; a target-only start cannot overwrite
the full selection. Missing expected inventory must be visible. Existing
`PROMETHEUS_DEV_DATA_EXPECTED` is explicit on/off; a conflict must fail rather
than silently selecting a new setting.

The existing Alloy 1.20.1 quality receiver is authenticated on 4319; 4317/4318
remain trace paths and Docker logs remain separate. A metrics fixture cannot
prove trace/log delivery. A quiet batch is not an outage without an active-run
contract. Verified labels, selected target, backend success, scrape freshness
and application behavior are distinct. No operation, reload or notification
delivery follows automatically from source or isolated evidence.

Prior source/synthetic investigation reports 56 focused cases and separately
records 13 quality-source tests. These are initial read-only observations, not
current work acceptance. The exact declared Prometheus image was absent in the
initial local cache; user authorized only that digest's preparation for the
isolated test. Image retrieval is not signature or operating-image acceptance.

On 2026-11-02 the exact user-authorized Prometheus 3.15.1 digest
`sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2`
was pulled and read back for linux/amd64; the Alloy 1.20.1 digest
`sha256:2aa2099af76c0098d4af7a4d6e48f86cb66dc1a000222ad927a1c67c6542d13f`
was cached. This is image availability evidence only, not signature verification,
an isolated cluster result, or operating acceptance.

### Reuse and official applicability

SPEC-0224 records HOME acceptance on 2026-10-22 for the named management and
DEV PostgreSQL and Valkey monitoring jobs, with DEV deliberately stopped in
the recorded scenario. SPEC-0214 records a separate 2026-10-08 HOME merge and
authenticated quality relay acceptance, including an unauthenticated 401.
These historical records do not establish current runtime equivalence.

The following official sources were consulted for this task on 2026-11-02;
the supplied dependencies package was not available for a complete historical
comparison. Compose's [profile documentation](https://docs.docker.com/compose/how-tos/profiles/)
distinguishes an explicit target from enabling all profile siblings, while its
[startup-order documentation](https://docs.docker.com/compose/how-tos/startup-order/)
distinguishes running from healthy dependencies. The pinned
[Alloy 1.20 remote-write reference](https://grafana.com/docs/alloy/v1.20/reference/components/prometheus/prometheus.remote_write/)
describes queue and delivery metrics; actual emitted names and labels still
require the pinned-image test. [Prometheus rule testing](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/)
defines synthetic evaluation rather than a live reload. These are design
inputs, not proof of live deployment or current backend function.

In the first isolated pinned-image run, the writer reports the emitted sent
samples counter and component label were observed. The candidate detects a
pending queue with no sent-counter progress over two minutes and separately
detects a missing counter. A highest-sent sample timestamp is not treated as
wall-clock transmission time. Final rule behavior still requires verification.

### D08 Airflow direct-start companions (2026-11-08)

A direct user request on 2026-11-08 re-ran the exporter scope as D08 on
`main` `2f86dd9e3`. The Airflow hypothesis was reproduced with the start
selector itself: `compose-start.py plan --target` for `airflow-scheduler`,
`airflow-triggerer` and `airflow-dag-processor` returned only the producer and
`airflow-init`, without `airflow-statsd-exporter`, although all three send
StatsD (`AIRFLOW__METRICS__STATSD_HOST`). Only `airflow-apiserver` carried a
companion row in POL-0078; `airflow-worker` reached the exporter through its
apiserver dependency. An earlier name search had matched the exporter in the
plan's `observations` list, not in `targets`; the membership check above is
the record. POL-0078 now gives each of the three producers its own row with
just the exporter, so a direct start adds one service and not the Airflow
stack; the apiserver and worker plans keep their seven targets.
`test_every_airflow_metrics_producer_brings_the_statsd_exporter` failed for
the three producers before the change and passes after; a bare `docker
compose up` outside the selector still does not add companions, as POL-0078
states.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and ownership | 82 | W87 | Git status and public documentation fingerprints | Clean 169c1b62f9a29738dde587b584418f9e93b78029 | PASS | Inputs and Authorization; Single-writer leases | required | - |
| D08 Airflow direct-start companions | 82 | W87 | `compose-start.py plan --target` membership and `test_compose_start` RED then GREEN | POL-0078 companion table; `main` `2f86dd9e3` | PASS | Scheduler, triggerer and dag-processor plans lacked `airflow-statsd-exporter` before; each now adds only the exporter; apiserver and worker plans unchanged at 7 targets | required | - |
| Isolated image availability | 84 | W89 | Exact digest pull/readback and cached image inspection | Prometheus 3.15.1 and Alloy 1.20.1, linux/amd64 | PASS | Availability only; see Safety and evidence boundaries. | required | - |
| First isolated OTLP fixture | 84 | W89 | Pinned Alloy and Prometheus fixture exit and cleanup | Synthetic credentials and test-owned resources | PASS | Cleanup passed; source correction remained pending. See First isolated OTLP fixture below. | required | - |
| Corrected isolated OTLP fixture | 84 | W89 | Pinned Alloy and Prometheus fixture rerun and cleanup | Corrected frozen QA source; synthetic credentials and test-owned resources | PASS | Exit 0 and cleanup passed; trace/log transport, live Grafana and prior-state restore remain NOT_RUN. | required | - |
| Dashboard query fixture | 83 | W88 | Native isolated Prometheus query evaluation and OTLP regression | Eight changed panels, 11 PromQL expressions, synthetic data | PASS | Query results were checked for empty vectors, exit 0 and owned cleanup passed. A separate concurrent probe hit its 64 MiB limit (exit 137); it was not this fixture result. | required | - |
| Quality fixture regression | 84 | W89 | Synthetic/static suite and changed-line trace coverage | Final candidate QA source; subprocess internals excluded | PASS | 19 synthetic tests; 81/98 changed executable lines (82.7%) across synthetic and fixture runs. | required | - |
| Companion selection | 82 | W87 | Source and synthetic selection and CLI checks | Assigned source writer packet | NOT_RUN | Await actual receipts | required | - |
| Launcher candidate | 82 | W87 | Public target plan and synthetic launcher suite | Candidate source; synthetic inputs | FAIL | Earlier target plan exit 0 and 14 tests passed, but Compose v5.6.1 synthetic configuration exposed an active omitted dependency. Earlier approval was withdrawn; corrected review is separate below. | required | - |
| Corrected launcher review | 82 | W87 | Active optional dependency closure and independent review | Source digest prefix `2d17dd15`, CLI `3d2bd3e7`, tests `1c128b43` | PASS | 18 independent tests and corrected source review passed; later changes require re-review. | required | - |
| CI routing | 85 | W90 | Synthetic routing and workflow contract; independent review | Current P07 CI source | PASS | Five P07 routing tests and independent review passed; complete CI selector remains blocked by existing P03 parity and was interrupted. Manifest required staged recheck. | required | - |
| Document metadata | 85 | W90 | `check-document-metadata.py --mode check-changed` | Default local base and separate explicit `HEAD` retry | CANCELLED | Both runs interrupted with exit 130 after prolonged execution without a result; cause remains unconfirmed. | required | - |
| Expected targets and alert semantics | 83 | W88 | Generated configuration, promtool and selected-target proofs | Assigned observability writer packet | NOT_RUN | Await actual receipts | required | - |
| Candidate rule behavior | 83 | W88 | Pinned promtool rule tests, no network | Synthetic selected targets and failure/recovery inputs | PASS | 13 scenarios, exit 0 and temporary-input cleanup; includes Alloy off/on, progress, missing and recovery. | required | - |
| Independent observability review | 83 | W88 | Review of current source and independent unit tests | Observability module SHA prefix `25b640e0` | PASS | No further blocking findings; independent 10 tests passed. Reviewer did not rerun promtool; writer's 13-scenario evidence is separate. Source path-to-daemon race remains. | required | - |
| Observability coverage | 83 | W88 | Python trace and synthetic tests | Observability module SHA `25b640e094a6b953a98186ce8df25dd38ad00ec154b5be11f2bb5a96874f4d2f` | PASS | 274/311 executable lines (88.1%); 10 unit tests. | required | - |
| Public inventory refresh | 85 | W90 | `workspace-inventory.py scan --connections` and `validate` | Public inputs and retained prior review records | PASS | At the recorded scan: 41,939/41,939 file entries; whole-body 6/2,319 and partial 78/2,319; render 0/17; operation and restore 0/112. Subsequent changed inputs require refresh. | required | - |
| Authenticated OTLP delivery | 84 | W89 | Pinned isolated Alloy/Prometheus test | Owned synthetic fixture only | NOT_RUN | Await actual receipts | required | - |
| Selection and recovery handoff | 85 | W90 | Expected on/off, absent and recovery evidence | Current source and owner assessment | NOT_RUN | Await actual receipts | required | - |

## Criterion Acceptance

The first isolated fixture run exercised Alloy self metrics, counter and
histogram delivery, labels, authentication rejection, identity and replay,
Prometheus interruption and retry, and a new Alloy epoch. It preceded an
identified stderr-reflection correction, so final source needs a new check.
Actual Grafana, trace and log delivery and durable restore remain NOT_RUN.

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 82 | pending | Companion selection | IMPLEMENT_GAP until implemented and reviewed. | SPEC-0212 TSK-0046 |
| 83 | pending | Expected targets and alert semantics | IMPLEMENT_GAP until implemented and verified. | SPEC-0212 TSK-0046 |
| 84 | pending | Authenticated OTLP delivery | REUSE_ACCEPTED only for recorded SPEC-0214 scope; new proof remains separate. | SPEC-0212 TSK-0046 |
| 85 | pending | Selection and recovery handoff | IMPLEMENT_GAP; HOME/reload/remote acceptance remains NOT_RUN. | SPEC-0212 TSK-0046 |

## Review and Completion

Some final local gates remain pending. Actual HOME
operation, alert delivery, operational restore, remote CI and final acceptance
remain NOT_RUN until separately evidenced and authorized.

The observability writer reproduced a workspace-boundary issue: the existing
workspace and `_workspace` directories are group writable. Actual public
`obs-core`/DEV-off plan materialization rejects that path with
`unsafe_output_directory`; a synthetic group-writable directory is also
rejected with permissions unchanged (9 unit tests pass). Independent review
opposed weakening this check because an ancestor can be rebound. The operating
command was not run. Synthetic selection or rule passes do not resolve it.
The candidate now offers a separate protected temporary output under a
root-owned sticky `/tmp`, with UID-owned mode-0700 directories and rejection
of symlinks, preemption or mismatched existing output. An owned host temporary
fixture passed for a synthetic 0775 source root; the sandbox's `/tmp` has a
different owner and was rejected. This does not prove application on the
actual workspace. Temporary cleanup or reboot requires regeneration from a
verified plan before container restart; Compose source group-writer trust and
the path-to-daemon race remain separate limitations.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Workspace inventory](../../../90.references/data/0096-workspace-inventory/README.md)
- [Secret structure Task](tsk-0045-secret-structure-openbao.md)
- [Compose profiles policy](../../../05.operations/policies/01-common/0078-compose-profile-vocabulary.md)
- [Alloy recovery Runbook](../../../05.operations/runbooks/07-observability/0040-alloy.md)
