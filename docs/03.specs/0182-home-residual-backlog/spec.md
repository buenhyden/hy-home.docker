---
title: "HOME Residual Backlog Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0182"
parent_ids:
- "REQ-0027"
created: "2026-09-24"
---

# HOME Residual Backlog Specification

## Overview

Hold the SPEC-0180 residuals that the owner did not put in
[SPEC-0181](../0181-home-residual-operations/spec.md) on 2026-09-24:
recovery rehearsals and custody design, authentication acceptance, legacy
data, runtime follow-ups and repository follow-ups. This package tracks them
until the owner orders them into work or retires them.

## Boundaries and Inputs

Inputs are the archived SPEC-0180 Tasks, SPEC-0181 as first drafted, current
tracked source and the owning Stage 05 subjects. Live mutation, credential
work, data disposal and remote changes each need their own approval. Secret
values never enter output, diffs, Tasks or PRs.

Items at entry:

- **Recovery and custody design (owner):** an offsite backup target;
  PostgreSQL point-in-time recovery on HOME data (only the synthetic rehearsal
  ran); isolated stateful restore rehearsals, including MLflow, JupyterLab and
  CDC; cold start and host reboot rehearsals, with RPO/RTO still unverified
  planning ceilings; sustained and peak CPU/RAM/GPU and growth measurement;
  the Restic and pgBackRest same-host limit; the manual unseal versus
  auto-unseal decision for OpenBao.
- **Secrets (owner):** SEC-002 provisioning and runtime acceptance; a plan
  for tightening host secret files still at mode 664 without breaking
  container reads.
- **Authentication acceptance (owner):** the SSO route matrix (401/403, a
  non-allowed user, logout, role removal, Valkey outage); Terrakube's Keycloak
  client and removal of its API ForwardAuth at `iac` activation.
- **Legacy data (owner approval):** the MinIO data volume and
  `secrets/storage/minio_*.txt`; preserved Vault data, `vault_token.txt` and
  `vault_unseal_keys.legacy.txt`.
- **Runtime follow-ups (approved recreate):** `mng-pg` rebuild for the quieter
  `archive-push` log level; single-file config bind mounts that keep their
  original inode after a host edit; an assessment of running containers
  outside the HOME selection before any stop.
- **Repository follow-ups:** a Qdrant read-only API key for Prometheus; Open
  WebUI `VECTOR_DB_URL` without `VECTOR_DB`; the n8n queue host
  `mng-n8n-valkey` that no service declares; SeaweedFS metrics, scrape job
  and alerts; the runtime-version check reading SMTP enhanced status codes as
  pins; `examples/operations/compose-core-readiness/` still on `INFRA_*` keys
  and a Vault rig; Renovate host units reinstalled by copy; from the CI
  alignment round, remote branch protection changes, further remote workflow
  cleanup, atomic pre-commit update ownership, digest maintenance, caching
  and non-gating workflow retention.

## Behavior Contract

An item closes only with evidence of its kind, or is retired with the owner's
recorded reason. A failed or unexecuted step is never recorded as done.

## Technical Approach

The owner orders the items; a Plan then groups them by owner and approval, and
repository follow-ups go through reviewed PRs with regression tests where
logic changes.

## Interfaces and Data

Backup and restore (POL/RUN-0021), OpenBao (RUN-0085), the gateway and SSO
subjects, Compose services, the secret registry and the validators named
above. Evidence records names, paths, counts and statuses only.

## Failure Modes and Guardrails

Do not delete legacy data or secret files without an approval that names
them. Do not treat a rehearsal on synthetic data as a HOME recovery result.

## Acceptance Contract

1. Every item above is closed with evidence of its kind or retired with the
   owner's recorded reason.
2. Recovery results state what was restored, from where, and what stays
   unverified.
3. Repository follow-ups merge with their focused checks recorded.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [SPEC-0180](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md)
- [SPEC-0181](../0181-home-residual-operations/spec.md)

## Open Questions

The owner sets the order and chooses which items to retire. The offsite
target and the auto-unseal choice are open design decisions.

## Operational Impact

None until an item runs.
