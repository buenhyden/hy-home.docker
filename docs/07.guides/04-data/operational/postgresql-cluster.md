# postgresql-cluster Guide

## Overview (개요)

`postgresql-cluster`는 Patroni 관리 기반의 3개 노드 고가용성 PostgreSQL 시스템이다. etcd를 분산 설정 저장소(DCS)로 사용하며, HAProxy(`pg-router`)가 마스터와 복제본에 대한 트래픽 분산을 담당한다.

## Purpose

이 가이드는 `postgresql-cluster`의 아키텍처 이해, 데이타베이스 연결 방법, 그리고 초기화 프로세스를 안내하는 데 목적이 있다.

## Prerequisites

- `infra_net`에 대한 네트워크 접근 권한
- `04-data` 티어 공통 보안 정책 이해
- Docker Secrets에 정의된 `patroni_superuser_password` 인지

## Core Concepts

### 1. Patroni HA Architecture
Patroni는 PostgreSQL의 상태를 끊임없이 감시하며, 마스터 노드 장애 시 etcd에 기록된 리더 잠금(leader lock)을 기반으로 새로운 마스터를 선출한다.

### 2. DCS (Distributed Configuration Store)
etcd는 클러스터의 상태 및 리더 정보를 유지하는 전역 저장소 역할을 한다. 3개 노드 중 과반수(Quorum)가 동작해야 클러스터 제어가 가능하다.

### 3. pg-router (HAProxy)
클러스터 외부/내부 통신을 단일 지점으로 통합하며, 각 노드의 헬스체크 결과에 따라 RW(15432) / RO(15433) 트래픽을 분산한다.

## Step-by-Step Guide

### 1. 클러스터 상태 확인
Patroni CLI를 사용하여 클러스터 토폴로지와 복제 상태를 확인한다.

```bash
docker exec -it pg-0 patronictl -c /home/postgres/postgres.yml list
```

### 2. 데이바테이스 연결 (애플리케이션)
애플리케이션은 항상 `pg-router`를 통해 연결해야 한다.

- **Write (Master)**: `pg-router:15432`
- **Read (Replica)**: `pg-router:15433`

### 3. 초기 서비스 DB 생성
`pg-cluster-init` 작업이 플랫폼 구동 시 자동으로 실행되어 `app_db`와 `app_user`를 초기화한다. 수동 실행이 필요한 경우:

```bash
docker compose up pg-cluster-init
```

## Common Pitfalls

- **etcd 과반수 손실**: etcd 노드 2개 이상 장애 시 클러스터는 리더 선출이 불가능해지며 `Read-Only` 모드로 고정된다.
- **복명 지연 (Replication Lag)**: 대규모 쓰기 작업 시 `RO` 포트를 통한 읽기 데이타가 최신 상태가 아닐 수 있다.

## Best Practices

- **Connection Pooling**: PostgreSQL의 동시 연결 제한을 방지하기 위해 애플리케이션 레벨에서 연결 풀을 사용한다.
- **Secrets 관리**: 모든 중요 자격 증명은 `read_secret` 유틸리티를 통한 Docker Secrets 처리를 유지한다.

## Canonical References
- [postgresql-cluster Infra README](../../../../infra/04-data/operational/postgresql-cluster/README.md)
- [ARD: 0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)
- [Spec: 04-data/spec.md](../../../04.specs/04-data/spec.md)
