# 09-Tooling Optimization Hardening Runbook

## Overview (KR)

이 런북은 `09-tooling` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. 공개 경계 정책 누락, 네트워크 경계 드리프트, locust/k6 런타임 계약 실패, CI 게이트 실패를 중심으로 점검/복구한다.

## Purpose

- tooling 공개 경로 보안과 운영 안정성 기준을 빠르게 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## Canonical References

- [Spec](../../04.specs/09-tooling/spec.md)
- [Operations Policy](../../08.operations/09-tooling/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)

## When to Use

- `tooling-hardening` CI가 실패할 때
- SonarQube/Terrakube/Syncthing 접근 정책이 비정상일 때
- locust worker 실행 불안정/재시작 루프가 발생할 때
- k6 테스트 런타임 데이터 경로 이상이 발생할 때

## Procedure or Checklist

### Checklist

- [ ] 실패 항목(middleware, network, healthcheck, volume, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(품질게이트, IaC 실행, 테스트 신뢰도) 평가

### Procedure

1. 정적 구성 점검
   - `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
2. 하드닝 기준 점검
   - `bash scripts/check-tooling-hardening.sh`
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
   - `bash scripts/check-tooling-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

## Verification Steps

- [ ] tooling compose static validation 통과
- [ ] tooling hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

## Observability and Evidence Sources

- **Signals**: CI `tooling-hardening`, service health, ingress access logs, tool execution logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/09-tooling/*/docker-compose.yml`
  - `scripts/check-tooling-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: tooling 자동 변경 파이프라인 일시 중지(승인 필요)
- **Eval Re-run**:
  - `check-tooling-hardening`
  - `check-template-security-baseline`
  - `check-doc-traceability`
- **Trace Capture**: CI logs + compose config + service health 상태

## Related Operational Documents

- **Guide**: [../../07.guides/09-tooling/optimization-hardening.md](../../07.guides/09-tooling/optimization-hardening.md)
- **Operation**: [../../08.operations/09-tooling/optimization-hardening.md](../../08.operations/09-tooling/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
