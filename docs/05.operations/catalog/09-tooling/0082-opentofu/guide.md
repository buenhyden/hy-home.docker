---
title: "OpenTofu Guide"
version: "0.2.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0082"
parent_ids:
- "POL-0082"
implementation_services:
  infra/09-tooling/opentofu/docker-compose.yml:
  - opentofu
created: "2026-09-19"
---

# OpenTofu Guide

## Usage

### Purpose and runtime boundary

OpenTofu is an on-demand DEV IaC CLI job. It belongs only to the `iac` profile
and is excluded from HOME and general `tooling`. The root project builds a local
image from the inline Dockerfile, mounts `./workspace` read-write at `/workspace`,
and mounts the operator's AWS and Azure credential directories read-only. A
read-only credential mount still grants remote API authority.

The job has no daemon healthcheck and `restart: "no"`. `template-job-low`
defines its resource/security baseline. the declared networks allows provider/backend
network access. There are no Docker secrets or published ports in this leaf.

### State and command semantics

- The selected workspace configuration decides whether state is a local file in
  `/workspace` or a remote backend. The Compose file does not choose a backend.
- `tofu plan` reads provider APIs and state but does not change managed resources.
  It can still refresh state and emit sensitive values in plan output.
- `tofu apply`, `destroy`, `import`, `state push`, `force-unlock`, and state
  mutation are remote/destructive actions requiring exact separate approval.
- Backends provide storage and may provide locking. Do not disable locking. Use
  `force-unlock` only for the operator's own abandoned lock after proving no
  writer remains.

### Normal use

1. Work from the repository root and identify the exact directory below
   `infra/09-tooling/opentofu/workspace`, backend, workspace name, account, and
   expected resources.
2. Run `docker compose --profile iac config --quiet` and confirm only the
   expected IaC services with `docker compose --profile iac config --services`.
3. A no-authority smoke check is `docker compose --profile iac run --rm opentofu version`.
4. With read-only provider/backend authorization, run initialization, formatting,
   validation, and a reviewed plan for the exact workspace. Keep plan and state
   files in a protected path outside Git and do not paste their contents into
   evidence.
5. Applying a saved plan is a separate decision. Record plan digest, resource
   counts, approval, exit status, and post-apply checks without recording secrets.

### Backup and upgrade

Before an upgrade or state operation, determine the backend. For local state,
stop all writers and make a mode-0600 copy of the state and backup files. For a
remote backend, use its atomic/versioned backup facility or `tofu state pull`
to a protected file; never send the output to a terminal or chat. Verify an
isolated restore against a disconnected/test backend before relying on it.
Review every intervening OpenTofu upgrade note and test the saved plan workflow
without applying. No plan, state backup, restore, or provider call was executed
for this documentation change.

## Common Checks

- `docker compose --profile iac config --quiet`
- `docker compose --profile iac run --rm opentofu version`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

Use the [runbook](runbook.md) for state recovery, lock diagnosis, plan/apply
separation, and upgrades.

## Traceability

- [Policy](policy.md) (`POL-0082`)
- [Runbook](runbook.md) (`RUN-0082`)
- [OpenTofu Compose](../../../../../infra/09-tooling/opentofu/docker-compose.yml)

## Related Documents

- [OpenTofu provisioning workflow](https://opentofu.org/docs/cli/run/)
- [State storage and locking](https://opentofu.org/docs/language/state/backends/)
- [State locking](https://opentofu.org/docs/language/state/locking/)
- [Upgrade guide](https://opentofu.org/docs/intro/upgrading/)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [Operations index](../../../README.md)
