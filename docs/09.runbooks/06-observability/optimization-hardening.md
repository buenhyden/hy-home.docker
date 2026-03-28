# 06-Observability Optimization Hardening Runbook

: Observability Gateway/Compose Baseline Recovery

## Overview (KR)

이 런북은 `06-observability` 하드닝 항목에서 발생할 수 있는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health 의존성 회귀, 커스텀 이미지 런타임 하드닝 누락, CI 기준선 실패를 중심으로 점검/복구한다.

## Purpose

- 관측성 관리 경로의 보안/가용성 기준을 신속히 복구한다.
- compose/CI 회귀를 조기에 차단하고 안정 상태로 복원한다.

## Canonical References

- [Spec](../../04.specs/06-observability/spec.md)
- [Operations Policy](../../08.operations/06-observability/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md)

## When to Use

- `observability-hardening` CI가 실패할 때
- 관측성 UI/API가 Traefik 경유로 비정상 응답할 때
- 스택 부팅 시 Alloy/Grafana 의존성 대기로 장애가 반복될 때
- Loki/Tempo custom image 런타임 실패가 발생할 때

## Procedure or Checklist

### Checklist

- [ ] 실패 항목(middleware/depends_on/healthcheck/image/script/doc) 식별
- [ ] 최근 변경 커밋과 영향 범위 확인
- [ ] 운영 영향도(수집/조회/알림 경로) 평가

### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/06-observability/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/check-observability-hardening.sh`
3. 증상별 복구
   - middleware 누락:
     - 대상 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 재적용
   - 의존성 race:
     - Alloy/Grafana의 Loki/Tempo `depends_on`을 `service_healthy`로 복원
   - 호스트 수집기 신호 불량:
     - cAdvisor `/healthz` healthcheck 복원
   - custom image 회귀:
     - Loki/Tempo Dockerfile `USER 10001:10001` 복원
     - entrypoint secret guard 복원
4. 재검증
   - `bash scripts/check-observability-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

## Verification Steps

- [ ] observability compose `config` 검증 통과
- [ ] `check-observability-hardening` 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

## Observability and Evidence Sources

- **Signals**: CI `observability-hardening` 상태, Traefik 라우터 상태, container health
- **Evidence to Capture**:
  - 변경 전후 `check-observability-hardening.sh` 출력
  - compose `config` 결과
  - 관련 compose/Dockerfile/docs diff

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/06-observability/docker-compose.yml`
  - `infra/06-observability/loki/{Dockerfile,docker-entrypoint.sh}`
  - `infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-observability-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 링크 재확인

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: 관측성 자동화 변경 작업 일시 중지(승인 필요)
- **Eval Re-run**: `check-observability-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output + health 상태

## Related Operational Documents

- **Guide**: [../../07.guides/06-observability/optimization-hardening.md](../../07.guides/06-observability/optimization-hardening.md)
- **Operation**: [../../08.operations/06-observability/optimization-hardening.md](../../08.operations/06-observability/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
