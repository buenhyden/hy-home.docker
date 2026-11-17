---
title: "Kafka Operations Policy"
version: "2.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0036"
parent_ids:
- "AD-0005"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Kafka Operations Policy

## Purpose and Scope

### Objective

이 정책은 현재 소스 구성을 data protection, security, resource, lifecycle 측면에서 독립적으로 검증 가능한 operator control에 결합한다.

#### Authority

- Runtime source: [Kafka Compose](../../../../infra/05-messaging/kafka/docker-compose.yml),
  [LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml), [LAB 설명](../../../../labs/kafka-cluster/README.md),
  [Connect image Dockerfile](../../../../labs/kafka-cluster/connect/Dockerfile).
- Artifact: `POL-0036`; parent: `AD-0005`.
- Runtime authority는 연결된 Compose/source file에 남는다; exact pin은
  그곳에 유지된다.

### Applies To

Kafka-family 서비스는 OPTIONAL로 유지된다. 활성화 전에 이름이 지정된
producer/consumer와 승인된 capacity, retention, security, recovery 계획이
필요하다.

#### Exclusions

제거된 broker family에 대한 control은 현재 구현에 적용되지
않는다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0036-R1 | 정상 Kafka 선택 | 필수: root의 `messaging` 계열 profile로만 선택한다 | none | none |
| POL-0036-R2 | 세 broker topology | 금지: `labs/kafka-cluster/docker-compose.yml`을 root에 include | none | none |
| POL-0036-R3 | LAB | 필수: 별도 project/cluster ID/data directory만 사용한다 | none | none |
| POL-0036-R4 | 항상 | 필수: broker volume을 구분하고 `kafka_net`/health check/shared resource limit을 유지한다 | none | none |
| POL-0036-R5 | 현재 broker/controller/host listener가 PLAINTEXT | 금지: transport confidentiality나 client authentication 주장 | none | none |
| POL-0036-R6 | 항상 | 필수: external listener와 JMX exporter의 host 포트를 `127.0.0.1`에만 게시한다 | none | none |
| POL-0036-R7 | sensitive workload 이전 | 필수: broker TLS/SASL을 별도 architectural change로 계획한다 | none | none |
| POL-0036-R8 | Kafbat | 필수: native OIDC/RBAC/local CA trust/`kafbat_client_secret`을 유지한다 | none | none |
| POL-0036-R9 | Kafbat route | 필수: 표준 gateway chain만 사용한다 | none | none |
| POL-0036-R10 | 항상 | 금지: forwarding-header authentication으로 대체 | none | none |
| POL-0036-R11 | topic 생성/삭제/partition 증가/retention 축소/consumer offset 이동/connector 변경 | 필수: 명시적인 change scope와 rollback을 갖춘다 | none | none |
| POL-0036-R12 | 초기화 | 필수: 정상 `kafka-init` bootstrap topic은 replication factor 1, LAB `lab-kafka-init` topic은 replication factor 3(healthy LAB broker 3개 필요)으로 한다 | none | none |
| POL-0036-R13 | 항상 | 금지: 두 초기화를 서로의 cluster ID/offset/data directory에 적용 | none | none |
| POL-0036-R14 | 항상 | 금지: HOME에 CDC 서비스/`cdc` profile/Debezium credential/provisioning job 두기 | none | none |
| POL-0036-R15 | 항상 | 금지: Kafbat에 schema registry와 Connect cluster 설정 | none | none |
| POL-0036-R16 | LAB connector 등록/재구성/새 snapshot mode 재시작/삭제 | 필수: connector와 source database를 명시한 승인을 받는다 | 수동 | none |
| POL-0036-R17 | 항상 | 금지: LAB에 원천 DB와 credential 선언 | none | none |
| POL-0036-R18 | HOME에서 CDC 재사용 | 필수: POL-0107 승격 또는 새 결정을 거치고 새 원천의 slot/publication/topic을 새로 만든다 | none | none |
| POL-0036-R19 | 항상 | 금지: 이전 `hyhome_platform_slot`이나 `kafka-connect-data`에 남은 상태 재사용 | none | none |
| POL-0036-R20 | slot 삭제/offset reset | 금지: routine fix로 취급 | none | none |
| POL-0036-R21 | slot 삭제/offset reset | 필수: 승인/downstream duplicate·gap 계획/새 snapshot을 갖춘다 | 수동 | none |
| POL-0036-R22 | 원천 DB 연결 | 필수: `max_slot_wal_keep_size` 대비 slot lag를 모니터링한다 | none | none |
| POL-0036-R23 | recovery scope | 필수: topic records/configuration/consumer offset/KRaft metadata를 포함한다 | none | none |
| POL-0036-R24 | LAB에서 Schema Registry/Connect 사용 | 필수: schema history와 ID/Connect definition/internal config·offset·status topic도 같은 recovery 범위에 포함한다 | none | none |
| POL-0036-R25 | recovery | 필수: 별도의 compatible target으로의 producer replay나 승인된 cross-cluster replication을 우선한다 | none | none |
| POL-0036-R26 | 항상 | 금지: broker log 디렉터리의 raw live copy를 backup으로 취급 | none | none |
| POL-0036-R27 | manifest/artifact | 필수: encrypted된 별도 destination에 저장한다 | none | none |
| POL-0036-R28 | 선택된 workload | 필수: workload별 data retention과 RPO/RTO를 설정한다 | none | none |
| POL-0036-R29 | recovery artifact | 필수: daily 30일/weekly 90일 retention을 계획한다 | none | none |
| POL-0036-R30 | workload별 설정 전 | 필수: 계획 상한 RPO 24시간/RTO 8시간을 둔다(검증되지 않음) | none | none |
| POL-0036-R31 | 항상 | 필수: shared resource-template limit을 유지한다 | none | none |
| POL-0036-R32 | removal | 필수: producer/consumer/topic/schema/offset/connector inventory와 replay/restore 증거를 갖춘다 | none | none |
| POL-0036-R33 | restore | 필수: isolation 환경에서 rehearse한다 | none | none |
| POL-0036-R34 | restore rehearsal | 필수: schema compatibility/end offset/record count 또는 checksum/consumer position을 증명한다 | none | none |
| POL-0036-R35 | LAB connector 존재 | 필수: paused-then-resumed 동작도 증명한다 | none | none |
| POL-0036-R36 | pin 변경 전 | 필수: Apache Kafka protocol/storage compatibility/Confluent component compatibility와 license·edition terms/Kafbat release·security notes/client support를 검토한다 | 수동 | none |
| POL-0036-R37 | pin 변경 전 | 필수: rollback과 현재 recovery artifact를 보존한다 | none | none |
| POL-0036-R38 | 항상 | 금지: Cluster Linking이나 다른 commercial/edition-specific 기능이 사용 가능하다고 가정 | none | none |
| POL-0036-R39 | static 구성 검증 | 필수: RUN-0036의 root `messaging` render와 LAB render로 검증한다 | RUN-0036 root `messaging` render/LAB render | none |
| POL-0036-R40 | promotion/cutover 전 | 필수: application-level acceptance를 갖춘 isolated compatible restore를 요구한다 | none | none |
| POL-0036-R41 | 항상 | 필수: 검증되지 않은 runtime property를 명시적으로 기록한다 | none | none |
| POL-0036-R42 | 적용 identity 변경/운영 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0036-R43 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0036-R44 | engine secret/certificate | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0036-R45 | 앱 인증 연동 | 필수: 적용되는 `POL-0079`의 통제를 따른다 | none | none |
| POL-0036-R46 | source 반영/재기동 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0036-R47 | 보존/삭제 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0036-R48 | exporter/stateless job | 필수: 설정·credential과 그 작업이 변경하는 upstream state를 통제 대상에서 제외하지 않고 포함한다 | none | none |
| POL-0036-R49 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0036-R50 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- 정상 Kafka는 root의 `messaging` 계열 profile로만 선택한다. 세 broker
  topology는 root에 include하지 않는 `labs/kafka-cluster/docker-compose.yml`의 독립 LAB이며,
  별도 project, cluster ID, data directory만 사용한다.
