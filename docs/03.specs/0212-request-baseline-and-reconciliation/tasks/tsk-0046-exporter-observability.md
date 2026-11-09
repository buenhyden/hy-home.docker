---
title: "Exporter and Observability Contracts Task"
version: "0.1.7"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-09"
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

### D08 HOME alert census and selection rule (2026-11-08)

A read-only census of HOME Prometheus on 2026-11-08 found 38 active targets,
30 up and 8 down. All eight are DNS failures of services HOME does not run:
the Kafka broker, Connect, Schema Registry and exporter, OpenSearch, and the
three dedicated Valkey exporters. Six alerts fired since Prometheus restarted
on 2026-11-07 18:55 UTC: `ObservationSelectionMissing`,
`ObservationSelectionInvalid`, `OpenBaoAgentAuthFailure` and three
`ContainerHighThrottleRate`. Alertmanager delivered them to Slack (50
notifications, 0 failed).

`ObservationSelectionMissing` is correct: Prometheus runs from
`docker-compose.yml` alone, without the selector overlay that carries the
`hyhome_expected_*` rules, so the down targets cannot be told apart from
intended absences. Clearing it needs a selector start of Prometheus, a separate
HOME change. `ObservationSelectionInvalid` was a rule defect: with no
selection, `scalar(hyhome_expected_jobs_total)` is NaN and `0 != NaN` is
true, so one missing selection raised two alerts. The count and coverage terms
now require `hyhome_expected_selection_info`; the promtool case
`no-selection-marker` expects no `ObservationSelectionInvalid` and failed
before the change, and the existing invalid-selection case still fires.

The extra alerts mattered: `OpenBaoAgentAuthFailure` reflects an Agent that
has not authenticated since it started on 2026-11-02 07:20 UTC (`no known
secret ID`, 2,035 failures, the RUN-0103 restart case). Its recovery is the
owner's RUN-0103 `agent-restart` and is recorded with the secret owner, not
here.

### D08 selector and COMPOSE_FILE (2026-11-08)

Planning a HOME selector start to clear `ObservationSelectionMissing` showed
that `compose_start.execute_plan` always passed `-f docker-compose.yml` (plus
the observation overlay). An explicit `-f` makes `docker compose` ignore the
root `.env` `COMPOSE_FILE`, which since 2026-11-08 pins the n8n Valkey ACL and
Ollama overlays. A selector `up` would have recreated `mng-valkey` without the
named `n8n` user and `n8n-worker` without its Ollama network. With the owner's
choice, the selector now reads `COMPOSE_FILE` from the root `.env` only (a
process `COMPOSE_FILE` stays untrusted, as before), requires
`docker-compose.yml` first, refuses absolute, `..`, duplicate or missing
entries, records the list as `compose_files`, hashes each overlay into the
plan inputs and passes them as `-f` in order before the observation overlay.
Three tests failed before the change and pass after; a changed overlay after
planning refuses execution. A live plan reads the three HOME files. A target
plan selects only the targeted jobs, so the HOME apply uses `--selection HOME`
after a `docker compose --dry-run` of its recreations.

### D08 Alloy 4319 and quality metrics on HOME (2026-11-08)

**T04 source state.** The running `alloy` (`grafana/alloy:v1.20.1`) mounts
`config.home.alloy`, listens on 4317, 4318 and 4319, sits on
`quality_otlp_net`, and its remote write reports 0 failed samples. No source
gap was found, so the HOME path is reused as is. Without a token and with a
wrong token, a POST to `127.0.0.1:4319/v1/metrics` inside the container
returned `401 Unauthorized`. Before the canary, Prometheus held no `k6_*`
series.

**HOME canary.** With owner approval, `examples/operations/quality-metrics/executor_stage.py --home` ran with the
cached pinned images: k6 `9c2dee7f…`, Traefik `f86a2cab…`, WireMock
`f8c42a38…`, Alloy `2aa2099a…`, Python `79e7a9b9…`.

- **First run, 11:58Z: FAIL.** The executor stopped with `relay did not become
  ready`, exit 2. The guard fixture and run containers were removed. The relay
  was then started separately four times: by hand, under the run's CPU and
  memory limits, through `metrics_relay.start()` on throwaway networks, and
  with `quality_otlp_net` as egress. It was ready each time, in 9 seconds at
  0.25 CPU and 40 MiB. The real token file is owned by the relay's
  UID/GID 1000:1000 with mode 640. The cause of the first failure is UNKNOWN.
  A full test suite ran on the same host at the same time, but the load was 7
  on 12 cores.
