---
title: "05-Messaging Optimization Hardening Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0037"
parent_ids:
- "GDE-0037"
created: "2026-05-17"
---

# 05-Messaging Optimization Hardening Runbook

## When to Use

현재 Kafka hardening baseline에 대한 승인된 정적 진단에 사용한다. runtime
변경, restore, 정리, credential rotation은 별도 task가 필요하다.

## Procedure

1. 저장소 루트에서 현재 selector를 렌더링한다.

   ```bash
   docker compose --env-file .env.example --profile messaging config --quiet
   docker compose --env-file .env.example --profile messaging-cluster config --quiet
   bash scripts/hardening/check-all-hardening.sh 05-messaging
   ```

2. root로 렌더링한 서비스, profile, 네트워크, secret 참조, volume, health
   check, 리소스 제한을 검사한다. private 치환 값은 출력하지 않는다.
3. broker listener protocol이 명시적으로 계속 문서화되는지, Kafbat가 native
   OIDC template와 secret을 사용하는지, 모든 Kafbat route가
   `gateway-standard-chain@file`만 사용하는지 확인한다.
4. replication factor 3의 topic initialization이 three-broker-capable
   계획으로 제한되는지 확인한다.
5. 정확한 diff와 운영 문서를 검토한다. 컨테이너를 시작하지 않고 명령, 종료
   상태, 미해결 gap을 기록한다.

## Rollback or Recovery

정적 실패라면 이를 소유한 leaf source나 shared template을 식별하고 승인된
범위만 수정한다. 동일한 selector를 다시 렌더링한다. 실패한 secret, health,
resource, network, persistence 제어를 삭제해서 우회하지 않는다.

runtime incident라면 record나 credential 없이 broker/UI 로그를 보존하고
mutation을 중단한 뒤 [RUN-0036](0036-kafka.md)을 사용한다. raw log-directory
수리, offset 이동, schema 삭제, connector 재개, cluster identity 변경은
승인된 recovery task가 필요하다.

## Evidence

통과란 root configuration이 parse되고 현재 profile이 resolve되고 scoped
hardening script가 통과하고 native OIDC와 standard gateway routing이
일치하고 recovery ownership이 명시되었다는 뜻이다. runtime, 성능, OIDC 로그인,
failover, restore는 입증하지 않는다.

## Escalation

source/profile, persistence, secret, OIDC, listener-security, 또는 recovery
ownership drift에서 중단하고 messaging owner에게 escalation한다.

## Traceability

- Artifact: `RUN-0037`; parent guide: `GDE-0037`.
- 정적 evidence는 runtime이나 restore를 입증하지 않는다.

### References

- [Kafka runbook](0036-kafka.md)
- [Hardening policy](../policies/0037-messaging-optimization-hardening.md)

## Related Documents

- [Kafka runbook](0036-kafka.md)
- [Hardening policy](../policies/0037-messaging-optimization-hardening.md)
