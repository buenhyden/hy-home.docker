---
title: "Performance Testing Incident Runbook"
version: "1.2.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0064"
parent_ids:
- "GDE-0064"
created: "2026-05-17"
---

# 성능 시험 중단·복구 런북

## Overview

공유 서비스에 영향을 주는 k6·Locust LAB 부하 시험을 중단하고 진단하는 공통 절차다.
부하를 먼저 멈추고, root `k6` 작업 또는 독립 Locust LAB의 정확한 프로젝트를 확인한 뒤
대상 회복과 증거 완전성을 판정한다.

## Trigger and Preconditions

성능 테스트 실행 중 target service 또는 shared gateway/auth/data tier에 영향이 생겼을 때 사용한다.

- 테스트 중 target SLI가 승인된 한계 아래로 떨어진다.
- Gateway/Auth/Data tier가 부하 테스트 영향으로 degraded 상태가 된다.
- 결과 원본·checksum·summary·exit metadata가 누락되거나 바뀌어 판정 신뢰도가 떨어진다.
- 실행 주체가 root `k6`인지 별도 Locust LAB인지 불명확하다.

## Procedure

- [ ] 테스트 owner, target service owner, platform operator에게 중단 결정을 알린다.
- [ ] 실행 중인 leaf와 service name을 확인한다.
- [ ] 승인된 run_id·attempt·project_id, target origin, 사용자/요청률·시간 상한, 시나리오 hash와 시작 시각을 기록한다.
- [ ] Docker context, root 또는 LAB 프로젝트, 포트·네트워크·볼륨·자원과 정확한 중단·정리 범위를 확인한다.

### Steps

1. 실행 중인 performance service를 확인한다.

   ```bash
   docker compose --profile testing ps k6
   ```

2. Locust LAB가 선택된 경우 승인된 고유 프로젝트명과 `labs/.env`를
   사용해 `labs/locust.yml`의 master/worker 상태를 따로 확인하고
   [Locust 런북](0062-locust.md)의 중단 절차를 따른다. root의 `testing`
   프로필은 Locust를 포함하지 않는다.

3. k6 작업이면 [k6 런북](0061-k6.md)의 중단 절차를 따른다.
   WireMock 기능·부하 모드의 동시 기동 여부와 mock 포화도도 확인한다.

4. 대상 서비스 런북의 SLI·오류율·지연·포화도와 공유 계층의 상태로 회복을 확인한다.
   다음 정적 검사는 문서·설정 회귀만 검증하며 대상 회복을 증명하지 않는다.

   ```bash
   bash scripts/hardening/check-all-hardening.sh 11-quality
   python3 scripts/validation/run-ci-gate.py --profile changed --explain
   ```

5. 대상 SLI, 오류율, 지연, 영향 시간과 발생기 포화·dropped iteration·
   수집기 drop을 분리해 기록한다. 원본/summary/exit metadata의 checksum을
   확인하고 증거가 불완전하면 시험 판정을 통과로 확정하지 않는다.
   `perf_db` 적재 실패는 원본을 보존하고 동일 checksum 재적재만 시도한다;
   같은 run_id/attempt의 다른 파일은 충돌로 격리한다.

## Verification

- 명령 결과, 시각, 서비스명, 테스트 매개변수, 대상 SLI 요약과 최종 회복 상태를 기록한다.
- Locust 또는 k6 중 어떤 절차를 사용했는지 기록한다.

### Verification Steps

`--explain`은 실행하지 않는 계획 조회다. 후보 aggregate QA는
[quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix)의
원격 PR 경로가 소유하며 조회 결과를 검증 PASS로 기록하지 않는다.

- 실행 중이던 부하 생성 서비스가 중지되었다. UI의 idle 표시만으로 중단 완료를 판정하지 않는다.
- target SLI와 shared tier health가 정상 범위로 회복됐다.
- 관련 guide/policy/runbook이 root k6와 독립 Locust LAB의 서비스명·경계를 유지한다.
- 실행 상태, 시험 판정, 증거 완전성, 적재 상태가 서로 구분돼 있다.

### Observability and Evidence Sources

- **Logs**: 부하 생성기·대상·공유 gateway/auth/data 계층의 정제된 로그
- **Metrics**: 대상 SLI, 요청 오류율, 응답 지연과 Locust 요청 통계
- **Evidence to Capture**: 서비스명, 테스트 매개변수, 중단·회복 시각과 실패 검사

## Rollback and Escalation

### Rollback or Recovery

부하 생성기별 중단 절차와 대상별 복구 런북을 사용한다. 중단 후에도 원본 파일과
격리 결과 디렉터리를 보존하고 승인된 checksum과 대상 프로젝트만 재적재한다.
이 문서는 대상 서비스를 재시작하거나 결과 볼륨을 삭제하는 승인이 아니다.

1. load generator를 중단한 상태로 유지한다.
2. target service recovery는 해당 target의 runbook으로 전환한다.
3. 재실행은 target owner 승인과 conservative ramp-up plan이 있을 때만 수행한다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

부하 중지 후에도 대상이 회복되지 않거나 루트 Compose 문맥이 깨지거나 비밀 노출이 의심되면 플랫폼 책임자와 대상 소유자에게 보고한다.

## Related Documents

### Traceability

- 상위 문서: [Performance Testing Usage Guide](../guides/0064-performance-testing.md) (`GDE-0064`)
- 설계 근거: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0064-performance-testing.md) (`GDE-0064`), [Policy](../policies/0064-performance-testing.md) (`POL-0064`)

- [Operations index](../README.md)
- [Usage guide](../guides/0064-performance-testing.md)
- [Operations policy](../policies/0064-performance-testing.md)
- [Locust runbook](0062-locust.md)
- [k6 runbook](0061-k6.md)
