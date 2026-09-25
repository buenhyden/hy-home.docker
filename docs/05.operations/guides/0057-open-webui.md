---
title: "Open WebUI Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0057"
parent_ids:
- "POL-0057"
implementation_services:
  infra/08-ai/open-webui/docker-compose.yml:
  - open-webui
created: "2026-05-10"
---

# Open WebUI Usage Guide

## Usage

### Overview

이 문서는 `hy-home.docker` 환경에서 Open WebUI를 통해 Ollama 모델과 대화하고, 문서 기반 RAG를 사용하는 방법을 설명한다. 현재 구현은 `infra/08-ai/open-webui/docker-compose.yml`에 있고 root `docker-compose.yml`이 이를 무조건 include하며, `open-webui`는 `ai` profile을 선택할 때 기동된다. 접근/인증, 모델 선택, 문서 인덱싱, 기본 점검은 그 profile이 선택된 런타임을 기준으로 수행한다.

### Usage Type

`system-guide`

### Target Audience

- AI Engineer
- Operator
- Internal User
- Agent-tuner

### Purpose

- Open WebUI의 핵심 사용 흐름(접속, 인증, 모델 선택, 채팅)을 표준화한다.
- RAG 인덱싱 및 질의 흐름을 `OLLAMA_BASE_URL`, `RAG_EMBEDDING_MODEL` 기준으로 이해한다. `VECTOR_DB`가 없으므로 벡터는 Open WebUI 로컬 저장소에 있다.
- 장애 징후를 빠르게 식별하고 런북으로 연결한다.

### Prerequisites

- root `docker-compose.yml`은 `infra/08-ai/ollama/docker-compose.yml`과 `infra/08-ai/open-webui/docker-compose.yml`을 무조건 include하므로, 실행 시 `ai` profile을 선택해야 한다.
- `open-webui`, `ollama` 컨테이너가 root compose project 안에서 기동 가능해야 한다.
- `ollama` 컨테이너가 `http://ollama:${OLLAMA_PORT:-11434}`로 접근 가능해야 한다.
- Open WebUI 환경변수 확인:
  - `OLLAMA_BASE_URL`
  - `RAG_EMBEDDING_MODEL` (현재 값은 Compose 선언 확인)
- Keycloak의 전용 `home-openwebui` client와 native OIDC 경로가 정상이어야 한다.
  이 서비스는 `sso-auth@file`을 사용하지 않는다.

### Step-by-step Instructions

#### 1. Access & Authentication

1. 브라우저에서 `https://chat.${DEFAULT_URL}` 접속.
2. 로그인 화면에서 **Keycloak**을 선택하고 기존 계정으로 로그인한다.
3. 기존 권한으로 Open WebUI 대시보드에 들어가는지 확인한다. 로컬 비밀번호
   로그인과 신규 가입은 비활성화되어 있다.
4. 로그인 루프 또는 401 발생 시 먼저 인증 계층 상태를 확인한다.

#### 2. Model Selection & Chat

1. 상단 모델 선택기에서 Ollama 모델을 선택한다.
2. 간단한 프롬프트(예: `hello`)로 응답 확인.
3. 모델 목록이 비어 있으면 Open WebUI에서 Ollama 연결 상태를 점검한다.

#### 3. RAG Document Indexing

1. 문서 업로드 메뉴에서 PDF/TXT 문서를 업로드한다.
2. Open WebUI가 `RAG_EMBEDDING_MODEL`로 임베딩을 만들어 로컬 벡터 저장소에 저장하는지 확인한다.
3. 업로드된 문서를 지정하여 질의하고, 답변에 문서 근거가 반영되는지 확인한다.

#### 4. Quick Connectivity Checks

```bash
# Open WebUI health is internal unless a host port is explicitly published.
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health

## Open WebUI -> Ollama connectivity (컨테이너 내부)
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

```

### 5. Advanced Settings

1. 모델별 시스템 프롬프트(System Prompt)를 워크로드에 맞게 분리한다.
2. Temperature, Top-K, Top-P를 모델 특성에 맞춰 조정한다.
3. 임베딩 모델 변경 시 기존 인덱스 재생성 계획을 먼저 수립한다.

### Common Pitfalls

- **Ollama 연결 실패**: `OLLAMA_BASE_URL` 오타 또는 `ollama` 비정상 상태.
- **임베딩 모델 누락**: `RAG_EMBEDDING_MODEL`이 Ollama에 준비되지 않아 인덱싱 실패.
- **VRAM OOM**: 동시 인덱싱/추론 증가로 응답 지연 또는 실패.
- **SSO 문제**: 인증 미들웨어/리디렉션 설정 불일치로 접근 실패.

### Source-backed operating contract

- **Purpose/classification**: `open-webui` is an owner-confirmed `HOME` chat/RAG interface.
- **Profiles/source**: `ai`/`ai-llm` select the service. [Compose](../../../infra/08-ai/open-webui/docker-compose.yml), its selected image, and startup environment are authoritative.
- **Flow/dependencies**: users enter through Traefik `gateway-standard-chain@file`; native Keycloak OIDC uses client `home-openwebui`; Open WebUI calls Ollama over `ai_net` and keeps vectors in its local store. Current source does not use `sso-auth@file`. Password login/signup, email merge, and OAuth role/group management remain disabled.
- **State/secrets**: `open-webui:/app/backend/data` contains the default SQLite database, uploads, chat/user state, and application data. Preserve `openwebui_oidc_client_secret`, session/auth secrets declared by Compose, the root CA. RAG vectors live in the same data volume, so no separate vector-store backup applies. Never expose values in rendered config or logs.
- **Resources/security**: Compose values are source limits, not measured headroom. Keep the UI behind native OIDC and the gateway standard chain; do not enable local password/signup paths as an incident workaround.
- **Normal use/lifecycle**: render with `docker compose --profile ai config --quiet`; verify health, OIDC login, Ollama model listing, and a controlled RAG query. Stop Open WebUI before a consistent SQLite/data-volume backup. For upgrades, preserve the volume and matching secrets, review upstream migrations, update one version boundary, then verify identities/chats/uploads/OIDC and coordinate Qdrant recovery separately.
- **Upstream/license**: follow official [environment configuration](https://docs.openwebui.com/reference/env-configuration/), [SSO](https://docs.openwebui.com/features/authentication-access/auth/sso/), [updates/backups](https://docs.openwebui.com/getting-started/updating/), and [database migration](https://docs.openwebui.com/troubleshooting/manual-database-migration/) guidance. Verify the license terms of the pinned Open WebUI release before redistribution or modified deployment.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
- Runtime approval 후 `ai` profile을 선택한 상태에서 `docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0057-open-webui.md)을 따른다.

## Traceability

- Declared parent: [Open WebUI Operations Policy](../policies/0057-open-webui.md) (`POL-0057`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Policy](../policies/0057-open-webui.md) (`POL-0057`), [Runbook](../runbooks/0057-open-webui.md) (`RUN-0057`)

## Related Documents

- [Open WebUI Compose](../../../infra/08-ai/open-webui/docker-compose.yml)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Operations policy](../policies/0057-open-webui.md)
- [Recovery runbook](../runbooks/0057-open-webui.md)