- **Second run, 12:06Z: PASS.** A watcher recorded the relay's state and
  logs. The relay was healthy within about 5 seconds.
  - Prometheus received the counts from the k6 summary for instance
    `2cd96f3c-…-a1` and project `hyhome-quality-canary`:

    | Series | Value |
    | --- | --- |
    | `k6_http_reqs_total` | 337 |
    | `k6_checks_total{condition="nonzero"}` | 252 |
    | `k6_dropped_iterations_total` | 99916 |

  - The relay replaced the forged project and instance labels and dropped a
    name that does not start with `k6_`. One attempt produced 410 series.
  - All 30 of 30 queries on the live Grafana dashboard `infrastructure-k6`
    returned data.
  - The relay, runner, guard fixture, probe and scratch files were removed,
    and no `hyhome-k6relay-*` or `quality-relay-*` container remains.

**T05.** The metric sources were counted in Prometheus:

| Source | Series |
| --- | --- |
| Hermes | 14 |
| n8n | 212 |
| Airflow | 526 |
| GPU | 15 |
| Disk (`node_filesystem_avail_bytes`) | 7 |

`node_textfile_scrape_error` is 0. The Hermes labels are only `job_kind`,
`outcome` and `blocked_reason`, and the outcomes `blocked`, `conflict`,
`gateway_error` and `submitted` stay distinct, with no URL or personal ID in
any label. Two items are still open:

- **Hermes E11 alert:** firing and resolution are not yet observed. This waits
  for the D05 E9 run on 2026-11-09 08:00 KST.
- **Locust:** the LAB scope check was not run, and no LAB runtime was started.

### D08 HOME selector start after #828 (2026-11-08)

**Plan and drift.** On `main` `56dca2a34`, the plan with `--selection HOME
--dev-data-expected off` read all three HOME `COMPOSE_FILE` entries and listed 45
targets. A dry run of the exact command `up` uses showed 25 recreates, among
them `openbao`, `openbao-agent`, `mng-pg`, `qdrant`, the four `seaweedfs`
containers, `registry`, Airflow and Prometheus. For every one of them, the
stored `com.docker.compose.config-hash` differed from the current render, so
merged changes from 11-06 and 11-07, such as shared reservations and network
binds, had never been applied. The owner chose the full HOME start (option A)
over a Prometheus-only `obs-core` start or a deferral.

**Run, 13:04Z to 13:09Z: START_FAILED.**

- **Wrong plan path.** The first `up` returned `BLOCKED`, because `up` only
  reads a plan under `_workspace/repo-support/analysis/p07/plans/`.
- **Second `up`.** It recreated 25 containers and returned `START_FAILED`
  with `recovery_required`. OpenBao came back sealed, and its unhealthy
  health check kept the dependents at `Created`.
- **Prometheus restart loop, exit 64.** The plan declared
  `P07_DECLARED_DEV_EXPECTED=off`, while HOME `.env` sets
  `PROMETHEUS_DEV_DATA_EXPECTED=on`, and `dev-pg` and `dev-valkey` are
  running. Planning with `off` was the operator's error in this session.

**Recovery.**

- `docker compose up -d --no-deps` started Prometheus without the overlay, as
  before the run, plus the mng-pg helpers, `grafana-db-provision`, the seaweedfs
  volume, filer and buckets, and six Airflow services. `airflow-init` exited 0.
- `seaweedfs-buckets` first exited 254 with `InternalError`, because the
  filer was not ready yet. It was rerun, found all four buckets present and
  exited 0.
- Every container is healthy except `openbao`, which stays sealed and waits
  for the owner, and `openbao-agent`, which stays `Created` for RUN-0103
  `agent-restart`.

**OpenBao.** The owner unsealed the server, which was unsealed at 13:24:15Z.
The owner then ran RUN-0103 `agent-restart`, with the same inputs as the
morning recovery recorded in SPEC-0204 TSK-0006. It printed `issue rc=0` and
`agent: healthy`, and the rendered files had the expected modes, exit 0.

- **Agent.** It started at 13:31:56Z and logged `authentication successful`
  and `renewed auth token`, with no error.
- **Scrape targets.** `openbao` and `openbao-agent` are both `up`.
- **Containers.** Every one is healthy. The compose config hash of every
  running container equals the current render: no drift is left.
- **Pending-token alert.** `OpenBaoTooManyPendingTokens` is pending again
  from the two five-minute tokens. The windowed rule from #830 releases it
  once they leave the 15-minute window.

