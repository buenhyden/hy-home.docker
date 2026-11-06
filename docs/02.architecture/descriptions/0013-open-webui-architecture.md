---
title: "Open WebUI Architecture Description"
version: "1.1.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "architecture"
artifact_id: "AD-0013"
parent_ids:
- "REQ-0013"
created: "2026-03-27"
---
# Open WebUI Architecture Description

## Overview

Open WebUI is the HOME chat interface and retrieval-augmented generation (RAG)
orchestrator for the AI tier. It sits between end users and the local Ollama
inference API. Its obligations are owned by
[REQ-0013](../../01.requirements/0013-ai-open-webui.md).

## Scope

- **Owns:** the web UI and backend, RAG orchestration, and user, chat, upload
  and vector-store data under `/app/backend/data`.
- **Consumes:** the Ollama API at `http://ollama:${OLLAMA_PORT:-11434}` for
  inference and for embeddings (`RAG_EMBEDDING_ENGINE: ollama`), and native
  Keycloak OIDC through the `home-openwebui` client behind Traefik's standard
  gateway chain.
- **Does not own:** model weights (Ollama) or any Qdrant collection. Compose
  sets no external vector database, so RAG vectors use the application's
  built-in store in its data volume.
- **Non-goals:** model training or fine-tuning.

## Structure

### Architecture

The `open-webui` service (`infra/08-ai/open-webui/docker-compose.yml`, tier
label `ai`) joins `edge_net` and `ai_net`. Traefik serves `chat.${DEFAULT_URL}`
over TLS with `gateway-standard-chain@file`; it does not apply `sso-auth@file`,
because Open WebUI authenticates users itself through OIDC. The OIDC client
secret comes from a Docker secret or the OpenBao Agent output mounted read-only
under `/run/openbao/open-webui`.

## Runtime and Deployment

### Runtime View

- User input -> Open WebUI -> Ollama (generation).
- Document upload -> Open WebUI -> Ollama (embedding) -> built-in vector store.
- Query -> built-in vector store (retrieval) -> context and prompt -> Ollama.

### Deployment View

Open WebUI is a HOME service selected by the `ai` and `ai-llm` profiles. It
starts after Ollama reports healthy, and its health endpoint is `/health` on
container port `${OLLAMA_WEBUI_PORT:-8080}`. The image is the CUDA build pinned
in Compose; Compose reserves no GPU for this service. Data persists in the
`${DEFAULT_AI_MODEL_DIR}/open-webui` bind volume.

## Quality and Risks

### Quality Attributes

- **Security:** native Keycloak OIDC; Compose disables password login, signup,
  email merge and OAuth role/group management, and the gateway supplies TLS and
  the standard chain.
- **Reliability:** depends on a healthy Ollama service.
- **Recoverability:** chat state and RAG vectors share one data volume, so a
  write-stopped capture of that volume restores both.

### Risks

- The service is stateful on local storage; horizontal scaling would first need
  an external database and vector store.

### Evolution

Moving RAG vectors to Qdrant would need a Compose change and a new decision;
none is current.

## Related Documents

- [REQ-0013 Open WebUI requirement](../../01.requirements/0013-ai-open-webui.md)
- [AD-0008 AI infrastructure](0008-ai-architecture.md)
- [ADR-0059 Native OIDC for Open WebUI and the Airflow UI](../decisions/0059-native-oidc-open-webui-and-airflow.md)

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
