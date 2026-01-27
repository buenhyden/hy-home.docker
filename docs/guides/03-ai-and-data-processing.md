# 🤖 AI & Data Processing Guide

로컬 LLM과 데이터 파이프라인 구성을 위한 가이드입니다.

## 1. Local LLM (Ollama)

클라우드 외부의 개인 정보를 안전하게 처리하기 위해 로컬 환경에서 거대 언어 모델을 실행합니다.

- **엔진**: `Ollama` (GPU 가속 지원)
- **API Endpoint**: `http://ollama-server:11434`
- **Web UI**: `https://ollama.${DEFAULT_URL}` (Open WebUI)

### 모델 다운로드 및 실행

Web UI에 접속하거나 CLI를 통해 모델을 추가할 수 있습니다:

```bash
docker exec -it ollama ollama run llama3
```

## 2. Vector DB (Qdrant)

RAG (Retrieval-Augmented Generation) 시스템 구축을 위한 고성능 벡터 검색 데이터베이스입니다.

- **Dashboard**: `http://qdrant:6333/dashboard`
- **특징**: 의미론적 검색을 위해 임베딩 데이터를 저장하고 초고속으로 검색합니다.

## 3. Workflow Automation (n8n)

다양한 서비스(API, DB, AI)를 노드 기반 워크플로우로 연결하여 자동화합니다.

- **접속 주소**: `https://n8n.${DEFAULT_URL}`
- **활용 예시**:
  - "데이터베이스에 새 항목이 생기면 LLM으로 요약하여 Slack으로 전송"
  - "정기적으로 웹사이트 데이터를 긁어와 Qdrant에 저장"

## 4. Object Storage (Minio)

S3와 호환되는 로컬 오브젝트 저장소입니다.

- **API 주소**: `http://minio:9000`
- **Console UI**: `https://minio-ui.${DEFAULT_URL}`
- **용도**: 아티팩트 저장, AI 모델 백업, 정적 파일 서빙.
