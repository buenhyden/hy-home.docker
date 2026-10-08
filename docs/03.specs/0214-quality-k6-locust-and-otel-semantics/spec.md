---
title: "Quality Load Tools and OTel Metric Semantics"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0214"
parent_ids:
- "REQ-0007"
- "REQ-0010"
- "AD-0006"
- "AD-0009"
- "ADR-0047"
created: "2026-10-07"
---

# Quality Load Tools and OTel Metric Semantics

## Overview

Keep k6 as the default load tool and Locust as a standalone LAB, as ADR-0047
decides. Preserve the existing `hyhome.quality-run/v1` contract, isolated
executor, strict artifacts, idempotent import and object store. Add one
authenticated live-metrics path from k6 to the existing Alloy and Prometheus,
and keep metric identities intact through temporality conversion. Fix the
Locust worker-count and deadline gaps. Version 0.2.0 adds the tracked relay
controller, the relay's identity override and egress network, the
absent-versus-zero dashboard rule, the Locust LAB supervisor and the operating
budgets of the metrics path.

## Scope

Included: the k6 manifest telemetry field and its compatibility rule, the
executor's OTLP ingress peer, the HOME Alloy quality receiver and transform,
the isolated metrics acceptance harness, the Locust LAB worker and deadline
inputs, and the documents that operate them.

Version 0.2.0 adds the per-run relay controller and its cancel and cleanup
paths, the internal `quality_otlp_net` egress network, the Locust job
supervisor in `scripts/operations/lab.py`, and the HOME relay run against the
real Alloy receiver.

Excluded: real application targets and load budgets, per-project producer
credentials, server-enforced project labels, token rotation and quota (owned
by the integration package, prompt 04 and SPEC-0204), a `perf_db` hypertable
without a named query consumer, a Locust CSV importer without a named
consumer, and Locust OpenTelemetry, which the pinned image cannot export.

## Contracts

1. k6 is the default generator. Locust runs only from `labs/locust.yml` for
   Python or protocol needs. WireMock simulates dependencies and is not a load
   generator. No CPU or latency benchmark is claimed between the tools.
2. `hyhome.quality-run/v2` adds one required `telemetry` object whose `mode`
   is `none` or `otlp`. v1 manifests remain valid and mean `none`. Any other
   key, an unknown mode or an endpoint supplied by the manifest is rejected.
   CLI and environment input cannot bypass manifest validation.
3. With `otlp`, the executor admits exactly one more approved peer on the
   internal quality network, the metrics ingress. It sets the k6 OTLP endpoint,
   protocol, bearer header and resource attributes itself from the validated
   manifest, and the scenario cannot override them. The run fails before
   traffic if the ingress peer contract does not hold.
4. HOME Alloy accepts quality metrics only on an authenticated OTLP receiver
   that is not published to the host. The public trace receiver no longer
   feeds metrics. Before delta-to-cumulative conversion the transform keeps
   the project, environment and service labels plus the bounded k6
   attributes `condition`, `expected_response`, `method`, `status`,
   `scenario` and the producer instance. It drops request names, URLs and
   every other attribute. Prometheus keeps the same label set.
5. Rate `condition` values and producer instances remain separate series.
   Counters, histograms, replay, outage and restart keep the existing tested
   semantics. Percentiles are not averaged.
6. Locust worker replicas and `--expect-workers` derive from one input.
   `--expect-workers-max-wait` bounds the wait, and a run that cannot reach the
   expected count exits non-zero without starting load.
7. The shared k6 Grafana dashboard reads the OTLP shape that reaches
   Prometheus: `k6_` names, run attempt as `instance`, millisecond histograms
   through `histogram_quantile` and the failure ratio from the `condition`
   counter. Panels that need URL or check names, which are dropped as
   unbounded, are replaced or removed.
8. Run, attempt, verdict, artifact and checksum records stay relational. A
   `perf_db` time-series table is added only for a named query consumer, with
   its time axis, precision, unique key, retention and replay rules decided
   first.

