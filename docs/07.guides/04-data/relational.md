# Relational Databases Guide

> PostgreSQL HA Cluster (Patroni/etcd) 사용 및 연결 가이드

---

## Overview (KR)

이 문서는 `hy-home.docker` 인프라의 관계형 데이터베이스(`relational`) 계층에 대한 가이드다. Patroni와 etcd를 이용한 고가용성(HA) 클러스터 구조를 이해하고, 애플리케이션에서 안전하게 연결하는 방법과 관리 절차를 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator

## Purpose

애플리케이션 개발자가 PostgreSQL HA 클러스터에 연결하고, 운영자가 클러스터 상태를 확인하며 관리하는 방법을 설명한다.

## Prerequisites

- `docker` 및 `docker compose` 설치
- 인프라 네트워크(`infra_net`)에 대한 이해
- PostgreSQL 기본 지식

## Step-by-step Instructions

### 1. 클러스터 아키텍처 이해

- **Patroni**: PostgreSQL 인스턴스의 생명주기를 관리하고 장애 시 자동 페일오버를 수행한다.
- **etcd**: 클러스터의 리더 선출 상태와 설정을 저장하는 DCS(Distributed Configuration Store) 역할을 한다.
- **HAProxy (pg-router)**: 애플리케이션의 접속 지점이며, 읽기/쓰기 트래픽을 분산한다.

### 2. 애플리케이션 연결 방법
- **Write (Primary)**: `pg-router:15432`로 연결한다. 리더 노드로 트래픽이 전달된다.
- **Read (Replica)**: `pg-router:15433`으로 연결한다. 가용한 모든 복제본 노드로 라운드 로빈 분산된다.

### 3. 클러스터 상태 확인

```bash
# pg-0 노드에서 patronictl 실행
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

## Common Pitfalls

- **직접 연결 지양**: 개별 노드(`pg-0`, `pg-1`, `pg-2`)에 직접 연결하면 페일오버 발생 시 가용성을 보장받을 수 없다. 반드시 `pg-router`를 경유한다.
- **네트워크 격리**: 데이터베이스는 `infra_net` 내부망에서만 접근 가능하다. 외부 노출이 필요한 경우 API 게이트웨이를 통한다.

## Related Documents

- **ARD**: `[../../02.ard/0004-data-architecture.md]`
- **Spec**: `[../../04.specs/04-data/spec.md]`
- **Operation**: `[../../08.operations/04-data/relational.md]`
- **Runbook**: `[../../09.runbooks/04-data/relational.md]`
