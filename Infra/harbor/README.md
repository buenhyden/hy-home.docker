# Harbor Container Registry

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 오픈소스 클라우드 네이티브 컨테이너 레지스트리입니다. 컨테이너 이미지의 저장, 서명, 취약점 스캔 기능을 제공합니다.

**주요 기능 (Key Features)**:
- **Role-Based Access Control**: 프로젝트 단위의 사용자 권한 관리.
- **Image Replication**: 다른 레지스트리(Docker Hub, GCR 등)와의 이미지 복제.
- **Vulnerability Scanning**: 이미지 취약점 자동 스캔 (Trivy 등 연동 가능).

**기술 스택 (Tech Stack)**:
- **Image**: Bitnami Harbor 2.x Series
- **Database**: PostgreSQL (External)
- **Cache**: Redis (External)

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**컴포넌트**:
- **Core**: API 처리, 인증, 권한 관리.
- **Registry**: 실제 이미지 데이터(레이어) 저장 및 배포.
- **JobService**: 비동기 작업(복제, 가비지 컬렉션 등) 처리.
- **Portal**: 웹 UI 프론트엔드.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수**:
- `HARBOR_ADMIN_PASSWORD`: 초기 관리자 비밀번호.
- `REGISTRY_STORAGE_PROVIDER_NAME`: 스토리지 백엔드 (현재 `filesystem` 사용).

**네트워크 포트**:
- **UI**: 443 (`https://harbor.${DEFAULT_URL}`) via Traefik.
- **Core API**: 내부 포트 사용.

## 5. 통합 및 API 가이드 (Integration Guide)
**Docker Login**:
```bash
docker login harbor.${DEFAULT_URL}
```
- Username: `admin` (또는 생성한 사용자)
- Password: 설정한 비밀번호

**엔드포인트 명세**:
- Base URL: `https://harbor.${DEFAULT_URL}/api/v2.0`

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인**: `harbor-core`가 `harbor-registry`의 상태를 의존적으로 확인하며 시작됩니다.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- `registry/data`: 이미지 바이너리 저장소 (가장 큼).
- `postgresql`: 메타데이터 (프로젝트, 유저, 태그 정보).
- **중요**: `HARBOR_CORE_SECRET` 등의 시크릿 키를 분실하면 암호화된 데이터를 복구할 수 없습니다.

## 8. 보안 및 강화 (Security Hardening)
- HTTPS 설정이 필수적이며(Traefik 처리), Docker 클라이언트는 공인 인증서 또는 신뢰된 CA를 요구합니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **502 Bad Gateway**: Core 서비스가 완전히 로딩되기 전 Traefik이 요청을 받을 때 발생. 잠시 대기 후 재시도.
- **Login Fail**: 패스워드 또는 시크릿 키 불일치.
