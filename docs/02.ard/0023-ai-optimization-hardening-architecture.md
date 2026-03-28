# 08-AI Optimization Hardening Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `08-ai` 계층의 최적화/하드닝 참조 아키텍처를 정의한다. gateway 경계 보안, GPU concurrency 제어, stateful 운영 일관성, health 기반 관측 안정성, 카탈로그 기반 운영 확장 정책을 아키텍처 관점에서 정리한다.

## Summary

AI tier는 두 개의 핵심 평면으로 구성된다.

- Ollama (로컬 LLM 추론/임베딩 엔진)
- Open WebUI (사용자 인터페이스 + RAG 오케스트레이션)

외부 진입은 Traefik TLS 경계에서 표준 middleware+SSO 체인을 공유한다.

## Boundaries & Non-goals

- **Owns**:
  - AI 관리 경로 gateway/SSO 경계 계약
  - Ollama GPU concurrency/resource 보호 계약
  - Open WebUI stateful 운영 계약
  - AI hardening CI 정책 게이트
  - 08-ai 카탈로그 확장 정책(모델 승격/접근 통제/로그 정책)
- **Consumes**:
  - `01-gateway` 표준 middleware chain
  - `02-auth` SSO middleware
  - `04-data` Qdrant 및 데이터 계층
- **Does Not Own**:
  - 모델 학습/파인튜닝 파이프라인
  - Qdrant 내부 스키마/인덱스 운영 세부
- **Non-goals**:
  - 즉시 분산 GPU 스케줄러 도입
  - 즉시 외부 LLM provider 병행 표준화

## Quality Attributes

- **Performance**: Ollama concurrency/queue 상한으로 GPU 과부하를 억제한다.
- **Security**: gateway-standard-chain + SSO 체인으로 공개 경계 보안을 통일한다.
- **Reliability**: health-gated dependency/healthcheck로 기동 안정성과 관측 신뢰도를 강화한다.
- **Scalability**: 모델 승격/리소스 정책 기반으로 단계적 확장을 가능하게 한다.
- **Observability**: exporter metrics health 계약과 CI 하드닝 게이트를 표준화한다.
- **Operability**: `check-ai-hardening.sh`를 AI tier 운영 기준선으로 사용한다.

## System Overview & Context

- **Ingress path**:
  - Client -> Traefik(websecure) -> ollama/chat routers -> Ollama/Open WebUI
- **Inference/RAG plane**:
  - Open WebUI -> Ollama (generation + embedding)
  - Open WebUI -> Qdrant (vector retrieval)
- **Control plane**:
  - SSO middleware, 정책 게이트 script/CI, 운영 문서(07/08/09)

## Data Architecture

- **Key Entities / Flows**:
  - 모델 아티팩트, 대화/세션 메타데이터, 임베딩 벡터 참조
- **Storage Strategy**:
  - Ollama 모델 캐시: `${DEFAULT_AI_MODEL_DIR}/ollama`
  - Open WebUI 상태 데이터: `${DEFAULT_AI_MODEL_DIR}/open-webui`
- **Data Boundaries**:
  - 벡터 인덱스 실데이터는 Qdrant 소유, AI tier는 호출/활용 정책을 소유한다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose (`infra/08-ai/*`)
- **Deployment Model**:
  - Ollama + exporter
  - Open WebUI (stateful) + ollama/qdrant dependency
- **Operational Evidence**:
  - `docker compose config` checks
  - `scripts/check-ai-hardening.sh`
  - CI `ai-hardening` job

## Catalog-aligned Expansion Targets

- **Ollama**:
  - 모델 캐시/스토리지 운영 정책 명문화
  - GPU scheduling/concurrency 상한 운영 표준화
  - 모델 승격 절차(실험 -> 운영) 수립
- **Open WebUI**:
  - SSO 강제/우회 금지 기준 강화
  - 모델 접근 권한 분리(역할/환경)
  - 대화 로그 보존/마스킹 정책 강화

## Related Documents

- **PRD**: [../01.prd/2026-03-28-08-ai-optimization-hardening.md](../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **Spec**: [../04.specs/08-ai/spec.md](../04.specs/08-ai/spec.md)
- **Plan**: [../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/08-ai/optimization-hardening.md](../07.guides/08-ai/optimization-hardening.md)
- **Operation**: [../08.operations/08-ai/optimization-hardening.md](../08.operations/08-ai/optimization-hardening.md)
- **Runbook**: [../09.runbooks/08-ai/optimization-hardening.md](../09.runbooks/08-ai/optimization-hardening.md)
