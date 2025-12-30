# Nginx Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 정적 파일 서빙 또는 특정 리버스 프록시 용도로 사용되는 Nginx를 정의합니다. 현재 구성에서는 MinIO 서비스에 의존성을 가지고 있으며, 인증서 및 설정 파일을 호스트로부터 마운트하여 사용합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **nginx** | Web Server / Proxy | HTTP/HTTPS 요청을 처리하는 웹 서버입니다. |

## 3. 구성 및 설정 (Configuration)

### 포트
- HTTP(`HTTP_PORT`) 및 HTTPS(`HTTPS_PORT`) 포트가 호스트에 직접 노출되어 있습니다.
- Traefik을 거치지 않고 직접 요청을 처리하는 용도로 사용될 수 있습니다.

### 볼륨
- `./config/nginx.conf`: Nginx 설정 파일
- `./certs`: SSL 인증서 디렉토리

### 의존성
- **minio**: MinIO 서비스가 시작된 후 실행되도록 설정되어 있어, MinIO의 프론트엔드 프록시 또는 정적 자산 서빙 역할을 수행할 가능성이 있습니다.
