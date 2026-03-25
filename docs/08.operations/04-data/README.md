# Data Operations Policy (04-data)

> Data Persistence, Backup & Security Governance (04-data)

## Overview

이 문서는 `hy-home.docker` 데이터 Tier(04-data)의 운영 원칙과 데이터 보호 기준을 정의한다.

## Policy Goals

- **Durability**: 시스템 장애 시에도 데이터 손실 최소화.
- **Availability**: 핵심 데이터베이스의 99.9% 가동률 지향.
- **Security**: 저장 데이터(At-rest)와 전송 데이터(In-transit)의 암호화.

## Operational Standards

### 1. 데이터 저장 및 마운트 정책

- **SSoT Path**: 모든 영구 데이터는 `${DEFAULT_DATA_DIR}` 하위에 서비스별로 격리하여 저장한다.
- **Volume Type**: 고성능 I/O가 필요한 서비스(PostgreSQL, OpenSearch)는 로컬 SSD 마운트를 우선한다.

### 2. 백업 및 유지관리

- **Backup Type**:
  - **SQL**: 매일 03:00 (KST) 논리적 백업(pg_dump) 및 물리적 스냅샷 병행.
  - **NoSQL/Object**: 증분 백업(Incremental) 또는 스냅샷 복제 수행.
- **Retention**: 최소 30일간의 백업본을 보관하며, 중요 데이터는 오프사이트(Off-site) 복제를 권고한다.

### 3. 보안 및 암호화

- **Secrets**: DB 비밀번호는 절대 환경 변수에 평문으로 노출하지 않으며, `03-security`의 Docker secrets 또는 Vault를 통해 주입한다.
- **TLS**: 지원되는 모든 데이터 서비스는 내부 통신 시에도 TLS 1.3 이상을 사용한다.

## Verification

- [ ] 정기적인 백업 복구 테스트 (Quartely).
- [ ] DB 인덱스 단편화 및 쿼리 성능 정기 점검.
- [ ] 미사용 데이터 및 로그 파일의 정기 삭제 정책 실행.

## Related Documents

- **Setup Guides**: `[../../07.guides/04-data/README.md]`
- **Recovery Runbook**: `[../../09.runbooks/04-data/README.md]`
