# 08-AI Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `08-ai` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, Ollama GPU 보호, Open WebUI stateful 운영, 모델 승격/접근 통제/로그 보존 정책을 통제한다.

## Policy Scope

- `infra/08-ai/ollama/docker-compose.yml`
- `infra/08-ai/open-webui/docker-compose.yml`
- `scripts/check-ai-hardening.sh`

## Applies To

- **Systems**: Ollama, Ollama Exporter, Open WebUI
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Ollama/Open WebUI 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - Ollama는 `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 유지한다.
  - Open WebUI는 `template-stateful-med`를 사용한다.
  - `ollama-exporter`는 `ollama` health 기반 의존성과 metrics healthcheck를 유지한다.
  - AI 변경은 `check-ai-hardening.sh` 및 CI `ai-hardening`을 통과해야 한다.
  - 모델 승격은 실험/검증/운영 단계와 승인 기록을 포함해야 한다.
  - Open WebUI 모델 접근 권한은 역할/환경 단위로 분리해야 한다.
  - 대화 로그는 보존 기간/마스킹 기준을 명시하고 비식별화 정책을 준수해야 한다.
  - optimization-hardening 문서(PRD~Runbook) 링크를 유지해야 한다.
- **Allowed**:
  - Ollama 상한값의 점진적 튜닝(운영 지표 기반)
  - 모델 승격 기준 강화(품질/안전/eval 항목 추가)
  - 로그 보존/마스킹 정책의 보수적 강화
- **Disallowed**:
  - 무승인 SSO/middleware 완화
  - 모델 승격 절차 생략 배포
  - 민감 대화 로그 무마스킹 저장

## Exceptions

- 장애 대응으로 일시 완화가 필요할 경우 승인 기록과 종료 시점이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

## Verification

- `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
- `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
- `bash scripts/check-ai-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

## Review Cadence

- 월 1회 정기 검토
- AI 이미지/모델 정책/인증 정책 변경 시 수시 검토

## Catalog Expansion Approval Gates

- **Ollama 승인 조건**:
  - 모델 캐시/스토리지 정책 문서화 및 운영 증적 확보
  - GPU concurrency/queue 상한 변경 시 근거 지표 첨부
  - 모델 승격(실험 -> 운영) 체크리스트 완료
- **Open WebUI 승인 조건**:
  - SSO 강제 경로 검증 및 우회 금지 확인
  - 모델 접근 권한 분리 정책(역할/환경) 문서화
  - 대화 로그 보존 기간/마스킹 규칙/파기 절차 문서화

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: 모델/프롬프트 변경은 PRD/Plan/Task 반영 후 승인된 승격 절차로 수행
- **Eval / Guardrail Threshold**: 하드닝 체크 + 정책 검증 + 승인 게이트 통과 필수
- **Log / Trace Retention**: 최소 필요 보존 원칙, 민감 데이터 마스킹 필수
- **Safety Incident Thresholds**: 인증 우회 의심, GPU OOM 반복, 비마스킹 로그 탐지 시 즉시 runbook 전환

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-08-ai-optimization-hardening.md](../../01.prd/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../../02.ard/0023-ai-optimization-hardening-architecture.md](../../02.ard/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md](../../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/08-ai/spec.md](../../04.specs/08-ai/spec.md)
- **Plan**: [../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/08-ai/optimization-hardening.md](../../07.guides/08-ai/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/08-ai/optimization-hardening.md](../../09.runbooks/08-ai/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
