---
trigger: model_decision
glob: ["kafka/**/*.yml", "kafka/**/*.yaml", "contracts/events/**", "docs/messaging/**/*.md"]
description: "Kafka Governance Standards: Enforces naming conventions, partition/replication safety, and DLQ policies."
---

# Kafka Topic Governance Standard

- **Role**: Messaging Platform Architect
- **Purpose**: Define standards for deterministic Kafka topic management to ensure messaging systems remain secure, scalable, and recoverable.
- **Activates When**: Creating or updating Kafka topics, configuring ACL permissions, or designing event-driven failure (DLQ) strategies.

**Trigger**: model_decision — Apply during the design and provisioning of Kafka messaging infrastructure.

## 1. Standards

### Principles

- **[REQ-KAF-01] Declarative Management**
  - All Kafka assets (Topics, ACLs, Schemas) MUST be managed via GitOps or automated operators. Manual production changes are PROHIBITED.
- **[REQ-KAF-02] Deterministic Partitioning**
  - Topics MUST declare an explicit partition count that aligns with expected throughput and consumer parallelism goals.
- **[REQ-KAF-03] Least-Privilege Messaging**
  - Access to topics (Produce/Consume) MUST be restricted to identified principal identities using explicit, non-wildcard ACLs.

### Governance Matrix

| Attribute | Requirement ID | Critical Action |
| --- | --- | --- |
| Naming | [REQ-KAF-04] | `<env>.<domain>.<purpose>.<event>` |
| Replication | [REQ-KAF-05] | Minimum 3-way replication in Production |
| Retention | [REQ-KAF-06] | Explicit time or size-based cleanup |
| Failure | [REQ-KAF-07] | Mandatory DLQ with redrive runbook |

### Must

- **[REQ-KAF-08] Standardized Naming**
  - Topic names MUST be lowercase, dot-separated, and include the environment prefix.
- **[REQ-KAF-09] Explicit Cleanup Policy**
  - Every topic MUST explicitly define its cleanup policy (`delete` or `compact`). Infinite retention is PROHIBITED unless approved.
- **[REQ-KAF-10] Documented Redrive Procedure**
  - Every DLQ topic MUST include a link to a documented procedure for recovering and re-processing failed messages.

### Must Not

- **[BAN-KAF-01] Partition Decreases**
  - DO NOT attempt to decrease partition counts on a live topic; this is destructive and unsupported.
- **[BAN-KAF-02] Shared Principal PII**
  - Messaging payloads MUST NOT contain unencrypted PII unless the topic is explicitly marked as "Restricted" and access is audited.

### Failure Handling

- **Stop Condition**: Stop topic provisioning if the manifest lacks explicit `retention.ms` or `replication.factor` values.

## 2. Procedures

- **[PROC-KAF-01] ACL Sync Audit**
  - IF adding a new consumer service THEN MUST update the topic's ACL manifest before deployment.
- **[PROC-KAF-02] Backpressure review**
  - Periodically monitor consumer lag to determine if a partition increase or consumer scale-out is required.

## 3. Examples

### Secure Topic Manifest (Conceptual YAML)

```yaml
topic: prod.orders.checkout.event
partitions: 12
replication: 3
retention: 7d
cleanup: delete
dlq: prod.orders.checkout.event-dlq
```

## 4. Validation Criteria

- **[VAL-KAF-01] Schema Consistency**
  - [ ] Every topic is mapped to a versioned schema in the Schema Registry.
- **[VAL-KAF-02] ACL Non-Wildcard Check**
  - [ ] Security audit confirms that zero production identities have `*` (Wildcard) read/write access.
- **[VAL-KAF-03] Redrive Verification**
  - [ ] QA test confirms that a message placed in the DLQ can be manually re-sequenced into the source topic.
