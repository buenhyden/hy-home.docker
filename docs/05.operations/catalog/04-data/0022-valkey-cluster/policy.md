---
title: "Valkey Cluster Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0022"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Valkey Cluster Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

This policy governs the LAB-only `valkey-cluster` profile. It does not authorize
promotion to HOME or replacement of `mng-valkey`.

## Controls

- Select the stack only through the root Compose project and the exact
  `valkey-cluster` profile. Leaf rendering is unsupported.
- Keep all six data volumes separate. Never point two nodes at one directory or
  reuse live `nodes.conf` identity in a recovery target.
- Keep `service_valkey_password` in Docker secret custody. Do not place its value
  in Compose, Markdown, shell history or evidence.
- Treat published client and cluster-bus ports as trusted-network exposure. The
  current source declares authentication but no TLS.
- Record the client, dataset, retention and capacity hypothesis before activation.
  Three replicas on one host are a topology exercise, not host availability.
- Preserve shared health checks, resource limits and the `infra_net` boundary.

## Data protection

RDB and AOF protect against different failure modes. A backup must preserve a
coordinated point across the primaries, the entire AOF set/manifest where present,
and a manifest of engine version, slot map, files, sizes and hashes. Store it on a
separate encrypted destination. Retain daily recovery sets for 30 days and weekly sets for 90 days on the
separate destination. The planning objective is RPO 24 hours and RTO 8 hours;
both remain unverified until an isolated rehearsal. Shared resource-template
limits are mandatory and promotion/removal requires measured demand, data-owner
decision and verified export/restore.

A restore must not attach backup files to the live cluster. It creates fresh
identity on an isolated compatible target, restores complete persistence sets,
and validates `cluster_state`, slot coverage, replicas, key counts and
application reads. Production cutover or data destruction requires approval.

## Change and upgrade policy

Pin changes require official release-note review, client and persistence
compatibility review, a fresh backup, isolated restore evidence and a rollback
artifact. Membership changes, resharding and credential rotation are runtime
changes and require a named task.

## Exceptions

The LAB cluster may be absent when no named cluster client exists. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Runtime source: [Valkey Cluster Compose](../../../../../infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml).
- Artifact: `POL-0022`; parent: `AD-0004`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

## References

- [Valkey persistence](https://valkey.io/topics/persistence/)
- [Valkey Cluster tutorial](https://valkey.io/topics/cluster-tutorial/)
- [Backup policy](../0021-backup-and-restore/policy.md)
- [Runbook](runbook.md)


## Related Documents

- [Domain catalog](../README.md)
