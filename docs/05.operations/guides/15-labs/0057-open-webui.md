---
title: "Open WebUI Usage Guide"
version: "1.2.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "operations"
artifact_id: "GDE-0057"
parent_ids:
- "POL-0057"
implementation_services:
  labs/open-webui/docker-compose.yml:
  - open-webui
created: "2026-05-10"
---

# Open WebUI Usage Guide

## Overview

Open WebUI는 root Compose에서 분리된 독립 LAB `labs/open-webui/docker-compose.yml`의 채팅·RAG 웹
애플리케이션이며 LAB profile `lab-open-webui`로 선택된다(ADR-0062, 2026-11-10 owner 개정). HOME의 로컬
LLM 채팅은 Hermes(Telegram·SSO dashboard)와 n8n Assistant/Agents가, 웹 검색은 n8n Assistant의
SearXNG가, RAG는 Qdrant와 n8n이 맡는다. 이 LAB은 Open WebUI 자체를 다시 써 보려는 실험에만 쓴다.

## Scope

### Audience and Goal

Open WebUI LAB을 준비하거나 실험하는 AI engineer와 운영자를 위한 문서다. LAB 경계, 필수 입력,
명령의 부작용과 정상 점검 방법을 찾는 것이 목표다.

## Concepts

### Current implementation

- **LAB boundary.** `hy-home-lab-open-webui` project의 `lab_open_webui_net` 하나만 사용하고 HOME
  network에 합류하지 않는다. 서비스는 `hy-home.tier: lab`, `traefik.enable: 'false'` label을 가지며
  gateway route가 없다. UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_OPEN_WEBUI_HOST_PORT:-18095}`에만
  게시된다.
- **필수 입력.** [`labs/.env.example`](../../../../labs/.env.example)의 `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`
  (Ollama endpoint), `LAB_OPEN_WEBUI_DEFAULT_URL`(Keycloak을 gateway 이름 `keycloak.<domain>`으로 찾는
  domain), `LAB_OPEN_WEBUI_CA_FILE`(루트 CA 파일)이다. HOME은 Ollama를 LAB network에 게시하지 않으므로
  소유자가 도달 가능한 endpoint를 승인하기 전까지 이 LAB은 렌더링 전용이다.
- **Data.** `${LAB_DATA_DIR}/open-webui/data`가 `/app/backend/data`에 bind된다. SQLite `webui.db`,
  upload, 내장 로컬 vector store(`VECTOR_DB` 미설정)와 `WEBUI_SECRET_KEY_FILE`이 가리키는 session key
  `.webui_secret_key`가 모두 여기 있다. HOME Qdrant는 LAB에서 도달할 수 없으므로 쓰지 않는다. HOME
  Restic은 LAB data를 백업하지 않는다.
- **Login.** native Keycloak OIDC(client `home-openwebui`, PKCE S256)만 쓴다. password login, signup,
  email merge, OAuth role/group 관리와 trusted-header 인증은 비활성이다. 등록된 redirect URI는 이전
  gateway host `https://chat.${DEFAULT_URL}/oauth/oidc/callback`이므로, LAB loopback origin에서
  로그인하려면 소유자가 승인한 redirect 등록과 HTTPS origin이 따로 필요하다(`WEBUI_AUTH_COOKIE_SECURE=true`).
  그 전까지 LAB 로그인 성공을 주장하지 않는다.
- **Secret.** OIDC client secret은 LAB 전용 `lab_open_webui_oidc_client_secret`
  (`${LAB_SECRET_DIR:-../../secrets/labs}/open-webui/oidc_client_secret.txt`, catalog `LAB-037`)이며 원래
  target `/run/secrets/openwebui_oidc_client_secret`에 mount된다. [entrypoint](../../../../labs/open-webui/docker-entrypoint.sh)가
  한 줄 secret과 공개·로컬 CA bundle을 검증한 뒤 process 안에서만 export한다. HOME OpenBao Agent는
  `08-ai/open-webui` 출력을 계속 render하지만 LAB은 이를 bind하지 않는다. LAB 사본 준비는 별도 승인이다.
