# Neo4j Recovery Runbook

: Neo4j Graph Database

> Runbook for database backup/restore and password management for Neo4j within the `04-data/specialized` tier.

## Overview (KR)

이 런북은 Neo4j 데이터베이스의 백업 추출, 복구 및 관리자 패스워드 재설정 절차를 정의한다. 장애 발생 시 운영자가 즉시 실행할 수 있는 명령어를 제공한다.

## Purpose

데이터 유실 방지를 위한 백업 수행 및 서비스 중단 시 빠른 데이터 복구를 지원한다.

## Canonical References

- `[../../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)`
- `[infra/04-data/specialized/neo4j/README.md](../../../../infra/04-data/specialized/neo4j/README.md)`

## When to Use

- 정기적인 데이터 백업(Dump)이 필요할 때.
- 기존 백업 수단으로부터 데이터를 복구해야 할 때.
- 관리자 패스워드 분실 또는 유출로 인한 재설정이 필요할 때.

## Procedure or Checklist

### 1. Database Dump (Backup)
Neo4j Community Edition은 인스턴스를 중지한 후 오프라인 덤프를 수행해야 한다.
1. 인스턴스 중지: `docker compose stop neo4j`
2. 덤프 생성:
   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database dump neo4j --to-path=/backups
   ```
3. 인스턴스 시작: `docker compose start neo4j`

### 2. Database Load (Restore)
1. 인스턴스 중지: `docker compose stop neo4j`
2. 데이터 복구:
   ```bash
   docker run --rm \
     --volumes-from neo4j \
     -v $(pwd)/backups:/backups \
     neo4j:5.26.23-community \
     neo4j-admin database load neo4j --from-path=/backups --overwrite-destination=true
   ```
3. 인스턴스 시작: `docker compose start neo4j`

### 3. Password Rotation
1. Docker Secret `neo4j_password` 값 업데이트.
2. 서비스 재시작: `docker compose up -d --force-recreate neo4j`

## Verification Steps

- [ ] `docker compose ps` 결과 `neo4j` 상태가 `Up (healthy)`인지 확인.
- [ ] `cypher-shell -u neo4j -p <password> "RETURN 1;"` 실행 결과 성공 확인.

## Observability and Evidence Sources

- **Signals**: Docker logs (`docker compose logs -f neo4j`), `/data/logs/neo4j.log`.
- **Evidence to Capture**: 덤프 파일 파일명 및 크기, 복구 로그 텍스트.

## Safe Rollback or Recovery Procedure

- 복구 실패 시, 기존 `neo4j-data` 볼륨의 백업 디렉토리를 보존하고 이전 시점의 덤프 파일을 사용하여 재시도한다.
