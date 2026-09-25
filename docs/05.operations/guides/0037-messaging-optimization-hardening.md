---
title: "05-Messaging Optimization Hardening Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0037"
parent_ids:
- "POL-0037"
created: "2026-05-17"
---

# 05-Messaging Optimization Hardening Usage Guide

## Usage

The current messaging surface is Kafka-only and OPTIONAL. Hardening verifies the
root-rendered Kafka family, Kafbat native OIDC, persistence, health, resources and
network exposure. It does not claim that PLAINTEXT broker listeners are secure or
that three same-host brokers provide host availability.

### Source-backed checks

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging-cluster config --quiet
bash scripts/hardening/check-all-hardening.sh 05-messaging
```

Run from the repository root. Inspect rendered services and verify:

- exact Kafka-family profiles and no removed broker family;
- separate broker/Connect volumes and no path reuse;
- health checks and shared CPU/memory limits;
- `kafka_net`, intended host port publication and PLAINTEXT listener risk;
- `kafbat_client_secret`, native `auth.type: OAUTH2`, local CA trust, RBAC groups,
  and `gateway-standard-chain@file` without forwarding-auth middleware;
- backup/restore ownership for topic, offset, schema, connector and KRaft state.

Static success does not prove runtime health, authentication flow, performance,
data durability or restore. Those require separately approved tests.

### Change workflow

Correct source at the owning leaf file and shared template, render the root
profiles again, run the scoped hardening check, inspect the diff, and follow
[RUN-0037](../runbooks/0037-messaging-optimization-hardening.md). Runtime security work such as TLS/SASL, credential
rotation, topic mutation or service restart requires a named plan and rollback.

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0037`; governing policy: `POL-0037`.
- Runtime authority: `root Kafka Compose plus scripts/hardening/check-all-hardening.sh`.

### References

- [Kafka security](https://kafka.apache.org/documentation/#security)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Kafka guide](0036-kafka.md)

## Related Documents

- [Domain catalog](../README.md)
