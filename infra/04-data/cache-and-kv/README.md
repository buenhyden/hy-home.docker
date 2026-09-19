---
title: "Cache & Key-Value Stores (04-data/cache-and-kv)"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2026-03-27"
---

# Cache and key-value data

## Overview

This area documents the repository's cache and key-value data package.

## Audience

It is intended for operators and maintainers of the Valkey deployment.

## Scope

It covers the selected package and the boundary between cluster and management
Valkey state.

## Structure

### Current package

[`valkey-cluster`](valkey-cluster/README.md) is the only package in this tier. Its
six Valkey nodes, init job and exporter use the exact `valkey-cluster` profile and
are classified LAB. It is distinct from HOME `mng-valkey`, which is owned by
`operational/mng-db` and supplies workflow broker/cache state.

## How to Work in This Area

### Operator boundary

Render the `valkey-cluster` profile through the root project. Keep six data paths
and cluster identities separate, protect `service_valkey_password`, and treat
published client and cluster-bus ports as trusted-network exposure. The same-host
three-primary/three-replica topology is not host availability.

Backup requires coordinated RDB checkpoints plus complete AOF sets/manifests and
an isolated fresh-identity restore.

## Related Documents

Use the [documentation entry point](../../../docs/README.md)
to locate Stage 05 subject `04-data/0022-valkey-cluster` and backup policy POL-0021.
