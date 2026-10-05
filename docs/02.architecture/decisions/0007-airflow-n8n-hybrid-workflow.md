---
title: "Airflow & n8n Hybrid Workflow Strategy"
version: "1.1.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0007"
parent_ids:
- "AD-0007"
created: "2026-03-26"
---
# ADR-0007: Airflow & n8n Hybrid Workflow Strategy

## Context

This document is the architecture decision record for the background and hybrid operating strategy behind adopting both Apache Airflow and n8n as workflow engines.

The project faces two different workflow needs.

1. **Complex data engineering**: ETL work that needs strict scheduling, retries, failure handling, and deep integration with the Python ecosystem.
2. **Fast API integration**: the need to quickly connect various external services (Slack, Google Sheets, etc.) with simple business logic, without writing code.

Solving both with a single solution does not work well: Airflow is too heavy for simple integrations, and n8n has limits managing complex data pipelines.

### Traceability

The confirming evidence for this decision is limited to the Architecture Description, Spec, and Operations documents linked in `Related Documents`, and the current repository configuration. It makes no claim about runtime state without separate execution evidence.

## Decision

- Adopt **Apache Airflow** as the "Core Orchestrator", handling complex data pipelines and system batch jobs.
- Adopt **n8n** as the "Integration Automator", handling external service federation and lightweight event-driven automation.
- The root-included dev compose uses the shared `mng-valkey` and the management PostgreSQL, while service-local compose declares dedicated Airflow/n8n Valkey services, separating the operational boundary.

  At the time this sentence was written, two compose files drew that
  boundary. Afterward, SPEC-0156 and SPEC-0171 changed the compose model to
  "the root unconditionally includes all files and a profile selects", so
  `infra/07-workflow/airflow/` and `infra/07-workflow/n8n/` each have only one
  compose file. The boundary itself remains, and only the mechanism for
  drawing it changed. The `dedicated-valkey` profile starts `airflow-valkey`
  and `n8n-valkey`; if not selected, the `${AIRFLOW_VALKEY_HOST:-mng-valkey}`
  and `${N8N_VALKEY_HOST:-mng-valkey}` defaults resolve to the shared
  `mng-valkey`. The decision remains valid and only its realized form
  changed, so the sentence above is preserved as a record of its time.
  Recorded by SPEC-0176.

### Decision Drivers

The decision context above records the applicable drivers and evidence.

## Alternatives

### Alternatives

### Options Considered

### [Alternative 1: Airflow Only]

- Good: simple with single-engine operation, strong control.
- Bad: even simple API integrations need a lot of code, and fast UI-based edits are not possible.

### [Alternative 2: n8n Only]

- Good: very fast development speed, intuitive visualization.
- Bad: complex dependency management and applying custom Python logic are difficult, and visibility into large-scale batch jobs is low.

## Consequences

- **Positive**:
  - Improves development and operational productivity by using the optimal tool for each purpose.
  - Lowers the barrier for non-developers (or AI agents) to participate in automation (n8n).
  - Secures strong data governance and traceability (Airflow).
- **Trade-offs**:
  - Operational overhead from managing two kinds of engines.
  - Increased resource (memory, CPU) consumption.

### Explicit Non-goals

- Does not standardize direct mutual calls between the two engines (done only through an API when needed).
- Does not use n8n for large-volume data processing.

## Related Documents

- **PRD**: [008-workflow.md](../../01.requirements/0008-workflow.md)
- **Architecture Description**: [0007-workflow-architecture.md](../descriptions/0007-workflow-architecture.md)
- **Spec**: [008-workflow/spec.md](../descriptions/0007-workflow-architecture.md)
