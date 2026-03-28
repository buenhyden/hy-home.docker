# 11-Laboratory Optimization Hardening Runbook

## Overview (KR)

이 런북은 `11-laboratory` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. direct 노출 복원, allowlist/SSO/gateway 체인 누락, 네트워크 경계 드리프트, CI 게이트 실패를 중심으로 점검/복구한다.

## Purpose

- Laboratory 관리 UI 보안 경계와 운영 안정성 기준을 신속히 복구한다.
- compose/script/CI 회귀를 표준 절차로 차단한다.

## Canonical References

- [Spec](../../04.specs/11-laboratory/spec.md)
- [Operations Policy](../../08.operations/11-laboratory/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)

## When to Use

- `laboratory-hardening` CI가 실패할 때
- dashboard/dozzle/portainer/redisinsight 접근 경계가 비정상일 때
- dashboard direct 접근 경로가 재노출되었을 때
- dozzle socket 권한 드리프트가 발생했을 때

## Procedure or Checklist

### Checklist

- [ ] 실패 항목(middleware, allowlist, network, direct exposure, socket 권한, script, docs) 식별
- [ ] 최근 변경 커밋 및 영향 범위 확인
- [ ] 운영 영향도(관리 UI 접근/보안/감사) 평가

### Procedure

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

## Verification Steps

- [ ] Laboratory compose static validation 통과
- [ ] laboratory hardening script 실패 0건
- [ ] optimization-hardening 문서 링크/README 인덱스 최신화 확인

## Observability and Evidence Sources

- **Signals**: CI `laboratory-hardening`, ingress access logs, service logs
- **Evidence to Capture**:
  - 변경 전후 hardening check 결과
  - compose config 결과
  - 관련 compose/script/docs diff

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example`
  - `scripts/check-laboratory-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 정책/가이드/태스크 문서 링크 재확인

## Related Operational Documents

- **Guide**: [../../07.guides/11-laboratory/optimization-hardening.md](../../07.guides/11-laboratory/optimization-hardening.md)
- **Operation**: [../../08.operations/11-laboratory/optimization-hardening.md](../../08.operations/11-laboratory/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
