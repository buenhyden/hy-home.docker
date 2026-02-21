---
trigger: model_decision
glob: ["**/cache/**", "**/redis/**", "**/storage/ephemeral/**"]
description: "Redis and Valkey Standards: Enforces explicit TTLs, consistent key naming, and fail-safe caching patterns."
---

# Redis and Valkey Usage Standards

- **Role**: In-Memory Storage Specialist
- **Purpose**: Define standards for the performant, reliable, and secure utilization of Redis and its protocol-compatible forks (Valkey) for caching and ephemeral data storage.
- **Activates When**: Configuring cache layers, implementing session management, or optimizing high-performance data lookups.

**Trigger**: model_decision — Apply during the design and implementation of in-memory data structures.

## 1. Standards

### Principles

- **[REQ-RED-01] Ephemeral Mindset**
  - Redis MUST be treated as volatile storage. Fundamental system state MUST NOT rely on Redis as the sole source of truth unless persistence is explicitly architected and tested.
- **[REQ-RED-02] Explicit TTL Governance**
  - Every key stored in Redis/Valkey MUST have an explicit Time-to-Live (TTL) defined. "Infinite" keys are PROHIBITED for caching use cases.
- **[REQ-RED-03] Fail-Safe Cache Degression**
  - Application logic MUST degrade gracefully if Redis is unavailable. The system MUST fall back to the primary database or local cache rather than failing critically.

### Key and Data Strategy

| Category | Requirement ID | Critical Action |
| --- | --- | --- |
| Naming | [REQ-RED-04] | `<app>:<domain>:<entity>:<id>` |
| Structure | [REQ-RED-05] | Smallest possible data structure (e.g., Hash over String) |
| Iteration | [REQ-RED-06] | Use `SCAN` instead of `KEYS` |
| Size | [REQ-RED-07] | Prevent "Big Keys" (> 1MB values) |

### Must

- **[REQ-RED-08] Standardized Key Prefixes**
  - All keys MUST utilize a consistent colon-separated prefix hierarchy to ensure keyspace isolation and discoverability.
- **[REQ-RED-09] Explicit Connection Pooling**
  - Application clients MUST utilize connection pooling to minimize TCP overhead and prevent connection exhaustion on the server.
- **[REQ-RED-10] Mandatory Memory Limits**
  - Each instance MUST have a `maxmemory` limit and an eviction policy (e.g., `allkeys-lru`) configured to prevent host system crashes.

### Must Not

- **[BAN-RED-01] Production 'KEYS' Usage**
  - The `KEYS` command is STRICTLY PROHIBITED in production; utilizing it causes severe single-threaded performance degradation.
- **[BAN-RED-02] Plain Text Sensitive Data**
  - Do NOT store unencrypted PII or credentials in Redis; utilize application-level encryption for sensitive ephemeral data.

### Failure Handling

- **Stop Condition**: Stop feature execution if the "Cache Miss" rate exceeds 90% over a 15-minute window, suggesting a logic error in the caching strategy.

## 2. Procedures

- **[PROC-RED-01] Key Audit Flow**
  - IF adding a new keyspace THEN MUST document its naming convention and TTL policy in the project's technical documentation.
- **[PROC-RED-02] Cold-Start Mitigation**
  - Verify for major releases that the cache warm-up procedure does NOT overwhelm the primary database during cold-start scenarios.

## 3. Examples

### Hierarchical Key Convention (Good)

```text
myapp:user:profile:123
myapp:session:token:abc
```

## 4. Validation Criteria

- **[VAL-RED-01] TTL Coverage Audit**
  - [ ] `SCAN` audit confirms that zero keys have an expiration of `-1` (Infinite) in the cache domain.
- **[VAL-RED-02] Latency Threshold**
  - [ ] Performance monitoring confirms that 99th percentile Redis command latency remains < 5ms.
- **[VAL-RED-03] Eviction Efficiency**
  - [ ] Metric analysis confirms that evictions are within expected limits and not impacting hit rates significantly.
