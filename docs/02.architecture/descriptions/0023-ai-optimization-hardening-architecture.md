---
title: "08-AI Optimization Hardening Architecture Description"
version: "1.1.1"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "architecture"
artifact_id: "AD-0023"
parent_ids:
- "REQ-0009"
created: "2026-03-28"
---

# 08-AI Optimization Hardening Architecture Description

## Overview

### Purpose and Readers

This Description records the hardening structure of the two core `08-ai`
planes: Ollama, the local LLM inference and embedding engine, and Open WebUI,
the chat interface and RAG orchestrator. It covers their gateway and identity
boundary, GPU concurrency limits, stateful storage and the hardening gate.
Requirement owners, implementers and operators share these concerns; the tier
structure itself is in [AD-0008](0008-ai-architecture.md).

### System Boundary

- **Owns**: the ingress and identity boundary of the Ollama and Open WebUI
  routes, the Ollama concurrency and queue ceiling, the Open WebUI stateful
  storage contract, and the `08-ai` checks of the hardening gate.
- **Consumes**: the `01-gateway` standard middleware chain, the `02-auth`
  ForwardAuth middleware and Keycloak OIDC.
- **Does not own**: model training or fine-tuning, Qdrant schema and index
  operation, and the other `08-ai` packages (ComfyUI, Crawl4AI, MLflow, Open
  Notebook), whose boundaries are recorded by their own owners; Open Notebook
  and MLflow are in [AD-0025](0025-laboratory-optimization-hardening-architecture.md).
- **Non-goals**: a distributed GPU scheduler and parallel external LLM
  providers.

## Context and Constraints

### Context

Users reach `ollama.${DEFAULT_URL}` and `chat.${DEFAULT_URL}` through Traefik `websecure`. The Description consumes the `01-gateway` standard middleware chain, the `02-auth` ForwardAuth middleware and Keycloak OIDC, and Open WebUI calls Ollama for generation and embedding.

### Constraints

Every public route passes the gateway standard chain, plus ForwardAuth for Ollama or native OIDC for Open WebUI. Ollama defaults to `OLLAMA_NUM_PARALLEL=2`, `OLLAMA_MAX_LOADED_MODELS=1` and `OLLAMA_MAX_QUEUE=16`, which bounds GPU load, and the hardening checks are static, so they prove no running service or login.

## Current Structure

### Building Blocks

- **Ingress**: Traefik `websecure` routes `ollama.${DEFAULT_URL}` through
  `gateway-standard-chain`, `sso-errors` and `sso-auth`
  (`infra/08-ai/ollama/docker-compose.yml:79`). It routes `chat.${DEFAULT_URL}`
  to Open WebUI through `gateway-standard-chain` only; Open WebUI
  authenticates users with native Keycloak OIDC, with the login form and OAuth
  sign-up disabled (`infra/08-ai/open-webui/docker-compose.yml:44-62,73`).
- **Inference and RAG**: Open WebUI calls Ollama for generation and embedding
  (`RAG_EMBEDDING_ENGINE: ollama`). It sets no external vector database, so its
  vector store is the default embedded store inside its own data volume.
- **Control**: the gateway and identity middleware, the hardening script and
  CI job, and the Operations guide, policy and runbook.

### Runtime and Deployment

#### Runtime View

- **Entities**: model artifacts, conversation and session metadata, and
  embedding vectors.
- **Storage**: the Ollama model cache is bound from
  `${OLLAMA_MODEL_DIR:-${DEFAULT_AI_MODEL_DIR}/ollama}`; Open WebUI state,
  including its embedded vector store, is bound from
  `${DEFAULT_AI_MODEL_DIR}/open-webui`.
- **Concurrency**: Ollama defaults to `OLLAMA_NUM_PARALLEL=2`,
  `OLLAMA_MAX_LOADED_MODELS=1` and `OLLAMA_MAX_QUEUE=16`
  (`infra/08-ai/ollama/docker-compose.yml:42-44`).

#### Deployment View

- **Platform**: Docker Compose packages `infra/08-ai/ollama` (Ollama and
  `ollama-exporter`) and `infra/08-ai/open-webui` (stateful, depends on
  Ollama), included by the root `docker-compose.yml` under the `ai` profile.
- **Evidence**: `scripts/validation/validate-docker-compose.sh`,
  `scripts/hardening/check-all-hardening.sh 08-ai` and the CI
  `infrastructure-hardening` job. These are static checks; they prove no
  running service or login.

## Interfaces

### Contracts

- Traefik `websecure` routes `ollama.${DEFAULT_URL}` and `chat.${DEFAULT_URL}` per the Ingress item in Building Blocks.
- Open WebUI calls Ollama for generation and embedding (`RAG_EMBEDDING_ENGINE: ollama`).
- Ollama concurrency and queue limits are set in `infra/08-ai/ollama/docker-compose.yml:42-44`.

### Failure Boundaries

Health-gated dependencies and healthchecks order startup. The Ollama concurrency and queue ceiling bounds GPU load. The embedded vector store shares the Open WebUI volume, so losing it loses the RAG index along with the application state. The guide, policy and runbook linked under Currentness and Lineage govern change and recovery.

## Decisions

### Decision Links

- **ADR**: [ADR-0059](../decisions/0059-native-oidc-open-webui-and-airflow.md)

### Quality and Risks

#### Quality Attributes

- **Performance**: the Ollama concurrency and queue ceiling bounds GPU load.
- **Security**: every public route passes the gateway standard chain, plus
  ForwardAuth for Ollama or native OIDC for Open WebUI.
- **Reliability**: health-gated dependencies and healthchecks order startup.
- **Observability**: `ollama-exporter` supplies metrics, and the hardening gate
  detects contract drift.

#### Risks

- Open WebUI relies on its own OIDC configuration rather than gateway
  ForwardAuth, so a change to that configuration changes its access boundary.
- The embedded vector store shares the Open WebUI volume; losing it loses the
  RAG index along with the application state.

## Traceability

### Requirement Mapping

- **PRD**: [REQ-0009](../../01.requirements/0009-ai.md)

### Currentness and Lineage

- **Tier Architecture Description**: [AD-0008 AI Infrastructure Architecture Description](0008-ai-architecture.md)
- **Open WebUI Architecture Description**: [AD-0013](0013-open-webui-architecture.md)
- **Guide**: [AI optimization hardening guide](../../05.operations/guides/09-ai-and-search/0058-ai-optimization-hardening.md)
- **Policy**: [AI optimization hardening policy](../../05.operations/policies/09-ai-and-search/0058-ai-optimization-hardening.md)
- **Runbook**: [AI optimization hardening runbook](../../05.operations/runbooks/09-ai-and-search/0058-ai-optimization-hardening.md)

#### Evolution

- **Ollama**: a model cache and storage policy, a GPU scheduling ceiling and a
  model promotion procedure from experiment to production.
- **Open WebUI**: role- or environment-based model access and a conversation
  log retention and masking policy.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
