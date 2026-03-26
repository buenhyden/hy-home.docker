<!-- Target: docs/03.adr/0008-ollama-openwebui-local-ai.md -->

# ADR-0008: Ollama and Open WebUI for Local AI Infrastructure

## Overview (KR)

이 문서는 AI 인프라 구축을 위한 핵심 기술 스택으로 Ollama와 Open WebUI를 선택한 결정 사항을 기록한다. 로컬 리소스 활용, 데이터 프라이버시, 그리고 RAG 확장성을 최우선으로 고려하였다.

## Context

프로젝트 내에서 지능형 서비스를 제공하기 위해서는 LLM 추론 엔진과 이를 활용할 수 있는 사용자 인터페이스가 필요하다. 또한, 내부 문서를 기반으로 한 답변 생성을 위해 RAG(Retrieval-Augmented Generation) 기능이 필수적이다. 상용 API(OpenAI 등)는 비용 및 보안 우려가 있어 제외하였으며, 로컬 운영이 가능한 다양한 오픈소스 대안을 검토하였다.

## Decision

- **추론 엔진**: `Ollama`를 채택한다. (Go 기반의 빠른 실행력, 간편한 모델 배포, 강력한 GPU 가속 지원)
- **UI/RAG**: `Open WebUI`를 채택한다. (UI 편의성, Qdrant 연동 RAG 기본 지원, OpenAI API 규격 호환)
- **액셀러레이터**: NVIDIA Docker 런타임을 통한 기술적 GPU 전용 패스를 유지한다.

## Explicit Non-goals

- vLLM, Text Generation Inference(TGI) 등 대규모 서빙 최적화 환경 구축 (리소스 소모가 극심하고 관리 포인트가 많음).
- 클라우드 전용 모델 API의 직접적인 대체 개발.

## Consequences

- **Positive**:
  - 외부 네트워크 단절 시에도 AI 서비스 이용 가능.
  - 별도의 API 토큰 비용 없이 무제한 실험 가능.
  - 데이터 유출 경로 완벽 차단.
- **Trade-offs**:
  - 호스트 OS의 GPU 드라이버와 커널 버전 의존성 발생.
  - 상용 모델 대비 로컬 오픈소스 모델의 성능 및 컨텍스트 길이 한계.

## Alternatives

### vLLM

- Good: 성능(Throughput)이 매우 뛰어나며 고효율 서빙 가능.
- Bad: 설정이 복잡하고 높은 VRAM을 상시 점유하며, Ollama 대비 모델 관리가 번거로움.

### LocalAI

- Good: 다양한 모델(Audio, Image 등)을 광범위하게 지원.
- Bad: 성능면에서 Ollama 대비 최적화가 부족하고 배포 설정이 상대적으로 무거움.

## Agent-related Example Decisions (If Applicable)

- **Model selection**: 경량 업무는 `llama3.1-8b`, 복잡한 추론은 `qwen2.5-coder` 계열 채택.
- **Tool gating**: 에이전트는 Open WebUI의 API 엔드포인트를 통해 간접적으로 추론 수행.

## Related Documents

- **PRD**: [2026-03-26-08-ai.md](../01.prd/2026-03-26-08-ai.md)
- **ARD**: [0008-ai-architecture.md](../02.ard/0008-ai-architecture.md)
- **Spec**: [08-ai/spec.md](../04.specs/08-ai/spec.md)
