---
title: "Kafka Runbook"
version: "1.4.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "operations"
artifact_id: "RUN-0036"
parent_ids:
- "GDE-0036"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Kafka Runbook

## Purpose

### Trigger and Outcome

이 런북은 HOME 단일 Kafka broker의 정적 진단과 계획된 백업·복제 캡처·격리 복원을 다룬다. 독립 LAB의 Schema Registry와 Connect는 LAB 런북을 따른다.

- Kafka family source나 profile 변경의 정적 진단이 필요할 때
- `KafkaBrokerDown`, `KafkaConsumersGroupLag`, `KafkaTopicUnderReplicatedPartition` 경보가 발생했을 때
- 승인된 백업·격리 복원을 계획할 때

### Scope

- HOME 선언은 [Kafka Compose](../../../../infra/05-messaging/kafka/docker-compose.yml)에 있다.
- LAB 진단과 HOME의 이전 Connect·Schema Registry 퇴역은 [RUN-0108](../15-labs/0108-kafka-cluster.md)을 따른다.
- Artifact: `RUN-0036`; parent guide: `GDE-0036`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

- [Domain catalog](../../README.md)
- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Policy](../../policies/06-messaging-and-cdc/0036-kafka.md)

## Preconditions

### Authority and Access

실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

### Safety Checks

백업·복제 캡처 전에 producer, consumer, schema, connector, retention, 수용 가능한 recovery point를 식별하고 변경을 일시 중지하거나 fence한다(`Planned backup or replication capture` 1단계). 운영 checkout의 repository root와 승인된 Docker context 확인은 Stop Conditions의 `Execution and stop boundary`에 있다.

## Steps

