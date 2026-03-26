<!-- Target: docs/04.specs/08-ai/spec.md -->

# AI Infrastructure Technical Specification (Spec)

## AI Infrastructure Specification

## Overview (KR)

이 문서는 `08-ai` 계층의 기술 설계와 구현 상세를 정의한다. Ollama 추론 엔진과 Open WebUI의 인터페이스 계약, 환경 변수 설정, 그리고 NVIDIA GPU 가속을 위한 인프라 명세를 다룬다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Docker Compose 서비스 정의 (`ollama`, `open-webui`, `ollama-exporter`)
  - 모델 영속 데이터 레이아웃 및 볼륨 매핑
  - RAG 환경 설정 및 임베딩 정책
- **Does Not Own**:
  - NVIDIA 드라이버 설치 (Host OS 영역)
  - Qdrant 컬렉션 관리 (Data 계층 Spec 영역)

## Related Inputs

- **PRD**: [../../01.prd/2026-03-26-08-ai.md](../../01.prd/2026-03-26-08-ai.md)
- **ARD**: [../../02.ard/0008-ai-architecture.md](../../02.ard/0008-ai-architecture.md)
- **Related ADRs**: [../../03.adr/0008-ollama-openwebui-local-ai.md](../../03.adr/0008-ollama-openwebui-local-ai.md)

## Contracts

- **Config Contract**:
  - `${DEFAULT_AI_MODEL_DIR}`: 모델 데이터가 저장될 호스트 경로
  - `${OLLAMA_PORT}`: 내부 11434 포트를 외부에 노출할 규격
- **Data / Interface Contract**:
  - OpenAI Compatible API (Ollama/WebUI 양방향)
- **Governance Contract**:
  - 모든 AI 트래픽은 `sso-auth` 미들웨어를 경유해야 함.

## Core Design

### Inference Engine (Ollama)

- **Execution Mode**: Local Binary via Docker.
- **Resource Limits**: 4 CPU Cores, 8GB Memory (Limit), 1 GPU (Reservation).
- **GPU Path**: `nvidia-container-runtime`을 통한 호스트 커널 직접 연결.

### UI & RAG (Open WebUI)

- **Backend**: Python (FastAPI based).
- **RAG Engine**: Ollama (Embedding) + Qdrant (Vector Store).
- **Embedding Model**: `qwen3-embedding:0.6b` (Standard across project).

## Interfaces

```yaml
# Ollama Interface Example
OLLAMA_BASE_URL: http://ollama:11434

# Open WebUI Environment
VECTOR_DB_URL: http://qdrant:6333
RAG_EMBEDDING_ENGINE: ollama
RAG_EMBEDDING_MODEL: qwen3-embedding:0.6b
```

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: LLM 추론 대행 및 지식 베이스 검색.
- **Inputs**: Text Prompt, Multi-modal Image (Optional), Document Path (for RAG).
- **Outputs**: Streaming Text Response, JSON structured data.

## Verification

### GPU Support Check

```bash
docker exec -it ollama nvidia-smi
```

### Model Availability Check

```bash
curl http://localhost:11434/api/tags
```

### RAG Integration Test

Open WebUI 설정 창에서 Qdrant 연결 상태 확인 및 임베딩 모델 테스트 수행.

## Success Criteria & Verification Plan

- **VAL-SPC-AI-01**: Ollama 컨테이너가 GPU를 인식하고 가속 추론이 가능한가.
- **VAL-SPC-AI-02**: chat.DOMAIN 주소로 SSO 로그인 후 대화가 가능한가.
- **VAL-SPC-AI-03**: 문서 업로드 시 Qdrant에 벡터 데이터가 정상 생성되는가.

## Related Documents

- **Plan**: [../../05.plans/2026-03-26-08-ai-standardization.md](../../05.plans/2026-03-26-08-ai-standardization.md)
- **Tasks**: [../../06.tasks/2026-03-26-08-ai-tasks.md](../../06.tasks/2026-03-26-08-ai-tasks.md)
