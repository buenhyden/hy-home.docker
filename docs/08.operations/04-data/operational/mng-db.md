# Management Database Operations Policy

> This document defines policy, controls, and approval rules for the mng-db system.

---

## Overview (KR)

이 문서는 `mng-db` (Management Database)에 대한 운영 정책을 정의한다. 플랫폼 핵심 메타데이타의 보호와 가용성을 유지하기 위한 통제 기준 및 검증 방법을 규정한다.

## Policy Scope

이 정책은 `infra/04-data/operational/mng-db` 및 해당 서비스가 제공하는 모든 논리적 데이타베이스(n8n, keycloak, airflow 등)를 대상으로 한다.

## Applies To

- **Systems**: mng-pg, mng-valkey, mng-pg-init
- **Agents**: AI Agent (자동화 관리 및 메타데이터 접근 시)
- **Environments**: 모든 구현 및 운영 환경 (dev, staging, prod)

## Controls

- **Required**:
    - 모든 패스워드는 `/run/secrets/`를 통해 주입되어야 한다.
    - 정기적인 연결 상태 점검(`pg_isready`)을 수행해야 한다.
- **Allowed**:
    - `01-gateway` 계층에서의 읽기 권한을 허용한다.
    - 메타데이타 백업 시 `shared_net`을 통한 비 HA 전송을 허용한다.
- **Disallowed**:
    - 대규모 비즈니스 데이타의 직접 저장을 금지한다.
    - 허가되지 않은 계정의 `postgres` 루트 DB 직접 접근을 금지한다.

## Exceptions

- **Emergency Access**: 보안 사고 발생 시 SRE의 승인 하에 루트 계정 접근을 허용하며, 행위 로그를 남겨야 한다.

## Verification

- **Compliance Check**: `docker-compose ps`를 통한 헬스 상태 점검.
- **Monitoring**: `mng-pg-exporter` (Port 9187) 및 `mng-valkey-exporter` (Port 9121) 메트릭 수집 확인.

## Review Cadence

- **Quarterly**: 매 분기별 백업 무결성 및 보안 주입 방식을 검토한다.

## AI Agent Policy Section

- **Log / Trace Retention**: 에이전트의 DB 접근 로그는 최소 30일간 보관한다.
- **Safety Incident Thresholds**: DB 부하(CPU usage)가 80%를 5분 이상 초과할 시 에이전트 자동화 작업을 중단한다.

## Related Documents

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)
- **Runbook**: [../09.runbooks/04-data/operational/mng-db.md](../../../09.runbooks/04-data/operational/mng-db.md)
- **Spec**: [../04.specs/04-data/spec.md](../../../04.specs/04-data/spec.md)
