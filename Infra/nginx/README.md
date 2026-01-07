# Nginx (Reverse Proxy & Auth Gateway)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 고성능 웹 서버이자 리버스 프록시입니다.  
본 인프라에서는 **Traefik**과 별도로 실행되며, OAuth2 Proxy와 연동하여 레거시 애플리케이션이나 특정 경로(`path-based routing`)에 대한 인증 게이트웨이 역할을 수행합니다.

## 2. 주요 기능 (Key Features)
- **Centralized Authentication**: OAuth2 Proxy와 연동하여 모든 요청에 대해 SSO 로그인 여부를 검사(`auth_request`)합니다.
- **Path-Based Routing**: `/minio/`, `/keycloak/`, `/app/` 등 URL 경로 기반으로 백엔드 서비스에 트래픽을 분배합니다.
- **SSL Termination**: 로컬 인증서(`/certs`)를 사용하여 HTTPS 연결을 종단합니다.
- **Response Buffering Control**: 대용량 파일 전송이 필요한 서비스(MinIO 등)에 대해 버퍼링 설정을 최적화합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `nginx:alpine`
- **Protocol**: HTTP/1.1, HTTP/2
- **TLS**: TLS v1.2/v1.3 지원

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 트래픽 흐름 (`/app/` 접근 시)
1.  **Client** -> **Nginx (443)**: HTTPS 요청 도착.
2.  **Nginx (Auth Check)** -> **OAuth2 Proxy**: `/_oauth2_auth_check` 내부 요청으로 세션 유효성 검증.
3.  **Result**:
    - **유효함 (200)**: 요청을 **Target App**으로 전달 (User 헤더 포함).
    - **유효하지 않음 (401)**: **OAuth2 Proxy Sign-in** 페이지로 리다이렉트.

### Upstream Service 연결
- `minio_server`: 9000
- `minio_console`: 9001
- `keycloak`: 8080
- `oauth2_proxy`: 4180

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **주의**: Nginx가 시작되기 전에 `minio` 등 Upstream 서비스가 정상 동작 중이어야(healthy) 합니다 (`depends_on` 설정됨).

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 설정 파일 수정 (nginx.conf)
`config/nginx.conf` 파일을 수정하여 라우팅 규칙을 추가/변경할 수 있습니다.
```nginx
# 예시: 새로운 앱 추가
location /new-app/ {
    auth_request /_oauth2_auth_check; # 인증 적용
    proxy_pass http://new-app:3000/;
}
```

### 6.2 인증서 관리
`certs/` 디렉토리에 SSL 인증서 파일이 존재해야 합니다.
- `cert.pem`: 서버 인증서
- `key.pem`: 개인 키
- `rootCA.pem`: 신뢰할 수 있는 CA 인증서 (Proxy 검증용)

## 7. 환경 설정 명세 (Configuration Reference)
### 볼륨 마운트 (Volumes)
- `./config/nginx.conf`: 메인 설정 파일 (`/etc/nginx/nginx.conf` 로 마운트).
- `./certs`: 인증서 저장소 (`/etc/nginx/certs` 로 마운트).

### 네트워크 포트 (Ports)
- **HTTP**: 호스트 포트 매핑 (예: 80). HTTPS로 리다이렉트됨.
- **HTTPS**: 호스트 포트 매핑 (예: 443).

## 8. 통합 및 API 가이드 (Integration Guide)
**Upstream Header Injection**:
인증 성공 시 Nginx는 백엔드 애플리케이션에 다음 헤더를 주입하여 전달합니다.
- `X-User`: 사용자 ID
- `X-Email`: 사용자 이메일
- `Authorization`: Bearer Access Token

## 9. 가용성 및 관측성 (Availability & Observability)
**Logging**:
- **Access Log**: `/var/log/nginx/access.log` (JSON 포맷 아님, nginx 기본 포맷).
- **Error Log**: `/var/log/nginx/error.log`.

**Health Check**:
- `/ping`: 200 OK "pong" 응답 (Nginx 자체 헬스체크용).

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**백업 대상**:
- `nginx.conf`: 라우팅 규칙이 정의된 설정 파일.
- `certs/`: 발급받은 인증서 파일.

## 11. 보안 및 강화 (Security Hardening)
- **SSL 설정**: TLS 1.2 이상만 허용하며, 강력한 암호화 스위트를 사용하도록 설정되어 있습니다.
- **Client Max Body Size**: 업로드 경로(`/minio/` 등)를 제외하고는 기본값으로 제한할 것을 권장합니다(현재는 전역 설정이 아닌 location 별로 제어 중).

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **502 Bad Gateway**: Upstream 서비스(MinIO, Keycloak 등)가 다운되었거나 네트워크 연결이 불가능한 경우. `docker logs nginx` 에러 로그를 확인하세요.
- **Too Many Redirects**: HTTPS 프록시 헤더(`X-Forwarded-Proto: https`)가 누락되어 백엔드 앱이 계속 HTTP로 리다이렉트 시키는 경우 발생할 수 있습니다. `nginx.conf` 헤더 설정을 확인하세요.

---
**공식 문서**: [https://nginx.org/en/docs/](https://nginx.org/en/docs/)
