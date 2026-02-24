---
title: 'RAG Stack (Ollama/Open WebUI/Qdrant) Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: 'N/A'
api_reference: 'N/A'
arch_reference: '../../../ARCHITECTURE.md'
tags: ['spec', 'implementation', 'infra', 'ai']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: N/A
> **Related API Spec**: N/A
> **Related Architecture**: `../../../ARCHITECTURE.md`

_Target Directory: `specs/infra/rag-stack/spec.md`_

---

## 0. Pre-Implementation Checklist (Governance)

> **Mandatory**: Coder agents MUST verify these checklists before generating code.

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style Monolith/Modular Monolith/Microservices? | Must     | Infra modular services | Section 1 |
| Service Boundaries | Are module boundaries documented (diagram/text)?      | Must     | Ollama/Open WebUI/Qdrant | Section 1 |
| Domain Model       | Are core domain entities and relationships defined?   | Must     | N/A | Section 3 |
| Backend Stack      | Are language/framework/libs (web, ORM, auth) decided? | Must     | N/A | Section 1 |
| Frontend Stack     | Are framework/state/build tools decided?              | Must     | N/A | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Levels (Unit/Integration/E2E/Load) defined?    | Must     | Integration validation | Section 7 |
| Test Tooling    | Agreed framework/runner and mock strategy?     | Must     | Compose + endpoint checks | Section 7 |
| Coverage Policy | Are goals defined as numbers (e.g., 100%)?      | Must     | N/A | Section 7 |
| AuthN/AuthZ     | Is auth approach designed (token/OAuth/RBAC)?  | Must     | N/A | Section 4 |
| Data Protection | Encryption/access policies for sensitive data? | Must     | N/A | Section 9 |
| Performance     | Are Core Web Vitals/Latency metrics targeted?  | Must     | N/A | Section 8 |
| Accessibility   | Is WCAG compliance integrated (contrast/ARIA)? | Must     | N/A | Section 8 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Environments | Are tiers (dev/staging/prod) clarified for this feature? | Must     | `OPERATIONS.md` | OPERATIONS.md |
| Logging      | Required structured logs defined (fields, IDs)?          | Must     | N/A | Section 9 |
| Monitoring   | Metrics and dashboards defined (RED/USE)?                | Must     | N/A | Section 9 |
| Alerts       | Are alert thresholds and routing defined?                | Must     | N/A | Section 9 |
| Backups      | Are backup policies defined for added data?              | Must     | N/A | Section 9 |

---

## 1. Technical Overview & Architecture Style

This spec defines the local RAG stack under `infra/08-ai`, composed of Ollama (inference), Open WebUI (chat UI), and Qdrant (vector store). The stack runs under an optional `ollama` profile to conserve resources.

- **Component Boundary**: `infra/08-ai/ollama`, `infra/08-ai/open-webui`, `infra/04-data/qdrant`.
- **Key Dependencies**: Qdrant for vector storage, Open WebUI for UI.
- **Tech Stack**: Docker Compose services for AI stack.

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **REQ-SPC-001** | Ollama provides inference endpoint | High | N/A |
| **REQ-SPC-002** | Open WebUI connects to Ollama via HTTP | High | N/A |
| **REQ-SPC-003** | Open WebUI uses Qdrant for vectors | High | N/A |
| **REQ-SPC-004** | Persist `.ollama` and qdrant storage volumes | High | N/A |

## 3. Data Modeling & Storage Strategy

- **Ollama**: Persistent model data at `/root/.ollama`.
- **Qdrant**: Vector storage at `/qdrant/storage`.

## 4. Interfaces & Data Structures

### 4.1. Core Interfaces

- **Open WebUI -> Ollama**: `OLLAMA_BASE_URL=http://ollama:11434`
- **Open WebUI -> Qdrant**: `QDRANT_URL=http://qdrant:6333`

### 4.2. AuthN / AuthZ (Required if protected data/actions)

N/A

## 5. Component Breakdown

- **Ollama**: Open-weight LLM inference engine.
- **Open WebUI**: Chat UI + document ingestion.
- **Qdrant**: Vector database for embeddings.

## 6. Edge Cases & Error Handling

- **Model storage missing**: Ollama re-downloads models (slow).
- **Qdrant unavailable**: Document ingestion fails.

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001]** Call Ollama inference endpoint and validate response.
- **[VAL-SPC-002]** Upload document in Open WebUI and confirm Qdrant vectors.

## 8. Non-Functional Requirements (NFR) & Scalability

- **Storage**: Ensure persistent volumes for large model downloads.

## 9. Operations & Observability

- **Deployment Strategy**: Optional profile (`ollama`).
- **Monitoring & Alerts**: N/A.
- **Logging**: Service logs for inference errors.
- **Data Protection**: N/A.
- **Sensitive Data Handling**: Do not persist sensitive prompts outside configured stores.
