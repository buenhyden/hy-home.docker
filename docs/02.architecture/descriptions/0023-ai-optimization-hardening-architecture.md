---
title: "08-AI Optimization Hardening Architecture Description"
version: "1.0.3"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "AD-0023"
parent_ids:
- "REQ-0009"
created: "2026-03-28"
---
# 08-AI Optimization Hardening Architecture Description

## Context and Stakeholders

This document defines the optimization/hardening reference architecture of
the `08-ai` layer. It organizes the gateway boundary security, GPU
concurrency control, stateful operational consistency, health-based
observation stability, and catalog-based operational expansion policy from
an architecture perspective.

### Stakeholders and Concerns

Requirement owners, implementers, and operators share the concerns recorded
in this section and the following views. Only concerns confirmed in the
existing document are covered here.

The AI tier consists of two core planes.

- Ollama (local LLM inference/embedding engine)
- Open WebUI (user interface + RAG orchestration)

External entry shares the standard middleware+SSO chain at the Traefik TLS
boundary.

## System Boundaries

This section preserves the system boundary, consumption relationships,
non-goals, and constraints already recorded in the current document.

- **Owns**:
  - AI management path gateway/SSO boundary contract
  - Ollama GPU concurrency/resource protection contract
  - Open WebUI stateful operation contract
  - AI hardening CI policy gate
  - 08-ai catalog expansion policy (model promotion/access control/log policy)
- **Consumes**:
  - `01-gateway` standard middleware chain
  - `02-auth` SSO middleware
  - `04-data` Qdrant and the data layer
- **Does Not Own**:
  - Model training/fine-tuning pipeline
  - Qdrant internal schema/index operation detail
- **Non-goals**:
  - Immediate adoption of a distributed GPU scheduler
  - Immediate standardization of parallel external LLM providers

## Quality Attributes

### Quality Scenarios

The quality scenarios point to the existing configuration, failure boundary,
and verification expectation to which the attributes below apply. Concrete
execution evidence is owned by the related Spec and Operations documents.

- **Performance**: suppresses GPU overload with an Ollama concurrency/queue
  ceiling.
- **Security**: unifies public boundary security with the
  gateway-standard-chain + SSO chain.
- **Reliability**: strengthens boot stability and observation reliability
  with health-gated dependency/healthcheck.
- **Scalability**: enables staged expansion based on model promotion/resource
  policy.
- **Observability**: standardizes the exporter metrics health contract and
  the CI hardening gate.
- **Operability**: uses `check-all-hardening.sh 08-ai` as the AI tier
  operational baseline.

## Components

### Viewpoints and Views

The context, component, or deployment representation in this section serves
as the view for that concern.

- **Ingress path**:
  - Client -> Traefik(websecure) -> ollama/chat routers -> Ollama/Open WebUI
- **Inference/RAG plane**:
  - Open WebUI -> Ollama (generation + embedding)
  - Open WebUI -> its local vector store (vector retrieval)
- **Control plane**:
  - SSO middleware, policy gate script/CI, operational documents (guides/policies/runbooks)

## Data Flow

### Data and Control Flows

The data and control flows include only the interactions specified in this
section and the existing infrastructure/deployment descriptions.

- **Key Entities / Flows**:
  - model artifacts, conversation/session metadata, embedding vector
    references
- **Storage Strategy**:
  - Ollama model cache: `${DEFAULT_AI_MODEL_DIR}/ollama`
  - Open WebUI state data: `${DEFAULT_AI_MODEL_DIR}/open-webui`
- **Data Boundaries**:
  - Qdrant owns the actual vector index data, and the AI tier owns the
    call/usage policy.

## Deployment View

- **Runtime / Platform**: Docker Compose (`infra/08-ai/*`)
- **Deployment Model**:
  - Ollama + exporter
  - Open WebUI (stateful) + ollama dependency
- **Operational Evidence**:
  - root-active compose validation through `scripts/validation/validate-docker-compose.sh`
  - optional AI compose contract checks through `scripts/hardening/check-all-hardening.sh 08-ai`
  - `scripts/hardening/check-all-hardening.sh 08-ai`
  - CI `infrastructure-hardening` job

## Evolution

- **Ollama**:
  - formalizing the model cache/storage operational policy
  - standardizing GPU scheduling/concurrency ceiling operation
  - establishing a model promotion procedure (experiment -> production)
- **Open WebUI**:
  - strengthening SSO enforcement/no-bypass criteria
  - separating model access permission (role/environment)
  - strengthening conversation log retention/masking policy

## Traceability

The disposition of the parent requirement and the related decision/implementation specs are owned by the PRD, ADR, and Spec links in `Related Documents`. This description does not replace the role of those documents.

## Related Documents

- **PRD**: [../01.requirements/0009-ai.md](../../01.requirements/0009-ai.md)
- **Spec**: [../03.specs/009-ai/spec.md](0008-ai-architecture.md)
- **ADR**: [../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../decisions/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Guide**: [../../05.operations/guides/08-ai/optimization-hardening.md](../../05.operations/guides/0058-ai-optimization-hardening.md)
- **Operation**: [../../05.operations/policies/08-ai/optimization-hardening.md](../../05.operations/policies/0058-ai-optimization-hardening.md)
- **Runbook**: [../../05.operations/runbooks/08-ai/optimization-hardening.md](../../05.operations/runbooks/0058-ai-optimization-hardening.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
