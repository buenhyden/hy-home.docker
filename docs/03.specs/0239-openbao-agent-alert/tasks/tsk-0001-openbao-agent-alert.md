---
title: "OpenBao Agent Telemetry and Alert Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0239-TSK-0001"
parent_ids:
- "SPEC-0239-PLAN-0001"
created: "2026-10-14"
---

# OpenBao Agent Telemetry and Alert Task

## Objective

Give `openbao-agent` a metrics endpoint, a Prometheus job and alerts, as
SPEC-0239 states.

## Inputs and Authorization

- **Request:** the owner asked on 2026-10-14 to review and proceed with the
  Agent alert and chose "Agent telemetry + scrape" (AskUserQuestion). SPEC-0204
  TSK-0006 had recorded the gap on 2026-10-13.
- **Baseline:** `main` `c96d46112`.
- **Not done:** no deployment, no Agent recreate, no HOME or credential
  access. RUN-0085's paragraph on the Agent alert gap and the SPEC-0204
  TSK-0006 "Agent alert gap" row belong to another writer and need updating
  after this merges.

## Work Log

### W1 Listener, Network and Scrape Job

Research of the OpenBao `v2.7.1` source (the pinned image) found: the Agent
supports a `telemetry` stanza; metrics are served only on a listener at
`/agent/v1/metrics`; `role = "metrics_only"` registers that path alone, while
a default listener always adds an API proxy; the metrics path has no
authentication; the Agent's service name is `bao`, so names are
`bao_agent_*` although the documentation says `vault`; template rendering
emits no metric.

`agent.hcl` gains `listener "tcp"` (`0.0.0.0:8100`, `metrics_only`,
`tls_disable = true`) and `telemetry` (`prometheus_retention_time = "24h"`,
`disable_hostname = true`). The Agent joins `obs_net`, where Prometheus
already runs, and publishes no port. TLS is not used: the Agent has no server
certificate, issuing one belongs to the P04 TLS delivery, and the endpoint
serves counters only. Prometheus gets job `openbao-agent` with the repository
labels in both `prometheus.yml` and `prometheus.dev.yml`, which stay
byte-identical.

The pinned image (`openbao/openbao:2.7.1@sha256:6d2b9385…`) ran locally with
`--network none`, temporary directories and no RoleID or SecretID. It accepted
the configuration; `/agent/v1/metrics?format=prometheus` returned
`bao_agent_auth_failure 3` (counter, no `_total`) while auth retried with "no
known role ID"; `/v1/sys/health`, `/agent/v1/cache-clear`, `/agent/v1/quit`
and `/` returned 404.

### W2 Alerts

`alert_rules.openbao.yml` gains `OpenBaoAgentMetricsScrapeFailing`
(`up{job="openbao-agent"} == 0` for 10 minutes, warning) and
`OpenBaoAgentAuthFailure` (`increase(bao_agent_auth_failure[15m]) > 0` for
5 minutes, warning; widened from `[5m]` after the IaC review). `tests/validation/fixtures/openbao-agent-alerts.test.yml`
checks each alert absent, firing and cleared; `AgentMetricsTests` runs it with
the cached promtool image and skips when that image is absent. A stale render
with working auth still has no metric; Docker health remains its only signal.

### W3 Documents and Checks

The OpenBao guide (0.6.0) states the listener, network and limit; the Grafana
README coverage row names the new job, which its coverage test requires.

### Review Round 1

On 2026-10-14 the controller ran the independent reviews this fork could not
start. `security-auditor` returned PASS with one wording finding: Agent-to-
server traffic may cross either shared network, still TLS-verified; the Plan
says so now. `iac-reviewer` returned FAIL on one item: with the Agent's
5-minute maximum auth retry backoff, a `[5m]` window could read zero between
retries, so a long outage would flap or never fire. The window is now
`[15m]`, and a second promtool case increments only every five minutes and
stays firing at 12, 14, 22 and 24 minutes; the first case now clears at 35
minutes. The `agent.hcl` comment now says the host can reach the port too.
Deployment notes from the IaC review: recreating the Agent deletes its token
sink and needs a fresh wrapped SecretID, so it is a credential operation;
`prometheus.yml` is a single-file bind mount, so Prometheus needs a restart,
not a reload; recreate the Agent before restarting Prometheus.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Config tests | 1 | W1 | `AgentMetricsTests` RED on `c96d46112` (2 errors, 1 failure), GREEN on the branch | Branch on `c96d46112` | PASS | W1 Listener, Network and Scrape Job | - |
| Image probe | 3 | W1 | Pinned image, `--network none`, no credentials: config accepted, metrics path only, `bao_agent_auth_failure` counter | Branch | PASS | W1 Listener, Network and Scrape Job | - |
| Alert cases | 2 | W2 | Agent promtool cases SUCCESS; audit cases SUCCESS; `promtool check rules` 7 rules | Branch | PASS | W2 Alerts | - |
| Checks | 4 | W3 | OpenBao agent contract (24), compose baseline, runtime compatibility, SEC01 version and surface ownership suites (154, 30 skipped); Registry tests (126); changed metadata (6 documents) 0 violations; links `--mode all` 0 failures; markdownlint 0 | Branch | PASS | W3 Documents and Checks | - |
| IaC review | 4 | W3 | Independent `iac-reviewer` of `f0f6b1b2b`: auth alert window too short | `f0f6b1b2b` | FAIL | Review Round 1 | - |
| IaC fix | 4 | W3 | `[15m]` window; slow-retry promtool case; agent contract suite (24, promtool cases run) | Branch | PASS | Review Round 1 | IaC review |
| Security review | 4 | W3 | Independent `security-auditor` of `f0f6b1b2b`: PASS, wording note applied | `f0f6b1b2b` | PASS | Review Round 1 | - |
| Candidate | 5 | W4 | Hosted `candidate-quality` | - | NOT_RUN | Work Log | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |

## Review and Completion

No criterion is accepted until the owner accepts it. Deployment needs a
separately approved Agent recreate.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
