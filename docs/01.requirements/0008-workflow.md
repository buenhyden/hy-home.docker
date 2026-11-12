---
title: "Workflow Tier (07-workflow) Requirements"
version: "1.2.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "requirements"
artifact_id: "REQ-0008"
created: "2026-03-26"
---

# Workflow Tier (07-workflow) Requirements

## Overview

### Problem and Outcome

Scattered script-based tasks are hard to monitor, and there is no standard
place to control integration work between systems. The `07-workflow` tier
provides code-defined pipeline orchestration (Airflow) and low-code
integration automation (n8n), so that data engineering jobs and simple API
integrations run, scale and are observed in one place.

### Stakeholders

- **Data engineer**: defines and schedules ETL pipelines in Python, for
  example a nightly load of source data into the warehouse.
- **Backend developer**: quickly builds a system automation or third-party
  integration, such as calling an API when a chat message arrives.
- **Agent**: runs a predefined workflow, for example a recovery workflow when
  a failure is detected.

The owner, @buenhyden, writes, reviews and accepts this package.

## Scope

### In Scope

- Code-defined batch and ETL orchestration with distributed
  workers, low-code integration automation with queued execution, execution
  monitoring, and agent control through an API.

### Constraints and Exclusions

- **Out of Scope**: Business logic of individual services, and the CI/CD
  pipeline, which GitHub Actions owns.
- **Non-goals**: Real-time stream processing, which the messaging tier owns.
- **Agent boundary**: An agent may query execution status, trigger an existing
  workflow and export a low-code workflow definition. It must not change
  orchestrator administrator settings or manipulate the workflow databases
  directly. Deploying a new pipeline or activating a low-code workflow needs
  human approval.

**Assumptions.**

The core PostgreSQL in `04-data` and the observability tier are available.

**Risks.**

- An orchestrator upgrade can interrupt its database schema migration.
- Both engines depend on `04-data` for state and on `06-observability` for
  metrics and logs.

## Requirements

### Functional Requirements

- **REQ-0008-FR-0001**: Support pipeline definitions written in Python code (Airflow).
- **REQ-0008-FR-0002**: Support scaling workers for distributed task execution.
- **REQ-0008-FR-0003**: Support GUI-based low-code automation with prebuilt integration nodes for external services (n8n).
- **REQ-0008-FR-0004**: Provide monitoring of workflow execution status and logs.
- **REQ-0008-FR-0005**: Provide an API through which agents control workflows.

## Acceptance Criteria

### Acceptance Conditions

- **REQ-0008-FR-0001**: Airflow loads pipeline definitions from its tracked
  pipeline source and renders with the workflow profile.
- **REQ-0008-FR-0002**: Airflow uses a distributed executor with separate
  scheduler and worker services, and n8n runs in queue mode with a separate
  worker.
- **REQ-0008-FR-0003**: n8n renders with its task runners and is reachable
  through the gateway.
- **REQ-0008-FR-0004**: Airflow exports execution metrics to the
  observability tier, and both engines keep execution history and logs on
  persistent storage.
- **REQ-0008-FR-0005**: Both engines expose an authenticated HTTP API for
  triggering and querying workflows.

### Verification Method

Rendered-configuration conditions (REQ-0008-FR-0001, REQ-0008-FR-0002, the task-runner rendering in REQ-0008-FR-0003 and the storage and metrics parts of REQ-0008-FR-0004) are judged by reviewing the rendered workflow configuration. Reachability through the gateway (REQ-0008-FR-0003) and the authenticated API (REQ-0008-FR-0005) are judged by runtime observations: a request through the gateway route and an unauthenticated and an authenticated API request. No current Spec Package cites REQ-0008; a Spec that implements it records the review result and the runtime observations in its Task evidence rows. The owner named in the frontmatter, @buenhyden, judges each condition from that evidence. The same owner accepts the requirement once every condition is judged met.

## Traceability

### Source and Constraints

This package records the owner's requirements for the workflow tier; no upstream
document governs it.

### Downstream Links

- **Architecture Description**: [0007-workflow-architecture.md](../02.architecture/descriptions/0007-workflow-architecture.md)
- **Guide**: [airflow.md](../05.operations/guides/08-workflows-and-automation/0050-airflow.md), [n8n.md](../05.operations/guides/08-workflows-and-automation/0053-n8n.md)
- **Policy**: [airflow.md](../05.operations/policies/08-workflows-and-automation/0050-airflow.md), [n8n.md](../05.operations/policies/08-workflows-and-automation/0053-n8n.md)
- **Runbook**: [airflow.md](../05.operations/runbooks/08-workflows-and-automation/0050-airflow.md), [n8n.md](../05.operations/runbooks/08-workflows-and-automation/0053-n8n.md)
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md)
- **Retired domain Spec SPEC-0008** (workflow): replaced by the workflow guides, policies and runbooks in the operations catalog under `docs/05.operations/`.
- **Retired requirement REQ-0019** (workflow optimization hardening): retired under SPEC-0169 because every clause named an implementation artifact (a middleware chain, run account, secret mount, compose declaration, or CI gate) rather than a solution-independent need. Its implementation contract lives in the workflow operations catalog policy under `docs/05.operations/`, and its documentation traceability clause moved to REQ-0026-FR-0011.
