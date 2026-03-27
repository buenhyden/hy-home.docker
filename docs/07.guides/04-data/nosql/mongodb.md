<!-- Target: docs/07.guides/04-data/nosql/mongodb.md -->

# MongoDB Replica Set Guide

> Document-oriented NoSQL database with flexible schemas and high availability via Replica Sets.

---

## Overview (KR)

이 문서는 MongoDB 8.2 Replica Set의 아키텍처, 데이터 모델링 원칙 및 `hy-home.docker` 환경에서의 연결 및 운영 가이드를 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

개발자가 MongoDB의 문서 기반 데이터 모델을 효율적으로 설계하고, 운영자가 레플리카 셋의 고가용성 메커니즘을 이해하여 안정적인 데이터 서비스를 제공할 수 있도록 돕는다.

## Prerequisites

- `infra/04-data/nosql/mongodb` 레플리카 셋 배포 환경
- MongoDB 셸 (`mongosh`) 또는 GUI 클라이언트 (Compass) 사용법
- JSON/BSON 데이터 구조에 대한 기초 지식

## Step-by-step Instructions

### 1. 레플리카 셋 상태 진단

클러스터의 멤버십과 상태를 확인한다.

```bash
docker exec -it mongodb-rep1 mongosh -u ${MONGODB_ROOT_USERNAME} --eval "rs.status()"
```

- **PRIMARY**: 모든 읽기/쓰기 작업이 수행되는 메인 노드.
- **SECONDARY**: Primary로부터 데이터를 복제하며 장애 시 새로운 Primary로 승격 가능.
- **ARBITER**: 데이터를 저장하지 않으며 투표에만 참여하여 정족수를 유지.

### 2. 애플리케이션 연결

고가용성을 위해 모든 노드를 포함한 연결 문자열을 사용한다.

```text
mongodb://${USER}:${PASS}@mongodb-rep1:27017,mongodb-rep2:27017/?replicaSet=MyReplicaSet&authSource=admin
```

### 3. 관리 UI 접근

**Mongo Express**를 통해 웹 기반으로 데이터를 관리할 수 있다.
- **URL**: `https://mongo-express.${DEFAULT_URL}`
- **Auth**: 배포 시 설정된 Basic Auth 정보를 확인한다.

### 4. 인덱스 최적화 및 쿼리 프로파일링

- `db.collection.explain()` 명령을 통해 쿼리 실행 계획을 수집한다.
- 쿼리 패턴에 맞는 적절한 인덱스(Compound, TTL, Text 등)를 생성하여 성능을 최적화한다.

## Common Pitfalls

- **Election Delay**: 노드 장애 시 새로운 Primary가 선정되는 동안(보통 수 초 내외) 일시적인 쓰기 거부가 발생할 수 있다. 애플리케이션 레벨의 재시도 로직이 필요하다.
- **Read Preference**: 기본값은 `primary`이나, 읽기 부하 분산을 위해 `secondaryPreferred` 설정을 고려할 수 있다. 단, 최신 데이터 정합성 이슈에 유의해야 한다.
- **WiredTiger Cache**: MongoDB는 시스템 메모리의 상당 부분을 캐시로 사용하므로 Docker 리소스 제한 시 `cacheSizeGB` 설정을 신중히 확인해야 한다.

## Related Documents

- **Infrastructure**: [MongoDB Infrastructure](../../../../infra/04-data/nosql/mongodb/README.md)
- **Operation**: [MongoDB Operations Policy](../../../08.operations/04-data/nosql/mongodb.md)
- **Runbook**: [MongoDB Recovery Runbook](../../../09.runbooks/04-data/nosql/mongodb.md)
