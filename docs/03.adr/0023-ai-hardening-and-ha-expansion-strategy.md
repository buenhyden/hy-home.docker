# ADR-0023: AI Hardening and HA Expansion Strategy

## Overview (KR)

이 문서는 `08-ai` 계층에 대해 즉시 적용 가능한 하드닝(경계 보안, GPU concurrency 상한, stateful 템플릿 정렬, exporter health-gating, CI 게이트)을 우선 시행하고, 카탈로그 확장 항목(모델 승격/접근 분리/로그 정책)은 단계적으로 추진하는 결정을 기록한다.

## Context

AI tier는 GPU/모델 리소스와 사용자 대화 경로를 동시에 다루므로, 보안/가용성/운영 통제의 불균형이 빠르게 장애와 정책 위반으로 이어질 수 있다. 카탈로그는 08-ai에서 운영 표준 강화를 요구하고 있어, 단기 안정화와 중기 확장을 분리한 의사결정이 필요하다.

## Decision

- 즉시 하드닝을 시행한다.
  - Ollama/Open WebUI 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 강제한다.
  - Ollama에 `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 명시한다.
  - Open WebUI를 `template-stateful-med`로 정렬한다.
  - `ollama-exporter`에 `ollama` health-gated dependency와 metrics healthcheck를 강제한다.
  - `scripts/check-ai-hardening.sh`와 CI `ai-hardening` job을 도입한다.
- 카탈로그 확장은 단계적으로 시행한다.
  - Ollama 모델 승격(실험 -> 운영) 절차 수립
  - Open WebUI 모델 접근 권한 분리 정책 수립
  - 대화 로그 보존/마스킹 정책 수립

## Explicit Non-goals

- 즉시 멀티노드 Ollama 클러스터 구축
- 즉시 외부 상용 LLM 다중 공급자 표준화
- Qdrant 데이터 모델 자체 변경

## Consequences

- **Positive**:
  - AI 공개 경로 보안 정책이 gateway 표준으로 정렬된다.
  - GPU 자원 폭주 가능성을 낮추고 서비스 안정성을 높인다.
  - AI tier 회귀를 PR 단계에서 자동 차단할 수 있다.
  - 카탈로그 확장 항목이 문서/태스크 단위로 실행 가능해진다.
- **Trade-offs**:
  - 동시성 상한 도입으로 단기 처리량이 제한될 수 있다.
  - SSO/접근 통제 강화로 기존 임시 테스트 경로 조정이 필요하다.

## Alternatives

### 카탈로그 확장을 즉시 전면 구현

- Good:
  - 기능 확장을 빠르게 체감 가능
- Bad:
  - 변경 반경이 커져 안정화/롤백 복잡도 증가

### 문서만 갱신하고 런타임/CI 하드닝 보류

- Good:
  - 단기 구현 비용 절감
- Bad:
  - 정책 위반/회귀를 자동 차단하지 못함

## Agent-related Example Decisions (If Applicable)

- Guardrail strategy: AI 공개 경로는 gateway+SSO 체인 필수
- Tool gating: `check-ai-hardening.sh`를 AI tier 머지 전 필수 정책 게이트로 적용

## Related Documents

- **PRD**: [../01.prd/2026-03-28-08-ai-optimization-hardening.md](../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../02.ard/0023-ai-optimization-hardening-architecture.md](../02.ard/0023-ai-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/08-ai/spec.md](../04.specs/08-ai/spec.md)
- **Plan**: [../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Related ADR**: [./0008-ollama-openwebui-local-ai.md](./0008-ollama-openwebui-local-ai.md)
