# AI Engine (Ollama & RAG)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 로컬 LLM(Large Language Model) 서빙 및 RAG(Retrieval-Augmented Generation) 파이프라인을 위한 AI 인프라입니다.

**주요 기능 (Key Features)**:
- **Local LLM**: Ollama를 통해 Llama3, Mistral 등 모델 로컬 구동 (GPU 가속).
- **RAG**: Qdrant(벡터 DB)와 연동하여 문서 기반 질의응답 구현.
- **Chat UI**: Open WebUI를 통한 ChatGPT 유사 인터페이스 제공.

**기술 스택 (Tech Stack)**:
- **Runtime**: Ollama 0.1.35
- **Vector DB**: Qdrant v1.16.1
- **UI**: Open WebUI (Git Main)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**구조**:
1. **User** -> **Open WebUI** (질의)
2. **Open WebUI** -> **Ollama** (임베딩/생성)
3. **Open WebUI** -> **Qdrant** (유사도 검색)

## 3. 시작 가이드 (Getting Started)
**사전 요구사항**:
- NVIDIA GPU 및 `nvidia-container-toolkit` 설치 권장.

**실행 방법**:
```bash
docker compose up -d
```
> **참고**: 최초 실행 시 모델 다운로드(수 GB)로 인해 시간이 소요됩니다.

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `OLLAMA_HOST`: `0.0.0.0:11434` (외부 접속 허용)
- `NVIDIA_VISIBLE_DEVICES`: `all` (GPU 사용)

**네트워크 포트**:
- **Ollama API**: 11434 (`https://ollama.${DEFAULT_URL}`)
- **Web UI**: 8080 (`https://chat.${DEFAULT_URL}`)
- **Qdrant**: 6333 (`https://qdrant.${DEFAULT_URL}`)

## 5. 통합 및 API 가이드 (Integration Guide)
**API 엔드포인트**:
- Generate: `POST /api/generate`
- Embeddings: `POST /api/embeddings`

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: `ollama list` 명령으로 모델 로드 상태 확인.
**모니터링**: `ollama-exporter`를 통해 GPU 사용량 및 추론 속도 메트릭 수집.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- `ollama-data`: 다운로드된 모델 파일 (~/.ollama).
- `ollama-webui`: 채팅 이력 및 사용자 설정.
- `qdrant-data`: 벡터 임베딩 데이터.

## 8. 보안 및 강화 (Security Hardening)
- 기본적으로 API 인증이 없으므로 Traefik 등을 통해 외부 접근을 통제해야 합니다.
- Open WebUI는 자체 로그인 시스템을 제공합니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **GPU Not Found**: Docker GPU 런타임 설정 확인.
- **Slow Inference**: CPU 모드로 동작 중인지 확인 (`docker logs ollama`).

**진단 명령어**:
```bash
docker exec -it ollama ollama list
docker logs ollama
```
