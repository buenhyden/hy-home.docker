# Ollama Inference Engine

## Overview

이 경로는 `hy-home.docker` 플랫폼의 핵심 추론 엔진인 Ollama 구성을 담당한다. NVIDIA GPU 가속을 통해 Llama 3, Mistral 등의 오픈소스 LLM을 로컬에서 효율적으로 구동하며, 지표 수집을 위한 Exporter를 포함한다.

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
| Purpose | Ollama Inference Engine service leaf in `08-ai`; services: `ollama`, `ollama-exporter`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/ollama/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `OLLAMA_HOST`, `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE`; profiles: `ai`, `dev` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/08-ai/ollama/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `ollama-data:/root/.ollama:rw`, `ollama-data` |
| Ports | `${OLLAMA_HOST_PORT}:${OLLAMA_PORT}` for Ollama API; exporter exposes `${OLLAMA_EXPORTER_PORT:-8000}` inside `infra_net` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.ollama.rule`, `traefik.http.routers.ollama.entrypoints`, `traefik.http.routers.ollama.tls`, `traefik.http.services.ollama.loadbalancer.server.port`, `traefik.http.routers.ollama.middlewares` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `ollama`, `ollama-exporter` |
| Operations | [Guide](../../../docs/05.operations/guides/08-ai/ollama.md), [Policy](../../../docs/05.operations/policies/08-ai/ollama.md), [Runbook](../../../docs/05.operations/runbooks/08-ai/ollama.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `bash scripts/hardening/check-all-hardening.sh 08-ai`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 상위 사용 가이드인 [Ollama usage guide](../../../docs/05.operations/guides/08-ai/ollama.md)를 먼저 읽는다.
2. 리소스 예약 및 모델 거버넌스는 [Ollama operations policy](../../../docs/05.operations/policies/08-ai/ollama.md)를 따른다.
3. 장애 발생 시 [Ollama recovery runbook](../../../docs/05.operations/runbooks/08-ai/ollama.md)에 따라 복구를 수행한다.

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 08-ai` after README or Compose reference changes that affect Ollama.
- Run `HYHOME_COMPOSE_PROFILES="core ai" bash scripts/validation/validate-docker-compose.sh` for the current root-active profile surface.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with `bash scripts/hardening/check-all-hardening.sh 08-ai` to confirm AI compose contracts.
- Do not run this service-local compose file as a standalone config check; it depends on root `infra_net` context.
- Check container logs and the linked runbook before changing configuration or secret references.
- For model loading errors: verify the model name with `ollama list` and confirm sufficient disk space for model storage.
- For API errors: check `docker logs --tail=200 ollama` and confirm the API port binding matches client configuration.
- For GPU errors: verify the NVIDIA container toolkit is installed and the GPU is accessible inside the container.

## Related Documents

- **Guide**: [Ollama usage guide](../../../docs/05.operations/guides/08-ai/ollama.md)
- **Policy**: [Ollama operations policy](../../../docs/05.operations/policies/08-ai/ollama.md)
- **Runbook**: [Ollama recovery runbook](../../../docs/05.operations/runbooks/08-ai/ollama.md)

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DEFAULT_AI_MODEL_DIR` | Yes | - | 모델 영구 저장 경로 |
| `OLLAMA_PORT` | No | 11434 | API 포트 |
| `OLLAMA_EXPORTER_PORT` | No | 11435 in `.env.example` | exporter 지표 수집 포트; compose fallback is `8000` when unset |

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
