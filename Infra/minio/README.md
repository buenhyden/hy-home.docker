# MinIO (S3 호환 객체 스토리지)

## 시스템 아키텍처에서의 역할

MinIO는 **S3 호환 객체 스토리지**로 대용량 파일, 백업, 미디어 저장을 담당합니다. Loki/Tempo의 스토리지 백엔드, CDN 파일 서빙 등에 사용됩니다.

**핵심 역할:**

- 🗄️ **객체 스토리지**: S3 API 호환 파일 저장
- 📦 **백엔드 스토리지**: Loki/Tempo 데이터 저장
- 🌐 **CDN**: 정적 파일 서빙
- 🔐 **접근 제어**: 버킷 정책 및 IAM

## 주요 구성 요소

### 1. MinIO Server

- **컨테이너**: `minio`
- **이미지**: `minio/minio:RELEASE.2025-09-07T16-13-09Z`
- **API 포트**: 9000
- **Console 포트**: 9001
- **Traefik**:
  - API: `https://minio.${DEFAULT_URL}`
  - Console: `https://minio-console.${DEFAULT_URL}`
- **IP**: 172.19.0.12

**자동 생성 버킷:**

- `tempo-bucket`: Tempo 트레이스
- `loki-bucket`: Loki 로그
- `cdn-bucket`: CDN 파일 (public)

### 2. 버킷 초기화

- **컨테이너**: `minio-create-buckets` (one-shot)
- **이미지**: `minio/mc:latest`
- **역할**: 초기 버킷 및 사용자 자동 생성

## 환경 변수

```bash
MINIO_PORT=9000
MINIO_HOST_PORT=9000
MINIO_CONSOLE_PORT=9001
MINIO_CONSOLE_HOST_PORT=9001
DEFAULT_URL=hy-home.local
```

### Docker Secrets

- `minio_root_user`: 루트 사용자
- `minio_root_password`: 루트 비밀번호
- `minio_app_user`: 애플리케이션 사용자
- `minio_app_user_password`: 앱 사용자 비밀번호

## 접속 정보

### MinIO Console (Web UI)

- **URL**: `https://minio-console.hy-home.local`
- **계정**: root user / password

### S3 API

- **Endpoint**: `https://minio.hy-home.local`
- **Region**: `us-east-1` (기본)

## 사용 방법

### AWS CLI 설정

```bash
aws configure set aws_access_key_id <app_user>
aws configure set aws_secret_access_key <app_password>
aws configure set default.region us-east-1
aws configure set default.s3.signature_version s3v4

# 파일 업로드
aws --endpoint-url https://minio.hy-home.local s3 cp file.txt s3://cdn-bucket/
```

### mc CLI

```bash
# Alias 설정
mc alias set myminio https://minio.hy-home.local <user> <password>

# 파일 업로드
mc cp file.txt myminio/cdn-bucket/

# 버킷 목록
mc ls myminio
```

## Loki/Tempo 연동

### Loki 설정 (loki-config.yaml)

```yaml
storage_config:
  aws:
    s3: s3://<user>:<password>@minio:9000/loki-bucket
    s3forcepathstyle: true
```

### Tempo 설정 (tempo.yaml)

```yaml
storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-bucket
      endpoint: minio:9000
      insecure: true
```

## 참고 자료

- [MinIO 문서](https://min.io/docs/)
- [S3 API](https://docs.aws.amazon.com/s3/)
