---
title: "Observability HOME Coverage Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0225-TSK-0001"
parent_ids:
- "SPEC-0225-PLAN-0001"
created: "2026-10-09"
---

# Observability HOME Coverage Task

## Objective

Keep LAB-only observability out of HOME and make every provisioned dashboard
show the data its purpose needs on HOME.

## Inputs and Authorization

On 2026-10-09 the owner asked to inspect the Grafana dashboards, stop showing
the items that moved to LAB, analyse the panels that collect or show nothing
and collect and visualise data that fits each dashboard's purpose, then
extended the request to everything in `infra/06-observability` that targets
LAB. For the three changes that move a network or host boundary the owner
chose: a SeaweedFS scrape-only network, node-exporter in the host network
namespace, and only the `processes` and `tcpstat` collectors. The branch builds
on the SPEC-0224 branch because both edit the same dashboards and alert files,
and is rebased onto `main` after SPEC-0224 merges.

## Work Log

### Audit Method

A script ran every target of every provisioned dashboard against HOME
Prometheus (PromQL) or Loki (LogQL, last 6 h). Custom, constant and interval
variables took their dashboard defaults; query variables, in double or single
quotes, were widened to match everything, so "empty" means no series exists
for the panel at all. The first runs widened only double-quoted matchers; the
figures below come from the corrected run, both sides on the same data. Three
read-only analyses then classified each empty panel as idle, renamed,
not scraped, not emitted in this deployment, a wrong selector, or LAB.

### LAB Inventory

| Surface | LAB-only reference | Result |
| --- | --- | --- |
| Prometheus jobs | None | No change |
| Alert rules | Four HAProxy rules; a commented job list naming `postgres-cluster`, `valkey-cluster`, `haproxy`, `opensearch-exporter` | Removed |
| Grafana | Cassandra, etcd, HAProxy, MongoDB, Valkey Cluster dashboards | Moved to `labs/dashboards/` with their sources |
| Gatus, Alloy, Loki, Tempo, Alertmanager | None | No change |

The `k3d-hyhome` series in HOME Prometheus and Loki belong to the integrated
hy-home.k8s cluster (RUN-0096), not LAB; cluster variables now default to
`hy-home` so they do not mix into HOME views. The single-node OpenSearch is a
root service behind its own profile and keeps its dashboards.

### W1 LAB Separation

The five dashboards moved to `labs/dashboards/` (outside provisioning) with a
README listing their sources, and the Grafana README now points there.

### W2 Collection

- SeaweedFS master, volume and filer serve metrics on 9324-9326 over
  `seaweedfs_metrics_net` (10.250.19.0/24, internal, isolated gateway), whose
  only other member is Prometheus; three jobs and `SeaweedFSNodeMetricsDown`
  were added. Binding the data APIs to one network would need fixed addresses
  on `seaweed_internal`, a network recreation and new health checks, so
  Prometheus is placed inside the SeaweedFS trust boundary instead.
- node-exporter moved to the host network namespace with
  `--web.listen-address=10.250.5.1:9100` (the `obs_net` gateway); a probe from
  `obs_net` and from `edge_net` both reached that address, so the listener is
  not routed from the LAN by default but open to non-internal bridges. Prometheus maps the name
  through `extra_hosts`. `processes` and `tcpstat` were enabled.
- OpenBao `prometheus_retention_time` 30 s → 24 h: its usage gauges are emitted
  every ten minutes and were visible about half of the time.
- Keycloak `KC_HTTP_METRICS_SLOS: '250'` (an option of the pinned image's
  `kc.sh start`), since the default buckets skip 0.25 s.
- Both PostgreSQL exporters enable `stat_checkpointer`; an isolated run with
  the monitor role exposed nine `pg_stat_checkpointer_*` series.
- Gatus checks the gateway certificate through the Keycloak discovery URL with
  `[CERTIFICATE_EXPIRATION] > 720h`.

### W3 Dashboards

Corrections: Kafka controller panels read `job="kafka-broker"`; consumer-lag
variables read `kafka_topic_partition_current_offset`; Traefik keeps full
service names (the shortening merged `@docker` and `@file` routers and caused
the one query error) and averages slow services per service; registry v3
cache counters; Grafana `grafana_alerting_alerts`; Alloy OTel semantic
convention seconds histograms and a Docker log-source row; PostgreSQL
checkpointer columns; Loki and Tempo single-binary selectors (`job`, cAdvisor
`name`, `container_name` log stream, ring members, distributor push
latency, v3 worker and live-store series, classic latency default);
Keycloak CPU against the container limit; OpenBao raft storage; Gatus
certificate warnings default to 0; Ollama running models default to 0.

