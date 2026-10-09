---
title: "Open WebUI Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
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

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

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

### Open WebUI -> Ollama connectivity (컨테이너 내부)
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

- **목적·분류**: `open-webui`는 소유자가 확인한 `HOME` chat/RAG interface다.
- **profile·구현 소유권**: `ai`/`ai-llm`으로 서비스를 선택한다. [Compose](../../../infra/08-ai/open-webui/docker-compose.yml), 선택된 image와 startup 환경 설정이 구현을 소유한다.
- **흐름·의존성**: 사용자는 Traefik `gateway-standard-chain@file`을 통해 접속한다. native Keycloak OIDC는 client `home-openwebui`를 사용한다. Open WebUI는 `ai_net`으로 Ollama를 호출하고 vector를 local store에 보관한다. 현재 source는 `sso-auth@file`을 사용하지 않는다. password login/signup, email merge와 OAuth role/group 관리는 비활성화된 상태를 유지한다.
- **상태·secret**: `open-webui:/app/backend/data`에는 기본 SQLite database, upload, chat/user state와 application data가 있다. `openwebui_oidc_client_secret`, Compose가 선언한 session/auth secret과 root CA를 보존한다. RAG vector도 같은 data volume에 있으므로 별도 vector-store backup은 적용되지 않는다. 렌더링된 config나 log에 값을 노출하지 않는다.
- **자원·보안**: Compose 값은 source limit이며 측정된 여유 용량이 아니다. UI를 native OIDC와 gateway standard chain 뒤에 유지한다. incident 우회책으로 local password/signup 경로를 활성화하지 않는다.
- **정상 사용·수명 주기**: `docker compose --profile ai config --quiet`로 렌더링하고 health, OIDC login, Ollama model 목록과 통제된 RAG query를 검증한다. 일관된 SQLite/data-volume backup 전에 Open WebUI를 중지한다. upgrade할 때는 volume과 이에 맞는 secret을 보존하고 upstream migration을 검토한 뒤 version 경계를 한 번에 하나씩 변경한다. 이후 identity/chat/upload/OIDC를 검증하고, RUN-0057을 통해 서로 대응하는 local Chroma index와 upload를 확인한다. Qdrant 의존성은 선언되어 있지 않다.
- **공식 문서·license**: 공식 [환경 설정](https://docs.openwebui.com/reference/env-configuration/), [SSO](https://docs.openwebui.com/features/authentication-access/auth/sso/), [update/backup](https://docs.openwebui.com/getting-started/updating/), [database migration](https://docs.openwebui.com/troubleshooting/manual-database-migration/) 지침을 따른다. 재배포하거나 수정하여 배포하기 전에 고정된 Open WebUI release의 license 조건을 확인한다.

### Local data and authentication boundary

선언 릴리스는 `DATA_DIR/vector_db`의 Chroma를 기본으로 쓰며 Compose에는 외부 vector-store나 Qdrant 연결이 없다. SQLite·vector·upload·identity와 embedding-model 출처를 함께 보존한다. CUDA image 이름만으로 GPU가 할당되지는 않으며 WebUI에는 GPU 예약이 없다. 로컬 entrypoint는 한 줄 OIDC secret과 검증된 CA bundle을 읽고 인자가 없으면 upstream `bash start.sh`로 시작한다.

`ENABLE_PASSWORD_AUTH=false`는 폼 숨김과 별도로 password 인증을 막는다. `ENABLE_OAUTH_PERSISTENT_CONFIG=false`는 OAuth 설정만 관장하며 모든 저장 설정을 끄지 않는다. 선언 버전의 `key/value`별 schema에 과거 단일 `id/data` 행 SQL 복구를 적용하지 않는다. Native login, signup/password 거부와 identity 연속성은 승인된 별도 검사로 확인하며 health가 대신하지 않는다.

### Pinned image and persisted settings

이미지는 [Compose](../../../infra/08-ai/open-webui/docker-compose.yml)의 CUDA tag에 registry index digest를 붙여 고정한다. 이미지만 이전 버전으로 되돌리기 전에 두 버전의 migration head를 비교한다. 같으면 데이터 복원 없이 되돌릴 수 있고, 다르면 백업 복원이 필요하다. 되돌릴 버전에 열려 있는 공개 advisory도 확인한다. 직전 digest와 비교 결과는 [SPEC-0226 Task](../../03.specs/0226-ai-runtime-pin-verification/tasks/tsk-0001-ai-runtime-pin-verification.md)에 있다.

CUDA 이미지를 쓰지만 GPU 예약이 없어 `torch.cuda.is_available()`은 `False`다. embedding은 원격 Ollama가 처리하고 로컬 GPU 기능은 쓰지 않는다. GPU는 Ollama와 ComfyUI가 이미 나누어 쓰므로 장치를 추가하지 않는다. `AIOHTTP_CLIENT_TIMEOUT`은 설정하지 않는다. 비워 두면 전체 요청 시간 제한이 없어서 느린 첫 load나 긴 streaming 답변이 WebUI 쪽에서 끊기지 않는다.

`ENABLE_PERSISTENT_CONFIG`가 기본값(켜짐)이면 DB `config` 행이 Compose 환경 변수보다 우선한다. migration이 남긴 빈 `webui.url` 행이 `WEBUI_URL`을 가리고 있어서 그 행만 지웠다. 재시작할 때 WebUI가 Compose 값으로 행을 다시 저장했다. 관리자가 직접 바꾼 설정은 건드리지 않는다. 세션 key는 `WEBUI_SECRET_KEY_FILE`로 data volume의 `.webui_secret_key`에 두고 restic state set으로 백업한다. 재생성 전에 실행 중인 key를 volume에 복사해야 사용자 세션이 유지된다.

### Common Checks

- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`
- Runtime approval 후 `ai` profile을 선택한 상태에서 `docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0057-open-webui.md)을 따른다.

### Traceability

- Declared parent: [Open WebUI Operations Policy](../policies/0057-open-webui.md) (`POL-0057`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Policy](../policies/0057-open-webui.md) (`POL-0057`), [Runbook](../runbooks/0057-open-webui.md) (`RUN-0057`)

## Related Documents

- [Open WebUI Compose](../../../infra/08-ai/open-webui/docker-compose.yml)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0057-open-webui.md)
- [Recovery runbook](../runbooks/0057-open-webui.md)
