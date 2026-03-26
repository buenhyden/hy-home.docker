<!-- Target: docs/08.operations/04-data/analytics/warehouses.md -->

# Warehouse (StarRocks) Operations Policy

> Policy and governance for the StarRocks OLAP warehouse.

---

## Overview (KR)

이 문서는 StarRocks 운영 정책을 정의한다. FE(Metadata)와 BE(Data/Compute) 노드의 리소스 할당, 보안 통제(HTTPS/Auth), 그리고 데이터 가용성 거버넌스를 규정한다.

## Policy Scope

StarRocks FE/BE 노드 및 관련 영속성 볼륨의 운영 거버넌스.

## Applies To

- **Systems**: `starrocks-fe`, `starrocks-be`
- **Agents**: Data Warehouse Managing Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - FE 노드와 BE 노드 간의 `FQDN` 기반 통신 강제 (`--host_type FQDN`).
  - BE 노드 데이터 저장을 위한 최소 디스크 잔량 (20% 이상) 유지.
  - 컨테이너 리소스 제한 (`JVM Heap` 및 `ulimit`) 명시적 설정.
- **Allowed**:
  - 단일 노드 테스트 환경 구성.
- **Disallowed**:
  - `root` 계정의 비밀번호 없는 외부 노출 (Production).
  - 백업 없이 FE 메타데이터 디렉토리 변경 금지.

## Exceptions

- 로컬 개발 환경에서는 단일 BE 노드 구성이 허용된다.

## Verification

- `SHOW FRONTENDS;` 및 `SHOW BACKENDS;` API를 통해 모든 노드가 `Alive: true` 상태인지 정기적으로 확인한다.
- `8030/metrics` 포트를 통한 쿼리 지연 시간 및 리소스 사용량 모니터링.

## Review Cadence

- Quarterly (데이터 성장률 및 노드 확장성 검토)

## Related Documents

- **ARD**: `[../../02.ard/0004-data-architecture.md]`
- **Runbook**: `[../../../09.runbooks/04-data/analytics/warehouses.md]`
- **Postmortem**: `[N/A]`
