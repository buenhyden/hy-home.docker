<!-- Target: docs/07.guides/08-ai/open-webui.md -->

# Open WebUI Interface & RAG Guide

> Open WebUI 기반 로컬 LLM 채팅 및 RAG 운영 가이드.

---

## Overview (KR)

이 문서는 `hy-home.docker` 환경에서 Open WebUI를 통해 Ollama 모델과 대화하고, 문서 기반 RAG를 사용하는 방법을 설명한다. 운영자가 재현 가능한 절차로 접근/인증, 모델 선택, 문서 인덱싱, 기본 점검을 수행할 수 있도록 정리한다.

## Guide Type

`system-guide`

## Target Audience

- AI Engineer
- Operator
- Internal User
- Agent-tuner

## Purpose

- Open WebUI의 핵심 사용 흐름(접속, 인증, 모델 선택, 채팅)을 표준화한다.
- RAG 인덱싱 및 질의 흐름을 `OLLAMA_BASE_URL`, `VECTOR_DB_URL`, `RAG_EMBEDDING_MODEL` 기준으로 이해한다.
- 장애 징후를 빠르게 식별하고 런북으로 연결한다.

## Prerequisites

- `open-webui` 컨테이너가 기동 가능해야 한다.
- `ollama` 컨테이너가 `http://ollama:${OLLAMA_PORT:-11434}`로 접근 가능해야 한다.
- `qdrant` 컨테이너가 `http://qdrant:${QDRANT_PORT:-6333}`로 접근 가능해야 한다.
- Open WebUI 환경변수 확인:
  - `OLLAMA_BASE_URL`
  - `VECTOR_DB_URL`
  - `RAG_EMBEDDING_MODEL` (기본값: `qwen3-embedding:0.6b`)
- SSO 환경(예: Keycloak + `sso-auth@file`)이 정상이어야 한다.

## Step-by-step Instructions

### 1. Access & Authentication

1. 브라우저에서 `https://chat.${DEFAULT_URL}` 접속.
2. SSO 로그인 완료 후 Open WebUI 대시보드 진입 확인.
3. 로그인 루프 또는 401 발생 시 먼저 인증 계층 상태를 확인한다.

### 2. Model Selection & Chat

1. 상단 모델 선택기에서 Ollama 모델을 선택한다.
2. 간단한 프롬프트(예: `hello`)로 응답 확인.
3. 모델 목록이 비어 있으면 Open WebUI에서 Ollama 연결 상태를 점검한다.

### 3. RAG Document Indexing

1. 문서 업로드 메뉴에서 PDF/TXT 문서를 업로드한다.
2. Open WebUI가 `RAG_EMBEDDING_MODEL`로 임베딩 생성 후 Qdrant에 저장하는지 확인한다.
3. 업로드된 문서를 지정하여 질의하고, 답변에 문서 근거가 반영되는지 확인한다.

### 4. Quick Connectivity Checks

```bash
# Open WebUI health
curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health

# Open WebUI -> Ollama connectivity (컨테이너 내부)
docker exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

# Open WebUI -> Qdrant connectivity (컨테이너 내부)
docker exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
```

### 5. Advanced Settings

1. 모델별 시스템 프롬프트(System Prompt)를 워크로드에 맞게 분리한다.
2. Temperature, Top-K, Top-P를 모델 특성에 맞춰 조정한다.
3. 임베딩 모델 변경 시 기존 인덱스 재생성 계획을 먼저 수립한다.

## Common Pitfalls

- **Ollama 연결 실패**: `OLLAMA_BASE_URL` 오타 또는 `ollama` 비정상 상태.
- **Qdrant 연결 실패**: `VECTOR_DB_URL` 오타, 네트워크 미연결, Qdrant 다운.
- **임베딩 모델 누락**: `RAG_EMBEDDING_MODEL`이 Ollama에 준비되지 않아 인덱싱 실패.
- **VRAM OOM**: 동시 인덱싱/추론 증가로 응답 지연 또는 실패.
- **SSO 문제**: 인증 미들웨어/리디렉션 설정 불일치로 접근 실패.

## Related Documents

- **PRD (Open WebUI)**: `[../../01.prd/2026-03-27-08-ai-open-webui.md]`
- **ARD (Open WebUI)**: `[../../02.ard/0013-open-webui-architecture.md]`
- **ADR (Open WebUI)**: `[../../03.adr/0016-open-webui-implementation.md]`
- **Spec (Open WebUI)**: `[../../04.specs/08-ai/open-webui.md]`
- **Plan (Open WebUI)**: `[../../05.plans/2026-03-27-08-ai-open-webui-plan.md]`
- **Task (Open WebUI)**: `[../../06.tasks/2026-03-27-08-ai-open-webui-tasks.md]`
- **Operation**: `[../../08.operations/08-ai/open-webui.md]`
- **Runbook**: `[../../09.runbooks/08-ai/open-webui.md]`
