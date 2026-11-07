---
title: "Secondary Listener Hardening Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-07"
layer: "specs"
artifact_id: "SPEC-0267-TSK-0001"
parent_ids:
- "SPEC-0267-PLAN-0001"
created: "2026-11-07"
---

# Secondary Listener Hardening Task

## Overview

### Objective

Execute W1–W5 of the Plan: inventory the six secondary listeners, bind them to
consumer-only addresses, add Grafana metrics authentication, declare the
Pyroscope metastore volume, test, document and, under separate approval, apply
the change in HOME.

## Inputs and Authorization

On 2026-11-07 the owner reviewed the secondary listeners recorded out of scope
by SPEC-0266 and chose: bind all six under a new Spec, add Grafana metrics
authentication, record n8n `/metrics`, Gatus `/metrics` and the POL-0096 LAN
listeners as accepted risks, and declare the Pyroscope metastore as a named
volume in a separate change. The Spec and Plan are `draft`; no
implementation starts until both are approved. The review read `main`
`fa6135043a4b770281400e5f7a6a7b4ceca66063` and the upstream documentation and source of each pinned
version. HOME recreation (W5) needs its own approval.

## Work Log

### Draft inputs (2026-11-07)

| Listener | Bind setting (upstream) | Consumers found in review | Note |
| --- | --- | --- | --- |
| SeaweedFS S3 `9327` | `-metricsIp` (4.48 `weed/command/s3.go:116`) | Prometheus, Alloy profiles | `seaweedfs_s3_metrics_net` already carries only these |
| OAuth2 Proxy `44180` | `OAUTH2_PROXY_METRICS_ADDRESS` (7.15) | Prometheus | Health check uses `4180` |
| Keycloak `9000` | `KC_HTTP_MANAGEMENT_HOST` (26.7.4 `ManagementOptions.java:66-69`) | Prometheus, Gatus, own health check on `127.0.0.1:9000` | Health check must move |
| n8n broker `5679` | `N8N_RUNNERS_BROKER_LISTEN_ADDRESS` (2.43.6 `runners.config.ts:32-33`) | `n8n-task-runner` over `n8n_main_runner_net` | Already token-protected; `n8n-worker` is not on `edge_net` |
| Grafana pprof `6060` | `GF_DIAGNOSTICS_PROFILING_ADDR` | Alloy `pyroscope.scrape` | A specific IP is implied, not stated, by the docs |
| Traefik `8082` | entrypoint `address: "<host>:8082"` (v3.7) | Prometheus, own `traefik healthcheck --ping` | Ping with a bound entrypoint is untested |

Main-port metrics: Grafana offers `[metrics] basic_auth_username` and
`basic_auth_password` (13.2.4 `conf/defaults.ini:2031-2033`); n8n documents
no metrics authentication; Gatus serves `/metrics` outside its OIDC router
and the repository patch test `metrics-remains-public-for-internal-scrape`
keeps it public. Loki and Tempo have no built-in authentication; Alloy's OTLP
receiver accepts an `auth` handler, but the senders run in LAB.

Pyroscope 2.4.0 keeps `-metastore.data-dir` and `-metastore.raft.dir` under
`./data/v2/metastore` with working directory `/`, so the metastore lives in
the image's anonymous `/data` volume (142.6M), not in the declared
`pyroscope-data` volume. A `down` or `rm` followed by `up` would give it an
empty volume and orphan the profile blocks.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft source and documentation review | `fa6135043`, upstream pins | NOT_RUN | Draft input only; the source-read inventory is W1 | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Awaiting W1 | @buenhyden |
| 2 | pending | - | Awaiting W2 | @buenhyden |
| 3 | pending | - | Awaiting W2 | @buenhyden |
| 4 | pending | - | Awaiting W2 | @buenhyden |
| 5 | pending | - | Awaiting W3 | @buenhyden |
| 6 | pending | - | Awaiting W1 | @buenhyden |
| 7 | pending | - | Awaiting W5 and its approval | @buenhyden |

## Review and Completion

Not started. The Spec and Plan are drafts.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0266 Task](../../0266-sso-only-backend-ingress/tasks/tsk-0001-sso-only-backend-ingress.md)
