---
title: "Hermes OTLP Observability Task"
version: "0.1.0"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hermes ingest source and tests | 108 | W113 | Receiver, route, port and dashboard contract tests | Alloy, Compose and dashboard change | NOT_RUN | Implementation in progress. | required | - |
| Hermes live telemetry readback | 108 | W113 | One Hermes trace in Tempo, one log line in Loki and one gateway metric in Prometheus | HOME after the approved apply | NOT_RUN | Waits for O1, O2 and the Alloy recreate. | required | - |

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
