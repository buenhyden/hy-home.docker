# MinIO Object Storage

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: AWS S3 API와 완벽하게 호환되는 고성능 분산 오브젝트 스토리지입니다.  
애플리케이션 로그, 백업 파일, 정적 자산(이미지, 영상), 데이터 분석용 데이터 레이크 등을 구축하기 위한 핵심 스토리지 인프라입니다.

## 2. 주요 기능 (Key Features)
- **S3 Compatibility**: AWS S3와 동일한 API를 제공하여 기존 S3 SDK 및 도구를 그대로 사용할 수 있습니다.
- **Web Console**: 버킷 생성, 파일 업로드/다운로드, 정책 관리 등을 위한 직관적인 GUI를 제공합니다.
- **Auto Initialization**: 서비스 시작 시 `setup` 컨테이너가 실행되어 필요한 버킷(`tempo`, `loki` 등)과 사용자 계정을 자동으로 구성합니다.
- **Prometheus Metrics**: 스토리지 사용량, 요청 통계 등 상세한 모니터링 메트릭을 기본 제공합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `minio/minio:RELEASE.2025-09-07...` (Server), `minio/mc` (Client Tool)
- **Protocol**: HTTP/HTTPS (S3 API)
- **Storage**: Filesystem (Volume)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 시스템 구조
1.  **MinIO Server**: 실제 데이터를 저장하고 S3 API 요청을 처리하는 메인 서버.
2.  **MinIO Console**: 서버 관리를 위한 웹 인터페이스 (별도 포트 9001 사용).
3.  **Setup Container**: `minio-create-buckets` 컨테이너가 실행되어 Root 계정으로 로그인 후 초기 버킷 및 App User를 생성하고 종료됩니다.

### 데이터 흐름
- **App** -> **Traefik (`https://minio.${DEFAULT_URL}`)** -> **MinIO API (9000)**
- **Admin** -> **Traefik (`https://console.minio.${DEFAULT_URL}`)** -> **MinIO Console (9001)**

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: `minio-create-buckets` 컨테이너가 "Exited (0)" 상태가 되면 초기화가 성공적으로 완료된 것입니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 Web Console 사용
1.  **접속**: `https://console.minio.${DEFAULT_URL}` (또는 `https://minio-console.${DEFAULT_URL}`)
2.  **로그인**: 
    - **ID**: `MINIO_ROOT_USER` (Docker Secret 또는 환경변수 참조)
    - **PW**: `MINIO_ROOT_PASSWORD`
3.  **기능**:
    - **Buckets**: 버킷 생성 및 탐색.
    - **Identity**: 사용자(User) 및 그룹(Group) 관리.
    - **Policies**: IAM 스타일의 접근 권한 정책 설정.

### 6.2 CLI (mc) 사용법
MinIO Client(`mc`)를 사용하여 로컬 터미널에서 스토리지를 관리할 수 있습니다.

```bash
# 별칭(Alias) 설정
mc alias set myminio https://minio.${DEFAULT_URL} <USER> <PASSWORD>

# 버킷 목록 확인
mc ls myminio

# 파일 업로드
mc cp my-file.txt myminio/my-bucket/
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`: Docker Secret을 통해 Root 계정 정보를 주입받습니다.
- `MINIO_PROMETHEUS_AUTH_TYPE`: `public` (프로메테우스가 인증 없이 메트릭을 수집하도록 허용).

### 볼륨 마운트 (Volumes)
- `minio-data`: `/data` (실제 파일이 저장되는 영구 볼륨).

### 네트워크 포트 (Ports)
- **API**: 9000 (`https://minio.${DEFAULT_URL}`)
- **Console**: 9001 (`https://console.minio.${DEFAULT_URL}`)

## 8. 통합 및 API 가이드 (Integration Guide)
**S3 Client 설정 예시**:
- **Endpoint**: `https://minio.${DEFAULT_URL}`
- **Region**: `us-east-1` (MinIO 기본값)
- **Access Key**: `minio_app_user` Secret 참조
- **Secret Key**: `minio_app_user_password` Secret 참조
- **Path Style Access**: `True` (권장)

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- `/minio/health/live`: Liveness Probe.
- `/minio/health/ready`: Readiness Probe.

**Monitoring**:
- `/minio/v2/metrics/cluster`: Prometheus 메트릭 엔드포인트.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- MinIO의 `/data` 볼륨을 백업하는 것이 가장 확실한 방법입니다.
- `mc mirror` 명령어를 사용하여 원격지 MinIO 또는 AWS S3로 실시간/주기적 동기화를 구성할 수 있습니다.

## 11. 보안 및 강화 (Security Hardening)
- **Root 계정 보호**: Root 계정은 초기 설정 및 비상시에만 사용하고, 애플리케이션은 별도로 생성된 `minio_app_user`와 제한된 권한(Policy)을 사용해야 합니다.
- **TLS**: 모든 통신은 Traefik을 통해 HTTPS로 암호화됩니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Setup Fail**: `minio-create-buckets` 로그 확인 시 "Connection refused"가 뜬다면 MinIO 서버가 아직 준비되지 않은 것입니다. `depends_on: service_healthy` 설정이 있는지 확인하세요.
- **Policy Denied**: "Access Denied" 오류 발생 시 해당 유저에게 할당된 Policy가 버킷에 대한 `s3:PutObject`, `s3:GetObject` 권한을 포함하는지 확인하세요.

---
**공식 문서**: [https://min.io/docs/minio/linux/index.html](https://min.io/docs/minio/linux/index.html)
