---
title: "05-Messaging Optimization Hardening Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0037"
parent_ids:
- "AD-0005"
created: "2026-05-10"
---

# 05-Messaging Optimization Hardening Operations Policy

## Overview

This policy binds current source configuration to data protection, security,
resource, lifecycle and independently verifiable operator controls.

## Policy Scope

This policy applies to the current optional Kafka-family source and its static
hardening contract. It does not authorize activation or security migration.

## Controls

Every messaging change must preserve root Compose validity, explicit profiles,
health checks, resource limits, persistence ownership, `infra_net`, secret files
and an actionable recovery owner. The only current broker family is Kafka.

### Security policy

- PLAINTEXT Kafka listeners are a documented gap and must not carry sensitive or
  untrusted traffic. TLS/SASL requires an architectural change and client rollout.
- Kafbat authenticates natively with OIDC and group RBAC. Its secret remains a
  Docker secret, its local CA remains mounted read-only, and its route uses the
  standard gateway chain. Forward-auth header trust is prohibited for this route.
- Administrative endpoints and host-published listeners remain within the named
  trusted boundary. Evidence must omit tokens, client secrets and record payloads.
- Topic/bootstrap changes require three-broker compatibility where replication
  factor 3 is declared.

### Reliability and recovery policy

Same-host replication is not host availability. New workloads must define
retention, partitions, replication, capacity, producer/consumer ownership,
RPO/RTO and replay source. Recovery must cover data, topic configs, offsets,
schemas, Connect state and KRaft identity and must be rehearsed on an isolated
cluster before promotion.

### Validation contract

Use the exact root-profile `config --quiet` commands in [GDE-0037](guide.md) for
`messaging` and `messaging-cluster`, then the scoped `05-messaging` hardening
script. Static passes
are configuration evidence only. Runtime startup, OIDC login, load or failover
requires explicit approval and a captured rollback.

## Exceptions

Documented one-shot job exceptions do not waive data/security controls. Exceptions do not authorize runtime mutation, plaintext secrets, raw active
storage copies or same-host availability claims.

## Verification

Verify root configuration and scoped static policy checks, then require an
isolated compatible restore with application-level acceptance before promotion or
cutover. Record unverified runtime properties explicitly.

## Review Cadence

Review after profile, image, volume, credential, consumer, retention or upstream
lifecycle change and at least annually while retained.

## Traceability

- Artifact: `POL-0037`; parent: `AD-0005`.
- Runtime authority remains the linked Compose/source files; exact pins stay there.

### References

- [Kafka policy](../0036-kafka/policy.md)
- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Hardening runbook](runbook.md)


## Related Documents

- [Domain catalog](../README.md)
