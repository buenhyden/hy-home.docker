# Syncthing

**Syncthing**은 기기 간에 파일을 지속적으로 동기화하는 오픈 소스 프로그램입니다.
클라우드 서버 없이 P2P 방식으로 안전하게 데이터를 동기화합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **syncthing** | 동기화 서버 | `8384` (GUI), `22000` (Sync) |

## 🛠 설정 및 환경 변수

- **GUI 접속**: `http://localhost:8384`
- **인증**: `FILE__USER`, `FILE__PASSWORD` 환경 변수로 초기 계정 설정.

## 📦 볼륨 마운트

- `syncthing-volume`: 설정 및 DB (`/var/syncthing`)
- `resources-contents-volume`: 동기화할 실제 데이터 폴더 (`/Sync`)

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```
