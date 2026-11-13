---
title: "Kafka Cluster LAB Operations Policy"
version: "0.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0108"
parent_ids:
- "AD-0026"
created: "2026-11-05"
---

# Kafka Cluster LAB Operations Policy

## Purpose

### Objective

이 정책은 `labs/kafka-cluster/docker-compose.yml`의 LAB 전용 세 broker KRaft cluster를 격리, 데이터,
자원과 승격 통제에 묶는다.

### Authority

- Runtime source: [Kafka LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml).
- Artifact: `POL-0108`; parent: `AD-0026`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

## Scope

### Applies To

LAB 전용 `lab-kafka` profile과 project `hy-home-lab-kafka`에 적용된다.

### Exclusions

HOME 단일 broker를 대체하거나 승격하는 것은 승인하지 않는다. 승격은 [POL-0107](0107-lab-promotion.md)을 따르는 별도 Task다.

## Rules

### Requirements

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
- 데이터 보존과 삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)과 별도 승인을
  따른다. 이 LAB 데이터는 HOME 데이터와 섞지 않는다.

### Enforcement

[RUN-0108](../../runbooks/15-labs/0108-kafka-cluster.md)의 정적 render와 `lab.py check kafka-cluster`로
검증한다. HOME 입력의 render와 runtime은 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면
`labs/.env`에 `LAB_KAFKA_CLUSTER_ID`가 없으며, agent는 그 파일을 읽지 않았다.

## Exceptions

### Exception Conditions

명명된 실험이 없을 때 LAB은 정지 상태로 둘 수 있다. 예외는 runtime 변경, HOME 데이터 재사용, host
노출을 승인하지 않는다.

### Approval and Review

image, profile, network, 데이터 경로, 승격 manifest가 바뀔 때와 승격 Task를 열기 전에 검토한다.

## Ownership

### Responsibilities

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Change and Adoption

- [Kafka LAB guide](../../guides/15-labs/0108-kafka-cluster.md)
- [Kafka LAB runbook](../../runbooks/15-labs/0108-kafka-cluster.md)
- [LAB promotion policy](0107-lab-promotion.md)
- [Domain catalog](../../README.md)
