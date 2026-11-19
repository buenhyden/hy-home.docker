---
title: "08-AI Optimization Hardening Architecture Description"
version: "1.2.0"
type: "sdlc/architecture-description"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "architecture"
artifact_id: "AD-0023"
parent_ids:
- "REQ-0009"
created: "2026-03-28"
---

# 08-AI Optimization Hardening Architecture Description

## Context and Boundaries

### System Boundary

- **Owns**: Ollama gateway ingress and identity, the Open WebUI LAB access
  and stateful storage boundaries, the Ollama concurrency and queue ceiling,
  and the `08-ai` checks of the hardening gate.
- **Consumes**: the `01-gateway` standard middleware chain, the `02-auth`
  ForwardAuth middleware and Keycloak OIDC.
- **Does not own**: model training or fine-tuning, Qdrant schema and index
  operation, and the other `08-ai` packages (ComfyUI, Crawl4AI, MLflow, Open
  Notebook), whose boundaries are recorded by their own owners; Open Notebook
  and MLflow are in [AD-0025](0025-laboratory-optimization-hardening-architecture.md).
- **Non-goals**: a distributed GPU scheduler and parallel external LLM
  providers.

#### Purpose and Readers

This Description records the hardening scope for HOME Ollama, the local LLM
inference and embedding engine, and the independent Open WebUI LAB. It covers
their distinct access and identity boundaries, GPU concurrency limits,
stateful storage and the shared hardening gate.
Requirement owners, implementers and operators share these concerns; the tier
structure itself is in [AD-0008](0008-ai-architecture.md).

#### Context

The HOME Ollama route uses Traefik `websecure`. Open WebUI uses a separate
LAB bind, native Keycloak OIDC, and an approved, reachable Ollama endpoint
for generation and embedding. The LAB has no gateway route or HOME network
attachment.

### Constraints

The HOME Ollama route passes the standard gateway chain and ForwardAuth.
LAB login requires a separately approved HTTPS origin and matching identity
redirect. The Ollama concurrency and queue defaults below bound GPU load.
Static hardening evidence covers configuration, while service health and
login require an actual runtime check.

## Structure

### Building Blocks

- **Ingress**: Traefik `websecure` routes `ollama.${DEFAULT_URL}` through
  `gateway-standard-chain`, `sso-errors` and `sso-auth`
  (`infra/08-ai/ollama/docker-compose.yml`). Open WebUI uses the bind in
  [`labs/open-webui/docker-compose.yml`](../../../labs/open-webui/docker-compose.yml)
  and native Keycloak OIDC with the login form and OAuth sign-up disabled.
- **Inference and RAG**: Open WebUI calls Ollama for generation and embedding
  (`RAG_EMBEDDING_ENGINE: ollama`). It sets no external vector database, so its
  vector store is the default embedded store inside its own data volume.
- **Control**: the gateway and identity middleware, the hardening script and
  CI job, and the Operations guide, policy and runbook.

### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `ollama.${DEFAULT_URL}` route (Traefik `websecure`) | HOME Ollama | The description names no consumer for this interface. | `gateway-standard-chain`, `sso-errors` and `sso-auth` in `infra/08-ai/ollama/docker-compose.yml` | The description records no failure handling for this interface. |
| Open WebUI LAB bind | Open WebUI | The description names no consumer for this interface. | [`labs/open-webui/docker-compose.yml`](../../../labs/open-webui/docker-compose.yml) with native Keycloak OIDC | The description records no failure handling for this interface. |
| `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` generation and embedding endpoint | Approved, reachable Ollama endpoint | Open WebUI | The description links no contract for this interface. | LAB health checks do not order startup across projects; verify access to the approved Ollama endpoint before accepting chat or embedding. |
| SSO and identity | `02-auth` ForwardAuth middleware and Keycloak OIDC | HOME Ollama route and Open WebUI | `sso-errors` and `sso-auth` in `infra/08-ai/ollama/docker-compose.yml` for HOME Ollama; [ADR-0059](../02.decisions/0059-native-oidc-open-webui-and-airflow.md) for Open WebUI native Keycloak OIDC | The description records no failure handling for this interface. |
| Metrics | `ollama-exporter` | The description names no consumer for this interface. | The description links no contract for this interface. | The description records no failure handling for this interface. |

- Traefik `websecure` routes `ollama.${DEFAULT_URL}` per the Ingress item in
  Building Blocks. Open WebUI uses its independent LAB bind.