9. `metrics_relay.py` is the only tracked way to create a relay. It names the
   relay after the run and attempt, labels it with the run ID, attempt and
   role, runs a digest-pinned `grafana/alloy` image as the controller's user
   with a read-only root filesystem, no capabilities, `no-new-privileges`, no
   host ports and bounded CPU, memory and PIDs, mounts only the tracked relay
   configuration and the token file read-only, and joins exactly the run
   network (alias `metrics-ingress`) and one egress network. The token file
   must be private to its owner. The executor admits a relay only if every one
   of these properties, the configuration hash and an internal egress network
   hold.
10. The relay replaces every producer resource attribute with the run's
    project, environment and `<run_id>-a<attempt>` instance, which it receives
    from the controller. A scenario that posts its own OTLP cannot claim
    another project or run. One shared bearer token authenticates every relay
    to HOME Alloy, so any holder of the token can still claim any project;
    per-project credentials, a server-enforced project label, rotation and
    quota remain with the integration package.
11. `quality_otlp_net` (10.250.17.0/24) is internal and holds only Alloy and
    the relays the controller attaches.
12. Cancel (SIGINT or SIGTERM), timeout and relay failure write an
    `interrupted` exit record and remove only containers that carry this
    run's labels: the attempt's k6 runner and its relay. `quality_run.py
    cleanup --run-id` removes a crashed run's leftovers and nothing else.
13. The k6 dashboard shows 0 dropped iterations when a run reported iterations
    and none dropped, no data when the run is absent, and "No checks
    reported" instead of a 0% check rate when no check exists.
14. `lab.py run` starts a job LAB, waits for its single `hy-home.lab.job`
    container within a deadline that fits the lease, stops that container
    with a grace period at the deadline or on SIGTERM so Locust can write its
    CSV, always stops the project, and returns the job's exit code, 124 for
    the deadline or 130 for a cancel. Locust results stay file-based.
15. The metrics path has stated budgets: the remote-write `sample_age_limit`
    of 5 minutes, the delta-to-cumulative `max_stale` of 5 minutes and
    `max_streams` of 10000, Prometheus' default 15-day retention, and a
    per-attempt series count measured on a real run.

## Acceptance Criteria

1. v1 and v2 manifests validate as specified, and invalid telemetry input is
   rejected by unit tests.
2. Executor unit tests prove the OTLP peer contract, the injected environment
   and rejection before traffic.
3. The isolated metrics harness shows separate `condition` and instance series,
   rejects an unauthenticated producer, keeps the existing temporality,
   histogram, replay, outage and restart results, and answers the dashboard's
   own queries from real k6 output.
4. The Locust LAB renders one worker input for replicas and expected workers,
   and an isolated run with too few workers exits non-zero within the bound.
5. Configuration, documents and the Task agree on what was observed, and
   HOME, real-target load and live Grafana stay `NOT_RUN` unless observed.
6. Unit tests prove the relay contract, the controller's create, readiness,
   stop and cleanup behaviour, and cancel handling; they fail against the
   0.1.0 source.
7. An isolated run goes from a path-guarded WireMock target through k6, the
   controller's relay and the authenticated Alloy receiver to Prometheus. The
   stored request, check and dropped-iteration counts equal k6's own summary,
   the dashboard queries return data, a forged identity never reaches
   Prometheus, a non-conforming relay and unapproved paths are refused, and
   cancel and run-scoped cleanup remove only their own containers.
8. An isolated Locust LAB run under `lab.py` supervision shows completion,
   exit-code propagation, the deadline, a cancel, a master crash and a worker
   loss, with the resulting CSV state and exact cleanup.
9. HOME Alloy joins `quality_otlp_net`, and a HOME relay run reaches the HOME
   Prometheus, or the step is recorded as `NOT_RUN` with its reason.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-quality-k6-locust-and-otel-semantics.md)
- [Relay and Locust lifecycle Task](tasks/tsk-0002-relay-controller-and-locust-lifecycle.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [Observability requirement](../../01.requirements/0007-observability.md)
- [Tooling requirement](../../01.requirements/0010-tooling.md)