- broker volume을 구분하고, `kafka_net`, health check, shared
  resource limit을 유지한다.
- 현재 broker, controller, host listener는 PLAINTEXT다. transport
  confidentiality나 client authentication을 주장하지 않는다. external
  listener와 JMX exporter의 host 포트는 `127.0.0.1`에만 게시한다.
  JMX 원격 listener는 제거되어 있다. sensitive workload 이전에 broker TLS/SASL을
  별도 architectural change로 계획한다.
- Kafbat은 native OIDC/RBAC, local CA trust, `kafbat_client_secret`을
  유지해야 한다. route는 표준 gateway chain만 사용하며, forwarding-header
  authentication으로 대체하지 않는다.
- Topic 생성/삭제, partition 증가, retention 축소, consumer offset 이동,
  connector 변경에는 명시적인 change scope와 rollback이 필요하다.
- 정상 `kafka-init`의 bootstrap topic은 replication
  factor 1이다. LAB의 `lab-kafka-init` topic은 replication factor 3이며 healthy
  LAB broker 3개가 필요하다. 두 초기화를 서로의 cluster ID·offset·data
  directory에 적용해서는 안 된다.

#### Change data capture

- Schema Registry와 Debezium Connect(CDC)는 2026-11-10 owner 결정(ADR-0062 개정)으로
  HOME을 떠나 `labs/kafka-cluster`의 `lab-schema-registry`, `lab-kafka-connect`가 되었다.
  HOME에는 CDC 서비스, `cdc` profile, Debezium credential과 provisioning job이 없다.
  Kafbat은 schema registry와 Connect cluster를 설정하지 않는다.
