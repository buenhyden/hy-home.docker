---
title: "Supabase Stack"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

# Supabase Stack

> PostgreSQL, Auth, Realtime, Storage를 갖춘 오픈소스 Firebase 대안입니다.

## Overview

`supabase` 스택은 `hy-home.docker` 내 애플리케이션을 위한 통합 백엔드 플랫폼을 제공합니다. PostgreSQL을 핵심 엔진으로 사용하며 인증(GoTrue), API 생성(PostgREST), 실시간 통신(Realtime), 오브젝트 스토리지(Storage API) 레이어를 Docker 환경에서 자가 호스팅 가능한 형태로 통합합니다.

## Audience

이 README의 주요 독자:

- **Full-stack Developers**: 애플리케이션 백엔드 연동 및 API 활용
- **Platform Operators**: 스택 배포 및 서비스 건강 상태 모니터링
- **AI Agents**: 서비스 API 명세 확인 및 하위 시스템 의존성 분석

## Scope

### In Scope

- **통합 스택 설정**: `docker-compose.yml`을 통한 다중 서비스 오케스트레이션.
- **서비스 메시와 네트워킹**: Kong Gateway를 통한 중앙 집중식 API 프록시.
- **지속성 관리**: PostgreSQL 데이터 및 스토리지 볼륨 관리.
- **관리 인터페이스**: Supabase Studio로 웹 기반 관리 도구 제공.

### Out of Scope

- **Custom Edge Functions**: 구체적인 비즈니스 로직 구현은 서비스 코드 계층에서 관리.
- **외부 마이그레이션**: 운영 환경의 DB 마이그레이션은 Supabase CLI 권장.

## Structure

```text
supabase/
├── .env.example        # 환경 변수 template
├── docker-compose.yml  # 통합 스택 설정
└── README.md           # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 Supabase Stack 서비스 leaf; services: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage` 등 7개 더; [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/supabase/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profiles: `supabase` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/supabase/docker-compose.yml` |
| Networks | `supabase_net` |
| Volumes | `${DEFAULT_DATA_DIR}/supabase/api/kong.yml:/home/kong/temp.yml:ro`, `${DEFAULT_DATA_DIR}/supabase/storage:/var/lib/storage`, `${DEFAULT_DATA_DIR}/supabase/functions:/home/deno/functions`, `${DEFAULT_DATA_DIR}/supabase/db/realtime.sql:/docker-entrypoint-initdb.d/migrations/99-realtime.sql`, `${DEFAULT_DATA_DIR}/supabase/db/webhooks.sql:/docker-entrypoint-initdb.d/init-scripts/98-webhooks.sql`, `${DEFAULT_DATA_DIR}/supabase/db/roles.sql:/docker-entrypoint-initdb.d/init-scripts/99-roles.sql`, `${DEFAULT_DATA_DIR}/supabase/db/jwt.sql:/docker-entrypoint-initdb.d/init-scripts/99-jwt.sql`, `${DEFAULT_DATA_DIR}/supabase/db/data:/var/lib/postgresql/data` 등 8개 더 |
| Ports | `${SUPABASE_KONG_HTTP_HOST_PORT:-8000}:8000/tcp`, `${SUPABASE_KONG_HTTPS_HOST_PORT:-8443}:8443/tcp`, `${SUPABASE_ANALYTICS_HOST_PORT:-4000}:4000`, `${SUPABASE_POSTGRES_HOST_PORT:-5432}:5432`, `${SUPABASE_POOLER_PROXY_PORT_TRANSACTION_HOST_PORT:-6543}:6543` |
| Labels | `hy-home.tier` |
| Secret refs | names: `supabase_db_password`, `supabase_jwt_secret`, `supabase_anon_key`, `supabase_service_key`, `supabase_dashboard_password`, `supabase_secret_key_base`, `supabase_vault_enc_key`, `supabase_pg_meta_crypto_key`, `supabase_openai_api_key`, `supabase_logflare_private_token`, `supabase_smtp_password`; mounts under `/run/secrets/` |
| Healthcheck | `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta` 등 5개 더에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/guides/0029-supabase.md`), Policy (`docs/05.operations/policies/0029-supabase.md`), Runbook (`docs/05.operations/runbooks/0029-supabase.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. **환경 로드**: `.env.example`을 기준으로 non-secret key surface를 확인합니다.
2. **Secret 준비**: 위 `Secret refs`의 Docker Secret 파일 경로가 준비되었는지 확인합니다. 값은 문서, 로그, commit에 기록하지 않습니다.
3. **서비스 가동**: 승인된 운영 절차에서 `supabase` profile을 포함해 전체 스택을 기동합니다.
4. **접근 주소**: Kong Gateway(`http://localhost:${SUPABASE_KONG_HTTP_HOST_PORT:-8000}`, `https://localhost:${SUPABASE_KONG_HTTPS_HOST_PORT:-8443}`)를 기준으로 확인합니다. 현재 compose는 Studio의 직접 host port를 publish하지 않습니다.

## Tech Stack

정확한 엔진 버전은 [docker-compose.yml](docker-compose.yml)이 소유합니다.

| Service | Technology | Role |
| :--- | :--- | :--- |
| **db** | PostgreSQL(pgvector) | 핵심 엔진 |
| **auth** | GoTrue | JWT 인증과 관리 |
| **rest** | PostgREST | 자동화된 REST API |
| **studio** | Supabase Studio | 통합 대시보드 |
| **kong** | Kong Gateway | API 게이트웨이 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `JWT_SECRET` | Yes | `supabase_jwt_secret`을 통한 Docker Secret 파일 |
| `POSTGRES_PASSWORD` | Yes | `supabase_db_password`를 통한 Docker Secret 파일 |
| `SUPABASE_PUBLIC_URL` | Leaf template only | upstream leaf 예시 값이며 root `.env` 입력으로 전달되지 않음 |

## Validation

Classification은 `OPTIONAL`입니다. 13개 서비스 모두 exact profile `supabase`를
사용합니다. 복구는 PostgreSQL globals/schema/data, Storage metadata와 오브젝트
파일, 마운트된 Kong/functions/pooler 설정, 보호된 Auth/JWT/SMTP/provider
설정을 새로운 격리된 스택에 함께 복원했을 때만 일관됩니다. 소유 artifact는
`GDE-0029`, `POL-0029`, `RUN-0029`입니다.

- Supabase에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- `docker compose --profile supabase config --quiet`로 Supabase 서비스, secret, database 참조가 정상 렌더링되는지 먼저 확인합니다.
- JWT, database, dashboard 설정을 변경하기 전에 Supabase 서비스 로그와 연결된 runbook을 확인합니다.

## Related Documents

- **Guide/Policy/Runbook**: `docs/05.operations/guides/0029-supabase.md`, `docs/05.operations/policies/0029-supabase.md`, `docs/05.operations/runbooks/0029-supabase.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift를 검증합니다.
