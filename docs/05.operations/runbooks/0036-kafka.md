---
title: "Kafka Cluster Runbook"
version: "1.2.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0036"
parent_ids:
- "GDE-0036"
created: "2026-05-17"
---

# Kafka Cluster Runbook

## When to Use

승인된 정적 진단, 백업 계획 또는 정확히 이 주제에 해당하는 격리된 복구에 사용한다.
실 쓰기, 복원, cutover, 정리, credential 변경은 별도 승인된 task가 필요하다.

## Procedure

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile messaging config --quiet
docker compose --env-file .env.example --profile messaging config --services
docker compose --env-file .env.example --profile messaging-cluster config --quiet
```

10개 예상 서비스, 별도의 broker/Connect volume, `kafka_net`, health check,
Kafbat native OIDC secret/config, 표준 gateway chain, PLAINTEXT listener를
확인한다. runtime을 사용하기 전에는 항상 `kafka-init`의 replication factor 3이
three-broker selector와 짝을 이루는지 확인한다.

### CDC connector lifecycle

1. 전제조건: `debezium-db-provision`이 `0`으로 종료됨; `mng-pg`가
   `SHOW wal_level` = `logical`을 보고함; Connect 로그에
   `debezium.properties rendered`가 남음; `GET /connector-plugins`에 plugin
   class가 나열됨.
2. 등록은 승인된 runtime 변경이다. `kafka_net`에 있는 컨테이너에서
   추적되는 JSON body로 `PUT /connectors/hyhome-app-postgres/config`를
   실행한다.
3. 각 상태를 개별적으로 검증한다: `GET .../status`가 connector와 task의
   `RUNNING`을 보여준다; 로그가 snapshot 완료를 보고한다; 승인된 table의
   테스트 변경이 해당 `hyhome.app.*` topic에 나타난다.
4. Lag: `hyhome_app_slot`에 대해 `pg_replication_slots`를 조회한다
   (`active`, `wal_status`,
   `pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)`).
   `wal_status = lost`는 slot이 무효화되었다는 뜻이다.
5. 유지보수를 위해 `PUT .../pause`로 일시 중지한다. 일시 중지 중에도 slot이
   WAL을 유지하므로 여유 디스크와 `max_slot_wal_keep_size`로 일시 중지 기간을
   제한한다.
6. 재동기화(승인된 경우에만): connector를 중지하고, downstream boundary를
   기록하고, slot 삭제와 offset 재설정을 함께 수행하고, 새 snapshot으로
   재등록하고, downstream 중복을 조정한다. 간단한 조치로 slot만 삭제하지
   않는다.
7. 비밀번호 rotation: secret을 교체하고, `debezium-db-provision`을 다시
   실행하고, Connect를 재시작한 뒤(properties 파일이 다시 렌더링됨),
   connector를 재시작한다.

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

## Evidence

source revision/version, 범위, timestamp, manifest/checksum 요약, 명령과 종료
상태, 검증 결과, 관측된 recovery point/시간, 미검증 gap을 모두 기록한다.
secret, raw payload, private resolved path는 제외한다.

## Rollback or Recovery

cutover가 실패하면 offset/write-boundary 검증 이후 producer와 consumer를
보존된 source cluster로 되돌리며, replay source와 target은 계속 보존된다.
cutover는 owner 승인, 최종 consistency capture, 애플리케이션 검증, 보존된
rollback window 이후에만 실행한다.

## Escalation

schema-ID drift, partition 누락, offset gap, checksum mismatch, connector
부작용, 호환되지 않는 storage/protocol format이 나타나거나 raw broker 디렉터리를
수리하라는 압박이 있으면 중단한다. 이 문서 task에서 백업이나 restore는 실행되지
않았다.

## Traceability

- Runtime source: [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
  및 [Connect image Dockerfile](../../../infra/05-messaging/kafka/Dockerfile.connect).
- Artifact: `RUN-0036`; parent guide: `GDE-0036`.
- 날짜가 기록된 verification record가 실행 사실을 명시하지 않는 한 절차는 계획 상태다.

### References

- [Apache Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Policy](../policies/0036-kafka.md)

## Related Documents

- [Domain catalog](../README.md)
