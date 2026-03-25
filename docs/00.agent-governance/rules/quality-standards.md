---
layer: agentic
---

# Agent Quality & Security Standards (March 2026)

This document defines the universal "Standard of Excellence" for all AI Agents interacting with `hy-home.docker`. It integrates documentation quality rubrics with technical security and performance mandates.

## 1. Documentation Quality Rubric (A-F)

Inspired by `@[/claude-md-improver]`, agents are assessed on these criteria:

| Grade | Description | Requirements |
| :--- | :--- | :--- |
| **A** | **Elite** | 100% Security compliance + < 200ms SLO awareness + Validated commands + 01-11 Taxonomy integration. |
| **B** | **Professional** | High security compliance + documented workflows + minor taxonomy gaps. |
| **C** | **Functional** | Basic security + missing performance SLOs + fragmented documentation. |
| **D** | **Substandard** | Missing healthchecks + legacy path references + vague instructions. |
| **F** | **FAIL** | **Hardcoded Secrets** OR **Broken Network isolation** OR **Documentation/Code mismatch**. |

### Quality Dimensions

- **Actionability**: Every command must be copy-paste ready and tested.
- **Conciseness**: Avoid generic AI prose; use token-efficient technical English.
- **Architecture Clarity**: Documentation must accurately reflect the `01-11` taxonomy.

## 2. Technical Security Standards

All service and infrastructure changes MUST adhere to these mandates:

- **Secrets Management**:
  - NEVER commit plain-text credentials in `.env` or `docker-compose.yml`.
  - Use **Docker Secrets** (`/run/secrets/`) for production-grade security.
- **Network Isolation**:
  - All inter-service traffic MUST use the `infra_net` bridge.
  - External exposure is restricted to the **01-gateway** tier.
- **Process Hardening**:
  - Enforce `security_opt: [no-new-privileges:true]`.
  - Prefer non-root users inside containers (`user: "1000:1000"`).

## 3. Performance SLO Standard

Agents must optimize for and document these Service Level Objectives:

- **Latency**:
  - Internal API/Service-to-Service: **< 200ms (p95)**.
  - User-facing Gateway Response: **< 500ms (p95)**.
- **Resource Efficiency**:
  - Every service MUST define `deploy: resources: limits` (CPU/Memory) to prevent OOM.
  - Optimize `healthcheck` intervals to minimize CPU overhead on idle nodes.
- **Availability**:
  - Every service MUST have a functional `healthcheck` and `restart: always/unless-stopped` policy.

## 4. Workflow & Taxonomy Compliance

- **JIT Loading**: Load specific `scopes/<layer>.md` ONLY when the task targets that layer.
- **Stage-Gate Hierarchy**: Follow the `01.prd` to `11.postmortems` folder naming convention strictly.
- **Human-Centric UI**: All User notifications MUST be in **Korean**, while internal logic stays in **English**.

## 5. Verification Checklist

Before marking a task as complete, an agent MUST:

1. [ ] Pass `bash scripts/validate-docker-compose.sh`.
2. [ ] Verify secret synchronization path.
3. [ ] Confirm performance resource limits are set.
4. [ ] Audit all links for dotted taxonomy compliance.
