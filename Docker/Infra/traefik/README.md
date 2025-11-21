# Traefik

**Traefik**은 최신 HTTP 역방향 프록시(Reverse Proxy) 및 로드 밸런서입니다.
Docker 컨테이너의 라벨(Label)을 자동으로 감지하여 라우팅을 구성합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **traefik** | Edge Router / Proxy | `80` (HTTP), `443` (HTTPS), `8080` (Dashboard) |

## 🛠 설정 및 환경 변수

- **대시보드**: `http://localhost:8080`
- **설정**: `traefik.yml` 또는 커맨드 라인 인자(`--log.level=INFO` 등)로 제어.
- **네트워크**: `nt-default`, `nt-webserver` 등 주요 네트워크에 연결되어 트래픽을 중계합니다.

## 📦 볼륨 마운트

- `/var/run/docker.sock`: Docker 이벤트 감지용 (필수)
- `traefik-certs-volume`: SSL 인증서 저장소

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **포트 점유**: 80, 443 포트를 사용하므로 호스트의 다른 웹 서버와 충돌하지 않도록 주의하세요.
