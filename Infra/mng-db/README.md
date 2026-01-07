# Management Database (Mng-DB)

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 인프라의 공통 관리 및 모니터링을 위한 핵심 데이터베이스 세트입니다.  
고성능 인메모리 저장소인 Redis와 신뢰성 있는 관계형 데이터베이스인 PostgreSQL을 통합하여 제공하며, 각 서비스의 메타데이터, 세션, 캐시 등을 중앙에서 관리합니다.

## 2. 주요 기능 (Key Features)
- **Shared Infrastructure**: 여러 서비스(Grafana, Keycloak, 등)에서 공통으로 사용하는 DB 인프라.
- **Monitoring Integration**: 각 DB 인스턴스에 Exporter가 사이드카로 배치되어 Prometheus 모니터링과 즉시 연동됨.
- **Management UI**: RedisInsight를 통해 Redis 데이터를 시각적으로 관리 가능.
- **High Security**: 비밀번호의 Secret 관리 및 데이터 암호화 통신 지원.

## 3. 기술 스택 (Tech Stack)
- **Redis**: `redis:8.4.0-bookworm` (Cache & Session)
- **PostgreSQL**: `postgres:17-bookworm` (Persistant Data)
- **UI**: `redis/redisinsight:2.70.1`

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 컴포넌트 구조
1.  **Mng-Redis**: 애플리케이션 캐싱 및 세션 저장소.
    - **Exporter**: 메트릭 수집용 사이드카 (`mng-redis-exporter`).
2.  **Mng-Pg**: 서비스 메타데이터 저장소.
    - **Exporter**: 메트릭 수집용 사이드카 (`mng-pg-exporter`).
3.  **RedisInsight**: Redis 데이터 관리 및 분석을 위한 웹 GUI.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **초기화**: `mng-pg` 실행 시 `./init/init_users_dbs.sql` 스크립트가 실행되어 필요한 데이터베이스와 사용자를 자동으로 생성합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 RedisInsight 활용
1.  **접속**: `https://redisinsight.${DEFAULT_URL}`
2.  **로그인**: Keycloak SSO 인증 (Traefik Middleware).
3.  **DB 연결**:
    - **Host**: `mng-redis`
    - **Port**: `6379`
    - **Username**: (공란)
    - **Password**: `redis_password` Secret 값.
    - **TLS**: `No` (내부망 통신).

### 6.2 데이터베이스 접속 (CLI)
컨테이너 내부에서 직접 접속하여 관리할 수 있습니다.

**Redis CLI**:
```bash
docker exec -it mng-redis redis-cli -a "$REDIS_PASSWORD" ping
```

**PostgreSQL CLI**:
```bash
docker exec -it mng-pg psql -U postgres
# DB 목록 확인
\l
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
**Redis**:
- `REDIS_PASSWORD`: Docker Secret(`/run/secrets/redis_password`)에서 로드.

**PostgreSQL**:
- `POSTGRES_USER`: 수퍼유저 ID.
- `POSTGRES_PASSWORD`: 수퍼유저 비밀번호 (Secret 권장).
- `POSTGRES_DB`: 기본 생성 DB명.

### 볼륨 마운트 (Volumes)
- `mng-redis-data`: Redis AOF/RDB 데이터 파일.
- `mng-pg-data`: PostgreSQL 데이터 디렉토리 (`/var/lib/postgresql/data`).

### 네트워크 포트 (Ports)
- **Redis**: 6379 (Internal)
- **PostgreSQL**: 5432 (Internal)
- **RedisInsight**: 5540 (GUI, `https://redisinsight.${DEFAULT_URL}`)

## 8. 통합 및 API 가이드 (Integration Guide)
**Connection Strings (Internal Service용)**:
- **Redis**: `redis://:${REDIS_PASSWORD}@mng-redis:6379`
- **Postgres**: `postgresql://${USER}:${PASS}@mng-pg:5432/${DB_NAME}`

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- **Redis**: `redis-cli ping` 명령으로 주기적 헬스체크 수행.
- **Postgres**: `pg_isready` 명령 사용.

**Monitoring**:
- **Redis**: `mng-redis-exporter`가 9121 포트에서 메트릭 제공.
- **Postgres**: `mng-pg-exporter`가 9187 포트에서 메트릭 제공.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**백업 정책**:
- **Redis**: `appendonly yes` 설정으로 모든 쓰기 작업을 로그에 기록하여 내구성을 확보합니다. Volume 백업 필요.
- **PostgreSQL**: 프로덕션 환경에서는 주기적인 `pg_dump` 또는 `WAL Archiving`을 통한 백업(예: pgBackRest)을 구성해야 합니다.

## 11. 보안 및 강화 (Security Hardening)
- **Network Isolation**: DB 포트(6379, 5432)는 외부에 직접 노출하지 않고 Docker Network 내부에서만 접근 가능하도록 설정되어 있습니다.
- **Authentication**: RedisInsight는 Traefik의 Keycloak 미들웨어를 통해 인증된 사용자만 접근할 수 있습니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Authentication Failed**: 비밀번호가 Secret 파일 내용과 일치하지 않는 경우. `docker-compose.yml`의 Secret 정의를 확인하세요.
- **Locked DB**: PostgreSQL의 트랜잭션 충돌로 인한 Lock 발생 시 `pg_stat_activity` 뷰를 확인하여 락킹 세션을 정리하십시오.

---
**공식 문서**:
- Redis: [https://redis.io/docs/](https://redis.io/docs/)
- PostgreSQL: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
