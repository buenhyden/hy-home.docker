---
title: AI Infrastructure Architecture Description
version: 1.0.0
type: sdlc/architecture-description
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: AD-0008
parent_ids:
  - REQ-0009
created: 2026-03-26
updated: 2026-08-10
---
# AI Infrastructure Architecture Description

## Context and Stakeholders

이 문서는 `08-ai` 계층의 참조 아키텍처와 품질 속성을 정의한다. 로컬 환경에서의 고성능 LLM 추론 및 RAG 시스템을 위한 GPU 자원 할당, 서비스 경계, 그리고 데이터 흐름에 대한 구조적 가이드라인을 제공한다.

### Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

`08-ai` 계층은 시스템의 '지능'을 담당하는 핵심 영역으로, 프라이버시가 보호되는 로컬 추론 엔진과 이를 활용하는 UI/RAG 인터페이스를 소유한다. NVIDIA GPU 자원을 추론 연산에 집중적으로 사용하며, 외부 모델 API에 의존하지 않는 독립적인 AI 에코시스템을 구축한다.

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owns**:
  - LLM 추론 엔진 (`Ollama`)
  - AI 사용자 인터페이스 및 RAG 오케스트레이터 (`Open WebUI`)
  - 로컬 모델 가중치 및 설정 관리
- **Consumes**:
  - GPU 하드웨어 자원 (via NVIDIA Container Toolkit)
  - 벡터 데이터베이스 (`04-data/qdrant`)
  - 사용자 인증 및 SSO (`02-auth/keycloak`)
- **Does Not Own**:
  - 벡터 처리 서버 자체 (Qdrant 인스턴스는 Data 계층 소유)
  - 서비스 모니터링 수집기 (Observability 계층 소유)
- **Non-goals**:
  - 고사양 GPU 클러스터 컴퓨팅 (단일 노드 또는 단일 리소스 그룹 최적화 중심)
  - 모델의 직접적인 학습(Training) 환경 제공

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Performance**: NVIDIA CUDA 가속을 통한 저지연 추론 달성. FP16/INT8 양자화 모델 활용 권장.
- **Security**: 모든 데이터는 프로젝트 내부 네트워크(`infra_net`) 내에 머물며, Keycloak을 통한 엄격한 RBAC 적용.
- **Reliability**: Healthcheck를 통한 추론 엔진 상태 감시 및 자동 복구.
- **Scalability**: 필요 시 Worker 컨테이너 증설을 통한 수평 확장(단, GPU 할당 정책 준수 필요).
- **Observability**: `ollama-exporter`를 통해 VRAM 사용량, 모델 로드 상태, API 호출 통계 상시 모니터링.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

시스템은 하이브리드 구조로 운영된다.

1. **Inference Layer (Backend)**: Ollama가 모델 저장소와 GPU를 직접 제어하며 OpenAI 호환 API를 제공한다.
2. **Interaction Layer (Frontend/Orchestrator)**: Open WebUI가 채팅 UI와 더불어 Qdrant와 연동된 RAG 로직(Embedding → Search → Augment)을 수행한다.

### AI Agent Architecture

- **Model/Provider Strategy**: 로컬 Ollama를 기본 제공자로 지정하되, 중요 태스크에 한해 외부 API(Claude/OpenAI)로의 폴백 전략 지원.
- **Tooling Boundary**: 에이전트는 Ollama API를 인터페이스로 사용하며 직접 모델 가중치나 GPU 드라이버를 조작하지 않는다.
- **Latency / Cost Budget**: 모델 리로딩 횟수 최소화 및 경량 임베딩 모델(`qwen3-embedding:0.6b`) 사용으로 리소스 효율 극대화.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

- **Key Entities / Flows**: User Prompt → Open WebUI (RAG Context Enrich) → Ollama (Inference) → Response Streaming.
- **Storage Strategy**: 대용량 모델 파일(`${DEFAULT_AI_MODEL_DIR}/ollama`)은 bind mount를 통해 호스트의 대용량 스토리지와 직접 연동한다.
- **Data Boundaries**: 사용자 문서는 Open WebUI 내부 DB와 Qdrant에만 존재하며, 추론 엔진에는 일시적인 컨텍스트로만 전달된다.

## Deployment View

- **Runtime / Platform**: Docker Compose v3.8+ (NVIDIA Container Support).
- **Deployment Model**: `ai` 프로필로 분리되어 필요 시에만 선택적으로 배포 가능.
- **Operational Evidence**: `nvidia-smi`를 통한 실시간 GPU 상태 확인 및 `ollama-exporter` 대시보드.

## Traceability

상위 요구사항의 disposition과 관련 결정·구현 명세는 `Related Documents`의 PRD, ADR, Spec 링크가 소유한다. 이 설명은 그 문서의 역할을 대체하지 않는다.

## Related Documents

- **PRD**: [009-ai.md](../../01.requirements/0009-ai.md)
- **Spec**: [009-ai/spec.md](0008-ai-architecture.md)
- **ADR**: [0008-ollama-openwebui-local-ai.md](../decisions/0008-ollama-openwebui-local-ai.md)
