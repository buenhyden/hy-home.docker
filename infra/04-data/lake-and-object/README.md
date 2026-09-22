---
title: "Lake & Object Storage (04-data/lake-and-object)"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
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

- [`seaweedfs`](seaweedfs/README.md) is the HOME S3 store. Consumers move to
  it one at a time with a freeze, a final delta copy and verification
  (SPEC-0180 S07); each has a bucket-scoped identity.
- [`minio`](minio/README.md) keeps serving consumers that have not moved yet
  and keeps its data until every cutover is accepted; it is then removed.

The two stores never share data paths. Copying between them goes only through
the S3 API (`seaweedfs-migrate`), never through their storage directories.

## How to Work in This Area

Use root Compose profiles and preserve distinct storage paths, secrets and network
boundaries.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to locate
Stage 05 subjects `04-data/0023-minio`, `04-data/0024-seaweedfs`, and backup policy
POL-0021.
