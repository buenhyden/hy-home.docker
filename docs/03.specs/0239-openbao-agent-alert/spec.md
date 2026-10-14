---
title: "OpenBao Agent Telemetry and Alert"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0239"
parent_ids:
- "REQ-0003"
- "REQ-0007"
- "AD-0003"
- "AD-0006"
created: "2026-10-14"
---

# OpenBao Agent Telemetry and Alert

## Overview

`openbao-agent` renders the Keycloak and Grafana admin credentials, but it
exposes no metric: `agent.hcl` has no telemetry or listener and Prometheus does
not scrape it. An authentication failure or a stopped Agent therefore shows
only as Docker `unhealthy`, and nothing alerts. The owner recorded that gap on
2026-10-13 for a separate Spec and chose on 2026-10-14 (AskUserQuestion)
"Agent telemetry + scrape".

## Scope

In scope: the Agent's `telemetry` stanza and one `metrics_only` listener, the
Agent's `obs_net` membership, the Prometheus `openbao-agent` job in both
Prometheus configurations, two alert rules, their promtool cases and tests,
and the guide and Grafana README rows. Out of scope: TLS for the listener, a
template staleness metric, a dashboard, deployment to HOME, and RUN-0085,
which its owner updates after merge.

## Contracts

1. The Agent serves `/agent/v1/metrics` on one `listener "tcp"` at port 8100
   with `role = "metrics_only"`, so the listener has no API proxy, cache or
   quit route; it needs no token and serves no secret.
2. The listener uses plain HTTP: the Agent holds no server certificate, and
   the endpoint carries counters only. No host port is published; the Agent
   joins `obs_net` so Prometheus can reach it.
3. Prometheus scrapes job `openbao-agent` at
   `openbao-agent:8100/agent/v1/metrics?format=prometheus` with the repository
   labels, identically in `prometheus.yml` and `prometheus.dev.yml`.
4. `OpenBaoAgentMetricsScrapeFailing` fires when `up` is 0 for 10 minutes, and
   `OpenBaoAgentAuthFailure` when `bao_agent_auth_failure` increased within
   15 minutes for 5 minutes, a window longer than the Agent's 5-minute maximum
   auth retry backoff. The Agent's metric prefix is `bao`, not the
   documented `vault`.
5. A render that goes stale while authentication works has no metric and
   stays a Docker health signal; this limit is stated where the gap was.

## Acceptance Criteria

1. Tests show the listener, telemetry, network and scrape job, and fail
   against `main`.
2. Promtool cases show each alert absent before, firing in, and clearing
   after its condition, and the existing audit-alert cases still pass.
3. The pinned Agent image accepts the configuration, serves only the metrics
   path, and names the counter `bao_agent_auth_failure`, observed locally
   without network or credentials.
4. Independent IaC and security reviews find nothing blocking, and the
   changed tests, metadata, links and markdownlint pass.
5. Hosted `candidate-quality` passes.

## Related Documents

- [REQ-0003](../../01.requirements/0003-security.md)
- [REQ-0007](../../01.requirements/0007-observability.md)
- [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [AD-0006](../../02.architecture/descriptions/0006-observability-architecture.md)
- [Plan](plan.md)
