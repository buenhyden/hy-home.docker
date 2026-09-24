---
title: "HOME Residual Backlog Specification"
version: "0.3.0"
type: "sdlc/spec"
status: "review"
owner: "@buenhyden"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0182"
parent_ids:
- "REQ-0027"
created: "2026-09-24"
---

# HOME Residual Backlog Specification

## Overview

Close the SPEC-0180 residuals that [SPEC-0181](../../98.archive/completed/03.specs/0181-home-residual-operations/spec.md)
did not take: repository follow-ups, runtime follow-ups and legacy data, and
recovery and authentication acceptance. The owner put all three groups in
scope on 2026-09-25 and retired the rest with reasons recorded below.

## Boundaries and Inputs

Inputs are the archived SPEC-0180 and SPEC-0181 Tasks, two read-only
investigations of 2026-09-25 recorded in the Tasks, current tracked source and
the owning Stage 05 subjects (RUN-0021 backup and restore, RUN-0024
SeaweedFS, RUN-0085 OpenBao, POL-0078 profiles, GDE-0079 application
authentication, RUN-0088 MLflow, RUN-0089 JupyterLab, RUN-0036 Kafka).

Owner decisions of 2026-09-25:

- All three groups are in scope.
- Legacy data is disposed of completely: the MinIO data directory and
  volume, the preserved Vault tree, the quarantined MinIO and Vault files and
  both images. Restic stops including the Vault tree; existing snapshots age
  out under their retention instead of being rewritten.
- Single-file configuration bind mounts get a documented recreate-on-edit
  rule and a hash comparison check; stale services are recreated. Mounts are
  not converted to directories.
- The SeaweedFS S3 metrics listener is reachable from every `edge_net`
  service, including the code-running ones; nothing publishes it and Traefik
  does not route it, the metrics are low sensitivity, and the S3 API is on
  the same network, so this is accepted.
- The offsite backup target and OpenBao auto-unseal start as options memos;
  the owner decides, and the decision is recorded before implementation.
- Retired: Terrakube's Keycloak client and API ForwardAuth removal wait for
  `iac` activation (the decision is already in the Terrakube Compose file and
  GDE-0079); the CI alignment follow-ups (remote branch protection, workflow
  cleanup, pre-commit update ownership, digest maintenance, caching and
  non-gating workflow retention) are retired while CI passes steadily.
- Closed by evidence at entry: SEC-002 is the OpenBao metrics token that
  SPEC-0181 rotated and alerted on; no secret value file is at mode 664; the
  Renovate host units are regular copies identical to the repository.

Live mutation, credential work, data disposal and remote changes each need an
approval that names the target. Secret values never enter output, diffs,
Tasks or PRs.

## Behavior Contract

Each item closes only with evidence of its kind: a merged change with its
checks for repository work, a live result stated as names, statuses, counts
and durations for runtime work, and an owner record for decisions and
custody. A rehearsal on synthetic data is never reported as a HOME recovery
result. A failed or unexecuted step is never recorded as done.

## Technical Approach

Three Tasks carry the work. Task 0001 makes the repository changes and their
live applies. Task 0002 handles runtime follow-ups and legacy disposal in
approved windows. Task 0003 runs the recovery and authentication acceptance,
writes the two options memos and, after the owner's decisions, the reboot
runbook and its rehearsal. The agent runs every step that needs no secret
input; the owner runs steps that do, and makes the decisions.

## Interfaces and Data

Qdrant and Prometheus secrets and scrape jobs, Open WebUI environment, the n8n
Valkey exporter, SeaweedFS S3 metrics and alert rules, the document-metadata
runtime-version check, the compose-core-readiness example, the `mng-pg`
image, single-file bind mounts, legacy directories, volumes, files and
images, the Restic include set, pgBackRest and Restic repositories, Traefik
SSO routes, and Keycloak test identities.

## Failure Modes and Guardrails

Record a final inventory before any deletion: names, sizes and hashes for
data, and names, sizes, modes and times only for credential files. Do not
delete what the approval does not name; the approval names the exact
commands, including root-level removal for root- or container-owned trees.
Restore rehearsals run on the data disk, on named isolated networks, and never
reach production SeaweedFS, `mng-pg` or the production replication slot.
Database dumps are written owner-only and deleted after verification.

The SSO outage check cuts only OAuth2 Proxy off from Valkey (network
disconnect and reconnect). Stopping `mng-valkey` would also stall the n8n
queue and the Airflow broker and is out of scope. Recreating `mng-pg`
restarts every management-database consumer, Keycloak included, so SSO is
down for that window; it never overlaps the SSO checks.

