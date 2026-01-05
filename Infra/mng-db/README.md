# Management DB (Mng-DB)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 시스템 관리 및 중요 데이터 저장을 위한 공용 데이터베이스 세트입니다. Redis(캐싱/세션)와 PostgreSQL(관계형 데이터) 인스턴스를 포함합니다.

**주요 기능 (Key Features)**:
- **Redis Cache**: 인증 세션, 임시 데이터 저장을 위한 인메모리 스토어.
- **Relational DB**: 서비스 설정, 사용자 정보 등을 위한 안정적인 RDBMS.
- **RedisInsight**: Redis 데이터를 시각적으로 관리할 수 있는 GUI 제공.

**기술 스택 (Tech Stack)**:
- **Redis**: 8.4.0 (Bookworm)
- **PostgreSQL**: 17 (Bookworm)
- **RedisInsight**: 2.70.1

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**시스템 구조도**:
```mermaid
graph TD
    App[애플리케이션] -->|Session| MngRedis
    App[애플리케이션] -->|Data| MngPg
    Admin[관리자] -->|GUI| RedisInsight
    RedisInsight -->|Monitor| MngRedis
```

## 3. 시작 가이드 (Getting Started)
**사전 요구사항 (Prerequisites)**:
- `infra_net` 외부 네트워크

**실행 방법 (Deployment)**:
```bash
docker compose up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**환경 변수 (Environment Variables)**:
| 변수명 | 설명 |
|---|---|
| `REDIS_PASSWORD` | Redis 접속 비밀번호 (Secret 사용) |
| `POSTGRES_USER` | PG 사용자명 |
| `POSTGRES_PASSWORD` | PG 비밀번호 |
| `POSTGRES_DB` | 초기 생성 DB명 |

**볼륨 마운트 (Volume Mapping)**:
- `mng-redis-data`: Redis 데이터 영속화
- `mng-pg-data`: PostgreSQL 데이터 영속화
- `redisinsight-data`: RedisInsight 설정 저장
- `./init/init_users_dbs.sql`: DB 초기화 스크립트

**네트워크 포트 (Network Ports)**:
- **Mng-Redis**: 6379 (Internal)
- **Mng-Pg**: 5432 (Internal)
- **RedisInsight**: 5540 (Internal, Traefik 노출)

## 5. 통합 및 API 가이드 (Integration Guide)
**엔드포인트 명세**:
- Redis Connection: `redis://:${REDIS_PASSWORD}@mng-redis:6379`
- Postgres Connection: `postgres://${USER}:${PASS}@mng-pg:5432/${DB}`
- RedisInsight UI: `https://redisinsight.${DEFAULT_URL}`

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인 (Health Check)**:
- Redis: `redis-cli ping`
- Postgres: `pg_isready`

**모니터링 (Monitoring)**:
- `mng-redis-exporter`: Redis 메트릭 수집
- `mng-pg-exporter`: Postgres 메트릭 수집

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**데이터 백업**:
- Redis: AOF(Append Only File) 활성화됨.
- Postgres: `pg_dump`를 통한 정기 백업 권장.

## 8. 보안 및 강화 (Security Hardening)
**보안 가이드라인**:
- RedisInsight는 `sso-auth` 미들웨어를 통해 Keycloak 인증 후 접근하도록 설정되어 있습니다.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Connection Refused**: 포트 및 네트워크 확인.
- **Auth Error**: 비밀번호 환경 변수 일치 여부 확인.

**진단 명령어**:
```bash
docker exec -it mng-redis redis-cli -a $REDIS_PASSWORD ping
docker exec -it mng-pg psql -U postgres
```