### Actions

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
```

`messaging`은 `kafka-1`, `kafbat-ui`, `kafka-exporter`, `kafka-init`을 선택한다.
`kafka_net`, health check, Kafbat native OIDC secret/config와 PLAINTEXT 경계를
확인한다. `kafka-init`의 토픽 복제 계수는 1이다. 정적 render는 실제 준비 상태를
증명하지 않는다. LAB의 일곱 서비스와 독립 project는 RUN-0108의 Static check를 따른다.

#### CDC source boundary

[ADR-0062의 Kafka CDC 개정](../../../02.architecture/decisions/0062-home-lab-membership.md#amendment-of-2026-11-10-kafka-cdc-kafka-connect-and-schema-registry)으로
HOME에서 `cdc` profile, `debezium-db-provision`, connector sample, 기능 SQL과 secret renderer를 제거했다.
LAB에는 Registry와 Connect가 있지만 connector, source DB, credential이 선언되어 있지 않다.
실제 CDC가 필요하면 별도 승인 범위에서 source·publication·slot·topic·offset·credential·rollback을
정의하고 등록, 연결, snapshot, stream, WAL 유지와 정리 경계를 검증한다. 예전 HOME 위치나 운영 slot을
그대로 재사용하지 않는다.

2026-10-08의 합성 CDC rehearsal은 이전 토폴로지의 snapshot·stream Avro decode,
schema version 변경, 재시작 후 offset 재개와 heartbeat를 약 260초에 검증했다(SPEC-0204-TSK-0005 W15).
해당 테스트와 입력은 현재 HOME에서 제거되었다. 이 기록은 현재 HOME 또는 LAB connector 준비 증거가 아니다.

#### Planned backup or replication capture

1. producer, consumer, schema, connector, retention, 수용 가능한 recovery
   point를 식별한다. topic, schema, connector에 대한 변경을 일시 중지하거나
   fence한다.
2. cluster ID, broker/storage format, topic configuration, partition 개수,
   high-water mark, consumer-group offset의 manifest를 export한다.
3. 승인된 메커니즘을 사용해 사용자 topic record를 별도의 호환 Kafka
   target으로 복제/재생한다. partition별 source와 target의 end offset을
   검증하고, 데이터 format이 지원하는 경우 개수/checksum을 기록한다.
4. schema 의존 데이터가 범위에 있으면 해당 Registry를 별도 식별한다. serialized 데이터가 요구하는
   schema subject, version, ID를 보존하는 공식
   호환 절차로 Schema Registry 이력을 마이그레이션한다.
5. connector가 승인 범위에 포함되면 secret 없이 Connect connector 정의를 export하고 호환되는 지원 방법으로
   config/offset/status 상태를 보존한다. 각 외부 시스템을 어떻게 조정할지
   기록한다.
6. manifest와 export된 데이터를 별도의 암호화된 destination에서 보호한다.
   active broker log 디렉터리나 KRaft metadata를 부분적으로 복사하지 않는다.

#### Planned isolated restore

1. 호환 버전에서 새 cluster identity를 가진 network-isolated Kafka target을
   준비한다. 외부 producer, consumer, connector는 차단된 상태로 유지한다.
2. topic configuration과 partition 개수를 재생성한다. schema에 의존하는 record는
   승인 범위의 schema/ID 복원 뒤에 로드한다.
3. topic record를 재생/복제하고 모든 partition의 예상 end offset, 샘플
   key/value/checksum, retention 동작을 검증한다.
4. consumer offset을 복원하거나 의도적으로 재배치하며, replay나 건너뛴
   범위를 문서화한다. connector 복원이 승인 범위에 있으면 보호된 custody에서 가져온
   credential로 정의를 재생성한다. offset/status 검증 중에는 connector를 중지한다.
5. disposable producer/consumer로 적용되는 schema 호환성을 확인한다. 범위에 포함된
   connector는 격리된 test endpoint에 대해서만 재개하고 idempotency/reconciliation을 검증한다.
6. 관측된 recovery point, 소요 시간, gap을 기록한다. 별도 cutover task가
   source 쓰기를 fence하고, 최종 delta를 캡처하고, client를 전환하고,
   rollback을 보존한다. live KRaft cluster ID를 재사용하지 않는다.

Rehearsal 2026-09-22 (1~3단계, owner 승인됨): `--internal` 네트워크의 live
버전에서 disposable single-node KRaft Kafka와 Schema Registry. 4개 subject
모두 `IMPORT` 모드에서 동일한 ID로 import되었다. CDC topic 하나(3개
partition, 563개 record)가 동일한 partition과 timestamp로 복사되었고 모든
key, value, header에 대한 SHA-256 digest가 일치했다. connector config
(비밀번호는 provider 참조로 대체)와 offset은 4단계용으로 캡처했다.
4~6단계는 실행하지 않았다. live database를 대상으로 한 Connect worker가 production
replication slot을 소비하게 되기 때문이다. rehearsal stack은 제거했다.

### Stop Conditions

중단 조건과 실행 경계는 아래 항목을 따른다.

#### Execution and stop boundary

HOME의 replication factor 1 토픽에는 broker 장애 내성이 없다. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../../guides/01-common/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../../policies/01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 재기동한다. 토픽을 생성하는 `kafka-init`은 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Validation

### Service Checks

복제 검증은 partition별 source와 target end offset이 일치하고 지원되는 format의 개수/checksum이 맞아야 하며, `Planned isolated restore`의 key/value/checksum·retention 검증을 통과해야 한다.

### Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

운영 checkout 증거에는 결과·시간·target·source revision·종료 코드만 요약하고 raw log, rendered Compose, payload, credential URI는 붙이지 않는다.

## Recovery

### Rollback

cutover가 실패하면 offset/write-boundary 검증 이후 producer와 consumer를
보존된 source cluster로 되돌리며, replay source와 target은 계속 보존된다.
cutover는 owner 승인, 최종 consistency capture, 애플리케이션 검증, 보존된
rollback window 이후에만 실행한다.

### Escalation

schema-ID drift, partition 누락, offset gap, checksum mismatch, connector
부작용, 호환되지 않는 storage/protocol format이 나타나거나 raw broker 디렉터리를
수리하라는 압박이 있으면 중단한다. 위 2026-09-22 rehearsal 외의 백업이나 restore는 실행된 증거가 없다.
