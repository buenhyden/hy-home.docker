# 09-Tooling Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `09-tooling` 계층의 최적화/하드닝 운영 정책을 정의한다. 관리 경로 보안, 네트워크 경계, 테스트 도구 안정성, 카탈로그 확장 승인 게이트를 통제한다.

## Policy Scope

- `infra/09-tooling/*/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 09-tooling`

## Applies To

- **Systems**: terraform, terrakube, registry, sonarqube, k6, locust, syncthing
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - SonarQube/Terrakube/Syncthing 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - tooling compose는 `infra_net` external 경계 선언을 유지한다.
  - locust-worker healthcheck를 유지한다.
  - k6 volume 계약(`k6-data:/mnt/locust:rw`)을 유지한다.
  - tooling 변경은 `check-tooling-hardening.sh` 및 CI `tooling-hardening`을 통과해야 한다.
  - optimization-hardening 문서(PRD~Procedure) 링크를 유지해야 한다.
- **Allowed**:
  - 카탈로그 확장 항목을 단계적으로 도입하는 설계/운영 작업
  - 성능/품질/보안 기준의 보수적 강화
- **Disallowed**:
  - 무승인 SSO/middleware 완화
  - 검증 게이트 우회 배포
  - 감사/보존 정책 없이 확장 항목 운영 전환

## Exceptions

- 장애 대응 시 일시 완화는 승인 기록과 종료 조건이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

## Verification

- `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

## Review Cadence

- 월 1회 정기 검토
- tooling 구성/권한/정책 변경 시 수시 검토

## Catalog Expansion Approval Gates

- **terraform 승인 조건**:
  - plan/apply 승인 게이트 문서화
  - state 잠금/백업 정책 및 drift 자동 탐지 절차 정의
- **terrakube 승인 조건**:
  - workspace 분리 전략 문서화
  - 실행 권한 모델/RBAC 및 감사로그 연계 정의
- **registry 승인 조건**:
  - cosign 서명/검증 정책 정의
  - 취약점 스캔 실패 차단 정책 및 예외 절차 정의
- **sonarqube 승인 조건**:
  - 품질게이트 임계값 재정의
  - 브랜치 정책과 보안 룰셋 분리 운영
- **k6/locust 승인 조건**:
  - 회귀 baseline 저장/비교 및 시나리오 태그 표준화
  - 분산 실행 토폴로지와 데이터 초기화/정리 루틴 문서화
- **syncthing 승인 조건**:
  - 폴더 ACL/암호화 정책 및 충돌 처리 표준화

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: tooling hardening + 공통 기준선 통과 필수
- **Log / Trace Retention**: 도구별 감사/실행 로그 보존 정책 준수
- **Safety Incident Thresholds**: 인증 우회 의심/품질게이트 우회/테스트 오염 탐지 시 즉시 runbook 전환

## Related Documents

- **PRD**: [../../01.requirements/2026-03-28-09-tooling-optimization-hardening.md](../../../01.requirements/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md](../../../02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/09-tooling/spec.md](../../../03.specs/09-tooling/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/05.operations/09-tooling/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 09-Tooling Optimization Hardening Usage

#### Overview (KR)

이 문서는 `09-tooling` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Platform Product Owner

#### Purpose

- SonarQube/Terrakube/Syncthing 경로를 gateway+SSO 정책에 정렬한다.
- tooling compose 네트워크 경계를 일관화한다.
- locust/k6 테스트 런타임 계약을 안정화한다.
- tooling 하드닝 회귀를 script/CI로 조기 차단한다.
- 카탈로그 확장 항목을 운영 실행 가능한 로드맵으로 반영한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/09-tooling` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

#### Step-by-step Instructions

1. 정적 구성 점검
   - `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. Gateway/SSO 경계 정렬
   - SonarQube/Terrakube/Syncthing 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 네트워크 경계 표준화
   - tooling compose에 `infra_net` external 선언을 명시한다.
4. 테스트 런타임 안정화
   - locust-worker healthcheck를 확인한다.
   - k6 volume 참조가 `k6-data:/mnt/locust:rw`로 정렬되었는지 확인한다.
5. 기준선 검증 실행
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - 도구별 확장 항목(terraform/terrakube/registry/sonarqube/k6/locust/syncthing)을 tasks/operations에 반영한다.

#### Common Pitfalls

- 공개 라우터에 SSO 체인을 누락하는 실수
- compose별 네트워크 선언 편차를 방치하는 실수
- locust worker health 상태를 확인하지 않는 실수
- k6/locust 구성 드리프트를 문서 없이 방치하는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-09-tooling-optimization-hardening.md](../../../01.requirements/2026-03-28-09-tooling-optimization-hardening.md)
- **Spec**: [../../03.specs/09-tooling/spec.md](../../../03.specs/09-tooling/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 09-Tooling Optimization Hardening Procedure

#### Overview (KR)

이 런북은 `09-tooling` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. 공개 경계 정책 누락, 네트워크 경계 드리프트, locust/k6 런타임 계약 실패, CI 게이트 실패를 중심으로 점검/복구한다.

#### Purpose

- tooling 공개 경로 보안과 운영 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

#### Canonical References

- [Spec](../../../03.specs/09-tooling/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)

#### When to Use

- `tooling-hardening` CI가 실패할 때
- SonarQube/Terrakube/Syncthing 접근 정책이 비정상일 때
- locust worker 실행 불안정/재시작 루프가 발생할 때
- k6 테스트 런타임 데이터 경로 이상이 발생할 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(middleware, network, healthcheck, volume, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(품질게이트, IaC 실행, 테스트 신뢰도) 평가

##### Procedure

1. 정적 구성 점검
   - `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. 하드닝 기준 점검
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
3. 증상별 복구
   - middleware 회귀:
     - SonarQube/Terrakube/Syncthing 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - 네트워크 드리프트:
     - compose에 `infra_net` external 선언 복원
   - locust worker 불안정:
     - worker healthcheck/command 계약 복원
   - k6 경로 드리프트:
     - `k6-data:/mnt/locust:rw` volume 계약 복원
4. 재검증
   - `bash scripts/hardening/check-all-hardening.sh 09-tooling`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

#### Verification Steps

- [ ] tooling compose static validation 통과
- [ ] tooling hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `tooling-hardening`, service health, ingress access logs, tool execution logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/09-tooling/*/docker-compose.yml`
  - `scripts/hardening/check-all-hardening.sh 09-tooling`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: tooling 자동 변경 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-tooling-hardening`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + compose config + service health 상태

#### Related Operational Documents

- **Usage**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/09-tooling/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