- Open WebUI uses `LAB_OPEN_WEBUI_OLLAMA_BASE_URL` for generation and embedding.
- Ollama concurrency and queue limits are set in `infra/08-ai/ollama/docker-compose.yml:42-44`.

## Runtime Behavior

### Normal Flow

#### Runtime View

- **Entities**: model artifacts, conversation and session metadata, and
  embedding vectors.
- **Storage**: the Ollama model cache is bound from
  `${OLLAMA_MODEL_DIR:-${DEFAULT_AI_MODEL_DIR}/ollama}`; Open WebUI state,
  including its embedded vector store, is bound from
  `${LAB_DATA_DIR}/open-webui/data`.
- **Concurrency**: Ollama defaults to `OLLAMA_NUM_PARALLEL=2`,
  `OLLAMA_MAX_LOADED_MODELS=1` and `OLLAMA_MAX_QUEUE=16`
  (`infra/08-ai/ollama/docker-compose.yml:42-44`).

#### Deployment View

- **Platform**: root Compose includes `infra/08-ai/ollama` (Ollama and
  `ollama-exporter`). Open WebUI lives in a separate Compose project and
  `lab-open-webui` profile with its own network and data root.
- **Evidence**: `scripts/validation/validate-docker-compose.sh`,
  `scripts/hardening/check-all-hardening.sh 08-ai` and the CI
  `infrastructure-hardening` job. These are static checks; they prove no
  running service or login.

### Failure and Recovery

LAB health checks do not order startup across projects. Verify access to the
approved Ollama endpoint before accepting chat or embedding. The Ollama
concurrency and queue ceiling bounds GPU load. Losing the Open WebUI data bind
loses the embedded RAG index and application state. The operations owners
linked under Currentness and Lineage govern change and recovery.

## Quality Scenarios

### Scenarios

#### Quality Attributes

- **Performance**: the Ollama concurrency and queue ceiling bounds GPU load.
- **Security**: HOME Ollama uses the gateway standard chain and ForwardAuth.
  Open WebUI uses its LAB bind and native OIDC.
- **Reliability**: each project has its own health checks and requires a
  reachable dependency where applicable.
- **Observability**: `ollama-exporter` supplies metrics, and the hardening gate
  detects contract drift.

#### Risks

- Open WebUI relies on its own OIDC configuration rather than gateway
  ForwardAuth, so a change to that configuration changes its access boundary.
- The embedded vector store shares the Open WebUI volume; losing it loses the
  RAG index along with the application state.

### Trade-offs

- The Ollama concurrency and queue ceiling (`OLLAMA_NUM_PARALLEL=2`,
  `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_MAX_QUEUE=16`) bounds GPU load; a
  distributed GPU scheduler is a non-goal (Runtime View, System Boundary).
- Open WebUI relies on its own OIDC configuration rather than gateway
  ForwardAuth, so a change to that configuration changes its access boundary
  (Risks).
- Open WebUI sets no external vector database; the embedded store shares its
  data volume, so losing that bind loses the RAG index with the application
  state (Risks, Failure and Recovery).
- Static hardening evidence covers configuration only; service health and
  login require an actual runtime check (Constraints).

## Decisions and Adoption

### Decisions

- **Identity decision**: [ADR-0059](../02.decisions/0059-native-oidc-open-webui-and-airflow.md)
- **Current placement**: [ADR-0062](../02.decisions/0062-home-lab-membership.md)

### Adoption Boundaries

#### Requirement Mapping

- **PRD**: [REQ-0009](../../01.requirements/0009-ai.md)

#### Currentness and Lineage

- **Tier Architecture Description**: [AD-0008 AI Infrastructure Architecture Description](0008-ai-architecture.md)
- **Open WebUI Architecture Description**: [AD-0013](0013-open-webui-architecture.md)
- **Guide**: [AI optimization hardening guide](../../05.operations/01.guides/09.ai-and-search/0058-ai-optimization-hardening.md)
- **Policy**: [AI optimization hardening policy](../../05.operations/02.policies/09.ai-and-search/0058-ai-optimization-hardening.md)
- **Runbook**: [AI optimization hardening runbook](../../05.operations/03.runbooks/09.ai-and-search/0058-ai-optimization-hardening.md)

#### Evolution

- **Ollama**: a model cache and storage policy, a GPU scheduling ceiling and a
  model promotion procedure from experiment to production.
- **Open WebUI**: role- or environment-based model access and a conversation
  log retention and masking policy.

Runtime pins are owned by Compose/Dockerfile declarations; the [derived Compose image projection](../../../infra/tech-stack.versions.json) supplies Compose-image drift verification.
