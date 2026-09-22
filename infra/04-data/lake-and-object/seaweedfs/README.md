---
title: "SeaweedFS"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2025-12-06"
---

# SeaweedFS

## Overview

This package defines the repository's optional SeaweedFS surface.

## Audience

It is intended for operators and maintainers evaluating SeaweedFS.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines `seaweedfs-master`,
`seaweedfs-volume`, `seaweedfs-filer`, and `seaweedfs-s3`. Profiles
`seaweedfs` and `storage-seaweedfs` select all four. The privileged FUSE mount
was removed (SPEC-0180 S04): it had no consumer, and S3 is the interface.

## Structure

Master and volume state use `seaweedfs-master-data` and
`seaweedfs-volume-data`. Services join `infra_net`; the S3 route uses the standard
gateway chain. Current source declares no secret, internal authentication/TLS or
mounted security configuration. Master, volume, filer and S3 expose only their
declared internal HTTP/gRPC ports; no host `ports` mapping is declared. Each
service has an HTTP health check. Commands/configuration are inline;
`security.toml.example` is not mounted.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile seaweedfs config --quiet
docker compose --env-file .env.example --profile seaweedfs config --services
```

SeaweedFS remains OPTIONAL and is not an automatic MinIO replacement. Recovery
must coordinate engine-aware volume backup, filer metadata and quiesced
master/topology state at one point, then validate on a same-version isolated
target. The official backup page describes limitations, so recovery remains
unverified until rehearsal.

## Related Documents

Use the [documentation entry point](../../../../docs/README.md) to locate Stage 05
subject `04-data/0024-seaweedfs` and POL-0021. Official sources:
[data backup](https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup),
[security](https://github.com/seaweedfs/seaweedfs/wiki/Security-Configuration), and
[license](https://github.com/seaweedfs/seaweedfs/blob/master/LICENSE).
