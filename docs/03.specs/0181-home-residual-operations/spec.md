---
title: "HOME Residual Operations Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0181"
parent_ids:
- "REQ-0027"
created: "2026-09-24"
---

# HOME Residual Operations Specification

## Overview

Carry the open work that SPEC-0180 recorded as residual risk when the owner
completed it on 2026-09-24: owner-run custody and recovery work, live
acceptance that never ran, retained legacy data, and repository follow-ups
found during its S00–S19 stages. This package tracks and closes them; it does
not reopen SPEC-0180's delivered scope.

## Boundaries and Inputs

Inputs are the SPEC-0180 Tasks, especially Task 0008's deferred list and live
list, the hy-home.k8s handoff of 2026-09-24 (the notifications entry and the
Kiali token), the CodeQL results on #250, current tracked source and the owning
Stage 05 subjects. Each item keeps
its owner. Live mutation, credential work, data disposal and remote changes
each need their own approval, as in SPEC-0180. Secret values, unseal shares,
tokens and snapshot contents never enter output, diffs, Tasks or PRs.

Items at entry:

- **Custody and recovery (owner):** OpenBao raft snapshot to offline custody
  under POL-0021 (none exists on the host); offline custody of the recovery
  shares; an offsite backup target; PostgreSQL point-in-time recovery on HOME
  data (only the synthetic rehearsal ran); isolated stateful restore
  rehearsals (including MLflow, JupyterLab and CDC), cold start and host
  reboot rehearsals, with RPO/RTO still unverified planning ceilings; sustained
  and peak CPU/RAM/GPU and growth measurement; the Restic and pgBackRest
  same-host limit.
- **OpenBao operations (owner):** `secret/platform/notifications`
  (`slack_token`) for the hy-home.k8s Argo CD notifications, which needs a root
  session or an operator policy grant; confirmation of the `k8s-bootstrap` token
  role cap of `7200` (RUN-0096 Session 3); Agent SecretID delivery after each
  Agent restart; the manual unseal versus auto-unseal decision; the metrics
  token expiry on 2026-10-22 with no alert; the Kiali Grafana token expiry on
  2026-12-22 (reminder 2026-12-15); SEC-002 provisioning and runtime
  acceptance; a plan for tightening host secret files still at mode 664
  without breaking container reads.
- **Authentication acceptance (owner):** the SSO route matrix (401/403, a
  non-allowed user, logout, role removal, Valkey outage); Terrakube's Keycloak
  client and removal of its API ForwardAuth at `iac` activation.
- **Legacy data (owner approval):** MinIO data volume and
  `secrets/storage/minio_*.txt`; preserved Vault data, `vault_token.txt` and
  `vault_unseal_keys.legacy.txt`.
- **Runtime follow-ups (approved recreate):** `mng-pg` rebuild for the quieter
  `archive-push` log level; single-file config bind mounts that keep their
  original inode after a host edit; an assessment of running containers outside
  the HOME selection before any stop (SPEC-0180 Task 0005).
- **Repository follow-ups:** a Qdrant read-only API key for Prometheus; Open
  WebUI `VECTOR_DB_URL` without `VECTOR_DB`; n8n queue host
  `mng-n8n-valkey` that no service declares; SeaweedFS metrics, scrape job and
  alerts; the runtime-version check reading SMTP enhanced status codes as
  pins; `examples/operations/compose-core-readiness/` still on `INFRA_*` keys
  and a Vault rig; Renovate host units reinstalled by copy; three CodeQL
  `py/clear-text-storage-sensitive-data` alerts on test rehearsal passwords;
  from the CI alignment round, remote branch protection changes, further
  remote workflow cleanup, atomic pre-commit update ownership, digest
  maintenance, caching and non-gating workflow retention.

## Behavior Contract

An item closes only with evidence of the kind it names: a live result for live
work, a merged change with its checks for repository work, an owner record for
custody. An item may instead be retired with the owner's recorded reason. A
failed or unexecuted step is never recorded as done.

## Technical Approach

Group items by owner and approval so that one approved session closes several
items, for example one OpenBao session for the snapshot, the notifications
entry and the token role check. Repository follow-ups go through ordinary
reviewed PRs with regression tests where logic changes. The Plan orders the
groups once the owner sets priorities.

## Interfaces and Data

OpenBao KV paths and policies, Stage 05 runbooks (RUN-0021, RUN-0024,
RUN-0085, RUN-0096), POL-0021 retention and custody, Compose services and the
validators named above. Evidence records names, paths, counts and statuses
only.

## Failure Modes and Guardrails

Do not request or display tokens, shares or snapshot contents. Do not delete
legacy data or secret files without an approval that names them. Do not widen
an OpenBao policy beyond the paths an item needs.

## Acceptance Contract

1. Every item above is closed with evidence of its kind or retired with the
   owner's recorded reason.
2. Custody and recovery results state what was restored or stored, where, and
   what stays unverified.
3. Repository follow-ups merge with their focused checks recorded.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0031 Home and Development Host](../../02.architecture/descriptions/0031-home-development-host.md)
- [SPEC-0180](../0180-home-dev-convergence/spec.md)
- [SPEC-0180 Task 0008](../0180-home-dev-convergence/tasks/tsk-0008-storage-security-lakehouse-convergence.md)

## Open Questions

The owner sets the order and decides which items to retire instead of doing.
The offsite target and the auto-unseal choice are open design decisions.

## Operational Impact

None until an item runs. Each live item states its target, blast radius,
verification and rollback before its approval.
