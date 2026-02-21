---
trigger: model_decision
glob: ["**/*"]
description: "Specialized Cloud Standards: Enforces event-driven choreography (EventBridge), Saga orchestration (Step Functions), and Vercel/Modal deployment patterns."
---

# Specialized Cloud Standards

- **Role**: Cloud Orchestration Specialist
- **Purpose**: Define standards for advanced cloud integration patterns including event-driven choreography, complex workflows, and specialized AI/ML infrastructure.
- **Activates When**: Designing AWS EventBridge/Step Function logic, deploying to Vercel, or architecting AI pipelines on Modal.

**Trigger**: model_decision — Apply during the design and implementation of advanced cloud-integrated features.

## 1. Standards

### Principles

- **[REQ-SPC-01] Event-Driven Choreography**
  - Use EventBridge for cross-service decoupling. Services MUST emit domain events rather than calling external APIs directly for non-atomic side-effects.
- **[REQ-SPC-02] Managed Workflow Orchestration**
  - complex business logic involving multiple distributed steps MUST be orchestrated via Step Functions (Saga pattern) to ensure reliability and observability.
- **[REQ-SPC-03] Edge-First Latency optimization**
  - Utilize Vercel Edge Functions for globally-distributed middleware and lightweight routing logic to minimize TTFB (Time to First Byte).

### Specialized Technology Baseline

| Technology | Requirement ID | Critical Control / Pattern |
| --- | --- | --- |
| AWS Step Func | [REQ-SPC-04] | State payload size < 256KB |
| AWS EventBrg | [REQ-SPC-05] | Schema Registry enforcement |
| Vercel | [REQ-SPC-06] | Immutable production deployments |
| Modal (AI) | [REQ-SPC-07] | Managed Secrets & Auto-GPU scaling |

### Must

- **[REQ-SPC-08] Mandatory Dead-Letter-Queues (DLQ)**
  - All asynchronous event targets (SQS/SNS/EventBridge) MUST have a configured DLQ with associated monitoring.
- **[REQ-SPC-09] Workflow Idempotency Flags**
  - Step Function states MUST utilize idempotency tokens to prevent catastrophic re-execution of side-effects during retries.
- **[REQ-SPC-10] Secret Managed Integration**
  - External platform configurations MUST utilize natively-integrated secrets management (e.g., `modal.Secret`, Vercel Env Vars).

### Must Not

- **[BAN-SPC-01] Monolithic Workflow States**
  - Do NOT embed complex, multi-domain business logic within a single Lambda; decompose into a Step Function workflow.
- **[BAN-SPC-02] Synchronous Cross-Service Dependency**
  - Avoid synchronous HTTP calls between microservices for data synchronization; utilize EventBridge choreography instead.

### Failure Handling

- **Stop Condition**: Stop deployment if a Step Function definition identifies a lack of a Catch/Retry block on a mission-critical integration state.

## 2. Procedures

- **[PROC-SPC-01] Schema Evolution Review**
  - IF modifying an EventBridge event schema THEN MUST verify backward compatibility with all identified downstream consumers.
- **[PROC-SPC-02] Edge Latency audit**
  - Regularly monitor the execution duration of Vercel Edge functions to ensure they remain within the 50ms active execution window.

## 3. Examples

### Event-Driven Step Function (Good)

```json
{
  "StartAt": "ProcessOrder",
  "States": {
    "ProcessOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "Retry": [{ "ErrorEquals": ["States.ALL"], "IntervalSeconds": 2 }],
      "End": true
    }
  }
}
```

## 4. Validation Criteria

- **[VAL-SPC-01] Workflow Traceability**
  - [ ] Monitoring dashboard confirms that 100% of Step Function executions can be traced back to the original trigger event.
- **[VAL-SPC-02] DLQ Empty-Check Visibility**
  - [ ] Audit confirms that DLQ backlog metrics are correctly surfacing in the central DevOps dashboard.
- **[VAL-SPC-03] Vercel Immutable Pass**
  - [ ] Verification confirms that zero production environment changes can be made without a corresponding Git-driven deployment.
