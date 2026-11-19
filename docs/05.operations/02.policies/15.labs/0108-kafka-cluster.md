---
title: "Kafka Cluster LAB Operations Policy"
version: "0.3.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0108"
parent_ids:
- "AD-0026"
created: "2026-11-05"
next_review_at: "2027-05-13"
---

# Kafka Cluster LAB Operations Policy

## Purpose and Scope

### Objective

이 정책은 `labs/kafka-cluster/docker-compose.yml`의 LAB 전용 세 broker KRaft cluster를 격리, 데이터,
자원과 승격 통제에 묶는다.

#### Authority

- Runtime source: [Kafka LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml).
- Artifact: `POL-0108`; parent: `AD-0026`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

### Applies To

LAB 전용 `lab-kafka` profile과 project `hy-home-lab-kafka`에 적용된다.

#### Exclusions

[ADR-0062의 Kafka CDC 개정](../../../02.architecture/02.decisions/0062-home-lab-membership.md#amendment-of-2026-11-10-kafka-cdc-kafka-connect-and-schema-registry)은
HOME 단일 broker를 유지한다. LAB의 `replace-same` manifest는 교체 검토용 후보이며 승인 근거로
쓰지 않는다. HOME 교체는 변경된 구조 결정의 승인과 [POL-0107](0107-lab-promotion.md)의 별도
Task를 요구한다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0108-R1 | 항상 | 필수: 독립 Compose project와 정확한 `lab-kafka` profile로만 선택한다 | none | none |
| POL-0108-R2 | 항상 | 금지: root include | none | none |
| POL-0108-R3 | 항상 | 필수: `LAB_KAFKA_CLUSTER_ID`는 HOME `KAFKA_CLUSTER_ID`와 달라야 한다 | none | none |
| POL-0108-R4 | 항상 | 금지: HOME cluster의 metadata, offset, broker 디렉터리 재사용 | none | none |
| POL-0108-R5 | 항상 | 필수: 세 broker data는 `${LAB_DATA_DIR}/kafka/{1,2,3}`에 분리해 유지한다 | none | none |
| POL-0108-R6 | 항상 | 금지: HOME `${DEFAULT_MESSAGE_BROKER_DIR}`를 가리킴 | none | none |
| POL-0108-R7 | 항상 | 필수: `lab_kafka_net`은 internal로 유지한다 | none | none |
| POL-0108-R8 | 항상 | 금지: host port, HOME `kafka_net`, Traefik route 추가 | none | none |
| POL-0108-R9 | 항상 | 금지: PLAINTEXT 상태(인증/TLS 없음)에서 LAB network 밖으로 개방 | none | none |
| POL-0108-R10 | 항상 | 필수: `lab-schema-registry`와 `lab-kafka-connect`는 같은 `lab_kafka_net` 안에만 둔다 | none | none |
| POL-0108-R11 | 항상 | 금지: 두 서비스에 gateway route, host port, Docker secret, connector 정의, 원천 DB 자격 증명 선언 | none | none |
| POL-0108-R12 | connector 등록과 credential 도입 시 | 필수: 별도 승인과 LAB 전용 secret 행을 갖춘다 | 수동 | none |
| POL-0108-R13 | 항상 | 필수: 선언된 limit, healthcheck, replication factor 3, `min.insync.replicas` 2를 유지한다 | none | none |
| POL-0108-R14 | 항상 | 금지: host 가용성 주장(세 broker가 한 host에 있음) | none | none |
| POL-0108-R15 | 기동/정지 시 | 필수: `scripts/operations/lab.py`만 쓴다 | none | none |
| POL-0108-R16 | 항상 | 금지: `down -v`와 volume prune | none | none |
| POL-0108-R17 | 데이터 보존/삭제 시 | 필수: `POL-0021`과 별도 승인을 따른다 | 수동 | none |
| POL-0108-R18 | 항상 | 금지: LAB 데이터를 HOME 데이터와 혼합 | none | none |

- 독립 Compose project와 정확한 `lab-kafka` profile로만 선택한다. root include에는 넣지 않는다.
- `LAB_KAFKA_CLUSTER_ID`는 HOME `KAFKA_CLUSTER_ID`와 달라야 한다. HOME cluster의 metadata, offset,
  broker 디렉터리를 재사용하지 않는다.
- 세 broker data는 `${LAB_DATA_DIR}/kafka/{1,2,3}`에 분리해 유지한다. HOME
  `${DEFAULT_MESSAGE_BROKER_DIR}`를 가리키지 않는다.
- `lab_kafka_net`은 internal로 유지한다. host port, HOME `kafka_net`, Traefik route를 추가하지 않는다.
  현재 source는 인증과 TLS 없이 PLAINTEXT이므로 LAB network 밖으로 열지 않는다.
- `lab-schema-registry`와 `lab-kafka-connect`는 같은 `lab_kafka_net` 안에만 두고 gateway route, host port,
  Docker secret, connector 정의와 원천 DB 자격 증명을 선언하지 않는다. connector 등록과 credential 도입은
  별도 승인과 LAB 전용 secret 행이 필요하다.
- 선언된 limit, healthcheck, replication factor 3과 `min.insync.replicas` 2를 유지한다. 세 broker가
  한 host에 있으므로 host 가용성을 주장하지 않는다.
- 기동·정지는 `scripts/operations/lab.py`만 쓰며 `down -v`와 volume prune을 쓰지 않는다.
- 데이터 보존과 삭제는 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)과 별도 승인을
  따른다. 이 LAB 데이터는 HOME 데이터와 섞지 않는다.

### Exceptions

#### Exception Conditions

명명된 실험이 없을 때 LAB은 정지 상태로 둘 수 있다. 예외는 runtime 변경, HOME 데이터 재사용, host
노출을 승인하지 않는다.

#### Approval and Review

image, profile, network, 데이터 경로, 승격 manifest가 바뀔 때와 승격 Task를 열기 전에 검토한다.

## Enforcement

### Mechanisms

[RUN-0108](../../03.runbooks/15.labs/0108-kafka-cluster.md)의 정적 render와 `lab.py check kafka-cluster`로
검증한다. HOME 입력의 render와 runtime은 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면
`labs/.env`에 `LAB_KAFKA_CLUSTER_ID`가 없으며, agent는 그 파일을 읽지 않았다.

### Limits

정책은 `RUN-0108`의 정적 render와 `lab.py check kafka-cluster`를 개별 규칙과 연결하지 않으며, 아래 규칙은 승인/검토에 의존하거나 강제 수단이 없다.

- 격리: 강제 수단 없음 `POL-0108-R1`~`R2`
- cluster/data: 강제 수단 없음 `POL-0108-R3`~`R6`
- network: 강제 수단 없음 `POL-0108-R7`~`R9`
- schema-registry/connect: 수동 검토 `POL-0108-R12`; 강제 수단 없음 `POL-0108-R10`~`R11`
- 운영: 수동 검토 `POL-0108-R17`; 강제 수단 없음 `POL-0108-R13`~`R16`, `POL-0108-R18`
- HOME 입력의 render와 runtime은 `NOT_RUN`이며 `labs/.env`에 `LAB_KAFKA_CLUSTER_ID`가 없다는 controller 보고가 있다.
- PLAINTEXT(인증/TLS 없음)이며 host 가용성은 주장할 수 없다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Kafka LAB guide](../../01.guides/15.labs/0108-kafka-cluster.md)
- [Kafka LAB runbook](../../03.runbooks/15.labs/0108-kafka-cluster.md)
- [LAB promotion policy](0107-lab-promotion.md)
- [Domain catalog](../../README.md)