**Selector gap.** POL-0078 keeps `dev-data` out of HOME, so a HOME plan accepts
only `--dev-data-expected off`, and the existing test treats `on` as invalid.
On HOME, though, DEV data is running and `.env` declares `on`, so no current
selector input can start Prometheus with the selection overlay. The owner must
choose one of two fixes:

- extend POL-0078 so that HOME can name `dev-data` when it is declared `on`;
- stop DEV data and declare `off`.

`ObservationSelectionMissing` keeps firing until then.

### D08 container throttle alerts (2026-11-09)

After the selector start, `ContainerHighThrottleRate` fired for
`airflow-triggerer`, `crawl4ai-egress`, `node-exporter` and `openbao-agent`.
The throttle ratio of the first three was 0.5 to 0.68 for the four days
Prometheus holds, so the alert is not new: the Prometheus restart only reset
its state. `openbao-agent` read 0 while it could not authenticate and 0.32
since. Each container's own healthcheck runs inside its CPU limit, and one
burst against a fractional limit throttles most of the few periods it runs in.
Measured on HOME:

- `airflow-triggerer` (0.5 CPU): `airflow jobs check` used 5.8 CPU-seconds and
  ran 10 seconds of every 15. Throttling withheld 0.23 CPU-second per second,
  a real cost. `airflow-dag-processor` runs the same check every 15 seconds
  under 2 CPUs and lost 0.06.
- `node-exporter` (0.5 CPU): the healthcheck fetched `/metrics`, a full
  collection, next to the scrape; scrapes took up to 2.4 seconds and
  throttling withheld 0.06.
- `crawl4ai-egress` and `openbao-agent`: 0.007 and 0.003 withheld, which is
  alert noise.

The fix keeps every limit. Both Airflow checks run every 60 seconds, which cuts
their cost by three quarters, and the node-exporter healthcheck fetches the
landing page `/`, which proves the listener without running a collector. The
rule also requires 0.1 CPU-second per second withheld, so a short burst no
longer fires it while a container starved under load still does. The HOME
apply of these changes is a separate approved step.

### D08 HOME selection with DEV data (2026-11-09)

The owner chose the first fix for the selector gap on 2026-11-09: POL-0078
1.15.0 lets a HOME plan add `dev-data` when it declares
`--dev-data-expected on`, the value root `.env` already holds. `create_plan`
adds the profile only in HOME mode with `on`; `off`, profile and target plans
are unchanged. A read-only HOME plan on the current checkout lists 50 targets
with `on`, the 45 HOME targets plus `dev-pg`, `dev-pg-exporter`,
`dev-pg-monitor-provision`, `dev-valkey` and `dev-valkey-exporter`, and 45
with `off`. Starting Prometheus through the selector, which clears
`ObservationSelectionMissing`, is a separate approved HOME step after merge.

### D08 HOME apply and Hermes run (2026-11-09)

With owner approval, plan `977274558bea` (HOME, DEV data `on`, 50 targets)
ran on `main` `b329bbe9d`. The first `up` returned `START_FAILED`:
`dev-pg-monitor-provision` exited 3 on
`monitor_cross_database_connect_requires_cluster_review`, because `template1`
still granted `CONNECT` to `PUBLIC`, and `dev-pg-exporter` stayed `Created`
until it was started directly. The owner approved
`REVOKE CONNECT ON DATABASE template1 FROM PUBLIC` on `dev-pg`; the second
`up` of the same plan returned `STARTED` and the job exited 0.

The owner also approved recreating six containers outside the HOME selection.
`dozzle`, `redisinsight`, `storybook` and `storybook-mcp` were recreated from
local images. `crawl4ai` moved from 0.9.4 to the repository-pinned 0.9.5 after
a pull of the pinned digest, together with `crawl4ai-egress`. A later dry run
of the plan and of the six containers recreates nothing, and every container
is healthy. OpenBao was not recreated. `hyhome_expected_selection_info` is 1,
`ObservationSelectionMissing` no longer fires, and no
`ContainerHighThrottleRate` fired in the first half hour; a longer window
remains unobserved.

