---
title: "05-Messaging Optimization Hardening Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0037"
parent_ids:
- "GDE-0037"
created: "2026-05-17"
---

# 05-Messaging Optimization Hardening Runbook

## When to Use

Use for approved static diagnosis of the current Kafka hardening baseline. Runtime
change, restore, cleanup and credential rotation need a separate task.

## Procedure

1. From the repository root, render the current selectors:

   ```bash
   docker compose --env-file .env.example --profile messaging config --quiet
   docker compose --env-file .env.example --profile messaging-cluster config --quiet
   bash scripts/hardening/check-all-hardening.sh 05-messaging
   ```

2. Inspect root-rendered services, profiles, networks, secret references, volumes,
   health checks and resource limits. Do not print private substituted values.
3. Confirm broker listener protocols remain explicitly documented, Kafbat uses its
   native OIDC template and secret, and every Kafbat route uses only
   `gateway-standard-chain@file`.
4. Confirm topic initialization with replication factor 3 is limited to a
   three-broker-capable plan.
5. Review the exact diff and operations documents. Record commands, exit status
   and unresolved gaps without starting containers.

## Rollback or Recovery

For a static failure, identify the owning leaf source or shared template and patch
only the approved scope. Re-render the same selectors. Do not bypass a failed
secret, health, resource, network or persistence control by deleting it.

For a runtime incident, preserve broker/UI logs without records or credentials,
stop mutation, and use [RUN-0036](../0036-kafka/runbook.md). Raw log-directory
repair, offset movement, schema deletion, connector resume and cluster identity
changes require an approved recovery task.

## Evidence

Pass means root configuration parses, current profiles resolve, the scoped
hardening script passes, native OIDC and standard gateway routing agree, and
recovery ownership is explicit. It does not prove runtime, performance, OIDC
login, failover or restore.

## Escalation

Stop on source/profile, persistence, secret, OIDC, listener-security or recovery
ownership drift and escalate to the messaging owner.

## Traceability

- Artifact: `RUN-0037`; parent guide: `GDE-0037`.
- Static evidence does not prove runtime or restore.

### References

- [Kafka runbook](../0036-kafka/runbook.md)
- [Hardening policy](policy.md)

## Related Documents

- [Kafka runbook](../0036-kafka/runbook.md)
- [Hardening policy](policy.md)