Existing Restic snapshots keep the Vault tree and the quarantined credential
files (the host set covers all of `secrets/`) until their retention expires,
up to twelve months; that is the accepted cost of not rewriting snapshots.

## Acceptance Contract

1. Six repository changes merge, each with a focused test: the Qdrant
   read-only scrape key (AI-009); the Open WebUI `VECTOR_DB_URL` removal with
   its corrected documents; the n8n exporter target, asserted on the rendered
   configuration; SeaweedFS S3 metrics with its scrape job and alerts; the
   runtime-version check ignoring SMTP enhanced status codes and section
   numbers; the compose-core-readiness orphan `.env.example` removal.
2. The live applies run and are verified: Prometheus scrapes Qdrant with the
   read-only key and SeaweedFS S3 (`up` 1), their alert rules are loaded, and
   Open WebUI is healthy without the dead key.
3. `mng-pg` runs the rebuilt image: `pgbackrest check` succeeds, the
   `archive-push` INFO lines stop, and the CDC connector, its task and the
   replication slot are running and active afterwards.
4. The recreate-on-edit rule and a host-to-container hash check are in the
   repository, the check is part of every live apply, and every running
   single-file configuration mount the owner keeps matches its host file.
5. After a recorded final inventory and its preconditions (the SeaweedFS
   cutover markers, MLflow object counts), the legacy data named in the
   approval is gone: the MinIO directory and volume, the Vault tree, the
   quarantined MinIO and Vault files, `secrets/.backup-20260923/` and both
   images; `security/vault` is out of the Restic include set and a new
   snapshot lacks it; RUN-0024, RUN-0085, POL-0021 and `secrets/README.md`
   no longer describe the data as present, the SPEC-0180 S07 rollback path is
   recorded as ended, and the legacy Vault root token is recorded as moot.
6. Every running container outside the HOME selection has a recorded owner
   decision (keep or stop, "keep all" allowed), and the decisions are
   applied.
7. A PITR restore of HOME PostgreSQL data from the real pgBackRest
   repository, and isolated restores of MLflow, JupyterLab (real content) and
   CDC (RUN-0036 planned isolated restore, steps 4–6) are recorded with
   recovery points, counts and elapsed times compared with the POL-0021 RPO
   and RTO targets.
8. Sustained and peak CPU, memory, GPU and disk growth are measured over an
   owner-chosen window and recorded.
9. The SSO behavioural matrix (no cookie, non-allowed user, logout, role
   removal, Valkey unreachable) is documented, and every row has a recorded
   result: pass, fail, or declined by the owner with a reason.
10. Each of the offsite backup target (including the Restic and pgBackRest
    same-host limit) and OpenBao auto-unseal has an ADR recording the owner's
    decision; a chosen option is implemented, and a deferral names its owner
    and its trigger or date.
11. A cold start and reboot runbook for the unseal method in place at the
    time exists, and one supervised reboot rehearsal is recorded.
12. The retired and entry-closed items carry their recorded reasons and
    evidence: Terrakube, the CI alignment follow-ups, SEC-002, mode 664, the
    Renovate units, the Vault-based compose-core-readiness rig kept as a
    generic fixture, and Open WebUI keeping its local vector store.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [SPEC-0180](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [SPEC-0181](../../98.archive/completed/03.specs/0181-home-residual-operations/spec.md)
- [Plan](plan.md)
- [Task 0001: repository follow-ups](tasks/tsk-0001-repository-follow-ups.md)
- [Task 0002: runtime and legacy data](tasks/tsk-0002-runtime-and-legacy-data.md)
- [Task 0003: recovery and authentication acceptance](tasks/tsk-0003-recovery-and-auth-acceptance.md)

## Open Questions

The offsite target and the auto-unseal mechanism are open until the memos
are decided. The measurement window and the keep or stop list are the
owner's choices.

## Operational Impact

Recreates of Qdrant, Prometheus, SeaweedFS (S3, master, volume, filer), Open
WebUI, `mng-pg` and any kept Superset or Kafbat UI, each in an approved
window. `mng-pg` restarts every management-database consumer, Keycloak
included. The SeaweedFS recreates interrupt Loki, Tempo and MLflow writes
briefly and stay clear of the nightly backup. Legacy disposal frees about 1.2
GB. The reboot rehearsal takes the host, and the hy-home.k8s containers on it,
down.
