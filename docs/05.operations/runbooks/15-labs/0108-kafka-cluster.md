---
title: "Kafka Cluster LAB Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "operations"
artifact_id: "RUN-0108"
parent_ids:
- "GDE-0108"
created: "2026-11-05"
---

# Kafka Cluster LAB Runbook

## Overview

Kafka LAB([`labs/kafka-cluster/docker-compose.yml`](../../../../labs/kafka-cluster/docker-compose.yml), project `hy-home-lab-kafka`)의 정적 점검,
`lab.py` 기동·정지, broker 진단과 복구 계획을 다룬다.

## Trigger

Kafka LAB의 정적 검증, 승인된 실험 기동, broker·topic 이상 진단, 승격 전 readiness 확인에 쓴다.

## Prerequisites

- `labs/.env`에 `LAB_DATA_DIR`과 HOME과 다른 `LAB_KAFKA_CLUSTER_ID`가 있다. HOME 입력의
  render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `LAB_KAFKA_CLUSTER_ID`가 없다.
  owner가 값을 넣는다.
- 기동 전 Docker context, project 이름, network·volume, 가용 CPU·memory·disk, `${LAB_DATA_DIR}/kafka/`
  의 UID/GID와 정리 대상을 owner가 승인한다.
- 이 런북의 모든 runtime 단계는 별도 승인이 필요하다. 이 문서 작성에서는 아무것도 실행하지 않았다.

## Procedure

### Static check

repository root에서 합성 입력으로 render한다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster/docker-compose.yml --profile lab-kafka config --services
```

다섯 서비스 `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-exporter`, `lab-kafka-init`이
나와야 한다. 다르면 멈춘다.

### Start and stop

승인된 경우에만 `lab.py`로 기동·정지한다. 이 명령은 HOME·다른 LAB과의 충돌과 선언 limit 예산을 먼저
검사하고 정리 대상을 ledger에 남긴다.

```bash
python3 scripts/operations/lab.py check kafka-cluster
python3 scripts/operations/lab.py up kafka-cluster --purpose "<목적>" --lease <기간>
python3 scripts/operations/lab.py down kafka-cluster
```

`down -v`와 volume prune은 쓰지 않는다. `down`은 volume을 남긴다.

### Diagnosis

1. `docker compose -p hy-home-lab-kafka ps`로 세 broker의 health를 본다.
2. broker가 unhealthy이면 그 broker log에서 cluster ID 불일치, data 디렉터리 권한, quorum 연결
   실패를 찾는다. log 원문은 evidence에 붙이지 않는다.
3. `lab-kafka-init`이 실패하면 세 broker가 healthy인지 먼저 확인한다. init은 `--if-not-exists`이므로
   broker가 회복된 뒤 다시 실행해도 된다.
4. topic 상태는 LAB network 안에서 `kafka-topics --describe`로 partition leader와 ISR을 확인한다.

### Planned backup and isolated restore

1. 승인된 window에서 producer를 멈추고 topic 목록, 설정, partition, consumer offset을 기록한다.
2. 승인된 replay 또는 replication으로 새 격리 cluster에 복원한다. 기존 KRaft identity나 개별 broker
   디렉터리를 재사용하지 않는다.
3. topic별 record 수와 offset을 비교하고 결과를 Task에 기록한다.

이 절차는 계획이며 실행된 적이 없다.

### Readiness

승격 전 [RUN-0107](0107-lab-promotion.md)의 readiness 검사를 `kafka-cluster`로 실행한다.

## Verification

source revision, 실행한 명령과 종료 코드, broker health, topic·ISR 요약, 미검증 gap을 기록한다.
secret, raw log와 rendered private 설정은 기록하지 않는다.

## Failure and Recovery

### Rollback or Recovery

LAB은 HOME 소비자가 없으므로 `lab.py down kafka-cluster`로 멈추면 HOME에 영향이 없다. 데이터는
`${LAB_DATA_DIR}/kafka/`에 남는다. 삭제는 별도 승인이다.

### Escalation

cluster ID가 HOME과 같거나, HOME 경로가 render에 나타나거나, 데이터 소유가 불명확하면 멈추고
@buenhyden에게 보고한다.

## Related Documents

### Traceability

- Runtime source: [Kafka LAB Compose](../../../../labs/kafka-cluster/docker-compose.yml).
- Artifact: `RUN-0108`; parent guide: `GDE-0108`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

- [Kafka LAB guide](../../guides/15-labs/0108-kafka-cluster.md)
- [LAB promotion runbook](0107-lab-promotion.md)
- [Domain catalog](../../README.md)
