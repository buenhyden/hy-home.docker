---
title: "Quality Load Tools and OTel Metric Semantics Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
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
ownership labels. The relabel allowlist keeps the same set plus `instance`,
`__name__`, and the histogram and summary labels `le` and `quantile`.
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

### W2 Manifest Telemetry and Metrics Ingress

`quality_run.py` now accepts `hyhome.quality-run/v2` as well as v1; `prepare`
copies the operator-supplied manifest unchanged.
v2 requires `telemetry` with exactly `mode` in `none` or `otlp`. v1 keeps its
exact key set and means `none`. An endpoint, unknown mode, non-object value or
a `telemetry` key on v1 is rejected.

`container_executor.execute` takes `metrics_peer`
(`--metrics-ingress-container`). OTLP mode without it, or the peer without
OTLP, is rejected before any Docker call. The front network must then hold
exactly the target and the ingress. The ingress must carry the run label and
`hyhome.quality.role=metrics-ingress` and use a digest-pinned
`grafana/alloy@sha256:` image. It must have a read-only rootfs, be
unprivileged with `CapDrop=[ALL]`, have no port bindings, carry the alias
`metrics-ingress` and join at most two networks. k6 then gets
`--out opentelemetry` beside the JSON output and executor-owned
`K6_OTEL_*`/`OTEL_RESOURCE_ATTRIBUTES` values. k6 never gets the token. The
new relay configuration `infra/11-quality/k6/metrics-ingress.alloy` holds it
and forwards to `alloy:4319`.

Unit tests: two new tests. They failed against the previous code (3
failures, RED) and pass with it. 23 `test_k6_results` tests pass.

Isolated E2E: the harness with `--k6-image
grafana/k6@sha256:9bd01d69…ace6` exited 0 with 24 PASS lines. k6 used the
executor's own `_telemetry_arguments` and ran 12 iterations against a 200
and a 404 path through the relay and the authenticated receiver. Prometheus
held `http_req_failed` split into two `condition` series for instance
`…0214-a1` and `expected_response="false"` request count 12, with no `url` or
`name` label. The first k6 run passed its checks but left the profile-scoped
relay because `down` omitted `--profile k6`. The harness now passes the
profile. The leftover project and its scratch were removed with the fixture's
own `compose down`, and the rerun reported exact cleanup.

The real-target executor run (guard plus WireMock plus ingress on HOME), the
HOME relay and HOME Alloy recreation are `NOT_RUN`.

### W1 Follow-up: Dashboard on the Verified OTLP Shape

The harness printed the metric names and labels that real k6 OTLP output
produces through the relay. Before the prefix setting the names were
`http_reqs_total`, `http_req_failed_total`, `data_sent_bytes_total`,
`iterations_total` and `*_milliseconds_bucket/_count/_sum` for every trend,
and the short first probe run had no `vus` series; the 20 s dashboard run
below did report `k6_vus`. The labels were `environment`,
`expected_response`, `instance`, `method`, `project_id`, `scenario`,
`service_name` and `status`. The `Infrastructure/k6` dashboard expected
`k6_*_rate`, `_p95`-style quantile gauges and `run_id`/`attempt`/`testid`
labels. That is the Prometheus remote-write output shape, so no panel could
match this path, and with the previous transform none could match at all.

The executor now sets `K6_OTEL_METRIC_PREFIX=k6_`. The dashboard filters by
`project_id` and `instance` (`<run_id>-a<attempt>`). Trends use
`histogram_quantile($quantile, sum by (le) (rate(..._milliseconds_bucket…)))`,
the failure and check ratios use `condition="nonzero"` over the total, and
the data metrics use `_bytes_total`. "Requests by URL" became "Requests by
method and status" (p50/p90/p95/p99). "Checks list" was removed because
check names are dropped as unbounded. The JSON formatting is unchanged, so the
diff shows only substantive changes.

The harness substitutes the variables and runs every k6 dashboard query
against the isolated Prometheus after a 20 s k6 run. 28 of 30 queries return
data. The two empty ones are `k6_checks_total` and
`k6_dropped_iterations_total`; the synthetic scenario has no checks and drops
no iterations. A first attempt with `$__rate_interval=1m` returned empty
`rate()` results because the run's last samples aged out of the window. The
harness uses `5m`, since the check concerns query shape, not timing. Failed
requests equal Rate `nonzero` (40). The dashboard tests failed 14 times
against the previous JSON (RED) and pass now. Live Grafana is `NOT_RUN`.

