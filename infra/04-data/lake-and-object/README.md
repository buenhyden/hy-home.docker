---
title: "Lake & Object Storage (04-data/lake-and-object)"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
created: "2026-05-15"
---

# Lake and object storage

## Overview

This area documents the repository's lake and object-storage packages.

## Audience

It is intended for operators and maintainers of the object-storage tier.

## Scope

It covers the retained HOME store and the optional filer/S3 experiment.

## Structure

### Packages and relationship

- [`minio`](minio/README.md) is the retained HOME S3-compatible store. Current
  bootstrap creates Loki, Tempo, CDN and document-intelligence buckets.
- [`seaweedfs`](seaweedfs/README.md) is OPTIONAL for a named filer/S3 experiment.
  Its master, volume, filer and mount semantics differ from MinIO.

Do not run both as interchangeable defaults or point them at each other's data.
MinIO migration requires S3/client, policy, object-metadata, recovery and rollback
proof; SeaweedFS is not preselected as the target.

## How to Work in This Area

Use root Compose profiles and preserve distinct storage paths, secrets and network
boundaries.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to locate
Stage 05 subjects `04-data/0023-minio`, `04-data/0024-seaweedfs`, and backup policy
POL-0021.
