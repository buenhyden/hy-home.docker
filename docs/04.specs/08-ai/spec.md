# 08-AI Optimization Hardening Technical Specification

## Overview (KR)

이 문서는 `infra/08-ai`(Ollama, Open WebUI) 계층의 최적화/하드닝 기술 명세다. gateway 경계 보안, GPU concurrency 제어, exporter health-gating, stateful 운영 일관성, CI 정책 게이트, 카탈로그 기반 확장 요구를 구현 계약으로 정의한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Ollama/Open WebUI Traefik middleware 계약
  - Ollama concurrency/queue/resource 보호 계약
  - Open WebUI stateful template 계약
  - `ollama-exporter` dependency/healthcheck 계약
  - `check-ai-hardening.sh` 정책 게이트 계약
- **Does Not Own**:
  - 모델 학습/파인튜닝 파이프라인
  - Qdrant 내부 운영 정책/스키마
  - 외부 LLM provider 통합 정책

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-08-ai-optimization-hardening.md](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../../02.ard/0023-ai-optimization-hardening-architecture.md](../../02.ard/0023-ai-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0008-ollama-openwebui-local-ai.md](../../03.adr/0008-ollama-openwebui-local-ai.md)
  - [../../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - Ollama/Open WebUI 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 사용한다.
  - Ollama는 `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE`를 명시한다.
  - Open WebUI는 `template-stateful-med`를 사용한다.
  - `ollama-exporter`는 `ollama`의 `service_healthy` dependency와 metrics healthcheck를 가진다.
  - 두 compose는 `infra_net` external network 선언을 포함한다.
- **Data / Interface Contract**:
  - Open WebUI -> Ollama(`OLLAMA_BASE_URL`) + Qdrant(`VECTOR_DB_URL`) 연결을 유지한다.
  - Embedding 모델 기본값은 `qwen3-embedding:0.6b`를 유지한다.
- **Governance Contract**:
  - `scripts/check-ai-hardening.sh` 통과가 AI tier 하드닝 기준선이다.
  - CI `ai-hardening` job이 PR 단계에서 회귀를 차단한다.

## Core Design

- **Gateway Security Plane**:
  - AI 공개 경로는 TLS 종료 후 gateway 표준 체인 + SSO 체인을 강제한다.
- **Inference Runtime Plane**:
  - Ollama는 concurrency/queue 상한으로 GPU 과부하를 억제한다.
- **Stateful Control Plane**:
  - Open WebUI는 상태 저장 서비스로 stateful 템플릿 정책을 따른다.
- **Observability Plane**:
  - exporter는 health 기반으로 기동하며 metrics endpoint를 healthcheck로 검증한다.

## Data Modeling & Storage Strategy

- Ollama 모델 데이터는 `${DEFAULT_AI_MODEL_DIR}/ollama` 바인드 볼륨을 사용한다.
- Open WebUI 상태 데이터는 `${DEFAULT_AI_MODEL_DIR}/open-webui` 바인드 볼륨을 사용한다.
- 대화/RAG 데이터 보존 정책은 운영 정책 문서(`08.operations/08-ai/optimization-hardening.md`)에서 통제한다.

## Interfaces & Data Structures

### AI Hardening Control Surface

```yaml
ai_hardening_controls:
  ingress_security:
    ollama: gateway-standard-chain + sso-errors + sso-auth
    open_webui: gateway-standard-chain + sso-errors + sso-auth
  gpu_safeguards:
    ollama_num_parallel: required
    ollama_max_loaded_models: required
    ollama_max_queue: required
  startup_health_contract:
    ollama_exporter_depends_on_ollama_health: required
    ollama_exporter_metrics_healthcheck: required
  stateful_policy:
    open_webui_template: template-stateful-med
```

## Edge Cases & Error Handling

- concurrency 상한이 과도하게 낮으면 응답 지연이 증가할 수 있어 운영 지표 기반 튜닝이 필요하다.
- middleware 체인 누락 시 인증 우회 경로가 생길 수 있으므로 CI 게이트에서 즉시 차단한다.
- exporter healthcheck 실패 시 metrics 경로/포트 및 `OLLAMA_EXPORTER_PORT` 값을 점검한다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: AI 라우터 접근 정책 회귀
  - **Fallback**: 최근 정상 compose 라우팅 설정으로 롤백
  - **Human Escalation**: Gateway/Auth 운영 승인자
- **Failure Mode**: Ollama GPU 과부하/queue 적체
  - **Fallback**: concurrency/queue 상한 보수적 값으로 재조정
  - **Human Escalation**: AI Platform Owner
- **Failure Mode**: exporter metrics 관측 실패
  - **Fallback**: healthcheck/depends_on 계약 복구 후 재기동
  - **Human Escalation**: SRE on-call

## Verification

```bash
docker compose -f infra/08-ai/ollama/docker-compose.yml config
docker compose -f infra/08-ai/open-webui/docker-compose.yml config
bash scripts/check-ai-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-AI-001**: AI compose static validation 통과
- **VAL-AI-002**: AI hardening baseline script 실패 0건
- **VAL-AI-003**: PRD~Runbook optimization-hardening 문서 링크 정합성 유지
- **VAL-AI-004**: 카탈로그 `08-ai` 확장 항목(모델 승격, 접근 분리, 로그 정책)이 Plan/Tasks/Operations에 반영

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/08-ai/optimization-hardening.md](../../07.guides/08-ai/optimization-hardening.md)
- **Operation**: [../../08.operations/08-ai/optimization-hardening.md](../../08.operations/08-ai/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/08-ai/optimization-hardening.md](../../09.runbooks/08-ai/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
