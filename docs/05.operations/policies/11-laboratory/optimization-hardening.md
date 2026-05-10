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
  - optimization-hardening 문서(PRD~Procedure)와 README 인덱스를 동기화한다.
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

- **PRD**: [../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md](../../../02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/11-laboratory/spec.md](../../../03.specs/11-laboratory/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/11-laboratory/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 11-Laboratory Optimization Hardening Usage

#### Overview (KR)

이 문서는 `11-laboratory` 계층 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. 관리 UI 보안 경계, 네트워크 표준화, 최소권한 적용, 기준선 검증 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Platform SRE
- DevOps Engineer
- Security Reviewer

#### Purpose

- 관리 UI를 gateway+allowlist+SSO 경계로 정렬한다.
- dashboard direct host 노출을 제거하고 Traefik 경유 접근으로 통일한다.
- dozzle 최소권한(socket read-only)을 적용한다.
- laboratory 하드닝 회귀를 script/CI로 조기 차단한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/11-laboratory` 수정 권한
- Traefik middleware(`gateway-standard-chain`, `sso-errors`, `sso-auth`) 준비

#### Step-by-step Instructions

1. 정적 구성 점검
   - `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. Ingress 경계 정렬
   - 각 Laboratory 라우터에 `gateway-standard-chain + service-ipallowlist + sso-errors + sso-auth`를 적용한다.
3. 네트워크 경계 표준화
   - 모든 compose에 `infra_net` external 선언을 명시한다.
4. 최소권한 적용
   - dashboard `ports` 제거 후 `expose`만 사용한다.
   - dozzle docker socket을 `:ro`로 전환한다.
5. 기준선 검증 실행
   - `bash scripts/check-laboratory-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`
6. 카탈로그 확장 로드맵 반영
   - dashboard 만료 정책, dozzle 로그 제한, portainer 승인 정책, redisinsight 감사 정책을 tasks/operations에 반영한다.

#### Common Pitfalls

- allowlist CIDR 설정 누락으로 운영자 접근이 차단되는 실수
- dashboard direct 포트 노출을 되돌려 우회 경로를 만드는 실수
- dozzle socket 권한을 read-write로 유지하는 실수
- 문서 링크/README 인덱스 동기화를 누락하는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md](../../../01.requirements/2026-03-28-11-laboratory-optimization-hardening.md)
- **Spec**: [../../03.specs/11-laboratory/spec.md](../../../03.specs/11-laboratory/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/11-laboratory/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 11-Laboratory Optimization Hardening Procedure

#### Overview (KR)

이 런북은 `11-laboratory` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. direct 노출 복원, allowlist/SSO/gateway 체인 누락, 네트워크 경계 드리프트, CI 게이트 실패를 중심으로 점검/복구한다.

#### Purpose

- Laboratory 관리 UI 보안 경계와 운영 안정성 기준을 신속히 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

#### Canonical References

- [Spec](../../../03.specs/11-laboratory/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)

#### When to Use

- `laboratory-hardening` CI가 실패할 때
- dashboard/dozzle/portainer/redisinsight 접근 경계가 비정상일 때
- dashboard direct 접근 경로가 재노출되었을 때
- dozzle socket 권한 드리프트가 발생했을 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패 항목(middleware, allowlist, network, direct exposure, socket 권한, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(관리 UI 접근/보안/감사) 평가

##### Procedure

1. 정적 구성 점검
   - `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. 하드닝 기준 점검
   - `bash scripts/check-laboratory-hardening.sh`
3. 증상별 복구
   - middleware/allowlist 회귀:
     - 각 서비스 라우터 체인을 `gateway-standard-chain + <service>-admin-ip + sso-errors + sso-auth`로 복원
   - 네트워크 드리프트:
     - compose에 `infra_net` external 선언 복원
   - dashboard direct 노출:
     - `ports` 제거, `expose`만 유지
   - dozzle 권한 드리프트:
     - `/var/run/docker.sock` 마운트를 `:ro`로 복원
4. 재검증
   - `bash scripts/check-laboratory-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

#### Verification Steps

- [ ] Laboratory compose static validation 통과
- [ ] laboratory hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

#### Observability and Evidence Sources

- **Signals**: CI `laboratory-hardening`, ingress access logs, service logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example`
  - `scripts/check-laboratory-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

#### Related Operational Documents

- **Usage**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/11-laboratory/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
