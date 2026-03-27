# Qdrant Operations Policy

> Operations policy for Qdrant vector database within the `04-data/specialized` tier.

## Overview (KR)

이 문서는 Qdrant 벡터 데이터베이스의 운영 정책을 정의한다. 인덱싱 설정, 세그먼트 최적화, 스냅샷 주기 및 API 보안 통제 기준을 규정한다.

## Policy Scope

Qdrant 서비스의 자원 효율성, 데이터 무결성 및 검색 품질 유지 정책을 규정한다.

## Applies To

- **Systems**: Qdrant (Containerized)
- **Agents**: AI Engineers, DevOps Operators
- **Environments**: Production (AI/Data Profile)

## Controls

### 1. Persistence and Snapshots
- **Automatic Snapshots**: 정기적인 스냅샷을 생성하여 `/qdrant/storage/snapshots`에 보관한다.
- **Data Dir**: 호스트의 `${DEFAULT_DATA_DIR}/qdrant/data`와 바인드 마운트를 유지한다.

### 2. Performance Optimization
- **Indexing**: 대규모 데이터 삽입 시 인덱싱 쓰레드 및 세그먼트 설정을 점검하여 성능 저하를 방지한다.
- **Resource Extension**: `template-stateful-med` 준수를 원칙으로 하며, 필요시 수직 확장을 고려한다.

### 3. Security Controls
- **API Access**: `QDRANT_API_KEY`를 통한 인증을 필수로 하며, 외부 노출은 Traefik TLS를 통한다.
- **Privilege**: `v1.17-unprivileged` 이미지를 사용하여 컨테이너 권한을 최소화한다.

## Exceptions

- 초기 대량 마이그레이션(Initial Loading) 기간 동안 텔레메트리 일시 중지 또는 리소스 임시 증설이 허용된다.

## Verification

- `/readyz` 엔드포인트를 통한 주기적 Healthcheck.
- 각 컬렉션의 `status`를 조회하여 인덱싱 완료 여부 확인.

## Review Cadence

- 반기별(Bi-annually) 검색 정확도(Recall/Precision) 및 데이터 정합성 검토.

## Related Documents

- **ARD**: `[../../02.ard/0004-data-architecture.md](../../02.ard/0004-data-architecture.md)`
- **Runbook**: `[../../09.runbooks/04-data/specialized/qdrant.md](../../09.runbooks/04-data/specialized/qdrant.md)`