### W3 Locust Worker Bounds

`labs/locust.yml` took the expected worker count from
`LAB_LOCUST_EXPECT_WORKERS` but fixed the worker replicas at 2 and waited for
workers without a limit. Both now come from the same input, and
`--expect-workers-max-wait` reads `LAB_LOCUST_EXPECT_WORKERS_MAX_WAIT`
(default 60 s) from `labs/.env.example`. Combined with the existing
`--run-time` and `--stop-timeout`, a run now has a deadline. The new
`test_locust_telemetry` contract failed against the previous file (RED) and
passes now. The lab public environment count fixture moved from 48 to 49
(38 optional).

An isolated run used project names `s0214loc-*`, a synthetic target and
scenario, 4 users for 8 s, and the pinned Locust 2.46.6 image:

| Run | Workers | Expected | Max wait | Exit | Requests | Leftovers |
| --- | --- | --- | --- | --- | --- | --- |
| w1 | 1 | 1 | 30 s | 0 | 156 | 0 |
| w2 | 2 | 2 | 30 s | 0 | 156 | 0 |
| w3 | 3 | 3 | 30 s | 0 | 156 | 0 |
| short | 2 | 3 | 10 s | 1 | 0 | 0 |

The shortage run logged "Gave up waiting for workers to connect", exited
non-zero, and its workers stopped. Locust OTel export stays unsupported
because the image has no OpenTelemetry SDK. Locust results stay file-based
in the LAB, and k6 remains the default load path.

### W4 Documents, Review and Final Validation

The k6 guide, policy and runbook, the Alloy guide, policy and runbook, and
AD-0006 now describe the OTLP metric path. The operations catalog showed one
stale cell: the Alloy row of the m0021 service inventory listed no secret
after W1. It now lists `["quality_otlp_token"]`.

An independent read-only review of the branch returned eleven findings. They
were handled as follows:

| Finding | Disposition |
| --- | --- |
| Latency panels used `s` for millisecond histograms | Fixed: nine units set to `ms`; new dashboard test RED then GREEN |
| Legends kept `$quantile_stat` | Fixed: eleven legends use `$quantile`; same test |
| RUN-0040 still pointed metric producers at 4317/4318 | Fixed: 4319 receiver, token and verification steps |
| k6 documents claimed the executor never starts a container | Fixed: guard-config path documented; live target traffic stays `BLOCKED` under SPEC-0204 |
| Task said there was no `vus` series | Fixed: the short probe lacked it; the 20 s run reported it |
| Relay second network was unconstrained | Fixed: `--metrics-egress-network` is required with the relay, and the relay must join exactly the run network and that network; `test_k6_results` RED then GREEN |
| Empty token file | Checked in an isolated Alloy: with an empty token, a request with no header gets 401 and an empty or a wrong bearer token gets the connection closed without a response; none is accepted. RUN-0040 requires a non-empty file before HOME recreation |
| POL-0040 scope excluded `config.home.alloy` | Fixed: scope, systems and verification name it |
| Task allowlist and v2 wording | Fixed |
| No tracked procedure creates the per-run relay | Deferred: forward dependency recorded in RUN-0061; HOME relay `NOT_RUN` |
| Per-attempt `instance` values grow Prometheus series | Accepted by contract 5; retention follows the existing Prometheus retention, no new rule |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Metric identity | 3 | W1 | Isolated metrics harness RED then GREEN | Pinned Alloy, Prometheus, Python digests | PASS | W1 Authenticated Receiver and Metric Identity | accepted |
| Manifest v2 | 1 | W2 | `test_k6_results` RED then GREEN | Working tree | PASS | W2 Manifest Telemetry and Metrics Ingress | accepted |
| Executor peer | 2 | W2 | Unit tests; isolated k6 OTLP E2E | Pinned k6, Alloy, Prometheus digests | PASS | W2 Manifest Telemetry and Metrics Ingress | accepted |
| Locust bounds | 4 | W3 | `test_locust_telemetry` RED then GREEN; isolated 1/2/3-worker and shortage runs | Pinned Locust 2.46.6 image, synthetic scenario | PASS | W3 Locust Worker Bounds | accepted |
| Records | 5 | W4 | Changed-profile local gate, staged lint, operations catalog, metadata, independent review | Working tree at the W4 commit | PASS | W4 Documents, Review and Final Validation | accepted |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
