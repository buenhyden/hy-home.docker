# Data Runbook (04-data)

> Database Recovery & Incident Response (04-data)

## Overview

이 런북은 `hy-home.docker`의 데이터 인프라(04-data)에서 발생할 수 있는 주요 장애 상황과 복구 절차를 정의한다.

## Purpose

데이터 소실을 방지하고, 서비스 중단 시간을 최소화하기 위함이다.

---

## Recovery Procedures

### 1. PostgreSQL Master 복구 (Split-Brain 대응)

클러스터 리더가 결정되지 않거나 여러 개일 경우 수행한다.

1. **상태 확인**: `patronictl list`로 현재 상태 파악.
2. **수동 승격**: 필요한 경우 특정 노드를 강제로 리더로 승격.
   ```bash
   docker exec pg-0 patronictl failover --candidate pg-1 --force
   ```
3. **HAProxy 확인**: `pg-router`가 새로운 리더를 정상적으로 인식하는지 확인.

### 2. Valkey 클러스터 재구성 (Slot Recovery)

슬롯 할당이 깨져 클러스터가 작동하지 않을 때 수행한다.

1. **상태 진단**: `valkey-cli --cluster check <node_ip>:6379`.
2. **슬롯 복구 (Fix)**:
   ```bash
   docker exec valkey-node-0 valkey-cli --cluster fix localhost:6379
   ```

### 3. 데이터 복원 (Physical Restore)

손상된 DB를 백업본으로부터 복원한다.

1. **서비스 중단**: 쓰기 작업이 발생하지 않도록 관련 앱 일시 정지.
2. **데이터 교체**: `${DEFAULT_DATA_DIR}`의 기존 데이터를 백업본으로 교체.
3. **클러스터 재시작**: `docker compose restart`.

---

## Maintenance Tasks

- **Vacuuming**: PostgreSQL의 성능 유지를 위해 주기적인 `VACUUM ANALYZE` 실행 확인.
- **Object Storage Health**: MinIO 등의 디스크 정합성 검사(Scrubbing).

## Verification Steps

- [ ] `pg_isready` 응답 확인.
- [ ] 애플리케이션 로그에서 Connection Pool 오류 여부 점검.

## Related Operational Documents

- **Operations Policy**: `[../../08.operations/04-data/README.md]`
- **PostgreSQL HA Guide**: `[../../07.guides/04-data/01.postgresql-ha.md]`
