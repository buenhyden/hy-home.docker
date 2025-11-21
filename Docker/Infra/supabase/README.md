# Supabase (Self-Hosted)

**Supabase**는 Firebase의 오픈 소스 대안으로, PostgreSQL 기반의 BaaS(Backend-as-a-Service) 플랫폼입니다.
데이터베이스, 인증, 스토리지, 엣지 함수, 리얼타임 구독 등을 제공합니다.

## 🚀 서비스 구성

| 서비스명 | 역할 | 포트 |
| --- | --- | --- |
| **studio** | 대시보드 UI | `3000` |
| **kong** | API Gateway | `8000` |
| **auth** | 인증 서버 (GoTrue) | `9999` |
| **rest** | REST API (PostgREST) | `3000` (Internal) |
| **realtime** | 실시간 구독 서버 | `4000` |
| **storage** | 파일 스토리지 API | `5000` |
| **db** | PostgreSQL 데이터베이스 | `5432` |

## 🛠 설정 및 환경 변수

- **대시보드**: `http://localhost:3000` (기본 계정 없음, 로컬 모드)
- **API URL**: `http://localhost:8000`
- **API Key**: `.env` 파일의 `ANON_KEY`, `SERVICE_ROLE_KEY` 사용.

## 📦 볼륨 마운트

- `./volumes/db/data`: 데이터베이스 데이터
- `./volumes/storage`: 파일 스토리지 데이터

## 🏃‍♂️ 실행 방법

```bash
docker compose up -d
```

## ⚠️ 주의사항
- **리소스**: 매우 많은 컨테이너가 실행되므로 충분한 시스템 리소스(CPU/RAM)가 필요합니다.
- **보안**: 기본 설정은 개발용입니다. 프로덕션 배포 시 `JWT_SECRET` 및 API Key를 반드시 변경하세요.
