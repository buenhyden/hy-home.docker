# Ollama Inference Engine

> Local LLM inference server with NVIDIA GPU acceleration.

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

## How to Work in This Area

1. 상위 시스템 가이드인 [Ollama System Guide](../../../docs/07.guides/08-ai/ollama.md)를 먼저 읽는다.
2. 리소스 예약 및 모델 거버넌스는 [Ollama Operations Policy](../../../docs/08.operations/08-ai/ollama.md)를 따른다.
3. 장애 발생 시 [Ollama Runbook](../../../docs/09.runbooks/08-ai/ollama.md)에 따라 복구를 수행한다.

## Related References

- **Guide**: [docs/07.guides/08-ai/ollama.md](../../../docs/07.guides/08-ai/ollama.md)
- **Operation**: [docs/08.operations/08-ai/ollama.md](../../../docs/08.operations/08-ai/ollama.md)
- **Runbook**: [docs/09.runbooks/08-ai/ollama.md](../../../docs/09.runbooks/08-ai/ollama.md)

---

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Ollama 서비스 실행 |
| `docker compose ps` | 컨테이너 상태 확인 |
| `docker compose logs -f` | 런타임 로그 확인 |
| `docker compose down` | 서비스 중지 |

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DEFAULT_AI_MODEL_DIR` | Yes | - | 모델 영구 저장 경로 |
| `OLLAMA_PORT` | No | 11434 | API 포트 |
| `OLLAMA_EXPORTER_PORT` | No | 11435 | 지표 수집 포트 |

## Testing

```bash
# 기본 헬스체크
curl http://localhost:11434/api/tags

# 추론 API 테스트
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"
}'
```

## AI Agent Guidance

1. 모델 데이터는 `/root/.ollama` (호스트의 `${DEFAULT_AI_MODEL_DIR}/ollama`)에 저장된다. 볼륨 삭제 시 모든 모델을 다시 다운로드해야 하므로 주의한다.
2. `ollama-exporter`를 통해 토큰 발생 속도 및 VRAM 가용량을 지속적으로 모니터링한다.
3. 새로운 모델을 추가하기 전 [Ollama Operations Policy](../../../docs/08.operations/08-ai/ollama.md)의 도입 기준을 확인한다.
