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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Supabase Stack service leaf in `04-data`; services: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, plus 7 more; root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/operational/supabase/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profiles: `data` |
| Compose linkage | root include active via [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/operational/supabase/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `${DEFAULT_DATA_DIR}/supabase/api/kong.yml:/home/kong/temp.yml:ro`, `${DEFAULT_DATA_DIR}/supabase/storage:/var/lib/storage`, `${DEFAULT_DATA_DIR}/supabase/functions:/home/deno/functions`, `${DEFAULT_DATA_DIR}/supabase/db/realtime.sql:/docker-entrypoint-initdb.d/migrations/99-realtime.sql`, `${DEFAULT_DATA_DIR}/supabase/db/webhooks.sql:/docker-entrypoint-initdb.d/init-scripts/98-webhooks.sql`, `${DEFAULT_DATA_DIR}/supabase/db/roles.sql:/docker-entrypoint-initdb.d/init-scripts/99-roles.sql`, `${DEFAULT_DATA_DIR}/supabase/db/jwt.sql:/docker-entrypoint-initdb.d/init-scripts/99-jwt.sql`, `${DEFAULT_DATA_DIR}/supabase/db/data:/var/lib/postgresql/data`, plus 8 more |
| Ports | `${SUPABASE_KONG_HTTP_HOST_PORT:-8000}:8000/tcp`, `${SUPABASE_KONG_HTTPS_HOST_PORT:-8443}:8443/tcp`, `${SUPABASE_ANALYTICS_HOST_PORT:-4000}:4000`, `${SUPABASE_POSTGRES_HOST_PORT:-5432}:5432`, `${SUPABASE_POOLER_PROXY_PORT_TRANSACTION_HOST_PORT:-6543}:6543` |
| Labels | `hy-home.tier` |
| Secret refs | names: `supabase_db_password`, `supabase_jwt_secret`, `supabase_anon_key`, `supabase_service_key`, `supabase_dashboard_password`, `supabase_secret_key_base`, `supabase_vault_enc_key`, `supabase_pg_meta_crypto_key`, `supabase_openai_api_key`, `supabase_logflare_private_token`, `supabase_smtp_password`; mounts under `/run/secrets/` |
| Healthcheck | Compose healthcheck declared for `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, plus 5 more |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/operational/supabase.md), [Policy](../../../../docs/05.operations/policies/04-data/operational/supabase.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/operational/supabase.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **환경 로드**: `.env.example`을 기준으로 non-secret key surface를 확인합니다.
2. **Secret 준비**: 위 `Secret refs`의 Docker Secret 파일 경로가 준비되었는지 확인합니다. 값은 문서, 로그, commit에 기록하지 않습니다.
3. **서비스 가동**: 승인된 운영 절차에서 `data` profile을 포함해 전체 스택을 기동합니다.
4. **접근 주소**: Kong Gateway(`http://localhost:${SUPABASE_KONG_HTTP_HOST_PORT:-8000}`, `https://localhost:${SUPABASE_KONG_HTTPS_HOST_PORT:-8443}`)를 기준으로 확인합니다. 현재 compose는 Studio의 직접 host port를 publish하지 않습니다.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **db** | PostgreSQL 17 | Core Engine (pgvector) |
| **auth** | GoTrue | JWT Auth & Management |
| **rest** | PostgREST | Automated REST API |
| **studio** | Supabase Studio | Unified Dashboard |
| **kong** | Kong Gateway | API Gateway |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `JWT_SECRET` | Yes | Docker Secret file via `supabase_jwt_secret` |
| `POSTGRES_PASSWORD` | Yes | Docker Secret file via `supabase_db_password` |
| `SUPABASE_PUBLIC_URL` | Yes | 플랫폼 외부 노출 URL |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Supabase.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with `docker compose -f infra/04-data/operational/supabase/docker-compose.yml --profile data config` to confirm Supabase service, secret, and database references render.
- Check Supabase service logs and the linked runbook before changing JWT, database, or dashboard settings.

## Related Documents

- **Guide**: [supabase.md](../../../../docs/05.operations/guides/04-data/operational/supabase.md)
- **Policy**: [supabase.md](../../../../docs/05.operations/policies/04-data/operational/supabase.md)
- **Runbook**: [supabase.md](../../../../docs/05.operations/runbooks/04-data/operational/supabase.md)

---
Copyright (c) 2026. Licensed under the MIT License.