- **Image·GPU.** [Compose](../../../../labs/open-webui/docker-compose.yml)가 CUDA tag와 digest를 고정한다.
  `labs/**`는 Renovate와 SEC01 ledger 밖이다. 번들 PyTorch cu128 build에는 sm_61 kernel이 없어 HOME GTX
  1060을 쓸 수 없고 GPU 예약도 없다. embedding은 Ollama가 처리한다. `ENABLE_OPENAI_API=false`를 유지하고 Docker socket과 terminal server는
  연결하지 않는다(SPEC-0226, 은퇴).

## Usage

### Commands and side effects

표의 `LAB`은 `docker compose --env-file labs/.env -f labs/open-webui/docker-compose.yml --profile lab-open-webui`다.
`LAB config` 렌더링만 승인 없이 안전하며, 그 외 명령은 `python3 scripts/operations/lab.py check|up|down open-webui`의
목적·lease·충돌·예산 규칙을 따르는 활성 lease 안에서, 승인된 Ollama endpoint와 LAB secret이 있을 때만 쓴다.

| Command | Effect |
| --- | --- |
| `LAB config --quiet` | 렌더링만; 필수 입력이 비어 있으면 거부 |
| `LAB up -d open-webui` | LAB data root에 schema를 만들거나 migration하고 웹 서버 시작 |
| `LAB exec open-webui curl -f http://localhost:8080/health` | container 내부 health만 확인; 로그인·RAG 증거 아님 |

### Persisted settings

`ENABLE_PERSISTENT_CONFIG`가 기본값(켜짐)이면 `webui.db`의 `config` 행이 Compose 환경 변수보다 우선한다.
`rag.embedding_model`과 `openai.enable` 행은 Compose 값과 함께 바꾸고, 행을 바꾸기 전에 data root를
백업한다. embedding 모델은 Ollama에 있는 `embeddinggemma-2:740m`(768차원)이며 바꾸면 재색인한다.
`AIOHTTP_CLIENT_TIMEOUT`은 설정하지 않는다.

### HOME data left in place

HOME 컨테이너 `open-webui`와 volume `hy-home-infra_open-webui`(`${DEFAULT_AI_MODEL_DIR}/open-webui`)는 이
source 이동으로 바뀌지 않는다. 정지·제거, LAB data root로의 data 이전 또는 삭제, Keycloak client와 DNS
정리는 각각 별도 승인 단계이며 순서는 [runbook](../../runbooks/15-labs/0057-open-webui.md#home-retirement-steps)이 소유한다.

### Common Checks

- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `python3 scripts/operations/lab.py check open-webui`

### Runbook Handoff

LAB 기동, 로그인 실패, data 복구와 HOME 퇴역 절차는 [runbook](../../runbooks/15-labs/0057-open-webui.md)을 따른다.

### Traceability

- Declared parent: [Open WebUI Operations Policy](../../policies/15-labs/0057-open-webui.md) (`POL-0057`)
- Governing authority: [ADR-0062](../../../02.architecture/decisions/0062-home-lab-membership.md),
  [LAB promotion policy](../../policies/15-labs/0107-lab-promotion.md) (`POL-0107`)
- Subject peers: [Policy](../../policies/15-labs/0057-open-webui.md) (`POL-0057`), [Runbook](../../runbooks/15-labs/0057-open-webui.md) (`RUN-0057`)

## Troubleshooting

- **렌더링 거부**: 필수 `LAB_OPEN_WEBUI_*` 입력이 비어 있다.
- **Ollama 연결 실패**: `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`이 LAB network에서 도달 불가하다.
- **로그인 실패**: LAB origin redirect가 Keycloak에 등록되지 않았거나 HTTPS origin이 없다.
- **임베딩 모델 누락**: `RAG_EMBEDDING_MODEL`이 Ollama에 없다.

## Related Documents

- [Open WebUI LAB Compose](../../../../labs/open-webui/docker-compose.yml)
- [Open WebUI LAB README](../../../../labs/open-webui/README.md)
- [Operations index](../../README.md)
- [Operations policy](../../policies/15-labs/0057-open-webui.md)
- [Recovery runbook](../../runbooks/15-labs/0057-open-webui.md)