- LAB에서 connector를 등록, 재구성, 새 snapshot mode로 재시작, 삭제하려면
  connector와 source database를 명시한 승인이 필요하다. LAB은 원천 DB와 credential을 선언하지 않는다.
- HOME에서 CDC를 다시 쓰려면 POL-0107 승격 또는 새 결정이 필요하며, 새 원천의 slot·publication·topic을
  새로 만든다. 이전 `hyhome_platform_slot`이나 `kafka-connect-data`에 남은 상태를 재사용하지 않는다.
- Replication slot과 connector offset은 recovery state다. slot 삭제나
  offset reset은 routine fix가 아니라 destructive resynchronization이며,
  승인, downstream duplicate/gap 계획, 새 snapshot이 필요하다. 원천 DB를 연결하면
  `max_slot_wal_keep_size` 대비 slot lag를 모니터링한다.

#### Data protection

Recovery scope는 topic records/configuration, consumer offset, KRaft
metadata를 포함한다. LAB에서 Schema Registry나 Connect를 쓰면 schema history와 ID,
Connect definition, internal config/offset/status topic도 같은 범위다. 별도의 compatible target으로의
producer replay나 승인된 cross-cluster replication을 우선한다. broker log
디렉터리의 raw live copy는 backup이 아니다. manifest와 artifact는
encrypted된 별도 destination에 저장한다.

선택된 workload에는 workload별 data retention과 RPO/RTO를 설정한다;
계획된 recovery-artifact retention은 daily 30일, weekly 90일이다. 그
전까지 계획 상한은 RPO 24시간, RTO 8시간이며 검증되지 않았다. Shared
resource-template limit은 계속 필수다. Removal에는 producer, consumer,
topic, schema, offset, connector inventory와 replay/restore 증거가
필요하다. Restore는 isolation 환경에서 rehearsed되어야 하며, schema
compatibility, end offset, record count 또는 checksum, consumer position을 증명해야 하며,
LAB connector가 있으면 paused-then-resumed 동작도 증명해야 한다.

#### Upgrade and license policy

