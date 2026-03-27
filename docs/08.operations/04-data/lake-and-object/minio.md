# MinIO Object Storage Operations Policy

> S3-compatible object storage operations and governance.

---

## Overview (KR)

이 문서는 MinIO 오브젝트 스토리지의 운영 정책을 정의한다. 데이터 지속성 보장을 위한 백업 전략, 보안 통제 기준, 그리고 시스템 가용성 유지 및 성능 모니터링 방법을 규정한다.

## Policy Scope

- MinIO 데이터 볼륨 및 메타데이터 보호
- 전역 및 애플리케이션 레벨의 액세스 통제 (IAM)
- 저장소 할당량 및 모니터링 기준

## Applies To

- **Systems**: MinIO Cluster, MinIO Single Node
- **Agents**: Operators, Backup Jobs
- **Environments**: Production, Staging

## Controls

- **Required**:
  - `MINIO_ROOT_USER_FILE` 및 `MINIO_ROOT_PASSWORD_FILE` 필수 사용 (Secret Management).
  - Prometheus 엔드포인트 활성화 및 전역 모니터링 시스템 연동.
  - 중요 데이터 버킷에 대한 주기적 백업 (mc mirror).
- **Allowed**:
  - `cdn-bucket`에 대한 익명(Anonymous) 읽기 권한.
  - 개발 환경에서의 Console 직접 액세스.
- **Disallowed**:
  - Root 자격 증명을 애플리케이션 연동에 직접 사용 금지.
  - 공개되지 않은 버킷에 대한 퍼블릭 액세스 활성화 금지.

## Exceptions

- **CDN Assets**: 공개 정적 에셋의 경우 별도의 승인 없이 익명 읽기 권한을 허용한다.
- **Temporary Buckets**: 24시간 이내의 임시 작업용 버킷은 백업 대상에서 예외 처리할 수 있다.

## Verification

- `mc admin prometheus metrics`를 통한 헬스체크 및 성능 지표 검증.
- 주기적인 백업 완료 로그 확인.
- IAM 정책 검토 (최소 권한 원칙 준수 여부).

## Review Cadence

- Quarterly (분기별) 정책 및 보안 통제 검토.

## Related Documents

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/README.md)
- **Runbook**: [../09.runbooks/04-data/lake-and-object/minio.md](../../../09.runbooks/04-data/lake-and-object/minio.md)
- **Guide**: [../07.guides/04-data/lake-and-object/minio.md](../../../07.guides/04-data/lake-and-object/minio.md)
