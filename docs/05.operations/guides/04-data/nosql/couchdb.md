---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/nosql/couchdb.md -->

# CouchDB Operation Policy Usage Guide

## Usage
>
> Document-oriented NoSQL database optimized for multi-master replication and synchronization.

---

### Overview (KR)

이 문서는 CouchDB 3-노드 클러스터의 아키텍처, 데이터 동기화 메커니즘 및 `hy-home.docker` 환경에서의 사용 가이드를 제공한다. CouchDB의 HTTP 기반 API와 강력한 복제 기능을 활용하는 방법을 설명한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Agent-tuner

### Purpose

애플리케이션 개발자가 CouchDB의 오프라인 우선(Offline-first) 데이터 동기화 기능을 이해하고, 클러스터 환경에서 가용성 높은 서비스를 구축할 수 있도록 돕는다.

### Prerequisites

- `infra/04-data/nosql/couchdb` 클러스터 배포 환경
- HTTP REST API 및 JSON 데이터 형식에 대한 기본 지식
- PouchDB 또는 CouchDB 클라이언트 라이브러리에 대한 이해

### Step-by-step Instructions

#### 1. 클러스터 상태 확인

CouchDB 전체 노드가 정상적으로 연결되어 있는지 상태를 확인한다.

```bash
## 특정 노드 상태 확인
curl -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/_up
```

### 2. 데이터베이스 및 문서 생성

CouchDB는 모든 작업을 HTTP API를 통해 수행한다.

```bash
## 데이터베이스 생성
curl -X PUT -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/my_database

## 문서 생성
curl -X POST -H "Content-Type: application/json" \
     -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} \
     https://couchdb.${DEFAULT_URL}/my_database \
     -d '{"name": "hy-home", "type": "NoSQL"}'
```

### 3. 데이터 동기화 (Replication)

CouchDB의 핵심은 원격 데이터베이스 간의 동기화이다.

- **Check-pointer**: 복제 진행 상황을 추적하여 중단 시 재개 가능하게 한다.
- **Conflicts**: 동일 문서 동기화 시 발생하는 충돌을 리비전(`_rev`) 기반으로 해결한다.

#### 4. 뷰와 쿼리 (Views & Mango)

- **Design Documents**: Map-Reduce 뷰를 정의하여 인덱싱된 조회를 수행한다.
- **Mango Queries**: MongoDB와 유사한 JSON 스타일의 선언적 쿼리를 사용한다.

### Common Pitfalls

- **Sticky Session**: Traefik 설정에서 Sticky Cookie가 비활성화되면 노드 간 리비전 불일치로 인해 예상치 못한 충돌이 발생할 수 있다.
- **Compaction**: CouchDB는 문서를 업데이트할 때마다 새 리비전을 생성하므로, 주기적인 컴팩션(Compaction) 작업이 없으면 디스크 사용량이 급격히 증가한다.
- **Admin Party**: 기본 인증이 설정되지 않은 경우 누구나 접근 가능한 위험이 있으므로 항상 Secrets 기반 인증을 확인한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/nosql/couchdb.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/nosql/couchdb.md)
- [Recovery runbook](../../../runbooks/04-data/nosql/couchdb.md)
- [Operations template](../../../../99.templates/operation.template.md)
