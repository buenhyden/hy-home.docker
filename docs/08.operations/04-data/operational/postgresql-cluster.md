# postgresql-cluster Operations Policy

## Overview (개요)

`postgresql-cluster` 운영 정책은 Patroni 기반 클러스터의 데이터 무결성, 가용성 및 성능 유지를 위한 표준 운영 절차를 정의한다.

## Purpose

본 문서는 운영 데이타베이스 클러스터의 모니터링, 백업, 보안 및 변경 관리 지침을 제공한다.

## Scope

- Patroni 클러스터 상태 감시
- etcd 쿼럼 유지 관리
- HAProxy 라우팅 상태 모니터링
- 백업 및 복구 검증

## Role & Responsibility

- **인프라 팀**: 클러스터 노드 및 네트워크 가용성 보장
- **DBA/운영자**: 성능 최적화, 쿼리 모니터링, 백업 정책 수립
- **보안 팀**: 접근 제어 정책 및 감사 로그 검토

## Operational Controls

### 1. Monitoring Metrics
다음 지표를 임계치 기반으로 모니터링한다.
- **Failover Count**: Patroni 리더 변경 횟수 (경고: 1회/시간)
- **Replication Lag**: 마스터와 레플리카 간 지연 시간 (경고: > 100MB / 10s)
- **etcd Health**: etcd 쿼럼 가용성 (심각: 쿼럼 소실 시)

### 2. Backup & Retention
- **Backup Type**: WAL Archiving + Daily Full Snapshot
- **Retention**: 최소 30일 보관 (오프사이트 백업 포함 권장)
- **Validation**: 매월 1회 복구 테스트 수행

### 3. Access Control
- **Application**: `pg-router` 엔드포인트만 사용하며 `infra_net` 외부 접근 차단
- **Operator**: Docker Secrets에 정의된 관리자 계정만 사용하며, 모든 관리 작업은 감사 로그를 남김

## Compliance & Security

- 모든 데이타 전송은 가능하면 내부망을 통해 암호화 없이 수행하되, 외부망 노출 시 반드시 TLS를 적용한다.
- `patroni_superuser_password` 등 기밀 정보는 소스 코드에 절대 노출하지 않는다.

## Monitoring & Auditing

- Prometheus와 Grafana를 통해 실시간 상태를 대시보드화한다.
- PostgreSQL의 `log_statement` 설정을 통해 중요 변경 사항을 기록한다.

## Canonical References
- [postgresql-cluster Infra README](../../../../infra/04-data/operational/postgresql-cluster/README.md)
- [postgresql-cluster Guide](../../../07.guides/04-data/operational/postgresql-cluster.md)
