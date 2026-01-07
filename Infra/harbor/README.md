# Harbor Container Registry

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 오픈소스 엔터프라이즈급 컨테이너 레지스트리입니다.  
도커 이미지를 안전하게 저장, 서명, 스캔 및 관리하는 중앙 집중식 플랫폼 역할을 수행합니다.

## 2. 주요 기능 (Key Features)
- **Role-Based Access Control (RBAC)**: 프로젝트별 사용자 권한 관리(Guest, Developer, Admin 등).
- **Vulnerability Scanning**: 업로드된 이미지의 보안 취약점 자동 스캔 (Trivy 등 Scanner 연동 시).
- **Replication**: 다중 레지스트리(Docker Hub, AWS ECR, GCR 등) 간 이미지 복제 지원.
- **Garbage Collection**: 사용하지 않는 이미지 레이어를 정리하여 스토리지 공간 확보.

## 3. 기술 스택 (Tech Stack)
- **Image**: Bitnami Harbor 2.x Series (`registry`, `core`, `portal`, `jobservice`, `registryctl`)
- **Storage**: Filesystem (Volume Mount)
- **Database**: PostgreSQL (External Cluster)
- **Cache/Session**: Redis (External Cluster)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 주요 컴포넌트
1.  **Proxy (Traefik/Nginx)**: 모든 외부 요청의 진입점 (HTTPS/TLS Termination).
2.  **Core**: 인증(AuthN), 권한(AuthZ), 프로젝트 관리 등 메인 비즈니스 로직 처리.
3.  **Registry**: 실제 Docker 이미지 레이어(Blobs)와 매니페스트 저장.
4.  **JobService**: 이미지 복제, 가비지 컬렉션 등 백그라운드 작업 처리.
5.  **Portal**: 사용자 관리를 위한 웹 UI (AngularJS/Angular).

### 데이터 흐름
- **Docker Push**: Client -> Proxy -> Core(인증) -> Registry(데이터 전송).
- **Docker Pull**: Client -> Proxy -> Core(권한 확인) -> Registry(이미지 다운로드).

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **참고**: Harbor는 여러 서비스(`core`, `registry`, `db` 등)의 의존성이 복잡하므로, 완전히 시작되는 데 시간이 소요될 수 있습니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 기본 사용법 (Docker Client)
Harbor를 Private Registry로 사용하는 표준 절차입니다.

**로그인**:
```bash
# 기본 계정: admin / Harbor12345 (환경변수 설정값 확인)
docker login harbor.${DEFAULT_URL}
```

**이미지 태그 지정 (Tagging)**:
```bash
# 로컬 이미지 'my-image:latest'를 'library' 프로젝트에 푸시하기 위해 태그 변경
docker tag my-image:latest harbor.${DEFAULT_URL}/library/my-image:latest
```

**이미지 푸시 (Push)**:
```bash
docker push harbor.${DEFAULT_URL}/library/my-image:latest
```

### 6.2 Web Portal 사용법
1.  **접속**: 브라우저에서 `https://harbor.${DEFAULT_URL}` 접속.
2.  **로그인**: 관리자 계정 사용.
3.  **프로젝트 관리**:
    - `+ New Project` 버튼으로 새 프로젝트 생성.
    - `Public` 설정 시 로그인 없이 Pull 가능, `Private` 설정 시 인증 필요.
4.  **Robot Account**:
    - CI/CD 파이프라인(Jenkins, Github Actions)에서 사용할 토큰 기반 계정 생성.
    - Project > Robot Accounts 탭에서 생성 및 토큰 복사.

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `HARBOR_ADMIN_PASSWORD`: 관리자 초기 비밀번호.
- `HARBOR_REGISTRY_HTTP_SECRET`: Registry 서비스 내부 통신 보안 키.
- `EXT_ENDPOINT`: 외부에서 접근 가능한 Public URL (`https://harbor.${DEFAULT_URL}`).
- `POSTGRESQL_*`: 외부 메타데이터 DB 연결 정보.
- `_REDIS_URL_*`: 세션 및 캐시용 Redis 연결 정보.

### 볼륨 마운트 (Volumes)
- `harbor-registry-data-volume`: `/storage` (이미지 데이터가 저장되는 핵심 경로).
- `harbor-core-conf-volume`: `/etc/core` (설정 파일).

### 네트워크 포트 (Ports)
- **Harbor Portal**: 80/443 (외부 노출은 Reverse Proxy를 통함).
- **Registry**: 5000 (내부 통신용).

## 8. 통합 및 API 가이드 (Integration Guide)
**API Access**:
- **Base URL**: `https://harbor.${DEFAULT_URL}/api/v2.0`
- **Swagger UI**: 포털 접속 후 하단 또는 `/devcenter-api-2.0` 경로 확인.

**CI/CD Integration**:
- CI 파이프라인에서 `docker login` 시 **Robot Account** 사용을 적극 권장합니다.
- Robot Account는 만료 기한 설정이 가능하며, 사용자 계정과 달리 관리 기능이 제한되어 보안에 유리합니다.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- `harbor-core` 컨테이너는 `harbor-registry` 컨테이너의 상태에 의존합니다.
- 포털 접속 시 `502 Bad Gateway`가 뜬다면, 백엔드 서비스가 초기화 중인 경우가 많습니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**필수 백업 대상**:
1.  **Registry Data**: 실제 이미지 파일 (`harbor-registry-data-volume` 매핑 경로).
2.  **Metadata DB**: PostgreSQL Database (`registry`, `notary` 등).
3.  **Configuration**: 설정 파일 및 인증서.

**복구 시 주의사항**:
- `HARBOR_CORE_SECRET` 등 `secret` 관련 환경변수 값이 변경되면, 기존 암호화된 데이터를 복호화할 수 없어 서비스가 정상 동작하지 않을 수 있습니다. `docker-compose.yml`의 환경변수를 잘 보존하세요.

## 11. 보안 및 강화 (Security Hardening)
- **HTTPS**: Docker Client는 기본적으로 HTTPS를 요구합니다. `http` 사용 시 `insecure-registries` 설정이 필요하므로, 프로덕션에서는 반드시 TLS를 적용하세요.
- **Scanning**: 주기적으로 이미지 취약점 스캔을 수행하여 보안 위협을 탐지하세요.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Login Fail (x509: certificate signed by unknown authority)**:
    - 사설 인증서 사용 시 클라이언트(Docker Daemon)에 CA 인증서를 등록해야 합니다.
- **Push Fail (denied: requested access to the resource is denied)**:
    - 해당 프로젝트에 대한 쓰기 권한이 없는 경우입니다. 로봇 계정 권한이나 멤버 권한을 확인하세요.
    - 프로젝트 할당량(Quota) 초과 시에도 발생할 수 있습니다.

---
**공식 문서**: [https://goharbor.io/docs/](https://goharbor.io/docs/)