pin 변경 전에 Apache Kafka protocol/storage compatibility, Confluent
component compatibility와 license/edition terms, Kafbat release/security
notes, client support를 검토한다. rollback과 현재 recovery artifact를
보존한다. Cluster Linking이나 다른 commercial/edition-specific 기능이
사용 가능하다고 가정하지 않는다.

#### Accountable lifecycle boundary

적용 identity: 정상 `kafbat-ui`, `kafka-1`, `kafka-exporter`, `kafka-init`; LAB `lab-kafka-1..3`, `lab-kafka-exporter`, `lab-kafka-init`, `lab-schema-registry`, `lab-kafka-connect`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

optional stack은 없을 수 있다; listener-security exception이 암시되지
않는다. exception은 runtime mutation, plaintext secret, raw active storage
copy, same-host availability 주장을 승인하지 않는다.

#### Approval and Review

profile, image, volume, credential, consumer, retention, upstream
lifecycle 변경 후 검토하며, 보관 중에는 최소 연 1회 검토한다.

## Enforcement

### Mechanisms

[RUN-0036](../../runbooks/06-messaging-and-cdc/0036-kafka.md#steps)의 root `messaging` render와 LAB render로 static 구성을 검증한 다음, promotion이나
cutover 전에 application-level acceptance를 갖춘 isolated compatible
restore를 요구한다. 검증되지 않은 runtime property는 명시적으로 기록한다.

### Limits

이 정책에서 이름 붙은 검사는 root `messaging` render와 LAB render뿐이며(검증 행에만 연결), 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- 선택/분리: 자동 검사 없음(none) `POL-0036-R1`, `POL-0036-R2`, `POL-0036-R3`, `POL-0036-R4`
- listener/인증: 자동 검사 없음(none) `POL-0036-R5`, `POL-0036-R6`, `POL-0036-R7`, `POL-0036-R8`, `POL-0036-R9`, `POL-0036-R10`
- 변경: 자동 검사 없음(none) `POL-0036-R11`, `POL-0036-R12`, `POL-0036-R13`
- CDC: 자동 검사 없음(none) `POL-0036-R14`, `POL-0036-R15`, `POL-0036-R17`, `POL-0036-R18`, `POL-0036-R19`, `POL-0036-R20`, `POL-0036-R22`; 수동 검토/승인 `POL-0036-R16`, `POL-0036-R21`
- 데이터 보호: 자동 검사 없음(none) `POL-0036-R23`, `POL-0036-R24`, `POL-0036-R25`, `POL-0036-R26`, `POL-0036-R27`, `POL-0036-R28`, `POL-0036-R29`, `POL-0036-R30`, `POL-0036-R31`, `POL-0036-R32`, `POL-0036-R33`, `POL-0036-R34`, `POL-0036-R35`
- 업그레이드: 자동 검사 없음(none) `POL-0036-R37`, `POL-0036-R38`; 수동 검토/승인 `POL-0036-R36`
- 검증: 자동 검사 없음(none) `POL-0036-R40`, `POL-0036-R41`
- lifecycle: 자동 검사 없음(none) `POL-0036-R42`, `POL-0036-R44`, `POL-0036-R45`, `POL-0036-R46`, `POL-0036-R47`, `POL-0036-R48`, `POL-0036-R49`, `POL-0036-R50`; 수동 검토/승인 `POL-0036-R43`
- 정책이 밝힌 공백: 현재 broker/controller/host listener는 PLAINTEXT이며 broker TLS/SASL은 별도 architectural change로 남은 미구현 gap이다.
- 정책이 밝힌 공백: 계획 상한 RPO 24시간/RTO 8시간은 검증되지 않았다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter `owner`에 기록된 @buenhyden이다.

### Review Triggers

- [Domain catalog](../../README.md)
- [Kafka operations](https://kafka.apache.org/documentation/#operations)
- [Schema Registry migration](https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html)
- [Kafbat RBAC](https://ui.docs.kafbat.io/configuration/rbac-role-based-access-control)
- [Runbook](../../runbooks/06-messaging-and-cdc/0036-kafka.md)
