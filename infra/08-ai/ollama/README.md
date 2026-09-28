---
title: "Ollama Inference Engine"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# Ollama Inference Engine

## Overview

이 경로는 `hy-home.docker` 플랫폼의 핵심 추론 엔진인 Ollama 구성을 담당한다. NVIDIA GPU 가속으로 Llama 3, Mistral 등의 오픈소스 LLM을 로컬에서 효율적으로 구동하며 지표 수집을 위한 Exporter를 포함한다.

## Audience

이 README의 주요 독자:

- **AI Engineers**: 모델 라이프사이클 관리 및 성능 튜닝
- **DevOps Engineers**: 인프라 프로비저닝 및 리소스 통제
- **AI Agents**: 자동화된 추론 환경 이해 및 지표 분석

## Scope

### In Scope

- `docker-compose.yml`: Ollama 및 Ollama-Exporter 컨테이너 오케스트레이션
- GPU 가속 설정 (NVIDIA CUDA)
- 로컬 모델 영구 저장소 구성

### Out of Scope

- LLM 애플리케이션 로직 (Open WebUI 등 상위 서비스)
- 모델 학습 및 미세 조정 (Fine-tuning)
- 벡터 데이터베이스 구성 (`04-data` 계층 담당)

## Structure

```text
ollama/
├── docker-compose.yml  # Ollama & Exporter 컨테이너 설정
└── README.md           # 이 파일 (인프라 진입점)
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `08-ai`의 Ollama Inference Engine 서비스 leaf; 서비스: `ollama`, `ollama-exporter`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/ollama/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml` |
| Config values | env 키: `OLLAMA_HOST`, `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE`; 프로필: `ai`, `dev` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/ollama/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | `ai_net`, `edge_net`, `obs_net` |
| Volumes | `ollama-data:/root/.ollama:rw`, `ollama-data` |
| Ports | Ollama API용 `${OLLAMA_HOST_PORT}:${OLLAMA_PORT}`; exporter는 `ai_net` 내부에서 `${OLLAMA_EXPORTER_PORT:-8000}`을 노출 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.ollama.rule`, `traefik.http.routers.ollama.entrypoints`, `traefik.http.routers.ollama.tls`, `traefik.http.services.ollama.loadbalancer.server.port`, `traefik.http.routers.ollama.middlewares` |
| Secret refs | 선언되지 않음 |
| Healthcheck | `ollama`, `ollama-exporter`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0056-ollama.md`), Policy (`docs/05.operations/policies/0056-ollama.md`), Runbook (`docs/05.operations/runbooks/0056-ollama.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `bash scripts/hardening/check-all-hardening.sh 08-ai`로 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 사용 가이드인 Ollama usage guide (`docs/05.operations/guides/0056-ollama.md`)를 먼저 읽는다.
2. 리소스 예약 및 모델 거버넌스는 Ollama operations policy (`docs/05.operations/policies/0056-ollama.md`)를 따른다.
3. 장애 발생 시 Ollama recovery runbook (`docs/05.operations/runbooks/0056-ollama.md`)에 따라 복구한다.

## Validation

- Ollama에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 08-ai`를 실행합니다.
- 현재 루트에서 활성화된 프로필 범위를 확인하려면 `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- AI compose 계약을 확인하려면 `bash scripts/hardening/check-all-hardening.sh 08-ai`로 시작합니다.
- 이 서비스 로컬 compose 파일을 독립 설정 검사로 실행하지 않습니다. 루트 네트워크 컨텍스트에 의존합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- 모델 로딩 오류: `ollama list`로 모델 이름을 확인하고 모델 저장에 충분한 디스크 공간이 있는지 확인합니다.
- API 오류: `docker logs --tail=200 ollama`를 확인하고 API 포트 바인딩이 클라이언트 설정과 일치하는지 확인합니다.
- GPU 오류: NVIDIA container toolkit이 설치되어 있고 컨테이너 내부에서 GPU에 접근 가능한지 확인합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `ai`, `ai-llm`, `ollama`.
- Source authority: 이 패키지의 Compose와 선택된 이미지/빌드 입력. `infra/tech-stack.versions.json`은 파생 프로젝션입니다.
- Root preflight: `docker compose --profile ai config --quiet`. Root targeted start: `docker compose --profile ai up -d ollama ollama-exporter`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/guides/0056-ollama.md`; ID: `GDE-0056`, `POL-0056`, `RUN-0056`.
- 해당 런북의 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다. 모델/콘텐츠 출처를 보존하고 실행 중인 파일시스템 복사본을 복구 근거로 사용하지 않습니다.

## Related Documents

- **Guide**: Ollama usage guide (`docs/05.operations/guides/0056-ollama.md`)
- **Policy**: Ollama operations policy (`docs/05.operations/policies/0056-ollama.md`)
- **Runbook**: Ollama recovery runbook (`docs/05.operations/runbooks/0056-ollama.md`)
- [Documentation index](../../../docs/README.md)

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DEFAULT_AI_MODEL_DIR` | Yes | - | 모델 영구 저장 경로 |
| `OLLAMA_PORT` | No | 11434 | API 포트 |
| `OLLAMA_EXPORTER_PORT` | No | `.env.example`에서 8000 | exporter 지표 수집 포트; 설정하지 않으면 compose의 기본값은 `8000`입니다 |

## Testing

```bash
# 기본 헬스체크
curl "http://localhost:${OLLAMA_HOST_PORT:-11434}/api/tags"

# 추론 API 테스트
curl "http://localhost:${OLLAMA_HOST_PORT:-11434}/api/generate" -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
