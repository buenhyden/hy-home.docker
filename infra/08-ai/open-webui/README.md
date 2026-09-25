---
title: "Open WebUI"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2025-11-12"
---

# Open WebUI

## Overview

Open WebUI (formerly Ollama WebUI) provides a ChatGPT-like interface for local LLMs. Beyond simple chat, it acts as a RAG (Retrieval-Augmented Generation) orchestrator, using its built-in local vector store for document search and Ollama for embedding generation.

## Audience

이 README의 주요 독자:

- End Users (Chat interface)
- AI Engineers (RAG & Prompt Engineering)
- Developers (Service integration)
- Operators (Resource management)
- AI Agents

## Scope

### In Scope

- `docker-compose.yml`: Interface & RAG backend orchestration.
- RAG configuration: embedding model; vectors stay in Open WebUI's local store (`VECTOR_DB` unset).
- Traefik routing and native OIDC configuration.

### Out of Scope

- Model weights: Managed in [ollama](../ollama/README.md).
- Vector persistence: Open WebUI's local store in its data volume; Qdrant is not used.

## Structure

```text
open-webui/
├── docker-compose.yml  # Svelte-based interface & RAG backend
├── docker-entrypoint.sh # Client secret and combined CA loading
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Open WebUI service leaf in `08-ai`; services: `open-webui`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` |
| Config files | `docker-compose.yml`, `docker-entrypoint.sh` |
| Config values | env keys: `OLLAMA_BASE_URL`, `RAG_EMBEDDING_ENGINE`, `RAG_EMBEDDING_MODEL`; profiles: `ai` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` |
| Networks | `ai_net`, `edge_net` |
| Volumes | `open-webui:/app/backend/data:rw`, `open-webui` |
| Ports | Not declared |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-webui.rule`, `traefik.http.routers.open-webui.entrypoints`, `traefik.http.routers.open-webui.tls`, `traefik.http.services.open-webui.loadbalancer.server.port`, `traefik.http.routers.open-webui.middlewares` |
| Secret refs | `openwebui_oidc_client_secret`; root:root 0600 host file |
| Healthcheck | Compose healthcheck declared for `open-webui` |
| Operations | Guide (`docs/05.operations/guides/0057-open-webui.md`), Policy (`docs/05.operations/policies/0057-open-webui.md`), Runbook (`docs/05.operations/runbooks/0057-open-webui.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with `bash scripts/hardening/check-all-hardening.sh 08-ai`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Read the Open WebUI Interface & RAG Guide (`docs/05.operations/guides/0057-open-webui.md`).
2. Access the UI at `https://chat.${DEFAULT_URL}` with SSO.
3. Verify the connection to Ollama before document indexing.

## Troubleshooting

- Start with `bash scripts/hardening/check-all-hardening.sh 08-ai` to confirm Open WebUI hardening contracts.
- Do not run this service-local compose file as a standalone config check; it depends on the root network context.
- Check Open WebUI logs and the linked runbook before changing RAG, auth, or model endpoint settings.

### Convergence contract

- Classification: **HOME**. Exact profiles: `ai`, `ai-llm`.
- Source authority: this package Compose and its selected image/build inputs; `infra/tech-stack.versions.json` is a derived projection.
- Root preflight: `docker compose --profile ai config --quiet`. Root targeted start: `docker compose --profile ai up -d open-webui`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/guides/0057-open-webui.md`; IDs `GDE-0057`, `POL-0057`, `RUN-0057`.
- The subject runbook's isolated recovery is planned and unexecuted. Preserve model/content provenance and never use a live filesystem copy as restore evidence.

## Related Documents

- [Ollama Implementation](../ollama/README.md)
- [Qdrant Implementation](../../04-data/specialized/qdrant/README.md)
- Open WebUI usage guide (`docs/05.operations/guides/0057-open-webui.md`)
- Open WebUI operations policy (`docs/05.operations/policies/0057-open-webui.md`)
- Open WebUI recovery runbook (`docs/05.operations/runbooks/0057-open-webui.md`)
- [Documentation index](../../../docs/README.md)

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 08-ai` after README or Compose reference changes that affect Open WebUI.
- Run `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh` for the current root-active profile surface.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` to keep service documentation and operation links synchronized.

## Configuration

### Native OIDC

Open WebUI uses the dedicated Keycloak client `home-openwebui`, S256 PKCE and
`/oauth/oidc/callback`. Its router keeps only `gateway-standard-chain@file`.
Trusted-header auth, OAuth signup, email merge, role/group management and password
authentication are disabled. The existing administrator keeps the same local ID
and role after the verified OIDC linkage. Public/local CA roots are combined; TLS
verification is enabled.

`ENABLE_LOGIN_FORM=false` hides the form, while `ENABLE_PASSWORD_AUTH=false`
separately rejects the password API. Persisted UI configuration must also be
verified. See the runbook
(`docs/05.operations/runbooks/0057-open-webui.md`) for secret ownership,
one-key configuration updates and recovery.

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `OLLAMA_BASE_URL` | Yes | Endpoint for Ollama API. |
| `RAG_EMBEDDING_MODEL` | Yes | Model used for document indexing; the current value is owned by Compose. |

## Change Impact

- Changes to `docker-compose.yml` may affect SSO authentication flows.
- Updating `RAG_EMBEDDING_MODEL` requires re-indexing of existing documents.

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../tech-stack.versions.json) provides drift verification.
