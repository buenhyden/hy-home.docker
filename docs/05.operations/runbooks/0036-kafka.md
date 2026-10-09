---
title: "Kafka Runbook"
version: "1.3.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0036"
parent_ids:
- "GDE-0036"
created: "2026-05-17"
---

# Kafka Runbook

## Overview

이 런북은 Kafka family의 정적 진단, CDC connector 수명주기, 계획된 백업·복제 캡처, 격리 복원 절차를 다룬다. 정상 대상은 단일 broker이고, 다중 broker LAB은 별도 실행 계약을 따른다.

## Trigger and Preconditions

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리된 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

### Execution and stop boundary

정상 대상은 replication factor 1의 단일 broker `kafka-1`이며 broker 장애 내성이 없다: `debezium-db-provision`, `kafbat-ui`, `kafka-1`, `kafka-connect`, `kafka-exporter`, `kafka-init`, `kafka-rest-proxy`, `schema-registry`. 독립 LAB 대상: `lab-kafka-1/2/3`, `lab-kafka-exporter`, `lab-kafka-init`(실행 계약은 [Kafka LAB 안내](../../../labs/kafka-cluster.md)). 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster.yml --profile lab-kafka config --quiet
```

정상 서비스 8개와 LAB 서비스 5개의 분리, 별도 cluster ID·broker volume·network,
정상 `kafka_net`과 LAB `lab_kafka_net`, health check, Kafbat native OIDC
secret/config, PLAINTEXT 경계를 확인한다. 정상 `kafka-init`은 RF1이며
LAB `lab-kafka-init`은 세 broker에 RF3이다. 정적 render는 실제 준비 상태를
증명하지 않는다.

### CDC connector lifecycle

1. 전제조건: `dev-platform-provision`과 `debezium-db-provision`이 각각 `0`으로 종료되고, `dev-pg/platform_dev`의 `wal_level=logical`, 권한·publication·heartbeat 범위를 별도 검증한다. Connect의 secret provider와 PostgreSQL plugin 준비 상태도 확인한다.
2. 새 connector JSON은 `dev-pg/platform_dev`, `hyhome_platform_publication`, `hyhome_platform_slot`, topic prefix `hyhome.platform`을 선언한다. 기존 `mng-pg/app_db`의 slot·publication·topic·offset을 재사용하지 않는다. 등록과 snapshot은 승인된 runtime 변경이며 현재 NOT_RUN이다.
3. 승인된 등록 이후 `GET /connectors/<approved-name>/status`에서 connector/task `RUNNING`, snapshot 완료, 승인된 테스트 변경의 `hyhome.platform.*` topic 도착을 각각 확인한다. JSON 파일 존재나 등록 성공만으로 CDC PASS라고 기록하지 않는다.
4. `dev-pg`의 `pg_replication_slots`에서 `hyhome_platform_slot`의 `active`, `wal_status`, `confirmed_flush_lsn` 지연과 WAL 디스크 여유를 확인한다. `wal_status=lost`이면 snapshot/offset 복구 계획 없이 slot만 재생성하지 않는다.
5. maintenance pause 중에도 slot이 WAL을 유지한다. 재동기화에는 downstream 경계, 새 snapshot, 중복 처리와 rollback을 함께 승인받는다. secret rotation도 별도 승인과 소비자 재시작 검증이 필요하다.
6. 격리 시험은 `HYHOME_CDC_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.CdcStreamRehearsalTests`로 한다. 내부 network에 합성 데이터만 쓰는 dev-pg·Kafka·Schema Registry·Connect를 띄우고 다음을 확인한다. 추적 중인 provisioning SQL과 connector JSON이 그대로 동작하는지, Properties 특수문자와 비ASCII가 든 비밀번호로 인증하는지, snapshot과 stream 행이 Avro로 decode되는지, 열 추가가 schema version 2가 되는지, worker 재시작 뒤 중복 snapshot 없이 offset에서 이어지는지, heartbeat가 행을 쓰고 slot을 전진시키는지. topic은 partition 3개라 순서는 key 단위로만 보장된다. 2026-10-08에 통과했다(약 260초).

### Planned backup or replication capture

1. producer, consumer, schema, connector, retention, 수용 가능한 recovery
   point를 식별한다. topic, schema, connector에 대한 변경을 일시 중지하거나
   fence한다.
2. cluster ID, broker/storage format, topic configuration, partition 개수,
   high-water mark, consumer-group offset의 manifest를 export한다.
3. 승인된 메커니즘을 사용해 사용자 topic record를 별도의 호환 Kafka
   target으로 복제/재생한다. partition별 source와 target의 end offset을
   검증하고, 데이터 format이 지원하는 경우 개수/checksum을 기록한다.
4. serialized 데이터가 요구하는 schema subject, version, ID를 보존하는 공식
   호환 절차로 Schema Registry 이력을 마이그레이션한다.
5. secret 없이 Connect connector 정의를 export하고 호환되는 지원 방법으로
   config/offset/status 상태를 보존한다. 각 외부 시스템을 어떻게 조정할지
   기록한다.
6. manifest와 export된 데이터를 별도의 암호화된 destination에서 보호한다.
   active broker log 디렉터리나 KRaft metadata를 부분적으로 복사하지 않는다.

### Planned isolated restore

1. 호환 버전에서 새 cluster identity를 가진 network-isolated Kafka target을
   준비한다. 외부 producer, consumer, connector는 차단된 상태로 유지한다.
2. topic configuration과 partition 개수를 재생성한다. 여기 의존하는 record를
   로드하기 전에 schema/ID를 복원한다.
3. topic record를 재생/복제하고 모든 partition의 예상 end offset, 샘플
   key/value/checksum, retention 동작을 검증한다.
4. consumer offset을 복원하거나 의도적으로 재배치하며, replay나 건너뛴
   범위를 문서화한다. 보호된 custody에서 가져온 credential로 connector
   정의를 재생성한다. offset/status 상태를 검증하는 동안 connector는 일시
   중지 상태로 유지한다.
5. disposable producer/consumer schema-호환 테스트를 실행한다. connector는
   격리된 test endpoint에 대해서만 재개하고 idempotency/reconciliation을
   검증한다.
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

## Verification

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback and Escalation

### Rollback or Recovery

cutover가 실패하면 offset/write-boundary 검증 이후 producer와 consumer를
보존된 source cluster로 되돌리며, replay source와 target은 계속 보존된다.
cutover는 owner 승인, 최종 consistency capture, 애플리케이션 검증, 보존된
rollback window 이후에만 실행한다.

### Escalation

schema-ID drift, partition 누락, offset gap, checksum mismatch, connector
부작용, 호환되지 않는 storage/protocol format이 나타나거나 raw broker 디렉터리를
수리하라는 압박이 있으면 중단한다. 이 문서 task에서 백업이나 restore는 실행되지
않았다.

## Related Documents

- [Domain catalog](../README.md)
- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Policy](../policies/0036-kafka.md)

### Traceability

- Runtime source: [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
  및 [Connect image Dockerfile](../../../infra/05-messaging/kafka/Dockerfile.connect).
- Artifact: `RUN-0036`; parent guide: `GDE-0036`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.
