# Ollama System Guide

> LLM Inference Engine & Model Management

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 핵심 추론 엔진인 Ollama에 대한 가이드다. NVIDIA GPU 가속을 활용한 모델 실행, 모델 라이프사이클 관리, 그리고 타 서비스와의 연동 방법을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- AI Engineer
- Developer
- Operator
- AI Agent

## Purpose

Ollama를 통해 로컬 환경에서 오픈소스 LLM을 효율적으로 구동하고, 플랫폼 내 인텔리전스 계층을 구축하는 방법을 이해한다.

## Prerequisites

- NVIDIA GPU (Pascal 아키텍처 이상 권장)
- NVIDIA Container Toolkit 설치 및 Docker 연동
- 충분한 시스템 메모리 및 VRAM (7B 모델 기준 최소 8GB VRAM 권장)

## Step-by-step Instructions

### 1. 서비스 상태 확인

Ollama 컨테이너가 정상적으로 GPU를 인식하고 있는지 확인한다.

```bash
docker exec -it ollama nvidia-smi
```

### 2. 모델 관리 (CLI)

Ollama 내부 CLI를 사용하여 모델을 다운로드하거나 확인한다.

```bash
# 모델 다운로드
docker exec -it ollama ollama pull llama3

# 모델 리스트 확인
docker exec -it ollama ollama list
```

### 3. API 사용 (Inference)

플랫폼 내부에서 `http://ollama:11434/api` 엔드포인트를 통해 추론을 수행한다.

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello!"
}'
```

### 4. 리소스 모니터링

`ollama-exporter`에서 제공하는 프로메테우스 포맷의 지표를 확인한다.

- Endpoint: `http://ollama-exporter:11435/metrics`
- 주요 지표: `ollama_vram_usage_bytes`, `ollama_tokens_per_second`

## Common Pitfalls

- **VRAM OOM**: 너무 큰 모델(70B+)을 로드할 경우 GPU 메모리 부족으로 서비스가 중단될 수 있다. [Operations Policy](../../08.operations/08-ai/ollama.md)에 따라 적절한 양자화 모델을 선택해야 한다.
- **SSO Authentication**: 외부에서 호출할 경우 Traefik의 SSO 미들웨어를 거치게 되므로, 내부 서비스 간 통신 시에는 `infra_net` 내부 도메인(`ollama:11434`)을 사용한다.

## Related Documents

- **Spec**: `[../04.specs/08-ai/ollama-spec.md]` (TBD)
- **Operation**: `[../08.operations/08-ai/ollama.md]`
- **Runbook**: `[../09.runbooks/08-ai/ollama.md]`
- **Infrastructure**: [infra/08-ai/ollama/](../../../infra/08-ai/ollama/README.md)
