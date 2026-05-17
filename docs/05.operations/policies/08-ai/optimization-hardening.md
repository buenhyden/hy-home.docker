# 08-AI Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `08-ai` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, Ollama GPU 보호, Open WebUI stateful 운영, 모델 승격/접근 통제/로그 보존 정책을 통제한다.

## Policy Scope

- `infra/08-ai/ollama/docker-compose.yml`
- `infra/08-ai/open-webui/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 08-ai`

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
  - optimization-hardening 문서(PRD~Procedure) 링크를 유지해야 한다.
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
- `bash scripts/hardening/check-all-hardening.sh 08-ai`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

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

- **PRD**: [../../01.requirements/2026-03-28-08-ai-optimization-hardening.md](../../../01.requirements/2026-03-28-08-ai-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md](../../../02.architecture/requirements/0023-ai-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/08-ai/spec.md](../../../03.specs/08-ai/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/05.operations/08-ai/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 08-AI Optimization Hardening Usage

#### Overview (KR)

이 문서는 `08-ai` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 경계 보안, GPU concurrency 제어, stateful 템플릿 일관성, health 기반 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- AI Platform Owner

#### Purpose

- Ollama/Open WebUI 공개 경로를 gateway+SSO 정책에 정렬한다.
- Ollama GPU 자원 보호를 위한 concurrency/queue 상한을 적용한다.
- Open WebUI stateful 운영 일관성을 확보한다.
- AI 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목(모델 승격/접근 분리/로그 정책)을 운영 기준으로 반영한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/08-ai` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

#### Step-by-step Instructions

1. 정적 구성 점검
   - `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
   - `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - Ollama/Open WebUI 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. Ollama 리소스 보호 적용
   - `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 상한을 확인/조정한다.
4. Open WebUI stateful 일관성 확인
   - Open WebUI가 `template-stateful-med`를 사용하도록 확인한다.
5. Exporter 안정성 강화 확인
   - `ollama-exporter`가 `ollama` `service_healthy`에 의존하는지 확인한다.
   - metrics healthcheck(`http://localhost:${OLLAMA_EXPORTER_PORT:-11435}/metrics`)를 확인한다.
6. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`
7. 카탈로그 확장 운영 기준 반영
   - 모델 승격 절차(실험 -> 운영)를 tasks/operations에 반영한다.
   - Open WebUI 모델 접근 권한 분리 기준을 반영한다.
   - 대화 로그 보존/마스킹 정책을 반영한다.

#### Common Pitfalls

- middleware 체인을 일부 라우터에만 적용하는 실수
- Ollama 상한 없이 고동시성 부하를 허용해 GPU OOM을 유발하는 실수
- Open WebUI를 stateless 템플릿으로 운용해 상태 드리프트를 유발하는 실수
- exporter health 계약 없이 모니터링 신뢰도를 낮추는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-08-ai-optimization-hardening.md](../../../01.requirements/2026-03-28-08-ai-optimization-hardening.md)
- **Spec**: [../../03.specs/08-ai/spec.md](../../../03.specs/08-ai/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/08-ai/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 08-AI Optimization Hardening Procedure

#### Overview (KR)

이 런북은 `08-ai` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, Ollama concurrency 설정 누락, Open WebUI stateful 드리프트, exporter health 계약 실패, CI 게이트 실패를 중심으로 점검/복구한다.

#### Purpose

- AI 공개 경로 보안과 GPU 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

#### Canonical References

- [Spec](../../../03.specs/08-ai/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md)

#### When to Use

- `ai-hardening` CI가 실패할 때
- Ollama/Open WebUI 경로 접근 정책이 비정상일 때
- Ollama GPU 과부하/OOM 또는 queue 적체가 반복될 때
- exporter metrics 수집이 실패할 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(middleware, concurrency, template, healthcheck, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(응답 지연, 인증 실패, GPU 사용률 급등) 평가

##### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/08-ai/ollama/docker-compose.yml config`
   - `docker compose -f infra/08-ai/open-webui/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
3. 증상별 복구
   - middleware 회귀:
     - Ollama/Open WebUI 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - Ollama 과부하/queue 적체:
     - `OLLAMA_NUM_PARALLEL`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_QUEUE` 보수값으로 복원
   - Open WebUI stateful drift:
     - `template-stateful-med` 재적용
   - exporter metrics 실패:
     - `depends_on` health gating 및 metrics healthcheck 계약 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 08-ai`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

#### Verification Steps

- [ ] AI compose static validation 통과
- [ ] AI hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `ai-hardening`, Ollama exporter metrics, Open WebUI health, gateway access logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/08-ai/ollama/docker-compose.yml`
  - `infra/08-ai/open-webui/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 08-ai`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: 승인된 운영 모델에서 직전 안정 모델로 fallback
- **Tool Disable / Revoke**: AI 자동 배포/승격 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-ai-hardening`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + exporter metrics + compose config

#### Related Operational Documents

- **Usage**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/08-ai/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
