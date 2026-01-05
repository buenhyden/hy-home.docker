# Nginx

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 경량 웹 서버 및 리버스 프록시입니다. 정적 파일을 호스팅하거나 간단한 라우팅을 수행하는 데 사용됩니다.

**주요 기능 (Key Features)**:
- **Static Content Serving**: 웹 자산(서버, JS, CSS 등) 제공.
- **SSL Termination**: HTTPS 인증서 처리.

**기술 스택 (Tech Stack)**:
- **Image**: `nginx:alpine`

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
- Traefik이 1차 라우팅을 담당하므로, 이 Nginx는 주로 특정 정적 파일을 서빙하거나 MinIO 등과 연계된 부가 기능을 수행할 수 있습니다.
- `minio` 서비스에 의존성을 가지고 있습니다.

## 3. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**파일 마운트**:
- `./config/nginx.conf`: Nginx 메인 설정 파일.
- `./certs`: 인증서 디렉토리.

**네트워크 포트**:
- HTTP/HTTPS 포트가 호스트에 매핑되어 있습니다 (`${HTTP_HOST_PORT}`, `${HTTPS_HOST_PORT}`).

## 5. 통합 및 API 가이드 (Integration Guide)
- 설정 파일(`nginx.conf`)을 수정하여 라우팅 규칙을 정의하십시오.

## 6. 가용성 및 관측성 (Availability & Observability)
- 컨테이너 상태(`docker logs nginx`)를 확인하십시오.

## 7. 백업 및 복구 (Backup & Disaster Recovery)
- 설정 파일(`conf`)과 인증서(`certs`)를 백업해야 합니다.

## 8. 보안 및 강화 (Security Hardening)
- `certs` 디렉토리에 유효한 SSL/TLS 인증서를 배치하여 보안 통신을 적용하십시오.
