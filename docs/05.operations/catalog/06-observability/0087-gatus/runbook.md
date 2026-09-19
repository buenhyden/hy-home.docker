---
title: "Gatus Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
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

### Native OIDC operation

The running service now uses `config.oidc.yaml` with native OIDC after owner
login acceptance. The router keeps only the standard gateway chain and excludes
the metrics prefix. The original `config.yaml` is preserved for configuration
rollback. Changing a live bind-mounted file
can affect the running service immediately. Do not edit the live file to prepare
an unapproved transition. Current rollout status belongs to
[Task 0004](../../../../03.specs/0180-home-dev-convergence/tasks/tsk-0004-native-oidc-service-migration.md).

The client is `home-gatus` with exact callback
`https://status.${DEFAULT_URL}/authorization-code/callback`, confidential code
flow and S256. Its client secret is a Docker Secret; the service runs as UID 1000
and requires a UID-1000-owned mode-0600 file. `GATUS_OIDC_ALLOWED_SUBJECT` is the
exact Keycloak user `sub`, not an email or display name. Empty allowlists must not
reach startup. The local CA is combined with public roots, not substituted for
them, and TLS verification remains enabled.

The pinned source build includes a reviewed patch for Secure/HttpOnly cookies,
S256 PKCE, transient-state cleanup and case-sensitive subject matching. Rebuilds
must verify the source archive checksum, apply the patch without fuzz and pass
Go security tests; a changed upstream pin requires patch review again.

For a subsequent approved rollout, preserve the existing image for rollback,
back up SQLite consistently, and replace only Gatus with the same data volume.
During a future migration or rollback requiring a temporary gateway, retain it
until allowed-subject login and denied/invalid-session checks pass. The current
accepted runtime has removed that temporary gateway. Verify cookie flags and native session expiry independently of container
health. Gatus's local session has a one-hour TTL in the active config; Keycloak
logout alone does not prove that local session has been revoked. Do not claim
cross-application single logout without a separate observed test.

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

- Runtime pins are owned by Compose/Dockerfile declarations; the [curated version projection](../../../../../infra/tech-stack.versions.json) verifies drift.

- [Operations index](../../../README.md)
- [Official Gatus configuration, storage and authentication](https://github.com/TwiN/gatus)
