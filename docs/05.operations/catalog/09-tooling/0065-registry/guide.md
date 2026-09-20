---
title: "Docker Registry Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0065"
parent_ids:
- "POL-0065"
implementation_services:
  infra/09-tooling/registry/docker-compose.yml:
  - registry
created: "2026-05-10"
---

# Docker Registry Usage Guide

## Usage

### Purpose and classification

The Registry is an on-demand OPTIONAL OCI image store under `tooling` and `registry`.
It stores pushed manifests and blobs in `${DEFAULT_REGISTRY_DIR}`. Locally built
images may be reproducible from tracked Dockerfiles; pushed third-party or unique
artifacts are recoverable only when their digests/content are backed up or still
available from a trusted upstream.

### Current implementation and security gap

- [Registry Compose](../../../../../infra/09-tooling/registry/docker-compose.yml)
  owns the image, profiles, host publication, healthcheck, and storage mount.
- Host port `${REGISTRY_PORT:-5000}` is published without a bind address. The
  tracked service config contains no Registry TLS or authentication settings and
  no Traefik route. Unless an external firewall/daemon policy supplies protection,
  the current endpoint is unauthenticated HTTP. That external protection is not
  proven by source and must not be assumed.
- `/v2/` health proves HTTP response only. It does not prove authorization,
  digest integrity, push/pull, storage durability, or client trust.
- The bind-backed `/var/lib/registry` is authoritative filesystem storage.
  Deletion is not enabled, and garbage collection is not a normal cleanup step.

### Normal use

1. Validate with `docker compose --profile registry config --quiet` from the root.
2. Before any push, verify the endpoint is confined to the approved trusted
   network. Do not store sensitive/proprietary artifacts until TLS and access
   control are implemented and tested.
3. Tag by immutable release/digest policy, push, then pull by digest and verify
   the manifest digest. Record repository, tag, digest, and source authority.
4. Treat the filesystem and digest inventory as one backup unit.

### Backup and upgrade

The tracked config has no read-only maintenance mode. For a consistent filesystem
backup, block clients and stop the Registry, then snapshot/copy the complete bind
directory and record a catalog/tag/digest inventory. Restore to an isolated
Registry, verify `/v2/`, catalog/tags, and pull selected digests before promotion.
Garbage collection requires the Registry to be read-only or stopped and a
separate destructive-data approval. Before upgrading, take the consistent backup,
review Distribution release/storage changes, test the restored copy with the new
image, and verify push/pull/digests. No backup, restore, GC, or upgrade ran here.

## Common Checks

- `docker compose --profile registry config --quiet`
- `docker compose --profile registry config --services`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`

## Runbook Handoff

Use the [runbook](runbook.md) for push/pull failures, storage recovery, planned
upgrade, or separately approved garbage collection.

## Traceability

- [Policy](policy.md) (`POL-0065`)
- [Runbook](runbook.md) (`RUN-0065`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [CNCF Distribution deployment and security](https://distribution.github.io/distribution/about/deploying/)
- [Registry configuration](https://distribution.github.io/distribution/about/configuration/)
- [Registry garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Registry project and Apache license](https://distribution.github.io/distribution/)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
