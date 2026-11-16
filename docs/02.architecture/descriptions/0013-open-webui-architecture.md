---
title: "Open WebUI Architecture Description"
version: "1.1.3"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "architecture"
artifact_id: "AD-0013"
parent_ids:
- "REQ-0013"
created: "2026-03-27"
---

# Open WebUI Architecture Description

## Overview

### Purpose and Readers

Open WebUI is an independent LAB for evaluating chat and retrieval-augmented
generation (RAG) with a local Ollama endpoint. Its obligations are owned by
[REQ-0013](../../01.requirements/0013-ai-open-webui.md).

### System Boundary

- **Owns:** the web UI and backend, RAG orchestration, and user, chat, upload
  and vector-store data under `/app/backend/data`.
- **Consumes:** an approved, reachable Ollama endpoint for inference and
  embeddings (`RAG_EMBEDDING_ENGINE: ollama`), and native Keycloak OIDC
  through the `home-openwebui` client and Keycloak gateway name.
- **Does not own:** model weights (Ollama) or any Qdrant collection. Compose
  sets no external vector database, so RAG vectors use the application's
  built-in store in its data volume.
- **Non-goals:** model training or fine-tuning.

## Context and Constraints

### Context

The LAB publishes the UI on its own bind address. It uses the operator's approved Ollama endpoint and reaches the identity provider through the Keycloak gateway name. Successful browser access and authentication require a suitable LAB origin and separate runtime evidence.

### Constraints

The service is stateful on local storage; horizontal scaling would first need an external database and vector store. Compose disables password login, signup, email merge and OAuth role/group management. Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.

## Current Structure

### Building Blocks

[`labs/open-webui/docker-compose.yml`](../../../labs/open-webui/docker-compose.yml)
defines the `open-webui` service on `lab_open_webui_net` alone. It declares no
gateway route or HOME network attachment. Its native OIDC entrypoint reads the
LAB-only Compose secret. The retained HOME OpenBao Agent output has no LAB bind.

### Runtime and Deployment

#### Runtime View

- User input -> Open WebUI -> Ollama (generation).
- Document upload -> Open WebUI -> Ollama (embedding) -> built-in vector store.
- Query -> built-in vector store (retrieval) -> context and prompt -> Ollama.

#### Deployment View

The independent `lab-open-webui` profile defines `/health` on container port
`8080`. Its host publication defaults to `127.0.0.1:18095`. It uses the CUDA
image pinned in Compose without a GPU reservation. The LAB data bind at
`${LAB_DATA_DIR}/open-webui/data` holds SQLite, uploads, vectors and the
session key. Root Compose excludes the LAB. HOME promotion stays undecided,
and retirement of earlier HOME state requires separate approval under RUN-0057.

## Interfaces

### Contracts

- `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` selects the approved local inference and
  embedding endpoint.
- The native Keycloak OIDC configuration uses PKCE S256 and a LAB-only
  client secret. The declared callback still uses the prior gateway origin.
  LAB login requires a registered redirect for an approved HTTPS origin.
- `/health` on container port `8080` reports application health.

### Failure Boundaries

A missing or unreachable model endpoint blocks chat and embedding acceptance.
Compose does not order Ollama startup across project boundaries. Chat state and
RAG vectors share one data volume. A write-stopped capture and a verified
isolated restore are separate steps under RUN-0057.

## Decisions

### Decision Links

- [ADR-0059 native OIDC decision](../decisions/0059-native-oidc-open-webui-and-airflow.md)
- [ADR-0062 current placement](../decisions/0062-home-lab-membership.md)

### Quality and Risks

#### Quality Attributes

- **Security:** native Keycloak OIDC with password login, signup, email merge
  and OAuth role/group management disabled. LAB login depends on approval of
  the secure origin described above.
- **Reliability:** depends on a healthy Ollama service.
- **Recoverability:** preserve the full LAB data root and the corresponding
  credential custody. HOME Restic does not cover LAB state.

#### Risks

- The service is stateful on local storage; horizontal scaling would first need
  an external database and vector store.

## Traceability

### Requirement Mapping

- [REQ-0013 Open WebUI requirement](../../01.requirements/0013-ai-open-webui.md)

### Currentness and Lineage

- [AD-0008 AI infrastructure](0008-ai-architecture.md)
- [RUN-0057 LAB operation and separately approved HOME retirement](../../05.operations/runbooks/15-labs/0057-open-webui.md)

#### Evolution

Moving RAG vectors to Qdrant would need a Compose change and a new decision;
none is current.
