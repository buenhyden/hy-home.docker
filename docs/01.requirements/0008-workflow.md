---
title: "Workflow Tier (07-workflow) Product Requirements"
version: "1.0.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "requirements"
artifact_id: "REQ-0008"
parent_ids: []
created: "2026-03-26"
---
# Workflow Tier (07-workflow) Product Requirements

## Problem and Goals

This document defines the product requirements for the `07-workflow` tier (Airflow, n8n). The tier's goal is to efficiently manage complex business logic and data flow by providing data pipeline automation, task orchestration, and powerful low-code integration features.

### Problem Statement

Currently scattered script-based tasks are hard to monitor, and there is no standardized platform for centrally controlling complex integration work between systems.

## Stakeholders and User Needs

Build an integrated workflow engine that spans complex data engineering tasks to simple API integrations, maximizing operational efficiency and providing an environment where agents can autonomously orchestrate tasks.

### Personas

- **Data Engineer**: Needs to define and schedule complex ETL pipelines in Python code.
- **Backend Developer**: Wants to quickly handle simple system automation or third-party integration.
- **AI Agent**: Executes predefined workflows or designs and triggers new automation scenarios.

### Key Use Cases

- **STORY-01**: A data engineer processes source data every night and loads it into the data warehouse via an Airflow DAG.
- **STORY-02**: A developer uses n8n to build, in 5 minutes, an integration scenario that calls a specific API when a Slack message arrives.
- **STORY-03**: A system monitoring agent runs a response workflow in n8n to attempt automatic recovery when a specific failure is detected.

## Functional Requirements

- **REQ-0008-FR-0001**: Support complex Python-based DAG definitions (Airflow).
- **REQ-0008-FR-0002**: Support worker scaling for distributed processing (CeleryExecutor).
- **REQ-0008-FR-0003**: Support GUI-based low-code automation and integration with 400+ external nodes (n8n).
- **REQ-0008-FR-0004**: Provide real-time monitoring of workflow execution status and logs.
- **REQ-0008-FR-0005**: Provide an interface for agents to control workflows via API.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0008-FR-0001**: Complete Airflow migration for all core data pipelines (100%).
- **REQ-0008-FR-0002**: Reduce new integration build time via n8n by 50%.
- **REQ-0008-FR-0003**: 100% notification handling rate on task failure.

## Constraints

- **In Scope**:
  - Dedicated to complex batch and ETL processes centered on business logic.
  - Leverage Python code-based extensibility and dynamic pipeline generation.
  - Guarantee large-scale data processing through distributed task handling via CeleryExecutor.
- **Out of Scope**:
  - Development of individual business logic (owned by each service area).
  - The CI/CD pipeline itself (owned by GitHub Actions).
- **Non-goals**:
  - Real-time streaming processing (Messaging Tier territory).

### AI Agent Requirements

- **Allowed Actions**: Query workflow execution status, manually trigger a specific workflow, export n8n JSON.
- **Disallowed Actions**: Change Airflow administrator settings, direct DB manipulation.
- **Human-in-the-loop Requirement**: Deploying a new DAG and activating an n8n workflow require final human approval.

## Risks

- **Risks**: Possible DB schema migration interruption during an Airflow upgrade.
- **Dependencies**: `04-data` (PostgreSQL) and `06-observability` (metrics/logging).

### Verification

#### Workflow Compose Check

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
```

#### Workflow Hardening Check

```bash
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

#### Runtime Health Check

When the runtime is running, check the internal health of Airflow and n8n in the `airflow-apiserver` and `n8n` containers, respectively.

## Traceability

- **Architecture Description**: [0007-workflow-architecture.md](../02.architecture/descriptions/0007-workflow-architecture.md)
- **Spec**: [008-workflow/spec.md](../02.architecture/descriptions/0007-workflow-architecture.md)
- **Plan**: 2026-03-26-07-workflow-standardization.md
- **ADR**: [0007-airflow-n8n-hybrid-workflow.md](../02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md)
- **Guide**: [airflow.md](../05.operations/guides/0050-airflow.md), [n8n.md](../05.operations/guides/0053-n8n.md)
- **Policy**: [airflow.md](../05.operations/policies/0050-airflow.md), [n8n.md](../05.operations/policies/0053-n8n.md)
- **Runbook**: [airflow.md](../05.operations/runbooks/0050-airflow.md), [n8n.md](../05.operations/runbooks/0053-n8n.md)
