---
title: "Gatus Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0087"
parent_ids:
- "POL-0087"
created: "2026-09-19"
---

# Gatus Guide

## Usage

Gatus provides always-on HOME endpoint availability checks. Service `gatus` is selected by `availability`, `obs` or `dev`; root Compose owns inclusion. Configuration is mounted read-only from the tracked config directory. SQLite history persists at `/data/gatus.db` on `gatus-data`.

The UI is served through authenticated Traefik at the status hostname. There is no direct host publication. `GATUS_PORT` owns its internal listener and gateway backend. Endpoint success measures each configured probe, not full application acceptance.

## Common Checks

Validate the public Compose model, inspect service health and confirm the gateway requires authentication. Review configured endpoint names and status codes without publishing bodies or private configuration. Separate a failed monitored dependency from failure of Gatus itself.

## Runbook Handoff

The [runbook](runbook.md) owns bounded checks and recovery. The [policy](policy.md) owns exposure, data and approval controls.

[Compose](../../../../../infra/06-observability/docker-compose.yml) owns activation, mounts and routing. [Dockerfile](../../../../../infra/06-observability/gatus/Dockerfile) owns upstream build pins; the local image name is not an upstream version. Gateway image provenance is available through the [curated version projection](../../../../../infra/tech-stack.versions.json).

## Traceability

- [AD-0031](../../../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Official Gatus configuration, storage and authentication](https://github.com/TwiN/gatus)
