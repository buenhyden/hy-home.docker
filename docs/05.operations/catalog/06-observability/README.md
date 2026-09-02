---
title: Operations — 06 Observability
version: 1.0.0
type: operation/domain-readme
layer: operations
owner: "@buenhyden"
---

# Operations — 06 Observability

> Observability operations documents grouped by stable service and retention subjects.

## Overview

This domain co-locates the existing LGTM, Alloy, alerting, profiling, and
retention roles under their current four-digit subject directories.

## Audience

- Operators, SREs, observability engineers, developers, and AI agents.

## Scope

- Existing observability usage, approved controls, recovery procedures, and
  retention boundaries.
- No service startup, alert delivery, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Alertmanager](0039-alertmanager/guide.md) | [Guide](0039-alertmanager/guide.md), [Policy](0039-alertmanager/policy.md), [Runbook](0039-alertmanager/runbook.md) |
| [Alloy](0040-alloy/guide.md) | [Guide](0040-alloy/guide.md), [Policy](0040-alloy/policy.md), [Runbook](0040-alloy/runbook.md) |
| [Grafana](0041-grafana/guide.md) | [Guide](0041-grafana/guide.md), [Policy](0041-grafana/policy.md), [Runbook](0041-grafana/runbook.md) |
| [LGTM stack](0042-lgtm-stack/guide.md) | [Guide](0042-lgtm-stack/guide.md) |
| [Loki](0043-loki/guide.md) | [Guide](0043-loki/guide.md), [Policy](0043-loki/policy.md), [Runbook](0043-loki/runbook.md) |
| [Optimization hardening](0044-optimization-hardening/guide.md) | [Guide](0044-optimization-hardening/guide.md), [Policy](0044-optimization-hardening/policy.md), [Runbook](0044-optimization-hardening/runbook.md) |
| [Prometheus](0045-prometheus/guide.md) | [Guide](0045-prometheus/guide.md), [Policy](0045-prometheus/policy.md), [Runbook](0045-prometheus/runbook.md) |
| [Pushgateway](0046-pushgateway/guide.md) | [Guide](0046-pushgateway/guide.md), [Policy](0046-pushgateway/policy.md), [Runbook](0046-pushgateway/runbook.md) |
| [Pyroscope](0047-pyroscope/guide.md) | [Guide](0047-pyroscope/guide.md), [Policy](0047-pyroscope/policy.md), [Runbook](0047-pyroscope/runbook.md) |
| [Retention](0048-telemetry-retention/policy.md) | [Policy](0048-telemetry-retention/policy.md) |
| [Tempo](0049-tempo/guide.md) | [Guide](0049-tempo/guide.md), [Policy](0049-tempo/policy.md), [Runbook](0049-tempo/runbook.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [Observability infrastructure](../../../../infra/06-observability/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
- [Incident records](../../incidents/README.md)
