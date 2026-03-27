<!-- Target: docs/07.guides/08-ai/ollama.md -->

# Ollama Inference Engine Guide

> 로컬 LLM 추론 엔진(Ollama) 운영 및 연동 가이드.

---

## Overview (KR)

이 문서는 `hy-home.docker` AI 계층의 핵심 추론 엔진인 Ollama 사용 방법을 설명한다. 모델 라이프사이클(풀/조회/호출), GPU 가속 확인, Open WebUI 연동, exporter 관측 흐름을 표준 절차로 제공한다.

## Guide Type

`system-guide`

## Target Audience

- AI Engineer
- Developer
- Operator
- Agent-tuner

## Purpose

- Ollama 모델 운용 절차를 표준화한다.
- API/CLI/관측(Exporter) 경로를 일관된 방식으로 점검한다.
- Open WebUI/RAG 연동 전에 필요한 추론 계층 준비 상태를 확보한다.

## Prerequisites

- NVIDIA GPU 및 NVIDIA Container Toolkit이 정상 설치되어야 한다.
- `ollama` 컨테이너가 기동 가능해야 한다.
- 모델 영속 저장 경로 `${DEFAULT_AI_MODEL_DIR}/ollama`가 준비되어야 한다.
- 기본 포트/엔드포인트:
  - API: `${OLLAMA_PORT:-11434}`
  - Exporter: `${OLLAMA_EXPORTER_PORT:-11435}`

## Step-by-step Instructions

### 1. Service & GPU Health Check

```bash
# 호스트 GPU 상태
nvidia-smi

# Ollama health endpoint
curl -f http://localhost:${OLLAMA_PORT:-11434}/api/tags

# 컨테이너 내부 GPU 인식 확인
docker exec ollama nvidia-smi
```

### 2. Model Lifecycle (CLI)

```bash
# 모델 다운로드
docker exec ollama ollama pull llama3

# 모델 목록 확인
docker exec ollama ollama list
```

### 3. Inference API Check

```bash
curl http://localhost:${OLLAMA_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello from hy-home"
}'
```

### 4. Open WebUI Integration Check

1. Open WebUI 환경변수 `OLLAMA_BASE_URL`가 `http://ollama:${OLLAMA_PORT:-11434}`를 가리키는지 확인.
2. Open WebUI UI에서 모델 목록이 정상 조회되는지 확인.
3. 모델 미노출 시 `ollama` health/log를 먼저 확인.

### 5. Exporter Observability Check

```bash
# exporter metrics endpoint
curl -f http://localhost:${OLLAMA_EXPORTER_PORT:-11435}/metrics
```

- 주요 관측 대상: 모델 로드 수, 메모리 사용량, scrape 상태.

## Common Pitfalls

- **GPU 미인식**: 컨테이너는 실행되지만 CPU 추론으로 강등됨.
- **VRAM OOM**: 대형 모델 동시 로드 시 응답 실패/지연.
- **모델 태그 불일치**: Open WebUI 설정 모델명과 Ollama 실제 태그 불일치.
- **Exporter 미수집**: 관측 포트 설정 불일치로 지표 공백 발생.

## Related Documents

- **PRD (AI 공통)**: `[../../01.prd/2026-03-26-08-ai.md]`
- **ARD (AI 공통)**: `[../../02.ard/0008-ai-architecture.md]`
- **ADR (AI 공통)**: `[../../03.adr/0008-ollama-openwebui-local-ai.md]`
- **Spec (AI 공통)**: `[../../04.specs/08-ai/spec.md]`
- **Plan (AI 공통)**: `[../../05.plans/2026-03-26-08-ai-standardization.md]`
- **Task (AI 공통)**: `[../../06.tasks/2026-03-26-08-ai-tasks.md]`
- **Operation**: `[../../08.operations/08-ai/ollama.md]`
- **Runbook**: `[../../09.runbooks/08-ai/ollama.md]`
- **Infrastructure**: `[../../../infra/08-ai/ollama/README.md]`
