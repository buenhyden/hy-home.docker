---
title: "Docker Registry Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0065"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Docker Registry Operations Policy

## Overview

The Registry is an OPTIONAL artifact store. The current tracked endpoint lacks native
TLS/auth and therefore may serve only an explicitly confined trusted network.

## Policy Scope

Activation, exposure, image provenance/digests, filesystem retention, backup,
garbage collection, upgrade, and removal.

## Controls

- **Activation:** use `registry` or general `tooling`; it is excluded from HOME.
- **Exposure/auth:** do not assume firewall or daemon restrictions. Before
  sensitive use or broader access, implement and validate TLS plus authentication
  or a trusted authenticated reverse proxy. Insecure registry client settings are
  permitted only for the bounded DEV network and are not a production control.
- **Artifacts:** retain source authority and digest for each required image.
  Mutable tags are not recovery evidence.
- **Data/retention:** `/var/lib/registry` content and digest inventory are one
  recovery unit. Define retention before enabling delete; deletion is currently off.
- **Backup/restore:** stop or make the registry read-only, snapshot the full
  filesystem, and rehearse isolated catalog/tag/digest pulls before relying on it.
- **Garbage collection:** requires explicit destructive approval and a stopped or
  read-only registry. Never run GC while uploads can occur.
- **Resources:** monitor the `${DEFAULT_REGISTRY_DIR}` filesystem and leave enough
  capacity for backup/restore and upgrade testing; no invented threshold is policy.
- **Upgrade:** validate storage compatibility and push/pull by digest on a restored
  copy before changing the active image.
- **Removal:** classify every required artifact as reproducible or backed up and
  verify the successor before deleting storage.

## Exceptions

No exception permits untrusted plaintext credential transport, GC with writers,
or deleting the only copy of an artifact.

## Verification

`/v2/` health is insufficient. Runtime acceptance includes network boundary,
TLS/auth where required, push, pull, and digest equality.

## Review Cadence

Review when exposure, authentication, storage, deletion, image, or artifact
retention changes.

## Traceability

- [Guide](guide.md) (`GDE-0065`)
- [Runbook](runbook.md) (`RUN-0065`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Registry Compose source](../../../../../infra/09-tooling/registry/docker-compose.yml)
- [CNCF Distribution deployment](https://distribution.github.io/distribution/about/deploying/)
- [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
