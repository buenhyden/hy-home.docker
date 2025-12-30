# MinIO Object Storage Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 AI/ML 및 클라우드 네이티브 애플리케이션을 위한 고성능 객체 스토리지인 MinIO를 정의합니다. Docker Secrets를 통해 보안 자격 증명을 관리하며, 초기 버킷 자동 생성을 위한 스크립트 컨테이너를 포함합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **minio** | Object Storage | S3 호환 API를 제공하는 스토리지 서버입니다. (`:9000` API, `:9001` Console) |
| **minio-create-buckets**| Initializer | `mc` (MinIO Client)를 사용하여 시작 시 필요한 버킷과 정책을 자동으로 생성합니다. |

## 3. 구성 및 설정 (Configuration)

### 보안 (Security)
- **Docker Secrets**: `minio_root_user`, `minio_root_password` 등을 통해 관리자 계정과 애플리케이션 계정을 안전하게 주입합니다.
- **API Access**: `MINIO_API_ROOT_ACCESS`가 활성화되어 있습니다.

### 초기화 (Initialization)
`minio-create-buckets` 컨테이너가 `minio` 서비스가 헬스체크를 통과하면 실행됩니다.
- **Buckets Created**: `tempo-bucket`, `loki-bucket`, `cdn-bucket`
- **Policy**: 애플리케이션 유저에게 `readwrite` 권한 부여 및 `cdn-bucket`에 대한 퍼블릭 접근 권한 설정.

### 로드밸런싱 (Traefik)
- **API Endpoint**: `https://minio.${DEFAULT_URL}` (S3 API Endpoint)
- **Console UI**: `https://minio-console.${DEFAULT_URL}` (Web Management Console)

### 데이터 볼륨
- `minio-data`: `/data` 경로에 매핑되어 객체 데이터를 영구 저장합니다.
