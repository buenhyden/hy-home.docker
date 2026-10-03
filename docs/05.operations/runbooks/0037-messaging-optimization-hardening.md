---
title: "05-Messaging Optimization Hardening Runbook"
version: "1.1.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
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

### Execution and stop boundary

HOME 대상: `debezium-db-provision`, `kafbat-ui`, `kafka-1`, `kafka-connect`, `kafka-exporter`, `kafka-init`, `kafka-rest-proxy`, `schema-registry`. LAB 대상은 별도 `labs/kafka-cluster.yml`의 `lab-kafka-1/2/3`, exporter, init이다. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

1. 저장소 루트에서 현재 selector를 렌더링한다.

   ```bash
   docker compose --env-file .env.example --profile messaging config --quiet
   LAB_DATA_DIR=/tmp/hy-home-lab-kafka-static LAB_KAFKA_CLUSTER_ID=static-contract-id docker compose --env-file labs/.env.example -f labs/kafka-cluster.yml --profile lab-kafka config --quiet
   bash scripts/hardening/check-all-hardening.sh 05-messaging
   ```

2. root로 렌더링한 서비스, profile, 네트워크, secret 참조, volume, health
   check, 리소스 제한을 검사한다. private 치환 값은 출력하지 않는다.
3. broker listener protocol이 명시적으로 계속 문서화되는지, Kafbat가 native
   OIDC template와 secret을 사용하는지, 모든 Kafbat route가
   `gateway-standard-chain@file`만 사용하는지 확인한다.
4. HOME RF1와 별도 LAB RF3 topic initialization의 cluster ID·data directory·offset이
   서로 분리되는지 확인한다.
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
ownership drift에서 중단하고 messaging @buenhyden에게 escalation한다.

## Traceability

- Artifact: `RUN-0037`; parent guide: `GDE-0037`.
- 정적 evidence는 runtime이나 restore를 입증하지 않는다.

### References

- [Kafka runbook](0036-kafka.md)
- [Hardening policy](../policies/0037-messaging-optimization-hardening.md)

## Related Documents

- [Kafka runbook](0036-kafka.md)
- [Hardening policy](../policies/0037-messaging-optimization-hardening.md)
