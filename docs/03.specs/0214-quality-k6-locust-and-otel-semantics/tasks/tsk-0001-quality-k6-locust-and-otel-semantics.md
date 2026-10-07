---
title: "Quality Load Tools and OTel Metric Semantics Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0214-TSK-0001"
parent_ids:
- "SPEC-0214-PLAN-0001"
created: "2026-10-07"
---

# Quality Load Tools and OTel Metric Semantics Task

## Objective

Preserve the k6 result contract, add one authenticated live metrics path,
keep metric identities intact, and bound the Locust LAB.

## Inputs and Authorization

The current user request on 2026-10-07 asks to execute prompt 02 of the
analysis pack, with per-unit commits and a per-Spec PR merge. It names no real
application target, load budget or HOME recreation, so those lanes stay
`NOT_RUN`. Baseline `main` `f774a8666`. Registry issues SPEC-0214.

## Work Log

### Observed Baseline

- Pinned k6 `grafana/k6:2.2.0`
  (`sha256:9bd01d6941fca969cb61bb57d2da5ee9b385fe2aa8881df3798c196564d6ace6`,
  amd64). Its binary contains the `K6_OTEL_*` keys `EXPORTER_PROTOCOL`,
  `GRPC_EXPORTER_ENDPOINT`, `HTTP_EXPORTER_ENDPOINT`, `HTTP_EXPORTER_URL_PATH`,
  `HTTP_EXPORTER_INSECURE`, `HEADERS`, `SERVICE_NAME`, `SERVICE_VERSION`,
  `EXPORT_INTERVAL`, `FLUSH_INTERVAL`, `METRIC_PREFIX` and the TLS keys. The
  k6 v2.0.0 release notes state that Rate metrics export as one counter with a
  `condition` attribute (`nonzero`/`zero`).
- HOME Alloy `config.home.alloy` routed metrics from the host-published
  4317/4318 receiver into `quality_metrics`. Its datapoint `keep_keys` kept
  only `project_id`, `environment` and `service_name` before
  `deltatocumulative`, so `condition` and producer identity were removed and
  distinct streams shared one identity.
- Pinned Locust `locustio/locust:2.46.6`
  (`sha256:d43616228012a7d79b883e2ecd42f87640469377f2b666c4ab27e5248dfdf35f`)
  supports `--expect-workers-max-wait` and `--otel`, but the image lacks
  `opentelemetry.sdk` and the OTLP exporters, so Locust OTel is unsupported.
  `labs/locust.yml` used `LAB_LOCUST_EXPECT_WORKERS` for the master and a
  fixed `replicas: 2` for workers.

### W1 Authenticated Receiver and Metric Identity

`config.home.alloy` gains `local.file "quality_otlp_token"`,
`otelcol.auth.bearer "quality"` and `otelcol.receiver.otlp "quality"` (HTTP
`0.0.0.0:4319`, not published; the Compose `ports` list is unchanged). The
public 4317/4318 receiver now forwards traces only. The transform keeps the
resource `service.instance.id` and the datapoint attributes `condition`,
`expected_response`, `method`, `status` and `scenario` next to the three
ownership labels. The relabel allowlist keeps the same set plus `instance`.
The Alloy service mounts the new Compose secret `quality_otlp_token`
(registry `OBS-014`, `secrets/observability/alloy/quality_otlp_token.txt`).
It already joins `SECRETS_GID` 1000 and can read the `0640` file. The
private registry metadata was synced (`--sync-metadata`, values preserved,
secret files untouched). The token value itself was not generated; an
operator must issue it before HOME Alloy is recreated.

The isolated harness `examples/operations/quality-metrics/acceptance.py`
gained `--source`, OTLP datapoint attributes, producer instances, a bearer
token and an unauthenticated case. It used the pinned digests: Alloy
`grafana/alloy@sha256:b8ec653c…a839` (v1.19.2), Prometheus
`prom/prometheus@sha256:5ce7540c…cbb0` (v3.14.0) and Python
`python@sha256:79e7a9b9…e6f` (3.13.15-alpine). All three are amd64.

- RED, the configuration before this change: exit 1. The existing counter and
  histogram cases passed, then `synthetic_rate_total{condition="zero"}`
  never appeared because `condition` was removed.
- GREEN, this change: exit 0 with 21 PASS lines. Rate `zero=3` and
  `nonzero=2` arrive as separate series. Two producer instances give
  `count=2` and `sum=10`. An unauthenticated producer gets HTTP 401 and
  stores nothing. Delta and cumulative counters and histograms (count, sum
  and bucket), exact replay, missing-identity drop, Prometheus outage retry
  and the new restart epoch (4 then 6) are unchanged. Cleanup was exact.

`alloy fmt` accepted the configuration. HOME Alloy recreation and live
Grafana are `NOT_RUN`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Metric identity | 3 | W1 | Isolated metrics harness RED then GREEN | Pinned Alloy, Prometheus, Python digests | PASS | W1 Authenticated Receiver and Metric Identity | accepted |
| Manifest v2 | 1 | W2 | Unit tests | Pending | NOT_RUN | Pending | pending |
| Executor peer | 2 | W2 | Unit tests | Pending | NOT_RUN | Pending | pending |
| Locust bounds | 4 | W3 | Render and isolated run | Pending | NOT_RUN | Pending | pending |
| Records | 5 | W4 | Local gate and review | Pending | NOT_RUN | Pending | pending |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
