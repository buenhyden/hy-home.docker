# AI & LLM Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 로컬 LLM(Large Language Model) 실행 및 RAG(Retrieval-Augmented Generation) 구현을 위한 인프라스트럭처를 정의합니다. Ollama를 통해 모델을 서빙하고, Qdrant를 벡터 데이터베이스로 사용하며, Open WebUI를 통해 사용자 인터페이스를 제공합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **ollama** | Model Runner | Llama 3, Mistral 등 LLM 모델을 실행하는 런타임입니다. NVIDIA GPU(`gpu`) 자원을 사용하도록 설정되어 있습니다. |
| **qdrant** | Vector DB | 텍스트 임베딩을 저장하고 유사도 검색을 수행하는 벡터 데이터베이스입니다. RAG 구현의 핵심 컴포넌트입니다. |
| **open-webui** | Chat Interface | ChatGPT와 유사한 웹 인터페이스를 제공하며, RAG 기능을 위해 Ollama 및 Qdrant와 연동됩니다. |
| **ollama-exporter** | Metrics Exporter | Ollama 서비스의 메트릭을 수집합니다. |

## 3. 구성 및 설정 (Configuration)

### 리소스 (GPU)
Ollama 서비스는 NVIDIA GPU 사용을 위해 `deploy.resources.reservations.devices` 설정이 되어 있습니다. 호스트 머신에 NVIDIA 드라이버 및 `nvidia-container-toolkit` 설정이 필요합니다.

### 네트워크 및 연결
- **Ollama API**: `http://ollama:${OLLAMA_PORT}` (내부 통신)
- **Vector DB**: `http://qdrant:${QDRANT_PORT}` (내부 통신)

### RAG (검색 증강 생성)
Open WebUI는 환경 변수를 통해 RAG 설정을 로드합니다.
- `RAG_EMBEDDING_ENGINE=ollama`: 임베딩 생성에도 Ollama를 사용
- `VECTOR_DB_URL`: Qdrant 연결 주소

### 로드밸런싱 (Traefik)
- **Chat UI**: `https://chat.${DEFAULT_URL}` (사용자 접속용)
- **Ollama API**: `https://ollama.${DEFAULT_URL}` (외부 API 호출용)
- **Qdrant UI**: `https://qdrant.${DEFAULT_URL}` (대시보드 접속용)
