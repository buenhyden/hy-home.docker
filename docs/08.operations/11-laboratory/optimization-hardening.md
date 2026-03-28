# 11-Laboratory Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `11-laboratory` 계층 최적화/하드닝 운영 정책을 정의한다. 관리 UI 보안 경계, 실험성 서비스 운영 통제, 카탈로그 확장 승인 게이트를 명문화한다.

## Policy Scope

- `infra/11-laboratory/*/docker-compose.yml`
- `.env.example` (`LAB_ALLOWED_CIDRS`)
- `scripts/check-laboratory-hardening.sh`

## Applies To

- **Systems**: dashboard, dozzle, portainer, redisinsight
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like management plane

## Controls

- **Required**:
  - 모든 Laboratory 라우터는 `gateway-standard-chain@file` + service별 IP allowlist + `sso-errors@file,sso-auth@file`를 적용한다.
  - 모든 compose는 `infra_net` external 경계를 유지한다.
  - dashboard direct host `ports` 노출을 금지한다.
  - dozzle docker socket은 read-only로 유지한다.
  - laboratory 변경은 `check-laboratory-hardening.sh` 및 CI `laboratory-hardening` 통과가 필수다.
  - optimization-hardening 문서(PRD~Runbook)와 README 인덱스를 동기화한다.
- **Allowed**:
  - 카탈로그 확장 항목을 단계적으로 도입하는 정책/절차/문서 작업
- **Disallowed**:
  - 무승인 allowlist 완화
  - 인증 우회 direct 노출 복원
  - 감사 기준 없이 운영 캐시 직접 수정

## Exceptions

- 장애 대응 시 일시 완화는 승인 기록과 종료 조건이 필수다.
- 예외 종료 후 동일 릴리스 내 기준선 복구 및 재검증을 수행한다.

## Verification

- `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
- `bash scripts/check-laboratory-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

## Review Cadence

- 월 1회 정기 검토
- allowlist/권한/노출 정책 변경 시 수시 검토

## Catalog Expansion Approval Gates

- **dashboard 승인 조건**:
  - 실험성 dashboard 접근 만료 정책(자동 종료 기준) 문서화
  - 운영 예외 허용 시간/범위 명시
- **dozzle 승인 조건**:
  - 로그 열람 범위 제한 규칙(프로덕션 로그 차단 포함) 문서화
  - 로그 접근 감시/감사 방식 정의
- **portainer 승인 조건**:
  - 관리자 계정/세션 정책 강화 기준 문서화
  - 엔드포인트 등록 승인 절차(권한 분리) 명문화
- **redisinsight 승인 조건**:
  - 최소권한 접근정책 문서화
  - 운영 캐시 직접 수정 금지 + 감사로그 절차 정의

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/11-laboratory/optimization-hardening.md](../../07.guides/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/11-laboratory/optimization-hardening.md](../../09.runbooks/11-laboratory/optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
