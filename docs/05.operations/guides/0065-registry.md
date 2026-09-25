---
title: "Docker Registry Usage Guide"
version: "1.2.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
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

- [Registry Compose](../../../infra/09-tooling/registry/docker-compose.yml)
  owns the image, profiles, host publication, healthcheck, and storage mount.
- Host port `${REGISTRY_PORT:-5000}` is published on `127.0.0.1` only, to
  container port 5000. The tracked service config contains no Registry TLS or
  authentication settings and no Traefik route, so the endpoint is
  unauthenticated HTTP for local host users and for every container on the
  project default network (`registry:5000`). Docker trusts `127.0.0.0/8` registries over
  HTTP by default, so no insecure-registry daemon setting is needed.
- The container runs as `1000:1000`, the owner of `${DEFAULT_REGISTRY_DIR}`;
  root with every capability dropped cannot write that directory.
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

### Archiving locally built images

Locally built images that are not running can be kept in the Registry so the
Docker image store on `/` does not hold them. `${DEFAULT_REGISTRY_DIR}` lives on
the data disk.

1. Tag the image as `localhost:${REGISTRY_PORT:-5000}/<repository>:<tag>` and push it.
2. Pull the pushed reference by digest and compare the digest with the push
   output. Record repository, tag, digest and the source Dockerfile in the Task.
3. Remove the local tags only after step 2 succeeds. Never remove an image that a
   container, running or stopped, still uses.
4. To use it again, pull the Registry reference and retag it to the name the
   Compose file expects, or rebuild it from the tracked Dockerfile.

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

Use the [runbook](../runbooks/0065-registry.md) for push/pull failures, storage recovery, planned
upgrade, or separately approved garbage collection.

## Traceability

- [Policy](../policies/0065-registry.md) (`POL-0065`)
- [Runbook](../runbooks/0065-registry.md) (`RUN-0065`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [CNCF Distribution deployment and security](https://distribution.github.io/distribution/about/deploying/)
- [Registry configuration](https://distribution.github.io/distribution/about/configuration/)
- [Registry garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Registry project and Apache license](https://distribution.github.io/distribution/)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