Removals (features HOME does not run): Confluent Server stray-partition and
tiered-storage panels, SeaweedFS filer.sync, admin, worker and Lance panels,
Qdrant shard transfers, Airflow SLA misses, the tensor-core panel,
node-exporter timex, IRQ, power-supply, fan and systemd panels, Gatus domain
expiry, Alloy OTLP log and metric-exporter panels, Loki memcached, Consul, GCS
and Azure rows and per-component duplicates, Tempo gateway, Envoy, Kafka,
memcached, external-endpoint, vulture and memberlist panels, and Keycloak
JGroups panels.

### W4 HOME Rollout

From the detached checkout `a4a3a7dad`, and `4420a0514` for the dashboards (pre-rebase SHAs; see the mapping in Review and Completion):

| Step | Result |
| --- | --- |
| Config hash check | Each recreated service also received the merged SPEC-0218 PID limit (none set before); current PIDs were 10 to 58 against limits of 256 to 1024; no other hardening field differed |
| SeaweedFS master, volume, filer | Healthy; `seaweedfs_metrics_net` internal without a gateway address, three members; S3, Loki and Tempo stayed healthy |
| node-exporter, Prometheus | Healthy; listener only on `10.250.5.1:9100`; 160 host network-device series instead of the container's two |
| PostgreSQL exporters, Gatus | Healthy; checkpointer and certificate-expiry series present |
| Keycloak | Recreated at 12:14:37, healthy at 12:15:20; the 0.25 s bucket present; discovery 200 and Grafana redirect 302 through the gateway; scrape back at 12:15:45 |
| Prometheus rules | Reloaded: 95 rules, `SeaweedFSNodeMetricsDown` present, no HAProxy rule |
| Grafana | 45 dashboards loaded; none of the five LAB dashboards |
| Alloy (review fix) | Before: `node-exporter` did not resolve in Alloy. Recreated from the review-fix commit: healthy, `extra_hosts` maps the name to `10.250.5.1`, and Pyroscope again lists 11 `service_name` values including `node-exporter` |
| OpenBao | Not recreated: restart needs the owner's manual unseal (Shamir 2 of 3); the retention change waits for that restart |

Audit on the same HOME data, `main` dashboards against this branch:

| Dashboards | Panels with data | Empty | Errors |
| --- | --- | --- | --- |
| `main`, 50 | 748 | 520 | 1 |
| This branch, 45 | 772 | 207 | 0 |

Remaining empty panels and why:

| Dashboard | Empty | Reason |
| --- | --- | --- |
| OpenSearch (3) | 63 | The single-node service is stopped (`opensearch` profile) |
| Kafka Connect | 38 | No connector registered; per-connector and per-task series appear with one |
| SeaweedFS | 27 | Vacuum, scrub, replication, EC, filer HTTP, S3 handler and lifecycle series appear when those operations run |
| k6 | 12 | Data exists only during quality runs (remote write) |
| OpenBao | 13 | Usage gauges wait for the 24 h retention restart; route counters need requests |
| Qdrant | 10 | No collection, snapshot or API traffic yet |
| Airflow, Flower | 11 | No DAG or Celery task has run since the exporters started |
| Keycloak (2) | 7 | Event and error-ratio series restarted with Keycloak; they fill with sign-ins |
| Tempo (2) | 8 | Trace-by-ID queries, failed pushes, discarded spans not yet seen |
| Traefik | 5 | No 5xx, other codes or SLO-failing services; response-size histogram not emitted at rest |
| Alloy OpenTelemetry | 4 | No OTLP metric points, no failed spans, OTLP over HTTP unused |
| Others (7) | 9 | Idle or zero-filtered: Ollama loaded-model memory, OffsetCommit, consumer lag and consumption (no consumer group commits), TCP `syn_sent`, active PostgreSQL sessions, slow Alloy evaluations, Loki ingester read success and append failures |

### W5 Documents

POL-0024 (SeaweedFS metrics and trust boundary), RUN-0045 (node-exporter host
namespace and exposure), the Grafana and LAB dashboard READMEs and the service
inventory describe the changes.

### Review

An independent review of `1f47db7bd..13f629690` found four important and six
minor issues:

