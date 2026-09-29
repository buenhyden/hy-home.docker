---
title: "Kafka Operations Policy"
version: "1.2.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0036"
parent_ids:
- "AD-0005"
created: "2026-05-17"
---

# Kafka Operations Policy

## Overview

이 정책은 현재 소스 구성을 data protection, security, resource, lifecycle,
독립적으로 검증 가능한 operator control에 결합한다.

## Policy Scope

Kafka-family 서비스는 OPTIONAL로 유지된다. 활성화 전에 이름이 지정된
producer/consumer와 승인된 capacity, retention, security, recovery 계획이
필요하다. 제거된 broker family에 대한 control은 현재 구현에 적용되지
않는다.

## Controls

- exact root profile만 선택한다. leaf file을 별도의 Compose project로
  운영하지 않는다. `messaging-cluster`는 same-host LAB topology로 취급한다.
- broker와 Connect volume을 구분하고, `kafka_net`, health check, shared
  resource limit을 유지한다.
- 현재 broker, controller, host listener는 PLAINTEXT다. transport
  confidentiality나 client authentication을 주장하지 않는다. external
  listener, JMX, JMX exporter host 포트는 `127.0.0.1`에만 게시하며,
  sensitive workload 이전에 broker TLS/SASL을 별도 architectural change로
  계획한다.
- Kafbat은 native OIDC/RBAC, local CA trust, `kafbat_client_secret`을
  유지해야 한다. route는 표준 gateway chain만 사용하며, forwarding-header
  authentication으로 대체하지 않는다.
- Topic 생성/삭제, partition 증가, retention 축소, consumer offset 이동,
  connector 변경에는 명시적인 change scope와 rollback이 필요하다.
- bootstrap topic은 replication factor 3을 요청하므로 healthy broker 3개가
  필요하다. broker 1개 선택으로 이 initialization을 유효한 것처럼 실행해서는
  안 된다.

### Change data capture

- CDC credential, grant, publication은 `debezium-db-provision` job에
  속한다. connector에는 superuser, database ownership, 또는 heartbeat
  query를 위해 소유한 `debezium_heartbeat` schema를 넘어서는 write grant를
  절대 부여하지 않는다.
- `FileConfigProvider`는 `allowed.paths`로 제한하고, Connect REST gateway
  route는 SSO 뒤에 유지한다. port 8083에 대한 직접 `kafka_net` 접근은
  authorization control이 아니라 기록된 gap으로 취급한다.
- connector를 등록, 재구성, 새 snapshot mode로 재시작, 삭제하려면
  connector와 source database를 명시한 승인이 필요하다.
- Replication slot과 connector offset은 recovery state다. slot 삭제나
  offset reset은 routine fix가 아니라 destructive resynchronization이며,
  승인, downstream duplicate/gap 계획, 새 snapshot이 필요하다.
- `max_slot_wal_keep_size` 대비 slot lag를 모니터링한다. slot이
  invalidate되면 새 snapshot이 완료될 때까지 변경 사항이 누락된다.

### Data protection

Recovery scope는 topic records/configuration, consumer offset, KRaft
metadata, Schema Registry history와 ID, Connect definition, internal
config/offset/status topic을 포함한다. 별도의 compatible target으로의
producer replay나 승인된 cross-cluster replication을 우선한다. broker log
디렉터리의 raw live copy는 backup이 아니다. manifest와 artifact는
encrypted된 별도 destination에 저장한다.

선택된 workload에는 workload별 data retention과 RPO/RTO를 설정한다;
계획된 recovery-artifact retention은 daily 30일, weekly 90일이다. 그
전까지 계획 상한은 RPO 24시간, RTO 8시간이며 검증되지 않았다. Shared
resource-template limit은 계속 필수다. Removal에는 producer, consumer,
topic, schema, offset, connector inventory와 replay/restore 증거가
필요하다. Restore는 isolation 환경에서 rehearsed되어야 하며, schema
compatibility, end offset, record count 또는 checksum, consumer position,
paused-then-resumed connector 동작을 증명해야 한다.

### Upgrade and license policy

pin 변경 전에 Apache Kafka protocol/storage compatibility, Confluent
component compatibility와 license/edition terms, Kafbat release/security
notes, client support를 검토한다. rollback과 현재 recovery artifact를
보존한다. Cluster Linking이나 다른 commercial/edition-specific 기능이
사용 가능하다고 가정하지 않는다.

## Exceptions

optional stack은 없을 수 있다; listener-security exception이 암시되지
않는다. exception은 runtime mutation, plaintext secret, raw active storage
copy, same-host availability 주장을 승인하지 않는다.

## Verification

root 구성과 scoped static policy check를 검증한 다음, promotion이나
cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 검증되지 않은 runtime property는 명시적으로 기록한다.

## Review Cadence

profile, image, volume, credential, consumer, retention, upstream
lifecycle 변경 후 검토하며, 보관 중에는 최소 연 1회 검토한다.

## Traceability

- Runtime source: [Kafka Compose](../../../infra/05-messaging/kafka/docker-compose.yml)
  와 [Connect image Dockerfile](../../../infra/05-messaging/kafka/Dockerfile.connect).
- Artifact: `POL-0036`; parent: `AD-0005`.
- Runtime authority는 연결된 Compose/source file에 남는다; exact pin은
  그곳에 유지된다.

### References

- [Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Runbook](../runbooks/0036-kafka.md)

## Related Documents

- [Domain catalog](../README.md)
