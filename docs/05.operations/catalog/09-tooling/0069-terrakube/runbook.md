---
title: "Terrakube Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "RUN-0069"
parent_ids:
- "GDE-0069"
created: "2026-05-17"
---

# Terrakube Recovery Runbook

## When to Use

Use for API/UI/executor failure, stuck runs, OIDC failure, missing state/output,
or an approved backup/restore/upgrade. Work from the repository root.

## Procedure

1. Freeze new Terrakube runs. Record workspace/run IDs, VCS ref, state key,
   component status, and whether any apply is active. Do not stop an active apply
   until its remote effect and recovery owner are understood.
2. Validate and inspect bounded state:

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac ps terrakube-api terrakube-ui terrakube-executor
   docker compose --profile iac logs --tail=200 terrakube-api terrakube-ui terrakube-executor
   ```

3. Classify before restarting:
   - UI only: inspect gateway and OIDC redirect/claims.
   - API DB errors: inspect `mng-pg`; do not retry migrations repeatedly.
   - missing state/output: inspect SeaweedFS bucket/key and DB reference without
     downloading state into logs.
   - stuck execution: inspect Valkey coordination and executor/Docker access;
     confirm remote provider action before cancellation or replay.
4. Restart only the failed component after the dependency and active-run check.
   Replaying a job or apply requires separate authorization.

### Coordinated backup and isolated restore

1. Block scheduling, wait for or safely resolve active runs, then stop API/UI and
   executor so no Terrakube writer remains.
2. Use the PostgreSQL owner's online logical/physical backup procedure and the
   SeaweedFS set in the daily backup (RUN-0024) for `tfstate`. Record one recovery-point
   receipt joining DB backup ID, object snapshot/version inventory, source commit,
   and Keycloak/client configuration. Capture no secret/state contents.
3. Restore both stores to isolated targets. Use replacement secrets and disable
   provider, VCS webhook, and executor egress.
4. Start the restored component set against only the isolated stores. Verify
   organization/workspace/run counts, referenced state/output keys, OIDC role
   mapping, and a non-applying plan. Do not point the restored executor at live accounts.
5. Promote only after review; otherwise discard the isolated copy and leave the
   source unchanged.

### Upgrade

Complete the coordinated backup, review every migration/release note, test the
new API/UI/executor against restored stores, then upgrade the compatible set.
On failure, stop the new set and restore both DB and objects with the prior images.

## Evidence

Record sanitized component health, run/workspace counts, backup IDs/checksums,
state-key counts, release/source commit, non-applying plan result, and final state.

## Rollback or Recovery

These coordinated backup/restore and upgrade steps are **planned but unexecuted**.
Do not claim recovery from a component restart or one-store snapshot.

## Escalation

Stop on an active/unknown apply, missing DB-object consistency, Docker-socket
unexpected access, auth ambiguity, unavailable backup, or destructive migration.

## Traceability

- [Guide](guide.md) (`GDE-0069`)
- [Policy](policy.md) (`POL-0069`)
- [Terrakube Compose](../../../../../infra/09-tooling/terrakube/docker-compose.yml)

## Related Documents

- [Terrakube documentation](https://docs.terrakube.io/)
- [Operations index](../../../README.md)
