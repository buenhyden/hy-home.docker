---
title: "Relay Controller and Locust Lifecycle Task"
version: "0.1.0"
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
two workers each, through `lab.supervise`. Exit 0:

| Case | Outcome | Controller code | Master exit | Workers left at stop | CSV | Requests | Leftovers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| propagated (`--exit-code-on-error 1`) | failed | 1 | 1 | 0 | complete | 180 | 0 |
| completed | completed | 0 | 0 | 0 | complete | 180 | 0 |
| deadline (12 s of 120 s) | deadline_exceeded | 124 | 0 | 0 | complete | 346 | 0 |
| cancelled (SIGTERM at 8 s) | cancelled | 130 | 0 | 0 | complete | 227 | 0 |
| master crash (SIGKILL at 8 s) | failed | 137 | 137 | 2 | last periodic write | 156 | 0 |
| worker drop (SIGKILL one worker) | completed | 0 | 0 | 0 | complete | 314 | 0 |

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
with `project.id=forged-project` and instance `forged` to the relay.

The final run used `acceptance.py`
`b8484bd2e0d6846e81d6503d353e891b2e7022c3bfa47f65317b33492ba0acfd`,
`executor_stage.py`
`c18a0ebd002115afe462ba910193c0c8f647a04c67d842e3794a0e0acc6675d9`,
`metrics_relay.py`
`83cb9f9d0aa57414959fa43b6a0bec966a935ffb1531a3dd8e8c3b916d19cacb`,
`metrics-ingress.alloy`
`bf4479f829c51f0c5a9c039bac373954e10dd5fb6c9fc8f7a7fb4818a3ee245c`,
`container_executor.py`
`4227bf534fa53f4b0d82744ed87e9cec0d57b826d373c4f88ac901ad1ba8a249` and
`quality_run.py`
`1d0c542e54cc59b82dcb5bf473280087df1ded4a98e5d8a60b738f98eafef660`.
It exited 0. Every earlier synthetic case passed unchanged, including the 401
for a producer without a token. Then:

| Step | Result |
| --- | --- |
| a1: 2 VUs, 20 rps, 20 s, 100000 iterations | `passed`/`complete`; relay and runner gone afterwards |
| Prometheus vs k6 summary (a1) | requests 337 = 337, passing checks 252 = 252, dropped iterations 99916 = 99916 |
| Forged OTLP | stored only as `forged_counter_total{project_id="metrics-rehearsal",instance="<run>-a1"}` = 1; no series with `project_id="forged-project"` or `instance="forged"` |
| Dashboard queries (a1) | 30 of 30 return data, including checks and dropped iterations |
| a2: 3 iterations, no drops | `passed`/`complete`; drops query returns 0; the same query for an absent run returns no data |
| a3: relay with a writable root filesystem | `quality_run.py` exit 2, `isolation_preflight_failed`, no k6 container |
| a4: SIGTERM 3 s after k6 started | exit 130, `runner_cancelled`, runner and relay removed, another run's relay-labelled container untouched |
| `cleanup --run-id` | removed this run's leftover relay only |
| Cleanup | guard fixture, harness project, network and scratch removed; no `hyhome-k6*` container left |

An earlier run of the same stage before a refactor gave the same results
(341 requests, 99915 dropped, 30 of 30 queries). Commit `04d111660`.

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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Relay contract and controller | 6 | W5 | `test_k6_results` RED (missing module) then 27 GREEN | Working tree | PASS | W5 Relay Controller, Relay Contract and Cancel Cleanup | accepted |
| Dashboard absent vs zero | 6 | W6 | New dashboard test RED then GREEN; k6 drop probe | Pinned k6 digest | PASS | W6 Dashboard Absent-Versus-Zero Rule | accepted |
| Egress network | 9 | W7 | Render, catalog, compose tests, hardening | Working tree | PASS | W7 Relay Egress Network | accepted |
| Locust lifecycle | 8 | W8 | Unit tests; `lifecycle.py` six cases | Pinned Locust and WireMock digests | PASS | W8 Locust LAB Supervision | accepted |
| Isolated end-to-end relay | 7 | W9 | `acceptance.py` with the executor stage | Pinned Alloy, Prometheus, Python, k6, Traefik, WireMock digests | PASS | W9 Isolated End-to-End Relay Run | accepted |
| Import path | 5 | W10 | Hash comparison with SPEC-0203 real-PostgreSQL evidence; unit tests | Same importer, inspection and schema bytes | PASS | W10 Documents and Reused Import Evidence | accepted |
| HOME Alloy on `quality_otlp_net` and HOME relay canary | 9 | W10 | `executor_stage.py --home`; live Grafana API | Merged source | NOT_RUN | Review and Completion | pending |
| Real application target load | 5 | W10 | Approved target run | No approved target | NOT_RUN | Inputs and Authorization | pending |

## Review and Completion

Source, static and isolated work is complete. HOME Alloy recreation, the HOME
relay canary and the live Grafana query run after the merge and are recorded
here. Real application target load stays `NOT_RUN` without an approved target.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [TSK-0001](tsk-0001-quality-k6-locust-and-otel-semantics.md)