The 08:00 KST Hermes run delivered `business_ideas` and `news`; `devops` was
not delivered. Each job's first submission was refused as `source_quality`,
which the metric counts as `gateway_error`, and the other two succeeded on
retry. The `devops` retry used a path the tool refused
(`report_path_not_allowed`, the `blocked` outcome), and its next submission
timed out after 15 seconds (`delivery_uncertain`, Traefik 499). n8n execution
128 for that request was cancelled by the workflow's 30-second
`executionTimeout`. The worker registered a new JS Task Runner during that
execution and the launcher then reported it unresponsive, so a task runner cold
start is the likely cause, not a proven one; the next execution finished in 3.8
seconds. `HermesResearchBlocked` fires for `devops`, which observes E11 firing;
its resolution waits for the next successful `devops` run.

### D08 reboot test (2026-11-09)

The owner rebooted the host at 12:49 KST after the backup and the MLflow pilot
finished, then unsealed OpenBao. Four defects showed up during recovery:

- **Prometheus overlay lost.** The selector wrote the plan-bound
  `prometheus.yml` and `selection.yml` under `/tmp/hyhome-p07-<uid>/`. The
  reboot cleared `/tmp`, and Docker bound an empty root-owned directory in each
  file's place, so Prometheus looped on `is a directory` (26 restarts). The plan
  could not be rebuilt at the old path: #842 had removed ComfyUI from HOME,
  which changed the fingerprint from `977274558bea` to `393c7c24bf4b`. The owner
  asked for a folder inside the user's home instead of `/tmp`, and not the
  `_workspace` selections path, which is due for deletion. The selector now
  writes to `~/.local/share/hy-home/p07/<fingerprint>`. Every step from `/` to
  that folder is owned by root or the user and is not group-writable;
  `~/.local/state` (mode 775) would have failed the existing check.
- **`mng-pg` not shut down cleanly.** Its last clean checkpoint was 03:43:52Z.
  Crash recovery spent about 24 minutes syncing the data directory under
  saturated I/O, and dependent services restarted until 13:15 KST. Cause of the
  unclean stop: not yet investigated.
- **OpenBao did not come back.** It sealed at shutdown and exited 255. Its
  `unless-stopped` policy did not restart it at boot, unlike the assumption in
  RUN-0098. It was started by hand. Cause: not yet investigated.
- **`agent-restart` blocked by I/O.** The issuer helper failed in `prepare`,
  before any server write. The audit log shows only the two token lookups, and
  the journal ended `rolled_back`. A throwaway container of the same kind took
  52 s, above the helper's 20-second command limit. The Agent stays stopped
  until container starts settle.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and ownership | 82 | W87 | Git status and public documentation fingerprints | Clean 169c1b62f9a29738dde587b584418f9e93b78029 | PASS | Inputs and Authorization; Single-writer leases | required | - |
