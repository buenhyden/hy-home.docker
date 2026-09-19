---
title: "Gatus Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0087"
parent_ids:
- "POL-0087"
created: "2026-09-19"
---

# Gatus Runbook

## When to Use

Use for Gatus readiness, missing probe results or approved deployment and recovery. Work from the repository root. Record the configuration commit, actual mounted data path and backup destination before a runtime mutation.

## Procedure

1. Validate the public configuration without printing the rendered environment:

```bash
docker compose --env-file .env.example --profile availability config --quiet
docker compose --profile availability ps gatus
docker compose --profile availability exec -T gatus sh -ec 'wget -q -O /dev/null "http://127.0.0.1:${PORT}/health"'
```

1. Confirm the status route requests authentication and review probe status through an authorized session. Do not copy response bodies, tokens or endpoint credentials into evidence.
2. For approved deployment, build and replace only `gatus` using the reviewed Compose selection. Verify container health, UI authentication and expected probe names separately. Stop on unexpected mounts, permissions or image identity.

## Evidence

Record date, commit, service name, exit codes and sanitized health/probe outcomes in the current Task. Source validation alone does not establish runtime readiness or restored history.

## Rollback or Recovery

A consistent SQLite backup requires a coordinated snapshot or approved quiescence; copying only the live database file can omit WAL state. Obtain a protected backup of the entire data directory, preserving ownership, after approved shutdown. Restore into isolated storage and verify history and new probes before authorizing replacement of production data. Roll back configuration and image independently; never delete the volume as a troubleshooting default.

## Escalation

Stop and contact @buenhyden for missing backups, authentication failures, unknown data paths or any destructive replacement. Deployment and shutdown require a concrete approved target.

[Compose](../../../../../infra/06-observability/docker-compose.yml) owns activation, mounts and routing. [Dockerfile](../../../../../infra/06-observability/gatus/Dockerfile) owns upstream build pins; the local image name is not an upstream version.

## Traceability

- [AD-0031](../../../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Official Gatus configuration, storage and authentication](https://github.com/TwiN/gatus)
