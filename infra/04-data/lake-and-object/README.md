---
title: "Lake & Object Storage (04-data/lake-and-object)"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-05-15"
---

# Lake and object storage

## Overview

This area documents the repository's lake and object-storage packages.

## Audience

It is intended for operators and maintainers of the object-storage tier.

## Scope

It covers the HOME SeaweedFS store.

## Structure

### Packages and relationship

- [`seaweedfs`](seaweedfs/README.md) is the HOME S3 store; each consumer has
  a bucket-scoped identity. MinIO was removed after every consumer moved
  (SPEC-0180 S07); its data directory is kept as recovery material
  (RUN-0024).

## How to Work in This Area

Use root Compose profiles and preserve distinct storage paths, secrets and network
boundaries.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to locate
Stage 05 subject `04-data/0024-seaweedfs` and backup policy
POL-0021.
