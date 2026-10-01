---
title: "Performance Testing Incident Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0064"
parent_ids:
- "GDE-0064"
created: "2026-05-17"
---

# Performance Testing Incident Runbook

## Overview

> 범위: 공유 서비스에 영향을 주는 Locust/k6 성능 테스트의 중단과 진단.

이 런북은 성능 테스트 실행 중 target service 또는 shared gateway/auth/data tier에 영향이 발생했을 때 사용하는 공통 절차다.

### Purpose

테스트 부하를 우선 중단하고, 어떤 leaf(`locust` 또는 `k6`)가 실행 중인지 확인한 뒤, target 회복과 evidence capture를 완료한다.

## When to Use

- 테스트 중 target SLI가 승인된 한계 아래로 떨어진다.
- Gateway/Auth/Data tier가 부하 테스트 영향으로 degraded 상태가 된다.
- Locust 요청 통계가 누락되거나 일관되지 않아 테스트 결과 신뢰도가 떨어진다.
- 실행 leaf가 `locust`인지 `k6` wrapper인지 불명확하다.

## Procedure

### Checklist

- [ ] 테스트 owner, target service owner, platform operator에게 중단 결정을 알린다.
- [ ] 실행 중인 leaf와 service name을 확인한다.
- [ ] users, spawn rate, target, scenario file, 시작 시각을 기록한다.

### Steps

1. 실행 중인 performance service를 확인한다.

   ```bash
   docker compose --profile testing ps k6 locust-master locust-worker
   ```

2. Locust leaf가 실행 중이면 Locust runbook의 stop 절차를 따른다.

3. k6 wrapper leaf가 실행 중이면 k6 runbook의 stop 절차를 따른다.

4. 대상 서비스 런북의 SLI·오류율·지연·포화도와 공유 계층의 상태로 회복을 확인한다.
   다음 정적 검사는 문서·설정 회귀만 검증하며 대상 회복을 증명하지 않는다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 11-quality
   python3 scripts/validation/run-ci-gate.py --profile changed
   ```

5. target SLI, error rate, latency, affected time window를 evidence에 기록한다.

### Verification Steps

- 실행 중이던 부하 생성 서비스가 중지되었다. UI의 idle 표시만으로 중단 완료를 판정하지 않는다.
- target SLI와 shared tier health가 정상 범위로 회복됐다.
- 관련 guide/policy/runbook이 현재 service names와 root compose와 profile 선택 경계를 유지한다.

### Observability and Evidence Sources

- **Logs**: 부하 생성기·대상·공유 gateway/auth/data 계층의 정제된 로그
- **Metrics**: 대상 SLI, 요청 오류율, 응답 지연과 Locust 요청 통계
- **Evidence to Capture**: 서비스명, 테스트 매개변수, 중단·회복 시각과 실패 검사

### Safe Rollback or Recovery Procedure

1. load generator를 중단한 상태로 유지한다.
2. target service recovery는 해당 target의 runbook으로 전환한다.
3. 재실행은 target owner 승인과 conservative ramp-up plan이 있을 때만 수행한다.

## Evidence

- 명령 결과, 시각, 서비스명, 테스트 매개변수, 대상 SLI 요약과 최종 회복 상태를 기록한다.
- Locust 또는 k6 중 어떤 절차를 사용했는지 기록한다.

## Rollback or Recovery

부하 생성기별 중단 절차와 대상별 복구 런북을 사용한다. 이 문서는 대상 서비스를 재시작하는 검증된 절차를 제공하지 않는다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

부하 중지 후에도 대상이 회복되지 않거나 루트 Compose 문맥이 깨지거나 비밀 노출이 의심되면 플랫폼 책임자와 대상 소유자에게 보고한다.

## Traceability

- 상위 문서: [Performance Testing Usage Guide](../guides/0064-performance-testing.md) (`GDE-0064`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0064-performance-testing.md) (`GDE-0064`), [Policy](../policies/0064-performance-testing.md) (`POL-0064`)

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0064-performance-testing.md)
- [Operations policy](../policies/0064-performance-testing.md)
- [Locust runbook](0062-locust.md)
- [k6 runbook](0061-k6.md)
