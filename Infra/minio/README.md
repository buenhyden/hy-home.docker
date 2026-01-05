# MinIO (Object Storage)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: AWS S3 호환 고성능 오브젝트 스토리지입니다. 로그, 백업 파일, 정적 에셋 등을 저장하는 데 사용됩니다.

**주요 기능 (Key Features)**:
- **S3 Compatible**: AWS S3 API와 완벽 호환.
- **Web Console**: 직관적인 버킷 및 파일 관리 UI.
- **Auto Buckets**: 시작 시 `tempo`, `loki` 등 주요 버킷 자동 생성.

**기술 스택 (Tech Stack)**:
- **Image**: `minio/minio:RELEASE.2025-09-07...`

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**구조**:
- **MinIO Server**: 데이터 저장 및 API 제공.
- **MinIO Client (mc)**: 초기 버킷 생성 스크립트 실행.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `MINIO_ROOT_USER`: 루트 관리자 ID.
- `MINIO_ROOT_PASSWORD`: 루트 관리자 암호.

**네트워크 포트**:
- **API**: 9000 (`minio.${DEFAULT_URL}`)
- **Console**: 9001 (`minio-console.${DEFAULT_URL}`)

## 5. 통합 및 API 가이드 (Integration Guide)
**Endpoint**: `https://minio.${DEFAULT_URL}`
**Access Key**: `minio_app_user` Secret 값 참조.

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: `/minio/health/live`
**모니터링**: Prometheus Metrics 내장 (`public` 모드 설정됨).

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- `/data` 볼륨을 주기적으로 백업해야 합니다.
- `mc mirror` 명령어로 타 MinIO 또는 S3로 복제 가능.

## 8. 보안 및 강화 (Security Hardening)
- Root 계정 사용을 지양하고 용도별 부계정(Policy)을 생성하여 사용 중(`minio-create-buckets`).

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Bucket Not Found**: 초기화 스크립트가 실패했는지 확인.

**진단 명령어**:
```bash
docker logs minio
docker logs minio-create-buckets
```
