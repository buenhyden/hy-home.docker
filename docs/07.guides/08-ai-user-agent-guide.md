<!-- Target: docs/07.guides/08-ai-user-agent-guide.md -->

# 08-ai User & Agent Guide

## Overview (KR)

이 가이드는 사용자와 AI 에이전트가 `08-ai` 계층(Ollama, Open WebUI)을 효과적으로 활용하기 위한 지침을 제공한다. 로컬 LLM 인터페이스 접속 방법, RAG 활용법, 그리고 에이전트의 API 통합 가이드를 포함한다.

## For Users

### 1. Accessing the Interface

- **URL**: `https://chat.DOMAIN` (내부망 접속 시)
- **Authentication**: Keycloak SSO를 통해 로그인한다.
- **Initial Setup**: 로그인 후 프로필 설정에서 선호하는 테마와 언어를 선택할 수 있다.

### 2. Using Chat & Models

- 상단 모델 선택 브라우저에서 사용할 모델(예: `llama3.1`, `qwen2.5-coder`)을 선택한다.
- 텍스트 뿐만 아니라 지원되는 경우 이미지(Multi-modal) 업로드도 가능하다.

### 3. Knowledge Base (RAG)

- **Documents**: 왼쪽 사이드바의 'Workspace' -> 'Documents'에서 자신의 문서를 업로드할 수 있다.
- **Usage**: 채팅창에 `#`을 입력하여 특정 문서나 컬렉션을 참조하여 답변을 생성하도록 요청할 수 있다.

## For AI Agents

### 1. API Endpoint
- **Base URL**: `http://open-webui:8080/api` (Internal) 또는 `http://ollama:11434/api` (Inference only)
- **Format**: OpenAI API 규격을 준수한다.

### 1. GPU Allocation

- Ollama 컨테이너는 단일 GPU 전용 예약을 유지한다. (`deploy.resources.reservations.devices`)
- 다른 컨테이너가 GPU를 점유하여 추론 성능이 저하되지 않도록 모니터링한다.

### 2. VRAM Cleanup

- 오랫동안 사용되지 않는 모델은 Ollama 메모리에서 자동으로 언로드되도록 설정(`OLLAMA_KEEP_ALIVE=5m`)되어 있다.
- 필요 시 `curl http://ollama:11434/api/generate -d '{"model": "name", "keep_alive": 0}'` 명령으로 강제 언로드할 수 있다.

### 2. Standard Models
- **General Reasoning**: `llama3.1:8b`
- **Coding Tasks**: `qwen2.5-coder:7b`
- **Embedding**: `qwen3-embedding:0.6b`

### 3. Guidelines
- 에이전트는 대량의 문서를 처리할 때 시스템 부하를 고려하여 배치 처리를 지양한다.
- 모델 리로딩 시간을 줄이기 위해 가급적 표준 모델을 우선 사용한다.

## Related Documents

- **PRD**: [../../01.prd/2026-03-26-08-ai.md](../../01.prd/2026-03-26-08-ai.md)
- **Spec**: [../../04.specs/08-ai/spec.md](../../04.specs/08-ai/spec.md)
