---
title: "Docker Registry Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0065"
parent_ids:
- "GDE-0065"
created: "2026-05-17"
---

# Docker Registry Runbook

## When to Use

Use for `/v2/` failure, push/pull or digest mismatch, storage exhaustion, a
consistent backup/restore, an upgrade, or separately approved garbage collection.

## Procedure

1. From the repository root validate and capture bounded status:

   ```bash
   docker compose --profile registry config --quiet
   docker compose --profile registry ps registry
   docker compose --profile registry logs --tail=200 registry
   ```

2. Confirm `${DEFAULT_REGISTRY_DIR}` exists, is on the expected filesystem, and
   has adequate free space without listing private artifact contents. Verify the
   client reaches the intended trusted endpoint; do not widen firewall/client trust.
3. For a digest mismatch, stop promotion, record expected/observed digests, and
   pull from a known source. Do not retag over evidence or delete blobs.
4. Restart only `registry` after storage and network checks. Verify `/v2/`, then
   push/pull one non-sensitive canary and compare its digest.

### Consistent backup and restore

1. Block pushes/pulls and stop `registry` because the tracked config has no
   read-only maintenance mode.
2. Snapshot or copy the entire `${DEFAULT_REGISTRY_DIR}` filesystem to protected
   storage. Record source commit, filesystem snapshot/checksum, and repository/
   tag/digest inventory. Start the source only after snapshot completion.
3. Restore into an isolated Registry with no untrusted network route. Verify API,
   catalog/tag counts, and pull a representative set by digest.
4. Promote the restored store only after digest verification and explicit data
   replacement approval.

### Garbage collection and upgrade

- GC is destructive: take/verify the backup, keep the registry stopped or
  configure reviewed read-only mode, run a dry-run if supported, review the mark
  set, then execute only under explicit approval. Verify required digest pulls.
- For upgrade, test the new image against an isolated restored copy first. Verify
  canary push/pull and digest equality; revert image plus storage snapshot if the
  format or behavior is incompatible.

## Evidence

Record exits, endpoint boundary, source commit, snapshot ID/checksum, counts,
selected digests, and final service state. Do not capture credentials or layers.

## Rollback or Recovery

Backup/restore, GC, and upgrade rehearsal are **planned but unexecuted** here.
Never use `rm` on Registry storage as a recovery step.

## Escalation

Stop on untrusted exposure, unknown artifact provenance, missing backup, digest
mismatch, filesystem corruption, or requests for deletion/GC without approval.

## Traceability

- [Guide](guide.md) (`GDE-0065`)
- [Policy](policy.md) (`POL-0065`)
- [Registry Compose](../../../../../infra/09-tooling/registry/docker-compose.yml)

## Related Documents

- [Registry deployment](https://distribution.github.io/distribution/about/deploying/)
- [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
