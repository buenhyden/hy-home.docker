# Supabase Stack

> Open-source Firebase alternative with PostgreSQL, Auth, Realtime, and Storage.

## Overview

`supabase` 스택은 `hy-home.docker` 내 애플리케이션을 위한 통합 백엔드 플랫폼을 제공합니다. PostgreSQL을 핵심 엔진으로 사용하며, 인증(GoTrue), API 생성(PostgREST), 실시간 통신(Realtime), 오브젝트 스토리지(Storage API) 레이어를 Docker 환경에서 자가 호스팅 가능한 형태로 통합합니다.

## Audience

이 README의 주요 독자:

- **Full-stack Developers**: 애플리케이션 백엔드 연동 및 API 활용
- **Platform Operators**: 스택 배포 및 서비스 건강 상태 모니터링
- **AI Agents**: 서비스 API 명세 확인 및 하위 시스템 의존성 분석

## Scope

### In Scope

- **Integrated Stack Configuration**: `docker-compose.yml`을 통한 다중 서비스 오케스트레이션.
- **Service Mesh & Networking**: Kong Gateway를 통한 중앙 집중식 API 프록시.
- **Persistence Management**: PostgreSQL 데이터 및 스토리지 볼륨 관리.
- **Administrative Interface**: Supabase Studio를 통한 웹 기반 관리 도구 제공.

### Out of Scope

- **Custom Edge Functions**: 구체적인 비즈니스 로직 구현은 서비스 코드 계층에서 관리.
- **External Migrations**: 운영 환경의 DB 마이그레이션은 Supabase CLI 권장.

## Structure

```text
supabase/
├── .env.example        # Environment variable template
├── docker-compose.yml  # Comprehensive stack configuration
└── README.md           # This file
```

## How to Work in This Area

1. **환경 로드**: `.env.example`을 복사하여 `.env`를 생성하고, 특히 `JWT_SECRET`을 설정합니다.
2. **서비스 가동**: `docker compose up -d`를 통해 전체 스택을 기동합니다.
3. **접근 주소**: Studio(`http://localhost:3000`), Kong Gateway(`http://localhost:8000`).

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **db** | PostgreSQL 15 | Core Engine (pgvector) |
| **auth** | GoTrue | JWT Auth & Management |
| **rest** | PostgREST | Automated REST API |
| **studio** | Supabase Studio | Unified Dashboard |
| **kong** | Kong Gateway | API Gateway |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `JWT_SECRET` | Yes | 서비스 전체에서 사용되는 JWT 보안 키 |
| `POSTGRES_PASSWORD` | Yes | 핵심 DB 루트 패스워드 |
| `SUPABASE_PUBLIC_URL` | Yes | 플랫폼 외부 노출 URL |

## Related References

- **Guide**: [supabase.md](../../../docs/07.guides/04-data/operational/supabase.md)
- **Operation**: [supabase.md](../../../docs/08.operations/04-data/operational/supabase.md)
- **Runbook**: [supabase.md](../../../docs/09.runbooks/04-data/operational/supabase.md)

---
Copyright (c) 2026. Licensed under the MIT License.
