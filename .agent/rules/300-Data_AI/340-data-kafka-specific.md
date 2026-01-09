---
trigger: always_on
glob: "**/*.{py,js,ts,java,go}"
description: "Kafka: Partitioning, Offsets, and Idempotent production."
---
# Kafka Standards

## 1. Topic Design

- **Partitioning**: Choose keys carefully to ensure even distribution and ordering within partitions.
- **Naming**: Use a standard convention like `environment.domain.event` (e.g., `prod.users.created`).
- **Retention**: Define a clear retention policy (Time or Size based).

## 2. Producers

- **Acknowledge**: Use `acks=all` for high-durability requirements.
- **Idempotency**: Set `enable.idempotence=true` to prevent duplicate messages on retries.
- **Batching**: Optimize `linger.ms` and `batch.size` for throughput vs latency trade-offs.

### Example: Producer Config

**Good**

```yaml
acks: all
retries: 2147483647 # Max retries
enable.idempotence: true
```

**Bad**

```yaml
acks: 0 # Fire and forget, no delivery guarantee
```

## 3. Consumers

- **Commitment**: Use manual offset commits for "At Least Once" processing if auto-commit is too risky.
- **Consumer Groups**: Use unique group IDs for different services reading the same data.
- **Dead Letter Queues (DLQ)**: Route unprocessable messages to a DLQ for manual inspection.

## 4. Schemas

- **Evolution**: Use Schema Registry (Avro/Protobuf) to ensure backward/forward compatibility.
- **No Blobs**: Avoid sending large files over Kafka. Store the file in S3 and send the URI.
