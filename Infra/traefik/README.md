# Traefik Edge Router

## 1. 개요 (Overview)
이 디렉토리는 시스템의 진입점(Gateway) 역할을 하는 Traefik 리버스 프록시를 정의합니다. 모든 HTTP/HTTPS 트래픽을 받아 Docker 라벨 기반으로 적절한 서비스로 라우팅하며, SSL 인증서 관리와 미들웨어(인증, 헤더 조작 등)를 처리합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **traefik** | Edge Router / Proxy | 클라우드 네이티브 엣지 라우터입니다. `infra_net` 네트워크의 관문 역할을 합니다. |

## 3. 구성 및 설정 (Configuration)

### 진입점 (Entrypoints)
`ports` 설정을 통해 호스트의 포트를 수신합니다.
- **HTTP**: 80 (`web`) -> HTTPS로 리다이렉트 (설정 파일에 정의됨)
- **HTTPS**: 443 (`websecure`) -> TLS 적용
- **Dashboard**: 별도 포트 할당
- **Metrics**: 프로메테우스 수집용 포트

### 설정 파일 (`/etc/traefik/traefik.yml`)
정적 설정은 파일을 통해 관리되며, 동적 설정(라우터, 서비스)은 주로 Docker Label과 `./dynamic` 디렉토리의 파일을 통해 관리됩니다.
- `./certs`: 사설/공인 인증서 저장소
- `./dynamic`: 동적 설정 파일 (미들웨어 정의 등)

### 대시보드
- **URL**: `https://dashboard.${DEFAULT_URL}`
- **보안**: Basic Auth(`dashboard-auth`) 미들웨어가 파일로 정의되어 있어 접근을 제한합니다.

### 주요 기능
- **Service Discovery**: Docker 소켓(`/var/run/docker.sock`)을 감시하여 컨테이너가 뜨고 질 때 자동으로 라우팅 규칙을 갱신합니다.
- **Middleware**: SSO, Rate Limit, Header 수정 등의 미들웨어를 중앙에서 관리합니다.
