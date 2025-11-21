# n8n

**n8n**은 확장 가능한 워크플로우 자동화 도구입니다.
다양한 앱과 서비스를 연결하여 작업을 자동화할 수 있습니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **n8n** | 워크플로우 자동화 서버 | `5678` |

## 🛠 설정 및 환경 변수

- **DB 백엔드**: PostgreSQL (`Docker/Infra/postgresql`) 사용.
- **보안**: `N8N_ENCRYPTION_KEY` 설정 필수.
- **Webhook**: `WEBHOOK_URL` 설정을 통해 외부 트리거 수신.

## 📦 볼륨 마운트

- `n8n-data`: 사용자 데이터 및 설정 (`/home/node/.n8n`)

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **데이터베이스**: PostgreSQL 서비스(`pg-router`)가 실행 중이어야 합니다.
- **타임존**: `GENERIC_TIMEZONE`을 `Asia/Seoul`로 설정하여 스케줄링 정확도 확보.
