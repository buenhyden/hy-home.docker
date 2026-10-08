---
title: "Relay Controller and Locust Lifecycle Task"
version: "0.3.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0214-TSK-0002"
parent_ids:
- "SPEC-0214-PLAN-0001"
created: "2026-10-08"
---

# Relay Controller and Locust Lifecycle Task

## Objective

Close the runtime gaps TSK-0001 left open: a tracked per-run relay controller,
a proven path from an isolated target through k6, the relay, the
authenticated Alloy receiver and Prometheus to the dashboard, the relay's
trust boundary, the dashboard's absent-versus-zero rule, and a bounded Locust
LAB lifecycle.

## Inputs and Authorization

The user request on 2026-10-08 asks to execute prompt 02 of the analysis pack
("기존 k6·Locust·OTLP 구현의 운영 연결 완성"), with per-unit commits and a
per-Spec PR merge, HOME runs where possible, and `NOT_RUN` only for steps that
truly cannot run. The pack baseline is
`buenhyden/hy-home.docker@a56ab4e5bac84623735975e9ed79801fd874b9e4`; this work
starts from `main` `194b4eb19` (PR #383). Project-Template `main` is
`6b1c7394f1e08c0ce566f76b4644c2cad9c89891`, equal to the pack baseline. No
real application target or load budget is named, so real-target load stays
`NOT_RUN`.

## Work Log

### Starting State

TSK-0001's accepted evidence and its gaps, checked against the current tree:

| Criterion | TSK-0001 state | Gap at start |
| --- | --- | --- |
| 1, 2 | Manifest v2 and executor peer tests accepted | No tracked way to create the relay; only a test-harness Compose service built one |
| 3 | Isolated metrics harness accepted; k6 ran from Compose, not through the executor | No guard + target + executor + relay run |
| 4 | Locust worker bound accepted | No outer deadline, cancel, crash or worker-loss evidence |
| 5 | HOME, live Grafana `NOT_RUN` | HOME Alloy already ran `config.home.alloy` with the token mounted (4319 answered 401 without a token); no HOME relay run, no live Grafana query |

The HOME token file existed with mode `664`, readable by every local user.

### W5 Relay Controller, Relay Contract and Cancel Cleanup

`infra/11-quality/k6/metrics_relay.py` creates the relay
`hyhome-k6relay-<run>-a<attempt>` with `docker create --pull never`. It
carries the run, attempt and role labels, the controller's UID and GID, a
read-only root filesystem, `--cap-drop ALL`, `no-new-privileges`, 64 PIDs,
0.25 CPU, 256 MiB, a `/tmp` tmpfs and no host ports. It mounts exactly the
tracked `metrics-ingress.alloy` and the token file, both read-only. It joins
the run network with alias `metrics-ingress`, then `docker network connect`
adds the egress network, and it is started and waited on until Alloy's
`/-/ready` answers. A token file that other users can read, that is empty or
that has more than one line is refused. `stop` sends SIGTERM with 10 s to drain
Alloy's export queue and removes the container only if its labels match the
run and attempt. `cleanup` removes containers labelled with the run ID and the
role `metrics-ingress` or `k6-runner`, and nothing else.

The executor now admits a relay only through `metrics_relay.contract`: the
name must be this attempt's relay; the labels, digest image, exact command,
controller user, identity environment, read-only root, no capabilities,
`no-new-privileges`, no ports or extra hosts, exactly the two read-only
mounts, the configuration file's SHA-256 equal to the tracked file, exactly
the run and egress networks, the alias, and an internal bridge egress network
must all hold. `metrics-ingress.alloy` gains a transform that deletes every
producer resource attribute and sets `project.id`,
`deployment.environment.name` and `service.instance.id` from the
controller's environment, plus `service.name=k6`. A prototype confirmed that
Alloy v1.19.2 evaluates the concatenated `sys.env` statements at the default
stability level and that a posted `project.id=evil` leaves as the
controller's value.

On SIGINT or SIGTERM the executor writes `interrupted`, exit 130,
`runner_cancelled` and removes its own runner container; the timeout path uses
the same removal. `quality_run.py run` installs a SIGTERM handler, owns the
relay when given `--relay-image` and `--relay-token-file`, writes
`metrics_ingress_unavailable` if the relay cannot start, and always stops the
relay. `quality_run.py cleanup --run-id` is the crash path.

`test_k6_results`: 27 tests pass. Against the `main` source the suite cannot
import (`metrics_relay.py` does not exist), which is the RED state. New tests
cover 15 relay mutations (published port, writable root, missing
`no-new-privileges`, other image, other command, root user, forged identity,
other role, other attempt, tampered configuration, writable token mount,
extra mount, wrong egress, non-internal egress, missing alias), a foreign
relay name, the controller's create, readiness-failure removal and token
checks, stop and cleanup scoping, executor cancel and CLI cancel.
Commit `bcf77f77a`.

### W6 Dashboard Absent-Versus-Zero Rule

k6 sends `dropped_iterations` only after a drop and `checks` only when a check
exists. The drops target is now
`sum(k6_dropped_iterations_total{…}) or (0 * sum(k6_iterations_total{…}))`,
and the checks panel shows "No checks reported" as its no-value text. A probe
with the executor's CLI shape (1 VU, 20 rps, 3 s, 1000 iterations) reported
985 dropped iterations, so a positive case exists. The new test fails against
the previous dashboard and passes now. Commit `23ffba46e`.

### W7 Relay Egress Network

Root Compose declares `quality_otlp_net` (`10.250.17.0/24`, `internal: true`);
Alloy joins it. No repository file or HOME network used the subnet before.
AD-0026 lists the network, and the m0021 service inventory projection was
re-rendered for the Alloy row. Root render, the operations catalog, 108
`test_compose_baseline_gates`/`test_infra_tier_layout` tests (21 skipped as
before) and the `06-observability` hardening check pass. Commit `d85918212`.

### W8 Locust LAB Supervision

`lab.py run LAB --purpose --lease --deadline [--grace]` starts the project
with `up -d` (no `--wait`, since a short job can finish before it reports
healthy), finds the single container labelled `hy-home.lab.job=true`, waits
for it with `docker wait` bounded by the deadline, and on the deadline or
SIGTERM stops it with `docker stop --time <grace>` before stopping the
project. The ledger records `outcome`, `job_exit_code` and
`deadline_seconds`. The deadline must fit inside the lease. The Locust master
carries the job label; workers do not. Four new `test_lab_controller` tests
and one `test_locust_telemetry` test pass. Commit `d3a6a903b`.

`examples/operations/locust-telemetry/lifecycle.py` ran six cases against the
pinned Locust 2.46.6
(`locustio/locust@sha256:d43616228012a7d79b883e2ecd42f87640469377f2b666c4ab27e5248dfdf35f`)
and WireMock 3.13.2-alpine
(`wiremock/wiremock@sha256:f8c42a38dca3f4a1d7219af11c80438740f39eebb1505b0f029aed743c20e147`),
two workers each, through `lab.supervise`. The final run used `lab.py`
`09acffd82679267ec44642863268091810f1b90c74ac2434d866fe3e24a5afe1`,
`lifecycle.py`
`1423c665d61f89d97c57e2775743a6cda0fdd6812510d3bd7f37eb8578b0e422` and
`labs/locust.yml`
`41ec5df9291e8ac37b356df6147f2eaf622132de4539326f2703d3526f6a2e7b`. Exit 0:

| Case | Outcome | Controller code | Master exit | Workers left at stop | CSV | Requests | Leftovers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| propagated (`--exit-code-on-error 1`) | failed | 1 | 1 | 0 | complete | 180 | 0 |
| completed | completed | 0 | 0 | 0 | complete | 183 | 0 |
| deadline (12 s of 120 s) | deadline_exceeded | 124 | 0 | 0 | complete | 336 | 0 |
| cancelled (SIGTERM at 8 s) | cancelled | 130 | 0 | 0 | complete | 213 | 0 |
| master crash (SIGKILL at 8 s) | failed | 137 | 137 | 2 | last periodic write | 142 | 0 |
| worker drop (SIGKILL one worker) | completed | 0 | 0 | 0 | complete | 295 | 0 |

A run before the review fixes gave the same outcomes and codes.

Findings: a master stopped by SIGTERM writes its CSV and exits 0, so only the
controller code and `outcome` distinguish a deadline or cancel from a
completed run. Losing a worker does not change the master's exit code. After
a master crash both workers keep running until the project is stopped; the
controller stops it. The worker shortage case is TSK-0001 W3 evidence and was
not repeated.

Locust stays in the LAB. The pinned image has no OpenTelemetry SDK, so Locust
OTLP is unsupported and not merged into the k6 path. No named consumer needs
long-term Locust comparison, so no `perf_db` CSV adapter was built (Spec
contract 8).

### W9 Isolated End-to-End Relay Run

`examples/operations/quality-metrics/executor_stage.py` replaces the harness
stage that ran k6 from Compose. It starts the path-guard fixture (Traefik
`traefik@sha256:f86a2cab1b5c649070c49f883c743dd32d8485a56e3368c5f93b9e91f1e91259`
and WireMock) and runs `quality_run.py run` with `--relay-image`
(`grafana/alloy@sha256:b8ec653c44235fbe910879145dac3597d66b0aaecf60bcbbe82580767771a839`),
`--relay-token-file` and the harness's internal network as egress, against
the harness Alloy built from `config.home.alloy` and Prometheus
(`prom/prometheus@sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0`).
k6 is `grafana/k6@sha256:9bd01d6941fca969cb61bb57d2da5ee9b385fe2aa8881df3798c196564d6ace6`.
The scenario checks that `/health` returns 200 and `/unapproved` and
`/__admin/requests` return 404 through the guard, and once posts its own OTLP
with `project.id=forged-project` and instance `forged` to the relay: one
metric named `k6_forged_counter` and one named `outside_counter`.

The final run, after the review fixes below, used `acceptance.py`
`b8484bd2e0d6846e81d6503d353e891b2e7022c3bfa47f65317b33492ba0acfd`,
`executor_stage.py`
`46d34ff1be7b37aabf6504ace01415197ccca838475672663e360274e7d67712`,
`metrics_relay.py`
`99c0408e170d849b75e451d11db5dd62e7ec37fdb471d79be829f5175492b105`,
`metrics-ingress.alloy`
`5f6fcb5383a0d0172f6fa6473d81a0b9ed4126a87811d3255bcae71c68bcc1f8`,
`container_executor.py`
`4227bf534fa53f4b0d82744ed87e9cec0d57b826d373c4f88ac901ad1ba8a249` and
`quality_run.py`
`99950b162a26a8d0b7bfd7d8a19111fe031a200e8d38faeb425c5ec1adf873d6`.
It exited 0. Every earlier synthetic case passed unchanged, including the 401
for a producer without a token. Then:

| Step | Result |
| --- | --- |
| a1: 2 VUs, 20 rps, 20 s, 100000 iterations | `passed`/`complete`; relay and runner gone afterwards |
| Prometheus vs k6 summary (a1) | requests 341 = 341, passing checks 255 = 255, dropped iterations 99915 = 99915 |
| Forged OTLP | stored only as `k6_forged_counter_total{project_id="metrics-rehearsal",instance="<run>-a1"}` = 1; no series with `project_id="forged-project"` or `instance="forged"`; `outside_counter` dropped by the relay |
| Dashboard queries (a1) | 30 of 30 return data, including checks and dropped iterations |
| a2: 3 iterations, no drops | `passed`/`complete`; drops query returns 0; the same query for an absent run returns no data |
| a3: relay with a writable root filesystem | `quality_run.py` exit 2, `isolation_preflight_failed`, no k6 container |
| a4: SIGTERM 3 s after k6 started | exit 130, `runner_cancelled`, runner and relay removed, another run's relay-labelled container untouched |
| `cleanup --run-id` | removed this run's leftover relay only |
| Cleanup | guard fixture, harness project, network and scratch removed; no `hyhome-k6*` container left |

Two runs before the review fixes gave the same results (341 and 337
requests, 30 of 30 queries). One run during the fixes failed: the first
name filter, `^k6_[a-zA-Z0-9_]{1,128}$`, dropped k6 Rate metrics, which k6
exports as `k6_checks.total` and `k6_http_req_failed.total`, so the stored
check count never reached k6's 255. A debug relay showed the dotted names;
the pattern now allows `.` and a static test pins both forms. Commit
`04d111660` and the review-fix commit.

### W10 Documents and Reused Import Evidence

The k6 guide, policy and runbook, the k6 README, the Alloy policy, runbook
and README, the Locust guide, policy and runbook, the Locust LAB README, both
harness READMEs, AD-0026 and this Spec Package describe the relay controller,
the trust boundary, the budgets, the absent-versus-zero rule and the Locust
outcomes.

The import path (prompt item 8) was not re-run. SPEC-0203 TSK-0001
(archived) ran real PostgreSQL with `result_import.py`
`cac5dc97c1a296b11dbaf121eeb5810acb967080b3c6d7e9fd3fe1fe80c1be08`,
`result_inspection.py`
`964b214dcf59b44371fee3b800c1016de77d14a6e9a5d6afb2c3c5f885ccedaa` and
`schema.sql`
`a31a5e80f362f60befa16b4e77d19f51e470b154cd488945c3fc1e8e3dd58bb6`: insert,
exact replay, concurrent claim, conflicting payload, database outage and
restart. The same three files have the same hashes today. Manifest v2 adds
only `telemetry`, which the import envelope does not carry, so that evidence
still covers the importer; the unit tests for replay, conflict, outage and
timeout pass. Loading results after the run, not during it, stays the
default.

### W10 HOME Alloy and HOME Relay Canary

Run on 2026-10-08 from the HOME checkout at merge `f9fd05cae` (PR #384). The
token file `secrets/observability/alloy/quality_otlp_token.txt` was changed
from `664` to `640`; Alloy (UID 473) keeps read access through its
supplementary group 1000, and the relay runs as the file's owner. `docker
compose up -d --no-deps alloy` recreated Alloy, which became healthy on
`edge_net`, `obs_net` and `quality_otlp_net`. `quality_otlp_net` is internal,
`10.250.17.0/24`, with Alloy as its only member. A request without a token to
`alloy:4319` from that network got HTTP 401, and Alloy logged no token error.

`executor_stage.py --home` (`afb201d3b525f803ecf51333cad82463b7c8699e1b79b078aca00982c9558d2f`)
then ran the path-guard target and `quality_run.py run` with the
controller-owned relay, egress `quality_otlp_net` and the HOME token, project
`hyhome-quality-canary`. Exit 0:

| Step | Result |
| --- | --- |
| Run | `passed`/`complete`; relay and runner removed afterwards |
| HOME Prometheus vs k6 summary | requests 337 = 337, passing checks 252 = 252, dropped iterations 99916 = 99916 |
| Forged OTLP | `k6_forged_counter_total` stored under the run's own project and instance only; no forged project or instance series; `outside_counter` dropped |
| Series per attempt | 410 |
| Live Grafana | the provisioned dashboard `infrastructure-k6`, read through the Grafana API, answered 30 of 30 of its own queries through `/api/ds/query` |
| Cleanup | guard fixture, probe and scratch removed; no `hyhome-k6*` or probe container left |

The first canary attempt passed every Prometheus step and then failed to find
the dashboard by the title "k6"; its provisioned title is "k6 Prometheus".
The canary now reads the uid from the tracked dashboard file. The canary's
series stay in HOME Prometheus until the 15-day retention removes them.

With 410 series per attempt and `max_streams` 10000, about 24 attempts can
send within one 5-minute `max_stale` window before streams are dropped.

### Review

An independent read-only review of the branch returned ten findings:

| Finding | Disposition |
| --- | --- |
| `lab.py run` returned before its cleanup when `compose up -d` failed after starting services | Fixed: a start failure records `start_failed` and stops the project; new test RED then GREEN |
| A SIGTERM during `compose up` killed `lab.py run` before any handler existed | Fixed: the handler is installed before anything starts; a cancelled start records `cancelled`, exits 130 and stops the project |
| The relay contract did not check CPU, memory, PIDs, restart policy, entrypoint, extra environment, tmpfs or the token mount | Fixed: all are pinned to what the controller builds, and the token mount must be a private single-line file; nine new mutations RED then GREEN |
| A scenario could post unbounded metric names through the relay | Partly fixed: the relay passes only `k6_` names (dots allowed for Rate metrics) and caps a request at 4 MiB. A scenario can still add `k6_` series within its own run; this residual is documented in Spec contract 10 and GDE-0061, and series quota belongs to the integration package |
| A relay removal failure after the run escaped as a traceback | Fixed: reported as `quality-run: …` with exit 2 |
| `docker create` sat outside the removal guard | Fixed: create is inside the guard; a create interrupted mid-flight can still leave a container, which `cleanup --run-id` removes |
| A cancel during relay start could be recorded as a relay failure | Fixed: a failing removal no longer replaces the original cancel |
| The contract did not check the token mount's source | Fixed with the contract change above |
| GDE-0061 said the relay could reach only Alloy 4319 | Fixed: the guide now says the network membership is an operating rule, the executor checks only that the network is internal, and the hashed relay configuration sends only to 4319 |
| A `docker stop` timeout in `supervise` escaped as a traceback | Fixed: the timeout is absorbed and the project is still stopped |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Relay contract and controller | 6 | W5 | `test_k6_results` RED (missing module, then nine review mutations) then 28 GREEN | Working tree | PASS | W5 Relay Controller, Relay Contract and Cancel Cleanup | accepted |
| Dashboard absent vs zero | 6 | W6 | New dashboard test RED then GREEN; k6 drop probe | Pinned k6 digest | PASS | W6 Dashboard Absent-Versus-Zero Rule | accepted |
| Egress network | 9 | W7 | Render, catalog, compose tests, hardening | Working tree | PASS | W7 Relay Egress Network | accepted |
| Locust lifecycle | 8 | W8 | Unit tests incl. start failure and cancelled start; `lifecycle.py` six cases | Pinned Locust and WireMock digests | PASS | W8 Locust LAB Supervision | accepted |
| Isolated end-to-end relay | 7 | W9 | `acceptance.py` with the executor stage | Pinned Alloy, Prometheus, Python, k6, Traefik, WireMock digests | PASS | W9 Isolated End-to-End Relay Run | accepted |
| Import path | 5 | W10 | Hash comparison with SPEC-0203 real-PostgreSQL evidence; unit tests | Same importer, inspection and schema bytes | PASS | W10 Documents and Reused Import Evidence | accepted |
| HOME Alloy on `quality_otlp_net` and HOME relay canary | 9 | W10 | Alloy recreation; 4319 without token; `executor_stage.py --home`; live Grafana API | Merged `f9fd05cae`; HOME 2026-10-08 | PASS | W10 HOME Alloy and HOME Relay Canary | accepted |
| Real application target load | 5 | W10 | Approved target run | No approved target | NOT_RUN | Inputs and Authorization | pending |

## Review and Completion

Source, static, isolated and HOME work is complete: HOME Alloy joined
`quality_otlp_net`, and a HOME relay canary reached HOME Prometheus and the
live Grafana dashboard. Real application target load stays `NOT_RUN` without
an approved target, and per-project producer credentials, a server-enforced
project label, token rotation and quota stay with the integration package.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [TSK-0001](tsk-0001-quality-k6-locust-and-otel-semantics.md)
