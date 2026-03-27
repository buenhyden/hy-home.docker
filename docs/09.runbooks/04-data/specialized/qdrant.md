# Qdrant Recovery Runbook

: Qdrant Vector Database

> Runbook for snapshot management and disaster recovery for Qdrant within the `04-data/specialized` tier.

## Overview (KR)

이 런북은 Qdrant 데이터베이스의 스냅샷 생성, 복원 및 클러스터 상태 복구 절차를 정의한다. 데이터 손상 또는 유실 시 단계별 조치 지침을 제공한다.

## Purpose

벡터 컬렉션의 무결성을 유지하고 장애 시 신속한 서비스 복원을 지원한다.

## Canonical References

- `[../../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)`
- `[infra/04-data/specialized/qdrant/README.md](../../../../infra/04-data/specialized/qdrant/README.md)`

## When to Use

- 컬렉션 단위의 스냅샷 생성이 필요할 때.
- 특정 시점의 스냅샷으로 데이터를 복원해야 할 때.
- 서비스 응답 지연 또는 `/readyz` 실패 시 조치.

## Procedure or Checklist

### 1. Collection Snapshot Execution
실행 중인 상태에서 컬렉션별 스냅샷을 생성한다.
1. 스냅샷 요청:
   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots"
   ```
2. 생성 결과 확인: `/qdrant/storage/snapshots` 디렉토리 내 `.snapshot` 파일 생성 여부 점검.

### 2. Restoration from Snapshot
1. 컬렉션 삭제 (필요시): `curl -X DELETE "https://qdrant.${DEFAULT_URL}/collections/my_collection"`
2. 스냅샷 복원 요청:
   ```bash
   curl -X POST "https://qdrant.${DEFAULT_URL}/collections/my_collection/snapshots/recover" \
        -H "Content-Type: application/json" \
        --data '{ "location": "file:///qdrant/storage/snapshots/my_collection_snapshot.snapshot" }'
   ```

### 3. Emergency Health Recovery
1. 로그 확인: `docker compose logs -f qdrant`
2. 데이터 디렉토리 권한 점검: `1000:1000` (Unprivileged user) 소유 확인.
3. 임시 파일 정리: `/tmp` (tmpfs) 용량 확인 및 정리.

## Verification Steps

- [ ] `curl https://qdrant.${DEFAULT_URL}/readyz` 호출 시 `200 OK` 확인.
- [ ] 컬렉션 인벤토리 확인: `curl https://qdrant.${DEFAULT_URL}/collections`.

## Observability and Evidence Sources

- **Signals**: Qdrant Telemetry, Traefik Dashboard.
- **Evidence to Capture**: 컬렉션 현황 캡처, 스냅샷 파일 목록.

## Safe Rollback or Recovery Procedure

- 스냅샷 복원 실패 시, 호스트 레벨의 `${DEFAULT_DATA_DIR}/qdrant/data` 전체 백업 본을 사용하여 볼륨 데이터 전체를 교체한다.
