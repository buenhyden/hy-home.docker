---
title: "HOME Residual Backlog Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0182-PLAN-0001"
parent_ids:
- "SPEC-0182"
created: "2026-09-25"
---

# HOME Residual Backlog Plan

## Objective

Close the twelve [Spec](spec.md) criteria through three Tasks, each work unit
ending in a merged change or a recorded live result.
[Task 0003](tasks/tsk-0003-recovery-and-auth-acceptance.md) holds the
completion receipt.

## Dependencies

- Docker on the HOME host; the running `hy-home-infra` project; the main
  checkout for live applies (pulled with `umask 022`).
- The owner for secret generation, deletion and recreate approvals, Keycloak
  test identities, browser checks, the measurement window, the two design
  decisions and the reboot window.
- W11 follows W10; the reboot runbook documents the unseal method in place.

## Execution Sequence

Run order: W1, W2 (its SeaweedFS S3 recreate batched with W4's SeaweedFS
recreates), W12, W6, W4, W3, W5, W7, W8, W10, W9, W11. W6 precedes W4 so only
kept services are recreated; W3 never overlaps W9; W11 follows W10.

Task 0001, repository follow-ups:

1. W1: Six changes, each with a focused test: the n8n exporter target
   (`n8n-valkey`, default port), asserted on the rendered configuration; the
   runtime-version check ignoring SMTP enhanced status codes and section
   numbers, with a guard that a real `x.y.z` pin is still flagged; the Open
   WebUI `VECTOR_DB_URL` removal with its RAG, guide, policy and README
   corrections; the compose-core-readiness orphan `.env.example` removal and
   a generic-fixture note; SeaweedFS S3 `-metricsPort`, a Prometheus job in
   both configurations, an `up` alert and a data-disk free-space alert; a
   Qdrant read-only key (AI-009, at least 16 characters, different from
   AI-008) granted to Prometheus instead of AI-008.
2. W2: After merge: the owner generates AI-009; recreate Qdrant with both keys
   and check `/metrics` with the read-only key before switching; then
   recreate Prometheus and Open WebUI, and SeaweedFS S3 in the W4 window;
   verify both targets `up`, the new rules loaded and Open WebUI healthy; run
   the W4 hash check.

Task 0002, runtime and legacy data:

1. W3: RUN-0021 step 2 with `umask 077` for its dump (deleted after
   verification) and the current image tagged `:pre-0182` for rollback; build
   and recreate `mng-pg` outside the SSO checks; verify `pgbackrest check`, no
   new `archive-push` INFO lines, and the CDC connector and task `RUNNING`
   with `hyhome_app_slot` active and `wal_status` not `lost`.
2. W4: Add the recreate-on-edit rule to the owning operations document and a
   hash check script (reading shell-less containers with `docker cp`) that
   every live apply runs; recreate the kept stale services, SeaweedFS in the
   order master, volume, filer outside `hyhome-backup.timer`, then check Loki
   and Tempo flush errors and that vacuum is enabled; run the check clean.
3. W5: Preconditions: the three `hyhome-migration/*.cutover` markers exist and
   the MLflow artifact counts match. Record the final inventory (data hashes
   through a read-only container; credential files by name, size, mode and
   time). With an approval naming each target and command: remove the
   `security/vault` Restic include and confirm the next snapshot lacks it;
   remove the MinIO volume, then its directory (root-level), the Vault tree
   (root-level), the quarantined MinIO and Vault files,
   `secrets/.backup-20260923/` and both images. Correct RUN-0024, RUN-0085,
   POL-0021 and `secrets/README.md`, record the SPEC-0180 S07 rollback path as
   ended and the legacy Vault root token as moot.
4. W6: Tabulate the running containers outside the HOME selection (profile,
   reason, consumers, state, stop risk, including CDC's WAL on `mng-pg`);
   record the owner's decision for each; stop what the owner stops; amend
   POL-0078 if HOME changes.

Task 0003, recovery and authentication acceptance:

1. W7: RUN-0021 step 5 against the real pgBackRest repository; MLflow
   (RUN-0088) on a named isolated network with no route to production
   SeaweedFS or `mng-pg`; JupyterLab (RUN-0089) on real content; CDC through
   RUN-0036's planned isolated restore, steps 4–6, against a disposable
   source. Scratch on the data disk, root-level cleanup. Record recovery
   points, counts and elapsed times against the POL-0021 RPO and RTO.
2. W8: Prometheus queries over the owner's window for p95 and maximum CPU,
   memory, GPU and disk growth per service and host; record them with AD-0031.
3. W9: Document the SSO behavioural matrix in GDE-0079; run the no-cookie
   probes (agent) and the non-allowed user, logout and role removal checks
   (owner); for Valkey unreachable, disconnect only OAuth2 Proxy from the
   Valkey network and reconnect it (its own approval). Every row gets pass,
   fail or owner-declined with a reason.
4. W10: Options memos for the offsite backup target (with the same-host
    limit) and OpenBao auto-unseal; the owner decides; an ADR records each
    decision; implement the chosen options, or record the deferral's owner
    and trigger or date.
5. W11: Write the cold start and reboot runbook for the unseal method in
    place (ordered start, unseal, owner-run SecretID delivery, health gates,
    timing, the hy-home.k8s containers); take a fresh pgBackRest and Restic
    backup and `restic check` first; run one supervised reboot.
6. W12: Record the entry-closed and retired items with their evidence and
    reasons.

## Risk and Rollback

- Every recreate keeps the previous image or configuration commit;
  `mng-pg` rolls back to its `:pre-0182` tag under RUN-0021 step 2.
- `mng-pg` restarts every management-database consumer, Keycloak included:
  SSO is down for that window, and CDC must be checked after it.
- SeaweedFS recreates briefly interrupt Loki, Tempo and MLflow writes and
  must not overlap the nightly backup.
- Deletion is irreversible: it runs only after the preconditions and final
  inventory, and only on the named targets. Existing Restic snapshots keep
  the deleted data until retention expires.
- Restore rehearsals use data-disk scratch, named isolated networks and a
  disposable CDC source; dumps are owner-only and deleted.
- The Valkey check disconnects only OAuth2 Proxy; stopping `mng-valkey` would
  stall n8n and Airflow.
- The reboot rehearsal needs the owner present for the unseal and SecretID,
  and fresh backups first.

## Verification

Focused tests per repository change, promtool on rule changes, metadata,
links, operations catalog, corpus lifecycle and pre-commit; live checks by
target health, hashes, counts and log line counts, never by value.

## Rulings

- Mounts stay single-file; the rule and the hash check are the control.
- Existing Restic snapshots keep the Vault tree until retention expires;
  rewriting them is not worth its risk.
- Open WebUI keeps its local vector store; selecting Qdrant would need
  re-indexing and a secret, and nothing asks for it.
- The compose-core-readiness rig keeps Vault as a generic fixture; porting it
  to OpenBao touches about 200 lines of harness for no production gain.
