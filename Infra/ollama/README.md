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

## 10. 상세 사용 가이드 (Detailed Usage Guide)

### 10.1 CLI 사용법 (CLI Usage)
컨테이너 내부에서 `ollama` 명령어를 직접 실행하여 모델을 관리할 수 있습니다.

```bash
# 실행 중인 ollama 컨테이너 접속
docker exec -it ollama /bin/bash

# 모델 목록 확인
ollama list

# 모델 다운로드 (예: llama3)
ollama pull llama3

# 로컬에서 모델 실행 (대화형 모드)
ollama run llama3

# 모델 삭제
ollama rm llama3
```

### 10.2 API 사용법 (API Usage)
HTTP 요청을 통해 Ollama API를 사용할 수 있습니다.

**Generate (텍스트 생성)**:
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

**Chat (대화형 생성)**:
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ],
  "stream": false
}'
```

### 10.3 Open WebUI & RAG 가이드
Open WebUI를 통해 그래픽 인터페이스로 RAG 기능을 활용하는 방법입니다.

1.  **접속**: 브라우저에서 `http://localhost:8080` (또는 설정된 도메인) 접속.
2.  **문서 업로드**:
    *   채팅 입력창 옆의 `+` 버튼 또는 `Documents` 메뉴 클릭.
    *   PDF, TXT 등 문서 파일 업로드 및 컬렉션(Collection) 생성.
3.  **RAG 대화**:
    *   채팅 시 `#`을 입력하여 업로드한 컬렉션을 선택.
    *   질문 입력 시 해당 문서를 참조하여 답변 생성.

## 11. 설치된 모델 현황 (Installed Models)
현재 인프라에 설치된 LLM 모델 목록과 상세 정보입니다.

### 11.1 EXAONE Family (LG AI Research)
**1. EXAONE 3.5 (7.8B)**
- **태그**: `exaone3.5:7.8b`
- **개요**: 최신 이중언어(한국어, 영어) 모델로, 긴 문맥(32k) 처리와 일반적인 지시 수행에 능숙합니다.
- **특징**: Bilingual, Long Context, SwiGLU/GQA/RoPE 아키텍처.
- **용도**: 일반 대화, 문서 요약, RAG.

**2. EXAONE Deep (7.8B)**
- **태그**: `exaone-deep:7.8b`
- **개요**: 추론(Reasoning) 능력에 특화된 모델로, 수학, 코딩, 과학 분야의 복잡한 문제 해결에 최적화되어 있습니다.
- **특징**: 강화된 추론 능력, 경량화된 고성능 모델.
- **용도**: 복잡한 질의 응답, 수학/과학 문제 풀이, 심층 분석.

### 11.2 Qwen 3 Family (Alibaba Cloud)
**1. Qwen 3 (8B)**
- **태그**: `qwen3:8b`
- **개요**: "Thinking" 모드와 일반 모드를 오가는 고성능 모델로, 논리적 추론과 코딩 능력이 강화되었습니다.
- **특징**: 32k~128k 컨텍스트, 100개국어 지원, Agent 기능 강화.
- **용도**: 복잡한 추론, 언어 번역, 에이전트 작업.

**2. Qwen 3 VL (8B)**
- **태그**: `qwen3-vl:8b`
- **개요**: 시각-언어(Vision-Language) 멀티모달 모델로, 이미지 및 비디오 이해 능력이 뛰어납니다.
- **특징**: GUI 조작 가능(Agent), 시각적 코딩, 공간 인식, 영상 분석.
- **용도**: 이미지 분석, GUI 에이전트, 비디오 콘텐츠 이해.

**3. Qwen 3 Embedding (4B)**
- **태그**: `qwen3-embedding:4b`
- **개요**: 고성능 텍스트 임베딩 모델입니다.
- **특징**: 대규모 코퍼스 기반의 정밀한 벡터 표현.
- **용도**: RAG 시스템의 벡터화, 시맨틱 검색.

### 11.3 DeepSeek Family
**1. DeepSeek R1 (8B)**
- **태그**: `deepseek-r1:8b`
- **개요**: 추론(Reasoning)에 특화된 모델로, Chain-of-Thought(CoT) 과정을 통해 복잡한 문제를 단계별로 해결합니다.
- **특징**: Distilled Reasoning, 수학/코딩/논리 성능 우수.
- **용도**: 논리 퍼즐, 심층 사고가 필요한 작업.

**2. DeepSeek OCR (3B)**
- **태그**: `deepseek-ocr:3b`
- **개요**: OCR(광학 문자 인식) 및 문서 구조화 전문 Vision-Language 모델입니다.
- **특징**: 텍스트 검출 및 마크다운 변환 탁월, 다국어 지원.
- **용도**: PDF/이미지 문서의 텍스트 변환 및 구조화.

### 11.4 Google Gemma Family
**1. Gemma 3 (4B)**
- **태그**: `gemma3:4b`
- **개요**: 텍스트와 이미지를 동시에 처리할 수 있는 멀티모달 모델입니다.
- **특징**: 128k 컨텍스트, 멀티링구얼 지원, 경량화된 구조.
- **용도**: 이미지-텍스트 복합 질의, 긴 문서 처리.

**2. FunctionGemma (270M)**
- **태그**: `functiongemma:270m`
- **개요**: 함수 호출(Function Calling)에 특화된 초경량 모델입니다.
- **특징**: 자연어 명령 -> API 호출 변환 최적화, 엣지 구동 가능.
- **용도**: IoT 제어, 도구 호출 에이전트, 라우팅.

### 11.5 Other Models
**1. Ministral 3 (8B)**
- **태그**: `ministral-3:8b`
- **개요**: 엣지/로컬 환경에 최적화된 고효율 Dense 모델입니다.
- **특징**: 128k 컨텍스트, 시각/텍스트 멀티모달 기능 포함(변형에 따라), 빠른 추론 속도.
- **용도**: 온디바이스 AI, 로컬 챗봇.

**2. Olmo 3 (7B)**
- **태그**: `olmo-3:7b`
- **개요**: Allen Institute for AI의 완전 개방형(Open Weights/Data) 모델입니다.
- **특징**: 투명성 보장, 과학적 연구 및 재현성 중시, 65k 컨텍스트.
- **용도**: AI 연구, 투명성이 요구되는 응용 분야.

**3. Nomic Embed Text v2 MoE**
- **태그**: `nomic-embed-text-v2-moe:latest`
- **개요**: MoE(Mixture of Experts) 기반의 다국어 텍스트 임베딩 모델입니다.
- **특징**: 가변 차원(Matryoshka), 고효율/고성능 임베딩, 100개국어 지원.
- **용도**: 다국어 검색, 효율적인 RAG 구축.


