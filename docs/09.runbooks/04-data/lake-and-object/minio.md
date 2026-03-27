# MinIO Object Storage Runbook

: MinIO Service Recovery & Emergency Restoration

---

## Overview (KR)

이 런북은 MinIO 오브젝트 스토리지의 장애 상황에 대응하기 위한 실행 절차를 정의한다. 디스크 공간 부족, 관리자 자격 증명 분실, 그리고 클러스터 노드 장애 발생 시 운영자가 즉각적으로 수행할 수 있는 단계별 프로세스를 제공한다.

## Purpose

- MinIO 서비스 가용성 회복 및 데이터 손실 최소화
- 긴급한 환경 설정 오류 및 자격 증명 문제 해결
- 시스템 리소스 임계치 도달 시의 즉각적인 조치

## Canonical References

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/README.md)
- **Spec**: [../04.specs/04-data/spec.md](../../../04.specs/README.md)
- **Infra README**: [../../../../infra/04-data/lake-and-object/minio/README.md](../../../../infra/04-data/lake-and-object/minio/README.md)

## When to Use

- **Storage Exhaustion**: 디스크 공간 부족으로 인한 API 쓰기 거부
- **Credential Loss**: Root 사용자 비밀번호 분실 또는 노출 시
- **Node Failure**: 클러스터 내 특정 노드 장애 (Service Down)

## Procedure or Checklist

### Checklist

- [ ] `df -h` 명령어로 실제 물리 디스크 공간 확인.
- [ ] `mc du myminio` 명령어로 버킷별 사용량 분석.

### Procedure

1. **Storage Exhaustion (디스크 공간 부족)**
   - 불필요한 로그 데이터 또는 `tempo-bucket` 내 오래된 추적 데이터 삭제 검토.
   - 필요시 볼륨 크기 확장 (인프라 재배포 필요).

2. **Root Credential Reset (비밀번호 초기화)**
   - `infra/04-data/lake-and-object/minio/` 하위의 비밀번호 설정 확인.
   - `docker compose restart minio` 명령어로 서비스 재시작.
   - `mc` (MinIO Client) 설정 업데이트 확인.

3. **Node Failure (클러스터 노드 장애)**
   - `docker compose ps`로 다운된 노드 식별.
   - `docker compose logs [node-name]`으로 장애 원인 파악.
   - 서비스 재시작: `docker compose start [node-name]`.
   - 복구 확인: `mc admin info myminio`에서 노드 상태가 'online'인지 확인.

## Verification Steps

- [ ] `mc admin info myminio`: 클러스터 상태 및 쿼럼 확인.
- [ ] `mc ls myminio`: 버킷 및 객체 브라우징 가능 여부 확인.
- [ ] `curl -f http://minio:9000/minio/health/live`: 헬스체크 응답 확인.

## Observability and Evidence Sources

- **Signals**: Grafana MinIO Dashboard, Traefik error logs.
- **Evidence to Capture**: `docker compose logs minio`, `mc admin info myminio` output.

## Safe Rollback or Recovery Procedure

- 데이터 삭제 시 반드시 백업 상태를 먼저 확인한다.
- 비밀번호 변경 후 연동된 모든 서비스의 설정을 동기화하여 서비스 장애가 전파되지 않도록 한다.

## Related Operational Documents

- **Operation Policy**: [../08.operations/04-data/lake-and-object/minio.md](../../../08.operations/04-data/lake-and-object/minio.md)
- **System Guide**: [../07.guides/04-data/lake-and-object/minio.md](../../../07.guides/04-data/lake-and-object/minio.md)
