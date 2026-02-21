---
trigger: model_decision
glob: ["**/functions/**", "**/lambda/**", "**/serverless/**"]
description: "Serverless (FaaS) Standards: Enforces statelessness, idempotent event handling, and cold-start optimization for AWS/Azure/GCP."
---

# Serverless (FaaS) Standards

- **Role**: Serverless Infrastructure Architect
- **Purpose**: Define standards for building high-performance, cost-effective, and scalable serverless functions (Function-as-a-Service) using multi-cloud providers.
- **Activates When**: Implementing cloud functions (Lambda, Azure Functions, Cloud Run) or configuring serverless deployment frameworks.

**Trigger**: model_decision — Apply during the development and orchestration of serverless assets.

## 1. Standards

### Principles

- **[REQ-SRV-01] Absolute Statelessness**
  - Serverless functions MUST remain stateless. Persistent state MUST be offloaded to external services (Redis, S3, SQL).
- **[REQ-SRV-02] Cold-Start Resilience**
  - Initialization code MUST be minimized and optimized. Dependency trees MUST be pruned to ensure rapid cold-start performance.
- **[REQ-SRV-03] Idempotent Event Consumption**
  - Function logic MUST handle duplicate event deliveries gracefully (Idempotency), especially for event-driven triggers like SQS or Pub/Sub.

### Multi-Cloud Baseline

| Provider | Requirement ID | Critical Optimization |
| --- | --- | --- |
| AWS Lambda | [REQ-SRV-04] | ARM64 runtime & Lambda PowerTools |
| Azure Func | [REQ-SRV-05] | Durable Functions for stateful flows |
| GCP Cloud Run| [REQ-SRV-06] | Container-based "Scale to Zero" |
| Framework | [REQ-SRV-07] | Serverless Framework / AWS SAM |

### Must

- **[REQ-SRV-08] Thin Handler Pattern**
  - Function handlers MUST remain thin, delegating all core business logic to external service modules for testability.
- **[REQ-SRV-09] Resource Power-Tuning**
  - Memory and CPU allocation MUST be periodically tuned (e.g., via AWS Lambda Power Tuning) to find the optimal cost/performance balance.
- **[REQ-SRV-10] Externalized Client Init**
  - Heavy resource clients (DB connections, HTTP clients) MUST be initialized outside the handler to leverage execution environment reuse.

### Must Not

- **[BAN-SRV-01] Long-Running Computation**
  - Do NOT utilization serverless functions for tasks expected to exceed 15 minutes or those requiring significant local scratch space.
- **[BAN-SRV-02] Shared Secrets in Env**
  - Avoid hardcoding sensitive secrets in plaintext environment variables; utilized managed secret providers (Parameter Store, Key Vault).

### Failure Handling

- **Stop Condition**: Stop feature execution if a function's execution duration consistently nears the platform timeout limit (> 90%).

## 2. Procedures

- **[PROC-SRV-01] Cold-Start Audit**
  - IF adding a large library THEN MUST verify the impact on function cold-start latency using X-Ray or platform tracing.
- **[PROC-SRV-02] Resource Re-evaluation**
  - Conduct a monthly review of function invocation errors and timeouts to adjust memory and timeout configurations.

## 3. Examples

### Optimized Handler (Good)

```javascript
// Init outside handler for reuse
const client = new DatabaseClient();

export const handler = async (event) => {
  return await businessLogic.execute(client, event);
};
```

## 4. Validation Criteria

- **[VAL-SRV-01] Latency Compliance**
  - [ ] P99 cold-start latency remains below the project's established threshold (e.g., < 1s).
- **[VAL-SRV-02] Cost Integrity**
  - [ ] Monthly audit confirms that function resource allocations align with the 25% "buffer" margin over actual usage.
- **[VAL-SRV-03] Idempotency Pass**
  - [ ] Successive identical event executions result in zero redundant mutations in the primary database.
