<!-- Target: docs/07.guides/08-ai/open-webui.md -->

# Open WebUI Interface & RAG Guide

> Full-featured web interface for LLM interaction and RAG orchestration.

---

## Overview (KR)

이 문서는 Open WebUI에 대한 시스템 가이드다. 사용자 인터페이스 활용 방법, 로컬 LLM(Ollama) 연동, 그리고 Qdrant를 이용한 RAG(Retrieval-Augmented Generation) 워크플로우를 이해하고 설정하는 방법을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- End Users
- AI Engineers
- Operators
- Agent-tuner

## Purpose

Open WebUI의 주요 기능을 파악하고, 로컬 환경에서 ChatGPT와 유사한 사용자 경험을 구축하며, 문서 기반 답변(RAG) 기능을 활성화하는 것을 목표로 한다.

## Prerequisites

- **Ollama**: `08-ai/ollama` 서비스 정상 작동 (Embedding 모델 포함).
- **Qdrant**: `04-data/qdrant` 서비스 정상 작동 (Vector DB).
- **SSO**: Keycloak을 통한 사용자 인증 권한.

## Step-by-step Instructions

### 1. Access & Authentication

1. `https://chat.${DEFAULT_URL}`에 접속한다.
2. SSO(Keycloak)를 통해 로그인한다. 첫 로그인 시 관리자 권한 부여가 필요할 수 있다.

### 2. Model Selection & Chat

1. 상단 모델 선택 메뉴에서 사용할 LLM을 선택한다 (Ollama에서 서빙 중인 모델).
2. 채팅창에 메시지를 입력하여 대화를 시작한다.

### 3. RAG (Dokument Indexing)

1. 채팅창 왼쪽의 `+` 버튼 또는 설정 메뉴에서 문서를 업로드한다.
2. 업로드된 문서는 `qwen3-embedding` 모델을 통해 벡터화되어 Qdrant에 저장된다.
3. 질문 시 `#` 기호를 사용하여 특정 문서를 참조하거나, 전체 문서를 대상으로 RAG를 수행한다.

### 4. Advanced Settings
1. **System Prompt**: 각 모델별로 커스텀 시스템 프롬프트를 설정할 수 있다.
2. **Parameters**: Temperature, Top-K 등 추론 파라미터를 조정한다.

## Common Pitfalls

- **Connection Error**: Ollama 또는 Qdrant 컨테이너가 중지된 경우 UI에서 에러가 발생한다.
- **Embedding Mismatch**: RAG용 임베딩 모델이 Ollama에 로드되지 않으면 문서 처리가 실패한다.
- **VRAM OOM**: 대규모 RAG 처리 시 GPU 메모리 부족으로 인해 속도가 저하될 수 있다.

## Related Documents

- **Implementation**: `[../../../infra/08-ai/open-webui/README.md]`
- **Spec**: `[../../04.specs/08-ai/open-webui-spec.md]` (If exists)
- **Operation**: `[../../08.operations/08-ai/open-webui.md]`
- **Runbook**: `[../../09.runbooks/08-ai/open-webui.md]`
