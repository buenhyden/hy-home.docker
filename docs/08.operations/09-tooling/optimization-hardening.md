# 09-Tooling Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `09-tooling` 계층의 최적화/하드닝 운영 정책을 정의한다. 관리 경로 보안, 네트워크 경계, 테스트 도구 안정성, 카탈로그 확장 승인 게이트를 통제한다.

## Policy Scope

- `infra/09-tooling/*/docker-compose.yml`
- `scripts/check-tooling-hardening.sh`

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
  - optimization-hardening 문서(PRD~Runbook) 링크를 유지해야 한다.
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
- `bash scripts/check-tooling-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

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

- **PRD**: [../../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../../02.ard/0024-tooling-optimization-hardening-architecture.md](../../02.ard/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md](../../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/09-tooling/spec.md](../../04.specs/09-tooling/spec.md)
- **Plan**: [../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/09-tooling/optimization-hardening.md](../../07.guides/09-tooling/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/09-tooling/optimization-hardening.md](../../09.runbooks/09-tooling/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