| D08 Airflow direct-start companions | 82 | W87 | `compose-start.py plan --target` membership and `test_compose_start` RED then GREEN | POL-0078 companion table; `main` `2f86dd9e3` | PASS | Scheduler, triggerer and dag-processor plans lacked `airflow-statsd-exporter` before; each now adds only the exporter; apiserver and worker plans unchanged at 7 targets | required | - |
| D08 HOME alert census | 83 | W88 | Read-only Prometheus targets, alerts and Alertmanager counters | HOME Prometheus and Alertmanager, 2026-11-08 | FAIL | 8 of 38 targets down (unselected services); 6 alerts firing incl. a doubled selection alert and a 6-day OpenBao Agent auth failure; Slack delivery 50/0 | required | - |
| D08 selection rule guard | 83 | W88 | promtool `rules.test.yml` RED then GREEN with the running Prometheus image | `alert_rules.local.selection.yml` | PASS | `ObservationSelectionInvalid` no longer fires without a selection; the invalid-selection case still fires | required | - |
| D08 selector COMPOSE_FILE binding | 82 | W87 | `test_compose_start` RED then GREEN and a live read-only plan | Root `.env` `COMPOSE_FILE`; `compose_start.py` | PASS | 3 new tests fail before and pass after (24 OK); live plan lists `docker-compose.yml` and both HOME overlays with hashes | required | - |
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
| HOME OTLP canary | 84 | W89 | `executor_stage.py --home` through relay, HOME Alloy 4319, Prometheus and Grafana | Pinned cached images; project `hyhome-quality-canary` | FAIL | First run 11:58Z: relay not ready, exit 2; cleanup passed; cause UNKNOWN. See D08 Alloy 4319 and quality metrics on HOME. | required | - |
| HOME OTLP canary rerun | 84 | W89 | `executor_stage.py --home` through relay, HOME Alloy 4319, Prometheus and Grafana | Pinned cached images; project `hyhome-quality-canary` | PASS | Second run 12:06Z: summary counts equal in Prometheus (337 requests), forged identity replaced, 30/30 dashboard queries return data, cleanup passed. | required | HOME OTLP canary |
| HOME 4319 denial | 84 | W89 | POST without token and with a wrong token inside `alloy` | Live HOME receiver | PASS | Both `401 Unauthorized`. | required | - |
| HOME selector start | 85 | W90 | `compose-start.py up --plan` of `--selection HOME` after a matching dry run | Plan `c7a311e7…`, `main` `56dca2a34` | FAIL | START_FAILED: sealed OpenBao held dependents; Prometheus exit 64 on DEV `off` against `.env` `on`. See D08 HOME selector start after #828. | required | - |
| HOME selector recovery | 85 | W90 | Plain `up -d --no-deps` of stopped and looping containers, owner unseal and RUN-0103 `agent-restart`; health and config-hash census | Same `main`; containers listed in the section | PASS | All containers healthy, Agent authenticated, no config-hash drift; `ObservationSelectionMissing` stays until the owner decides the DEV gap. | required | - |
| Throttle alert census | 83 | W88 | Read-only Prometheus queries: throttle ratio over 4 days, throttled seconds, CPU, scrape duration; healthcheck timing | HOME Prometheus and containers, 2026-11-09 | PASS | Cause found: in-container healthchecks; see D08 container throttle alerts. | required | - |
| Throttle rule and healthcheck cost | 83 | W88 | promtool `container-throttle-alerts.test.yml` and `test_compose_baseline_gates` RED then GREEN | `alert_rules.local.infra.yml`; Airflow and observability Compose files | PASS | Old rule fired for the bursty case and the interval test failed before; both pass after; 145 tests OK, 31 skipped. | required | - |
| Throttle CI candidate quality | 83 | W88 | GitHub `candidate-quality` on #833 | Run 42530532757 | FAIL | `ci-gate-adapter-tests-skipped`: the promtool test skipped without its image inside an undeclared class. | required | - |
| Throttle CI skip declaration | 83 | W88 | GitHub `candidate-quality` on #833 | `ContainerThrottleAlertNativeTests` declared in `.github/workflow-contract.yml`; count 33 | PASS | Local replay with `docker` hidden: the test skips and the adapter skip validator passes; 193 tests OK. | required | Throttle CI candidate quality |
| HOME DEV-data selection | 85 | W90 | `test_compose_start` RED then GREEN and read-only HOME plans | POL-0078 1.15.0; `compose_start.py` | PASS | HOME with `on` failed `dev_state_conflict` before; 25 tests OK after; live plans 50 targets (`on`) and 45 (`off`). | required | - |
| HOME DEV-data start | 85 | W90 | `compose-start.py up --plan` of HOME with DEV data `on` | Plan `977274558bea`, `main` `b329bbe9d` | FAIL | START_FAILED: monitor provisioning refused while `template1` granted PUBLIC connect. | required | - |
| HOME DEV-data start rerun | 85 | W90 | `compose-start.py up --plan` of HOME with DEV data `on` | Same plan after the owner-approved `template1` revoke | PASS | STARTED; provisioning exit 0; later dry run recreates nothing; selection marker 1. | required | HOME DEV-data start |
| Non-HOME container recreate | 85 | W90 | Compose recreate and dry run of six named containers | Current source; pinned crawl4ai 0.9.5 | PASS | All six healthy; dry run recreates none. | required | - |
| Hermes scheduled run alert | 83 | W88 | Hermes log, n8n log, Traefik log and Prometheus alert readback | 2026-11-09 08:00 KST run | FAIL | `devops` undelivered: n8n execution 128 hit its 30-second timeout; `HermesResearchBlocked` firing; resolution unobserved. | required | - |
| Reboot: Prometheus overlay | 85 | W90 | Container log and mounts after the 2026-11-09 reboot | Plan `977274558bea` overlay under `/tmp` | FAIL | `/tmp` cleared; Docker bound empty root-owned directories; 26 restarts on `is a directory`. | required | - |
| Persistent overlay path | 85 | W90 | `tests.lib.ops.test_compose_observation` and `test_compose_start` | Overlay root `~/.local/share/hy-home/p07` | PASS | 35 tests OK; a group-writable step under home is refused; the real home is untouched. | required | - |
| Reboot: OpenBao Agent restart | 85 | W90 | RUN-0103 `agent-restart` and audit readback | Issuer `4f2e7f9b`, journal `rolled_back` | FAIL | Helper sink container exceeded 20 s under I/O pressure (52 s measured); no server write. | required | - |

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
