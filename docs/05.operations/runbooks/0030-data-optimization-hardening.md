---
title: "04-Data Optimization Hardening Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0030"
parent_ids:
- "GDE-0030"
created: "2026-05-17"
---

# 04-Data Optimization Hardening Runbook

## When to Use

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

## Procedure

1. 영향받은 서비스와 소유 Compose 파일 및 M0021 disposition으로부터 현재 root
   profile을 식별한다.
2. 저장소 루트에서 관련 명령을 실행한다.

   ```bash
   docker compose --env-file .env.example --profile mng config --quiet
   docker compose --env-file .env.example --profile valkey-cluster config --quiet
   docker compose --env-file .env.example --profile seaweedfs config --quiet
   docker compose --env-file .env.example --profile storage config --quiet
   bash scripts/hardening/check-all-hardening.sh 04-data
   ```

3. 서비스, profile, 네트워크, secret 참조, volume, health check, 리소스 제한,
   port publication을 검사한다. 완전히 치환된 configuration을 지속 evidence에
   남기지 않는다.
4. 소유 policy/runbook이 백업 범위, 별도 destination, isolation, 검증, rollback을
   명시하는지 확인한다. 미검증 runtime 속성을 기록한다.
5. 정확한 diff를 검토한다. 소유 source만 수정하고 동일한 확인을 반복한다.

### Regression response

parse 실패는 이를 소유한 root include, leaf source 또는 shared template에서
수정한다. 누락된 secret은 secret-management 절차를 통해 복원하며 inline
plaintext로 대체하지 않는다. state-path 충돌이 있으면 ownership이 입증될
때까지 변경을 중단한다.

실제 데이터 손실이나 손상이 발생하면 쓰기를 중단하고 엔진별 runbook을 사용한다.
management PostgreSQL/Valkey [RUN-0028](0028-management-database.md),
Valkey Cluster [RUN-0022](0022-valkey-cluster.md), 또는 SeaweedFS
[RUN-0024](0024-seaweedfs.md). 이 범용 runbook은 restore shortcut을 제공하지
않는다.

## Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback or Recovery

rollback은 client를 이전에 유효했던 source configuration과 엔진별 runbook으로
되돌린다. cutover는 owner 승인, 최종 consistency capture, 애플리케이션 검증,
보존된 rollback window 이후에만 실행한다.

## Escalation

범위, identity, checksum, 보안, 호환성, 또는 ownership drift에서 중단하고
안전한 evidence를 보존한 뒤 서비스/데이터 owner에게 escalation한다.

## Verification Record

### Acceptance

정적 acceptance는 root configuration parse 성공, scoped hardening 성공,
정확한 classification/profile 문서화, 명시적인 recovery owner를 요구한다.
날짜가 기록된 scoped evidence package가 달리 명시하지 않는 한 runtime 상태,
암호화, 용량, restore는 입증되지 않은 상태로 남는다.

## Traceability

- Artifact: `RUN-0030`; parent guide: `GDE-0030`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

## Related Documents

- [Policy](../policies/0030-data-optimization-hardening.md)
- [Guide](../guides/0030-data-optimization-hardening.md)
