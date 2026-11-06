---
title: "Observability Object Storage on SeaweedFS"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "ADR-0053"
parent_ids:
- "AD-0006"
created: "2026-11-06"
---

# ADR-0053: Observability Object Storage on SeaweedFS

## Context

The observability tier runs the Grafana LGTM stack (Loki, Grafana, Tempo,
Prometheus) with Grafana Alloy as the collector. Loki and Tempo store their
data in the shared SeaweedFS S3 service: the images are `hy/loki:*-seaweedfs`
and `hy/tempo:*-seaweedfs`, and each reads its own SeaweedFS S3 secret
(`seaweedfs_s3_loki_secret_key`, `seaweedfs_s3_tempo_secret_key`) and waits on
the `seaweedfs-buckets` job (`infra/06-observability/docker-compose.yml`). No
MinIO runtime exists. Long-term metrics storage is not implemented in tracked
Compose.

### Traceability

This record replaces ADR-0006, deleted in the same change (ADR-0051). ADR-0006
adopted the LGTM stack and Grafana Alloy, rejecting the ELK stack (heavy
memory and storage, weak tracing integration) and a vanilla OpenTelemetry
Collector (weaker Grafana ecosystem integration), and chose an S3 (MinIO)
backend for Loki and Tempo. The LGTM and Alloy decisions carry forward
unchanged; the backend is now SeaweedFS. Evidence is the current repository
configuration; no runtime state is claimed.

## Decision Drivers

- Metrics, logs and traces must correlate in one UI.
- One collector should replace per-signal agents.
- Object storage should be the shared S3 service the platform already runs,
  not a second one.

## Options

### Alternatives

- ELK stack: rejected; high memory and storage footprint and weak tracing
  integration.
- Vanilla OpenTelemetry Collector: rejected; weaker discovery and integration
  with Loki and Prometheus than Alloy.
- A dedicated MinIO for Loki and Tempo: rejected; it duplicates the shared
  SeaweedFS S3 service.
- LGTM with Alloy on the shared SeaweedFS S3: selected.

## Decision

1. Adopt the Grafana LGTM stack for metrics, logs and traces, navigated from
   one Grafana.
2. Adopt Grafana Alloy as the single collector for OTLP and Prometheus
   telemetry.
3. Loki and Tempo store their objects in SeaweedFS S3, each with its own
   bucket and its own credential injected as a Docker Secret.
4. The Loki and Tempo SeaweedFS collections are excluded from the backup state
   set (SPEC-0228); telemetry is rebuildable, not backed up.

## Consequences

- Positive: one Grafana UI for every signal; one collector to manage.
- Positive: object storage reuses the shared SeaweedFS service and its
  operations documents.
- Trade-off: Loki and Tempo depend on SeaweedFS availability; a SeaweedFS
  outage stops log and trace ingestion.
- Trade-off: Alloy's configuration language must be learned.

### Compliance

`scripts/hardening/check-all-hardening.sh 06-observability` and the CI
`infrastructure-hardening` job guard the tier. ELK is not excluded for a
specialized search need, which is evaluated on its own; commercial SaaS
migration is out of scope.

### Follow-up

None.

## Related Documents

- [REQ-0007 Observability](../../01.requirements/0007-observability.md)
- [AD-0006 Observability architecture](../descriptions/0006-observability-architecture.md)
- [ADR-0021 Observability hardening](0021-observability-hardening-and-ha-expansion-strategy.md)
