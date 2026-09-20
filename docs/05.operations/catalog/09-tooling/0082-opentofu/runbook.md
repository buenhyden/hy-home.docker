---
title: "OpenTofu Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0082"
parent_ids:
- "POL-0082"
created: "2026-09-19"
---

# OpenTofu Runbook

## When to Use

Use for a reviewed plan, lock failure, protected state backup/recovery, or
runtime/provider upgrade. Work from the repository root. Commands that access a
backend/provider require the authorization named below.

## Procedure

1. Record configuration commit, exact workspace directory, selected OpenTofu
   workspace, backend, account, command class, and rollback owner. Confirm no
   other writer is active.
2. Run static checks without provider authority:

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac run --rm opentofu version
   ```

3. For an authorized plan, initialize the exact workspace, select the intended
   OpenTofu workspace, and run validation before creating a saved plan. Store the
   plan outside Git with restrictive permissions. Record only its digest and
   resource action counts.
4. Stop before `apply`. A reviewer must bind the saved plan digest, account, and
   expected changes to explicit apply approval. Never substitute `-auto-approve`
   for this boundary.

### State backup and recovery

1. Determine local or remote backend and prove no active writer/lock owner.
2. For local state, copy the state and its backup files to a protected directory
   with mode `0600`. For remote state, prefer the backend's atomic/versioned
   snapshot. If using `tofu state pull`, redirect directly to a protected file;
   do not display it.
3. Verify checksum, backend/workspace identity, and protected retention. A file
   existing is not restore proof.
4. Restore first against an isolated backend with external provider/network
   access disabled. Compare lineage, serial, and `state list` privately.
5. `tofu state push` is a last-resort separately approved write. Preserve the
   current remote snapshot first and do not use `-force` to bypass lineage or
   serial protection unless the approval names that exact loss-acceptance case.

### Lock and upgrade recovery

- For a lock error, identify the holder and wait/stop the writer. Use
  `force-unlock` only for the operator's own abandoned lock ID.
- Before upgrading, take the state backup above, read intervening upgrade notes,
  rebuild the local image, initialize without changing backend settings, and
  compare a non-applied plan. Roll back the image/build if compatibility fails;
  roll back state only from the tested backup when the upgrade changed state.

## Evidence

Record exits, version, configuration/plan digests, backend/workspace identifiers,
sanitized action counts, lock owner decision, and final disposition. Never record
state, plan body, credentials, or provider responses containing secrets.

## Rollback or Recovery

Reverting Git or the image does not revert remote resources. Resource rollback
requires a new reviewed plan. State restore and upgrade rehearsal are currently
**planned but unexecuted** in this repository.

## Escalation

Stop on an unknown backend/workspace, missing protected backup, active lock
owner, lineage/serial mismatch, destructive plan, or credential/account ambiguity.

## Traceability

- [Guide](guide.md) (`GDE-0082`)
- [Policy](policy.md) (`POL-0082`)
- [OpenTofu Compose](../../../../../infra/09-tooling/opentofu/docker-compose.yml)

## Related Documents

- [OpenTofu state locking](https://opentofu.org/docs/language/state/locking/)
- [OpenTofu upgrading](https://opentofu.org/docs/intro/upgrading/)
- [Operations index](../../../README.md)