| Finding | Resolution |
| --- | --- |
| Alloy's Pyroscope source still scraped `node-exporter:9100`, which no longer resolves on `obs_net` | Alloy maps the name through `extra_hosts` like Prometheus; a test ties both to the `obs_net` gateway |
| GDE-0024 and the SeaweedFS README said only S3 serves metrics; RUN-0024 had no `SeaweedFSNodeMetricsDown` entry | Both describe the metrics network; RUN-0024 adds the alert procedure |
| `labs/dashboards/README.md` had no front matter | Added as draft |
| The remaining-empty table summed to 203, not 209 | The audit also missed single-quoted variables; both sides were re-run and the table now sums to 207 |
| "The LAN cannot reach" node-exporter was too strong | Reworded to not routed by default; RUN-0045 notes the `obs_net` precondition |
| The listener was coupled to the gateway without a test; no test bounded host networking or LAB rules and dashboards | Tests derive the gateway from the `obs_net` subnet, limit `network_mode: host` to node-exporter, check `seaweedfs_metrics_net` is internal and isolated, and keep LAB dashboards and LAB exporter metrics out of HOME |
| GDE-0045, GDE-0044, GDE-0041 and the tier README kept LAB or pre-host-network text | Updated |
| Prometheus overview, SeaweedFS and OpenSearch cluster variables defaulted to all | Default `hy-home` |
| Alloy Docker panel descriptions and a Keycloak percent threshold of 80 | Corrected |

A re-review of the fix range found no critical or important issue and eight
minor ones, all resolved: GDE-0045 job count (37) and SeaweedFS node jobs;
Alloy named beside Prometheus wherever `extra_hosts` must move; GDE-0044 and
POL-0044 no longer call node-exporter internal-only; the Keycloak CPU panel
description; the literal gateway assertions replaced by the derived ones; the
LAB metric pattern now also covers provisioned dashboards; the LAB dashboard
README is registered with the package README profile and has its required
sections; and the Evidence rows below carry the SHAs the HOME steps ran from.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LAB separation | 1 | W1 | LAB isolation and dashboard contract tests; promtool | `21562bcd0` | PASS | W1 LAB Separation | accepted |
| Collection | 2 | W2 | Compose, network, SeaweedFS, tier layout and Gatus tests; Compose rendering | `225894242` | PASS | W2 Collection | accepted |
| Dashboards | 3 | W3 | Dashboard contract tests; HOME query audit | `12e187934` | PASS | W3 Dashboards | accepted |
| HOME rollout | 3 | W4 | Health, listener, target, rule and Grafana checks | `4420a0514` (rebased `12e187934`) | PASS | W4 HOME Rollout | accepted |
| Review fixes | 3 | W4 | Network, host-network, gateway and LAB tests; dashboard tests; audit recount | `789fbd525` | PASS | Review | accepted |
| Alloy on HOME | 3 | W4 | Name resolution; Pyroscope `service_name` list | `b2745167d` (rebased `789fbd525`) | PASS | W4 HOME Rollout | accepted |
| Changed gate | 4 | W5 | `run-ci-gate.py --profile changed --local-only`, base `acc191655` | `ad33a5b9f` | PASS | Review and Completion | accepted |
| Staged style check | 4 | W5 | `run-ci-precommit.sh --mode local-staged` over `acc191655..HEAD`; the first run asked for `ruff format` on two tests, applied in `75f66c8f9` | `75f66c8f9` | PASS | Review and Completion | accepted |
| OpenBao retention on HOME | 3 | W4 | Owner restart and unseal; seal status, running config, Prometheus series | `f75275651` | PASS | Review and Completion | accepted |
| Remote candidate | 4 | W5 | `candidate-quality` run 37945693271, base `acc191655` | `e26c7d439` | PASS | Review and Completion | accepted |

## Review and Completion

SPEC-0224 merged as `acc191655`; this branch was rebased onto it without
conflicts or content changes: `ff9f2f48c`→`21562bcd0`,
`a4a3a7dad`→`225894242`, `4420a0514`→`12e187934`,
`13f629690`→`d347e6e44`, `b2745167d`→`789fbd525` (the Alloy rollout ran
from `b2745167d`). The changed gate passed on `ad33a5b9f` (rc 0) and the staged
style check on `75f66c8f9` (rc 0).

The first `candidate-quality` run (run 37941854676, head `d6c98311e`) failed
the hardening baseline: `check-all-hardening.sh` still required OpenBao's
`prometheus_retention_time` of 30 s. The local `--local-only` gate does not run
that baseline. The check now requires 24 h; `check-all-hardening.sh` passes
locally (rc 0). Run 37945693271 passed on head `e26c7d439` against base
`acc191655`, and PR #401 merged as `c3ce31973` (recorded with SPEC-0228).
On 2026-10-10 the owner restarted and unsealed OpenBao (recreated 08:34 KST).
It is unsealed and healthy, its running config holds
`prometheus_retention_time` 24h, and Prometheus scrapes 621 series including
the usage gauges that were sparse before (`vault_secret_kv_count`,
`vault_identity_entity_count`, `vault_core_mount_table_num_entries`). Complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
