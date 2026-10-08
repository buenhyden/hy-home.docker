---
title: "Kafka Cluster LAB"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
created: "2026-10-03"
---

# Kafka 다중 broker LAB

## Overview

[`kafka-cluster.yml`](kafka-cluster.yml)은 독립 Compose project
`hy-home-lab-kafka`입니다. 정상 root는 이 파일을 include하지 않습니다.
`lab-kafka-1/2/3` KRaft broker/controller, `lab-kafka-exporter`,
`lab-kafka-init`가 전체 closure이며 모두 `lab-kafka` 프로파일에 속합니다.
세 broker가 한 호스트를 공유하므로 호스트 장애 가용성 실험은 아닙니다.

## Audience

독립 Kafka 토폴로지를 검토하는 개발자와 운영자.

## Scope

학습용 세 broker의 독립 Compose, 네트워크, 저장소와 정적 검증을 다룬다. 실제 실행과 데이터 이관은 별도 승인이다.

## Structure

`kafka-cluster.yml`이 전체 LAB closure를 정의하고 이 문서가 사용·복구 경계를 소유한다.

## 상태와 접근 계약

| Field | Evidence |
| --- | --- |
| Project | `hy-home-lab-kafka` |
| Services | `lab-kafka-1`, `lab-kafka-2`, `lab-kafka-3`, `lab-kafka-init`, `lab-kafka-exporter` |

- 필수 `LAB_KAFKA_CLUSTER_ID`는 정상 `KAFKA_CLUSTER_ID`와 달라야 하며 KRaft 형식에 맞아야 합니다. 기존 cluster의 metadata·offset·broker 디렉터리를 재사용하지 않습니다.
- broker별 bind 상태는 `${LAB_DATA_DIR}/kafka/{1,2,3}`이고 정상 `${DEFAULT_MESSAGE_BROKER_DIR}`와 분리합니다. 호스트 디렉터리를 미리 만들고 실제 UID/GID와 용량을 확인한 뒤에만 실행합니다.
- `lab_kafka_net`은 이 project 내부 network입니다. 호스트 port, 정상 `kafka_net`, secret, Schema Registry, Connect는 연결하지 않습니다. PLAINTEXT 접근은 LAB network 내부에 한정합니다.
- `lab-kafka-init`은 세 broker가 healthy일 때 LAB topic `lab-events`, `lab-logs`를 replication factor 3으로 생성합니다. 생성 job의 성공과 실제 topic 상태는 별개로 확인해야 합니다.

## Usage

저장소 루트에서 합성된 LAB 경로와 정상 cluster와 다른 LAB ID를 공급하여 다음 명령을 실행합니다. 이 명령은 서비스를 시작하지 않습니다.

```bash
LAB_DATA_DIR=/tmp/hyhome-lab-kafka-synthetic LAB_KAFKA_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk docker compose --env-file labs/.env.example -f labs/kafka-cluster.yml --profile lab-kafka config --quiet
```

실행 전 Docker context, project name, 모든 port·network·volume, 가용 CPU/RAM/디스크, host bind UID/GID와 정확한 정리 대상이 별도로 승인되어야 합니다. 기동·종료는 `python3 scripts/operations/lab.py up kafka-cluster --purpose "<목적>" --lease <기간>`과 `lab.py down kafka-cluster`로 하며 충돌·예산 검사와 정리 대상 ledger를 남깁니다. 이 문서 갱신에서 LAB를 실행·정지하거나 상태를 삭제하지 않았습니다. `down -v` 또는 volume prune은 사용하지 않습니다. source 선언만으로 이전 정상 root의 broker 2/3 컨테이너가 정지되지는 않습니다.

## Related Documents

- [Kafka LAB Compose](kafka-cluster.yml)
- [운영 가이드 목록](../docs/05.operations/guides/README.md)
