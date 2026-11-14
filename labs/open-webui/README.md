---
title: "Open WebUI"
version: "1.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# Open WebUI

> Keycloak native OIDC를 사용하는 on-demand 로컬 LLM 채팅·RAG 웹 애플리케이션 LAB입니다.

## Purpose

### Service Role

Open WebUI는 독립 Compose project인 [Open WebUI LAB](docker-compose.yml)(`lab-open-webui` profile)입니다.
2026-11-10 owner 결정(ADR-0062 개정)으로 HOME `08-ai`에서 옮겼습니다. root Compose에 포함되지 않고
HOME network에 연결되지 않으며 Traefik route도 없습니다. UI는
`${LAB_HOST_BIND_IP}:${LAB_OPEN_WEBUI_HOST_PORT:-18095}`에만 게시됩니다.

HOME에서는 로컬 LLM 채팅을 Hermes와 n8n Assistant/Agents가, 웹 검색을 n8n Assistant의 SearXNG가,
RAG를 Qdrant와 n8n이 맡습니다. Ollama endpoint(`LAB_OPEN_WEBUI_OLLAMA_BASE_URL`)는 HOME이 LAB network에
게시하지 않으므로 owner 승인 전까지 이 LAB은 render 검증만 합니다.

#### Audience

이 README의 주요 독자:

- AI Engineers (LAB 실험)
- Operators (LAB lease와 HOME 퇴역)

#### In Scope

- 웹 서버 하나와 그 LAB data root(SQLite·upload·내장 로컬 vector store·session key).
- Keycloak native OIDC 로그인(client `home-openwebui`, PKCE S256)과 CA bundle을 만드는 entrypoint.

#### Out of Scope

- 모델 가중치와 Ollama 운영: HOME [ollama](../../infra/08-ai/ollama/README.md).
- HOME Qdrant(LAB에서 도달할 수 없으므로 `VECTOR_DB`를 설정하지 않음).
- HOME에 남은 컨테이너·volume의 정지·이전·삭제(별도 승인 단계).

#### Structure

```text
labs/open-webui/
├── docker-compose.yml   # 독립 LAB entrypoint
├── docker-entrypoint.sh # client secret과 결합 CA 로딩
├── promotion.yaml       # SPEC-0263 승격 manifest
└── README.md            # 이 파일
```

### Supported Environment

이미지는 [Compose](docker-compose.yml)가 digest로 고정한 Open WebUI 이미지이며 `lab-open-webui` profile의 독립 Compose project로 실행한다.

## Interfaces

### Inputs and Outputs

| 항목 | 값 |
| --- | --- |
| Profile·project | `lab-open-webui`, `hy-home-lab-open-webui` |
| Network | `lab_open_webui_net`만 사용 |
| Data | `${LAB_DATA_DIR}/open-webui/data` → `/app/backend/data` |
| 필수 입력 | `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`, `LAB_OPEN_WEBUI_DEFAULT_URL`, `LAB_OPEN_WEBUI_CA_FILE` ([.env.example](../.env.example)) |
| Secret | `lab_open_webui_oidc_client_secret` → `${LAB_SECRET_DIR}/open-webui/oidc_client_secret.txt` (`LAB-037`), target `openwebui_oidc_client_secret` |
| Image | CUDA tag와 digest 고정; `labs/**`는 Renovate와 SEC01 ledger 밖 |
| GPU | 예약 없음. 번들 PyTorch cu128 build에 sm_61 kernel이 없어 GTX 1060을 쓸 수 없음 |

password login, signup, email merge, OAuth role/group 관리와 trusted-header 인증은 꺼져 있습니다.
`ENABLE_OPENAI_API=false`입니다. `webui.db`의 `config` 행은 Compose 값보다 우선하므로 embedding 모델이나
OpenAI 설정을 바꿀 때 저장된 행도 함께 바꿉니다. 등록된 redirect URI는 이전 gateway host 기준이므로 LAB
origin 로그인에는 owner가 승인한 redirect 등록과 HTTPS origin이 필요합니다.

### Security Boundary

UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_OPEN_WEBUI_HOST_PORT:-18095}` -> 8080에만 게시하며 gateway route가 없고 HOME network에 연결되지 않는다. OIDC client secret은 `lab_open_webui_oidc_client_secret` 참조로만 전달한다.

## Development

### Local Workflow

1. Usage guide(`docs/05.operations/guides/15-labs/0057-open-webui.md`)와 LAB 승격 정책을 읽습니다.
2. `python3 scripts/operations/lab.py check open-webui`로 render와 충돌을 검사합니다.
3. 실제 기동은 승인된 Ollama endpoint, LAB secret 사본과 lease가 있을 때만 `lab.py up`으로 합니다.

### Checks

`python3 scripts/operations/lab.py check open-webui`로 render와 충돌을 검사하고 `bash scripts/hardening/check-all-hardening.sh 08-ai`로 native OIDC·no-route·bind 계약을 확인한다. 통과는 실제 기동의 증거가 아니다.

## Operations

### Runbook Links

- [LAB 목록](../README.md)
- Usage guide(`docs/05.operations/guides/15-labs/0057-open-webui.md`) (`GDE-0057`)
- Operations policy(`docs/05.operations/policies/15-labs/0057-open-webui.md`) (`POL-0057`)
- Runbook(`docs/05.operations/runbooks/15-labs/0057-open-webui.md`) (`RUN-0057`)
- ADR-0062(`docs/02.architecture/decisions/0062-home-lab-membership.md`)
- [문서 인덱스](../../docs/README.md)
- [15-labs runbooks](../../docs/05.operations/runbooks/15-labs/README.md): RUN-0107 lab-promotion

### Observability and Recovery

- `bash scripts/hardening/check-all-hardening.sh 08-ai`가 이 LAB의 native OIDC·no-route·bind 계약을 검사합니다.
- 필수 입력이 비면 render가 거부됩니다.
- 장애 대응과 HOME 퇴역 순서는 runbook(`docs/05.operations/runbooks/15-labs/0057-open-webui.md`)을 따릅니다.
