---
layer: ops
description: "Rule for observability coverage, telemetry quality, and troubleshooting readiness."
---

# Ops — Observability Rule

## Case
- **[REQ-OBS-01]** Ensure core services have metrics/logs/traces coverage.
- **[REQ-OBS-02]** Keep telemetry labels/schema coherent for correlation.
- **[REQ-LOG-01]** Use structured logs with traceable context.

## Style
- **[PROC-OBS-01]** Validate observability pipelines after config changes.
- **[REQ-OBS-04]** Keep dashboards and signals actionable for operations.
- **[BAN-OBS-01]** Avoid blind spots on critical service paths.

## Validation
- [ ] Critical services emit usable telemetry.
- [ ] Correlation identifiers are present across key signals.
- [ ] Telemetry pipeline configuration is validated.
