# Traefik Edge Router

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 클라우드 네이티브를 위한 모던 HTTP 리버스 프록시 및 로드 밸런서입니다.
인프라의 최전방에서 모든 외부 트래픽(Ingress)을 받아 적절한 Docker 컨테이너로 라우팅하며, HTTPS 종단(TLS Termination) 및 보안 미들웨어 처리를 담당합니다.

## 2. 주요 기능 (Key Features)
- **Auto Discovery**: Docker Socket을 모니터링하여 컨테이너가 시작되거나 중지될 때 라우팅 규칙을 자동으로 갱신합니다.
- **TLS Termination**: 제공된 인증서(`/certs`)를 사용하여 모든 서브도메인에 대해 HTTPS 보안 통신을 제공합니다.
- **Middleware Chain**: 인증(Basic/ForwardAuth), 압축, 헤더 조작, 속도 제한 등의 미들웨어를 파이프라인으로 구성합니다.
- **Dashboard**: 현재 활성화된 라우터, 서비스, 미들웨어의 상태를 웹 UI로 제공합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `traefik:v3.6.2`
- **Language**: Go
- **Ingress**: HTTP/HTTPS, TCP/UDP

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 트래픽 흐름
1.  **Ingress**: 80(HTTP, 443으로 리다이렉트) 또는 443(HTTPS) 포트로 요청 수신.
2.  **EntryPoints**: `web`(80) 및 `websecure`(443) 엔트리포인트에서 패킷 처리.
3.  **Routers**: `Host`(`*.example.com`) 및 `Path` 규칙에 따라 요청을 매칭.
4.  **Middlewares**: 인증(`auth`), 스트립 접두사(`stripPrefix`) 등 전처리 수행.
5.  **Services**: 최종적으로 백엔드 컨테이너의 IP와 포트로 로드 밸런싱.

### 파일 구조
- `config/traefik.yml`: 정적 설정 (EntryPoints, Providers, Logging).
- `dynamic/`: 동적 설정 (TLS 옵션, 미들웨어 정의 등).

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

**대시보드 접속**:
- URL: `https://dashboard.${DEFAULT_URL}`
- 계정: Basic Auth 설정된 계정 사용 (미들웨어 `dashboard-auth` 참조).

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 새로운 서비스 노출 방법
새로운 Docker 서비스를 추가할 때 `labels` 섹션에 다음을 추가하면 자동으로 라우팅됩니다.
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.${DEFAULT_URL}`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls=true"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080" # 내부 포트
```

### 6.2 미들웨어 적용
특정 서비스에 인증이나 IP 화이트리스트 등을 적용하려면 미들웨어를 연결합니다.
```yaml
  - "traefik.http.routers.myapp.middlewares=sso-auth@file, ip-allowlist@file"
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `DEFAULT_URL`: 기본 도메인 (예: `hy-home.local`).
- `HTTP_PORT` / `HTTPS_PORT`: 컨테이너 내부 수신 포트.

### 네트워크 포트 (Ports)
- **80**: HTTP (443으로 강제 리다이렉트 권장).
- **443**: HTTPS (메인 서비스 포트).
- **8080**: 대시보드 및 API (내부적으로 Listen).
- **8082**: Prometheus Metrics.

### 볼륨 마운트 (Volumes)
- `./certs`: TLS 인증서가 위치한 디렉토리.
- `./config/traefik.yml`: Traefik 초기화 설정.
- `/var/run/docker.sock`: Docker API 접근용 소켓 (읽기 전용).

## 8. 통합 및 API 가이드 (Integration Guide)
**인증 통합**:
- `sso-auth@file`: OAuth2 Proxy를 통한 SSO 인증 미들웨어가 동적 설정에 정의되어 있습니다.
- `dashboard-auth`: 대시보드 접근을 위한 ID/Password 인증 미들웨어입니다.

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- `traefik healthcheck --ping` 명령을 통해 자체 상태를 점검합니다.

**Metrics**:
- `/metrics` 엔드포인트에서 Prometheus 데이터를 노출합니다. Grafana 대시보드와 연동하여 요청 수(RPS), 응답 시간(Latency), 에러율 등을 모니터링할 수 있습니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**백업 대상**:
- `certs/`: 보안 인증서.
- `config/` & `dynamic/`: 커스텀 설정 파일들.

## 11. 보안 및 강화 (Security Hardening)
- **Socket Security**: `docker.sock`을 마운트하므로 Traefik 컨테이너 탈취 시 호스트 전체가 위험할 수 있습니다. `socket-proxy` 등을 사용하여 API 접근 권한을 제한하는 것이 권장됩니다.
- **TLS Policy**: 최신 TLS 버전(1.2+) 및 강력한 암호화 스위트(Cipher Suites)만을 허용하도록 설정되어 있습니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **404 Not Found**: 라벨에 설정된 `Host` 규칙과 실제 브라우저 요청 도메인이 불일치하는 경우.
- **Internal Server Error**: 백엔드 컨테이너가 죽어있거나 포트 설정이 잘못된 경우.
- **Certificate Error**: `certs/` 경로에 올바른 인증서가 없거나 만료된 경우 (기본 인증서로 대체됨).

---
**공식 문서**: [https://doc.traefik.io/traefik/](https://doc.traefik.io/traefik/)
