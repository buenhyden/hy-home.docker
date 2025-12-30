# Harbor Container Registry Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 오픈소스 컨테이너 레지스트리인 Harbor를 구성합니다. Docker 이미지 및 Helm 차트 등을 저장하고 관리하는 역할을 합니다. Redis와 PostgreSQL을 외부 서비스로 사용하며, 여러 컴포넌트로 나뉘어 실행됩니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **harbor-core** | Core Service | Harbor의 핵심 기능을 담당(인증, 프로젝트 관리 등)하며 API를 제공합니다. |
| **harbor-portal** | Web UI | 사용자 관리를 위한 웹 프론트엔드입니다. |
| **harbor-registry** | Image Registry | 실제 Docker 이미지를 저장하고 배포하는 레지스트리 엔진입니다. |
| **harbor-registryctl**| Controller | 레지스트리 제어 및 이미지 가비지 컬렉션 등을 담당합니다. |
| **harbor-jobservice**| Job Queue | 이미지 복제, 가비지 컬렉션 등 비동기 작업을 처리합니다. |

## 3. 구성 및 설정 (Configuration)

### 의존성 (Dependencies)
- **Redis**: 캐싱 및 작업 큐 관리를 위해 외부 Redis 사용 (`VALKEY_STANDALONE_HOSTNAME` 등 참조)
- **PostgreSQL**: 메타데이터 저장을 위해 외부 PostgreSQL 사용 (`POSTGRES_HOSTNAME` 등 참조)

### 스토리지 (Storage)
호스트의 파일 시스템을 바인드 마운트하여 데이터를 저장합니다. `${DEFAULT_CICD_DIR}/harbor/...` 경로를 사용합니다.
- `harbor-registry-data-volume`: 이미지 데이터
- `harbor-core-data-volume`: 코어 데이터
- `harbor-*conf-volume`: 각 서비스 설정 파일

### 환경 변수
`.env` 파일 및 `docker-compose.yml`의 환경 변수를 통해 비밀 키(`CORE_SECRET`, `REGISTRY_HTTP_SECRET` 등)와 DB/Redis 연결 정보를 설정합니다.

### 네트워크
- `infra_net`을 통해 다른 인프라 서비스와 격리된 통신을 수행합니다.
