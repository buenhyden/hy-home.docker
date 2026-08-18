# Operations — 06 Observability

> Observability operations documents grouped by stable service and retention subjects.

## Overview

This domain co-locates the existing LGTM, Alloy, alerting, profiling, and
retention roles under their frozen `ops-0039` through `ops-0049` identities.

## Audience

- Operators, SREs, observability engineers, developers, and AI agents.

## Scope

- Existing observability usage, approved controls, recovery procedures, and
  retention boundaries.
- No service startup, alert delivery, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [Alertmanager](ops-0039-alertmanager/guide.md) | [Guide](ops-0039-alertmanager/guide.md), [Policy](ops-0039-alertmanager/policy.md), [Runbook](ops-0039-alertmanager/runbook.md) |
| [Alloy](ops-0040-alloy/guide.md) | [Guide](ops-0040-alloy/guide.md), [Policy](ops-0040-alloy/policy.md), [Runbook](ops-0040-alloy/runbook.md) |
| [Grafana](ops-0041-grafana/guide.md) | [Guide](ops-0041-grafana/guide.md), [Policy](ops-0041-grafana/policy.md), [Runbook](ops-0041-grafana/runbook.md) |
| [LGTM stack](ops-0042-lgtm-stack/guide.md) | [Guide](ops-0042-lgtm-stack/guide.md) |
| [Loki](ops-0043-loki/guide.md) | [Guide](ops-0043-loki/guide.md), [Policy](ops-0043-loki/policy.md), [Runbook](ops-0043-loki/runbook.md) |
| [Optimization hardening](ops-0044-optimization-hardening/guide.md) | [Guide](ops-0044-optimization-hardening/guide.md), [Policy](ops-0044-optimization-hardening/policy.md), [Runbook](ops-0044-optimization-hardening/runbook.md) |
| [Prometheus](ops-0045-prometheus/guide.md) | [Guide](ops-0045-prometheus/guide.md), [Policy](ops-0045-prometheus/policy.md), [Runbook](ops-0045-prometheus/runbook.md) |
| [Pushgateway](ops-0046-pushgateway/guide.md) | [Guide](ops-0046-pushgateway/guide.md), [Policy](ops-0046-pushgateway/policy.md), [Runbook](ops-0046-pushgateway/runbook.md) |
| [Pyroscope](ops-0047-pyroscope/guide.md) | [Guide](ops-0047-pyroscope/guide.md), [Policy](ops-0047-pyroscope/policy.md), [Runbook](ops-0047-pyroscope/runbook.md) |
| [Retention](ops-0048-retention/policy.md) | [Policy](ops-0048-retention/policy.md) |
| [Tempo](ops-0049-tempo/guide.md) | [Guide](ops-0049-tempo/guide.md), [Policy](ops-0049-tempo/policy.md), [Runbook](ops-0049-tempo/runbook.md) |

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
