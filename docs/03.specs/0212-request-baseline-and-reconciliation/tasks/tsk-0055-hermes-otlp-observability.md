---
title: "Hermes OTLP Observability Task"
version: "0.2.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0055"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# Hermes OTLP Observability Task

## Overview

### Objective

Collect the host-run Hermes agent's traces, logs and gateway metrics in the
HOME observability stack. Today only the research textfile metrics reach
Prometheus through node-exporter. Hermes runs as the `hermes-gateway.service`
user unit and writes its logs to files under `~/.hermes/logs/`, which Alloy
does not read, and its built-in OTLP exporter is not configured.

## Inputs and Authorization

On 2026-11-11 the owner (@buenhyden) approved the OTLP route over file tailing:
Hermes exports OTLP/HTTP with its own log redaction, and Alloy accepts it on a
new bearer-authenticated receiver. The approval covers the repository change.
The token value under `secrets/`, the secret metadata row, the Hermes
configuration under `~/.hermes` (including the optional `otlp` extra), and the
Alloy recreate are owner actions or need their own approval, under the
[approval boundaries](../../../../.agents/governance/approval-boundaries.md).
The runtime apply waits until after the 2026-11-11 maintenance windows.

## Work Log

### Starting state (2026-11-11)

| Signal | State |
| --- | --- |
| Research metrics | Textfile through node-exporter to Prometheus; `HermesResearch*` alerts; Grafana `hermes-research` dashboard. |
| Logs | Not collected. Alloy reads only Docker container logs. |
| Traces | Not sent. Hermes has no `monitoring` section in its configuration. |
| Gateway health metrics | Not sent. `gateway_health_export` is off. |
| Alloy OTLP | `4317`/`4318` on the LAN address accept traces only; metrics enter only through the authenticated `quality` receiver on `4319`; no log route. |

### Design

| Signal | Route |
| --- | --- |
| Traces | Hermes OTLP → Alloy `hermes` receiver → existing batch → Tempo |
| Logs | Hermes OTLP logs (redacted by Hermes) → Alloy → Loki |
| Gateway metrics | Hermes OTLP metrics → Alloy → bounded relabel → Prometheus remote write |

The receiver listens on host loopback only and requires the
`hermes_otlp_token` bearer token.

### Owner actions

| Item | Action |
| --- | --- |
| O1 | Create the token file and add its secret metadata row. |
| O2 | After the merge and an approved Alloy recreate, set `monitoring.export.otlp` and `monitoring.gateway_health_export` in `~/.hermes/config.yaml` and install the `otlp` extra. |

### Live apply 2026-11-11

The owner approved the Alloy recreate on 2026-11-11 after #939 and #941 merged.
The first recreate left Alloy restarting for about six minutes (10:41 to 10:47
KST) because a `git pull` run under `umask 077` checked `config.home.alloy` out
as 0600 and the new token file was created 0600; Alloy runs as UID 473 with
group 1000. Restoring 0644 on the tracked files and 0640 on the token (owner)
recovered it. A later config-only change needed `--force-recreate`: Compose
does not treat a changed single-file bind mount as a change, and the running
container kept the old file until recreated. The owner enabled the `user`
`hermes_otel` plugin (v1.32.6) with `content_capture: "off"` and restarted the
gateway at 11:58 KST; the built-in gateway health export reports as
`hermes-gateway` and the plugin as `hermes-agent`.

Live readback the same day: `127.0.0.1:4320` answers 401 without the token and
is not reachable on the LAN address; Tempo holds `hermes-gateway`
`hermes.gateway_health` traces; Loki holds 565 `hermes-agent` lines in 30
minutes; Prometheus holds the plugin series (`hermes_token_usage_total` by
`token_type` and `model`, `gen_ai_execute_tool_duration_seconds_*` by
`gen_ai_tool_name`, `hermes_api_time_to_first_chunk_seconds_*`,
`hermes_session_count_total`). No cost series exists because the subscription
model is not priced, and turn exit reasons need the plugin's structured events
(`logs.events.enabled: true`), which are off by default.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hermes ingest source and tests | 108 | W113 | Receiver, route, port and dashboard contract tests | Alloy, Compose and dashboard change | NOT_RUN | Implementation in progress. | required | - |
| Hermes live telemetry readback | 108 | W113 | One Hermes trace in Tempo, one log line in Loki and one gateway metric in Prometheus | HOME after the approved apply | NOT_RUN | Waits for O1, O2 and the Alloy recreate. | required | - |
| Hermes ingest source and tests rerun | 108 | W113 | Receiver, route, port and dashboard contract tests | #939, #941 and the live-fit dashboard change | PASS | `HermesObservabilityContractTest` and `ObservabilityDashboardContractTests` OK; `alloy validate` rc 0 on v1.21.3. | required | Hermes ingest source and tests |
| Hermes live telemetry readback 2026-11-11 | 108 | W113 | One Hermes trace in Tempo, one log line in Loki and one gateway metric in Prometheus | HOME after the approved Alloy recreate and gateway restart | PASS | Tempo `hermes.gateway_health` traces; Loki 565 `hermes-agent` lines in 30 minutes; Prometheus `hermes_gateway_*` (56 series) and plugin series by `token_type` and `gen_ai_tool_name`; 401 without the token. Exit-reason events and cost stay empty as described. | required | Hermes live telemetry readback |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 108 | pending | Hermes ingest source and tests, Hermes live telemetry readback | Implementation in progress. | SPEC-0212 TSK-0055 |

## Review and Completion

Completion needs the source and test row PASS and one live trace, log line and
gateway metric read back after the owner-approved apply.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Hermes DevOps brief Task](tsk-0054-hermes-devops-brief.md)
- [Exporter observability Task](tsk-0046-exporter-observability.md)
