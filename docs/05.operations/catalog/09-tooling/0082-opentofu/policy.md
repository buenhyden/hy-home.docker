---
title: "OpenTofu Policy"
version: "0.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0082"
parent_ids:
- "AD-0009"
created: "2026-09-19"
---

# OpenTofu Policy

## Overview

OpenTofu is an explicit `iac` job. Static selection and validation never imply
permission to read a provider account or mutate remote infrastructure.

## Policy Scope

The local image build, `/workspace`, mounted cloud credentials, backend state,
locks, plans, provider operations, upgrades, and service retirement.

## Controls

- **Activation:** invoke the named `opentofu` job from the root project under
  `iac`; never include it in HOME or general tooling startup.
- **Authorization:** identify account, workspace, backend, expected resources,
  and permitted command class. Plan authorization does not authorize apply,
  destroy, import, state mutation, or force-unlock.
- **Credentials:** mounted AWS/Azure directories are sensitive authority even
  when read-only. Do not add credentials to the workspace or capture their values.
- **State and plans:** state and saved plans may contain secrets. Keep them out of
  Git, stdout evidence, and shared logs; protect backups with mode `0600` and a
  separate retention owner.
- **Locking:** preserve backend locking. Force-unlock requires proof that no
  operator or automation owns the lock and targets only the recorded lock ID.
- **Backup/recovery:** identify local versus remote state, take a protected
  snapshot before state mutation/upgrade, and rehearse restore on isolated state.
- **Upgrade:** review intervening notes, verify provider/backend compatibility,
  and compare a non-applied plan before changing the runtime source.
- **Removal:** preserve workspace, backend state, credentials, and ownership
  records until all managed resources have a successor. Removing a container
  never destroys infrastructure intentionally.

## Exceptions

No exception may bypass separate mutation approval, state protection, or lock
ownership. Record scope, expiry, recovery artifact, and exit condition.

## Verification

Static Compose checks prove selection only. Runtime evidence separates version,
init/validate, plan, apply, and post-apply results. Unexecuted state restore and
upgrade rehearsal remain gaps.

## Review Cadence

Review before every provider/backend/runtime upgrade and whenever credential
mounts, network access, or workspace ownership changes.

## Traceability

- [Guide](guide.md) (`GDE-0082`)
- [Runbook](runbook.md) (`RUN-0082`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [OpenTofu Compose source](../../../../../infra/09-tooling/opentofu/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [OpenTofu state storage](https://opentofu.org/docs/language/state/backends/)
- [OpenTofu state command safety](https://opentofu.org/docs/cli/commands/state/)
- [Operations index](../../../README.md)
