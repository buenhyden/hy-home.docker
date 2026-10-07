---
title: "Quality Load Tools and OTel Metric Semantics"
version: "0.1.0"
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
Locust worker-count and deadline gaps.

## Scope

Included: the k6 manifest telemetry field and its compatibility rule, the
executor's OTLP ingress peer, the HOME Alloy quality receiver and transform,
the isolated metrics acceptance harness, the Locust LAB worker and deadline
inputs, and the documents that operate them.

Excluded: real application targets and load budgets, HOME Alloy recreation,
per-project producer credentials (owned by the integration package), a
`perf_db` hypertable without a named query consumer, and Locust OpenTelemetry,
which the pinned image cannot export.

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

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-quality-k6-locust-and-otel-semantics.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [Observability requirement](../../01.requirements/0007-observability.md)
- [Tooling requirement](../../01.requirements/0010-tooling.md)
