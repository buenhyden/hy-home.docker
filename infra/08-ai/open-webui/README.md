---
title: "Open WebUI"
version: "1.1.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

# Open WebUI

## Overview

Open WebUI(이전 명칭 Ollama WebUI)는 로컬 LLM을 위한 ChatGPT와 유사한
인터페이스를 제공합니다. 채팅뿐 아니라 문서 검색에는 내장 로컬 벡터
스토어를, 임베딩 생성에는 Ollama를 사용하는 RAG(Retrieval-Augmented
Generation) 오케스트레이터 역할도 합니다.

## Audience

이 README의 주요 독자:

- End Users (채팅 인터페이스)
- AI Engineers (RAG 및 프롬프트 엔지니어링)
- Developers (서비스 통합)
- Operators (리소스 관리)
- AI Agents

## Scope

### In Scope

- `docker-compose.yml`: 인터페이스 및 RAG 백엔드 오케스트레이션.
- RAG 설정: 임베딩 모델. 벡터는 Open WebUI의 로컬 스토어에 유지됩니다(`VECTOR_DB` 미설정).
- Traefik 라우팅과 네이티브 OIDC 설정.

### Out of Scope

- 모델 가중치: [ollama](../ollama/README.md)에서 관리.
- 벡터 영속화: Open WebUI의 데이터 볼륨 내 로컬 스토어를 사용하며 Qdrant는 사용하지 않습니다.

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
| Purpose | `08-ai`의 Open WebUI 서비스 leaf; 서비스: `open-webui`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml`, `docker-entrypoint.sh` |
| Config values | env 키: `OLLAMA_BASE_URL`, `RAG_EMBEDDING_ENGINE`, `RAG_EMBEDDING_MODEL`; 프로필: `ai` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/open-webui/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | `ai_net`, `edge_net` |
| Volumes | `open-webui:/app/backend/data:rw`, `open-webui` |
| Ports | 선언되지 않음 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.open-webui.rule`, `traefik.http.routers.open-webui.entrypoints`, `traefik.http.routers.open-webui.tls`, `traefik.http.services.open-webui.loadbalancer.server.port`, `traefik.http.routers.open-webui.middlewares` |
| Secret refs | `openwebui_oidc_client_secret`; root:root 0600 호스트 파일 |
| Healthcheck | `open-webui`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0057-open-webui.md`), Policy (`docs/05.operations/policies/0057-open-webui.md`), Runbook (`docs/05.operations/runbooks/0057-open-webui.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `bash scripts/hardening/check-all-hardening.sh 08-ai`로 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. Open WebUI Interface & RAG Guide(`docs/05.operations/guides/0057-open-webui.md`)를 읽습니다.
2. SSO로 `https://chat.${DEFAULT_URL}`에서 UI에 접속합니다.
3. 문서 색인 전에 Ollama와의 연결을 확인합니다.

## Troubleshooting

- Open WebUI hardening 계약을 확인하려면 `bash scripts/hardening/check-all-hardening.sh 08-ai`로 시작합니다.
- 이 서비스 로컬 compose 파일을 독립 설정 검사로 실행하지 않습니다. 루트 네트워크 컨텍스트에 의존합니다.
- RAG, 인증, 모델 엔드포인트 설정을 변경하기 전에 Open WebUI 로그와 연결된 런북을 확인합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `ai`, `ai-llm`.
- Source authority: 이 패키지의 Compose와 선택된 이미지/빌드 입력. `infra/tech-stack.versions.json`은 파생 프로젝션입니다.
- Root preflight: `docker compose --profile ai config --quiet`. Root targeted start: `docker compose --profile ai up -d open-webui`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/guides/0057-open-webui.md`; ID: `GDE-0057`, `POL-0057`, `RUN-0057`.
- 해당 런북의 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다. 모델/콘텐츠 출처를 보존하고 실행 중인 파일시스템 복사본을 복구 근거로 사용하지 않습니다.

## Related Documents

- [Ollama Implementation](../ollama/README.md)
- [Qdrant Implementation](../../04-data/qdrant/README.md) (참고용; 08-ai에서는 연결되어 사용되지 않음)
- Open WebUI usage guide (`docs/05.operations/guides/0057-open-webui.md`)
- Open WebUI operations policy (`docs/05.operations/policies/0057-open-webui.md`)
- Open WebUI recovery runbook (`docs/05.operations/runbooks/0057-open-webui.md`)
- [Documentation index](../../../docs/README.md)

## Validation

- Open WebUI에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 08-ai`를 실행합니다.
- 현재 루트에서 활성화된 프로필 범위를 확인하려면 `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Configuration

### Native OIDC

Open WebUI는 전용 Keycloak 클라이언트 `home-openwebui`, S256 PKCE,
`/oauth/oidc/callback`을 사용합니다. 라우터는 `gateway-standard-chain@file`만
유지합니다. 신뢰 헤더 인증, OAuth 가입, 이메일 병합, 역할/그룹 관리, 비밀번호
인증은 비활성화되어 있습니다. 기존 관리자는 검증된 OIDC 연동 이후에도 동일한
로컬 ID와 역할을 유지합니다. 공개/로컬 CA 루트가 결합되어 있으며 TLS 검증이
활성화되어 있습니다.

`ENABLE_LOGIN_FORM=false`는 폼을 숨기고 `ENABLE_PASSWORD_AUTH=false`는
별도로 비밀번호 API를 거부합니다. 영속화된 UI 설정도 함께 확인해야 합니다.
시크릿 소유권, 원-키 설정 업데이트, 복구는 런북
(`docs/05.operations/runbooks/0057-open-webui.md`)을 참고합니다.

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `OLLAMA_BASE_URL` | Yes | Ollama API 엔드포인트. |
| `RAG_EMBEDDING_MODEL` | Yes | 문서 색인에 사용하는 모델. 현재 값은 Compose가 소유합니다. |

## Change Impact

- `docker-compose.yml` 변경은 SSO 인증 흐름에 영향을 줄 수 있습니다.
- `RAG_EMBEDDING_MODEL`을 업데이트하면 기존 문서를 다시 색인해야 합니다.

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
