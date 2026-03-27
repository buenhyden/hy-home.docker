# postgresql-cluster Guide

> Patroni 및 etcd 기반 고가용성(HA) PostgreSQL 클러스터 가이드
> High-Availability (HA) PostgreSQL Cluster Guide based on Patroni and etcd

---

## Overview (KR/EN)

### KR

이 문서는 `postgresql-cluster`의 아키텍처를 이해하고, 데이타베이스 노드 상태 확인 및 애플리케이션 연결 방법을 익히기 위한 시스템 가이드다. Patroni와 etcd가 어떻게 협력하여 고가용성을 유지하는지, 그리고 HAProxy(`pg-router`)를 통한 트래픽 라우팅 원리를 설명한다.

### EN

This document is a system guide for understanding the architecture of `postgresql-cluster` and learning how to check database node status and connect applications. It explains how Patroni and etcd work together to maintain high availability and the principles of traffic routing through HAProxy (`pg-router`).

## Guide Type

`system-guide`

## Target Audience

- Developer (연결 및 쿼리 테스트)
- Operator (클러스터 상태 점검 및 유지보수)
- AI Agent (인프라 무결성 검증 및 사고 대응 보조)

## Purpose

- Patroni HA 아키텍처의 동작 원리 이해
- etcd DCS(Distributed Configuration Store)의 역할 파악
- `pg-router`(HAProxy)를 이용한 읽기/쓰기 분산 연결 방법 습득

## Prerequisites

- `infra_net` 네트워크에 대한 이해 및 접근 권한
- Docker Secrets(`patroni_superuser_password`)에 대한 인지
- `patronictl` CLI 도구 기본 사용법 숙지

## Step-by-step Instructions

### 1. 클러스터 상태 모니터링

Patroni CLI를 사용하여 현재 리더(Leader) 노드와 복제본(Replica) 노드들의 상태를 확인한다.

```bash
# pg-0 노드에서 클러스터 리스트 확인
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

### 2. 애플리케이션 연결 정의

모든 애플리케이션은 개별 PostgreSQL 노드 주소가 아닌, `pg-router` 엔드포인트를 사용해야 한다.

- **Write (Master)**: `pg-router:15432` (리더 노드 자동 연결)
- **Read (Replica)**: `pg-router:15433` (레플리카들 간 라운드 로빈 분산)

### 3. 초기화 작업 (pg-cluster-init)

시스템 구동 시 `pg-cluster-init` 컨테이너가 자동으로 실행되어 서비스에 필요한 기본 DB와 사용자를 생성한다. 수동 재실행이 필요한 경우:

```bash
docker compose up pg-cluster-init
```

## Common Pitfalls

- **etcd Quorum Loss**: 3개 etcd 노드 중 2개 이상 장애 시 리더 선출이 중단되며 클러스터는 `Read-Only` 상태로 전환될 수 있다.
- **Connection Limits**: HAProxy 포트가 열려 있어도 각 노드의 `max_connections` 설정에 따라 연결이 거부될 수 있으므로 커넥션 풀 사용을 권장한다.

## Related Documents

- **Spec**: `docs/04.specs/04-data/spec.md`
- **Operation**: `docs/08.operations/04-data/relational/postgresql-cluster.md`
- **Runbook**: `docs/09.runbooks/04-data/relational/postgresql-cluster.md`
- **Infra**: `infra/04-data/relational/postgresql-cluster/README.md`
