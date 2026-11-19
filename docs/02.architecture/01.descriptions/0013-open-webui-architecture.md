---
title: "Open WebUI Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0013"
parent_ids:
- "REQ-0013"
created: "2026-03-27"
---

# Open WebUI Architecture Description

## Context and Boundaries

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

#### Purpose and Readers

Open WebUI is an independent LAB for evaluating chat and retrieval-augmented
generation (RAG) with a local Ollama endpoint. Its obligations are owned by
[REQ-0013](../../01.requirements/0013-ai-open-webui.md).

#### Context

The LAB publishes the UI on its own bind address. It uses the operator's approved Ollama endpoint and reaches the identity provider through the Keycloak gateway name. Successful browser access and authentication require a suitable LAB origin and separate runtime evidence.

### Constraints

The service is stateful on local storage; horizontal scaling would first need an external database and vector store. Compose disables password login, signup, email merge and OAuth role/group management. Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.

## Structure

### Building Blocks

[`labs/open-webui/docker-compose.yml`](../../../labs/open-webui/docker-compose.yml)
defines the `open-webui` service on `lab_open_webui_net` alone. It declares no
gateway route or HOME network attachment. Its native OIDC entrypoint reads the
LAB-only Compose secret. The retained HOME OpenBao Agent output has no LAB bind.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Ollama inference and embedding endpoint | Approved Ollama endpoint | `open-webui` | `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` with `RAG_EMBEDDING_ENGINE: ollama` | A missing or unreachable model endpoint blocks chat and embedding acceptance. |
| Native Keycloak OIDC | Keycloak through the Keycloak gateway name | `open-webui` (`home-openwebui` client) | PKCE S256 with a LAB-only client secret; [ADR-0059 native OIDC decision](../02.decisions/0059-native-oidc-open-webui-and-airflow.md) | The description records no failure handling for this interface. |
| Web UI host publication | `open-webui` | Browsers on the LAB bind address (default `127.0.0.1:18095`) | [`labs/open-webui/docker-compose.yml`](../../../labs/open-webui/docker-compose.yml) | The description records no failure handling for this interface. |
| `/health` on container port `8080` | `open-webui` | The description names no consumer for this interface. | The description links no contract for this interface. | The description records no failure handling for this interface. |

- `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` selects the approved local inference and
  embedding endpoint.
- The native Keycloak OIDC configuration uses PKCE S256 and a LAB-only
  client secret. The declared callback still uses the prior gateway origin.
  LAB login requires a registered redirect for an approved HTTPS origin.
- `/health` on container port `8080` reports application health.

## Runtime Behavior

### Normal Flow

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

### Failure and Recovery

A missing or unreachable model endpoint blocks chat and embedding acceptance.
Compose does not order Ollama startup across project boundaries. Chat state and
RAG vectors share one data volume. A write-stopped capture and a verified
isolated restore are separate steps under RUN-0057.

## Quality Scenarios

### Scenarios

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

### Trade-offs

- The service is stateful on local storage with RAG vectors in the built-in
  store of its data volume; horizontal scaling would first need an external
  database and vector store (Constraints, Risks).
- Chat state and RAG vectors share one data volume (Failure and Recovery).
- Reliability depends on a healthy Ollama service, and Compose does not order
  Ollama startup across project boundaries (Quality Attributes, Failure and
  Recovery).
- Password login, signup, email merge and OAuth role/group management are
  disabled in favor of native Keycloak OIDC; LAB login depends on approval of
  a secure origin (Quality Attributes).
- HOME Restic does not cover LAB state (Quality Attributes).

## Decisions and Adoption

### Decisions

- [ADR-0059 native OIDC decision](../02.decisions/0059-native-oidc-open-webui-and-airflow.md)
- [ADR-0062 current placement](../02.decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- [REQ-0013 Open WebUI requirement](../../01.requirements/0013-ai-open-webui.md)

#### Currentness and Lineage

- [AD-0008 AI infrastructure](0008-ai-architecture.md)
- [RUN-0057 LAB operation and separately approved HOME retirement](../../05.operations/03.runbooks/15.labs/0057-open-webui.md)

#### Evolution

Moving RAG vectors to Qdrant would need a Compose change and a new decision;
none is current.
