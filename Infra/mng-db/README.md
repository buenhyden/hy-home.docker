# 관리용 데이터베이스 (mng-db)

## 시스템 아키텍처에서의 역할

mng-db는 **관리 및 메타데이터용 단일 PostgreSQL + Redis**로 구성된 경량 데이터베이스 스택입니다. 주로 Keycloak, n8n 등 인프라 서비스의 메타데이터와 상태 정보를 저장하는 전용 데이터베이스

입니다.

**핵심 역할:**

- 🗄️ **메타데이터 저장**: 인프라 서비스 설정 및 상태
- 🔐 **인증 데이터**: Keycloak 사용자/세션 정보
- 📊 **단순성**: 클러스터 불필요한 관리용 단일 인스턴스
- 📈 **모니터링**: Exporter를 통한 메트릭 수집

## 구성 요소

### 1. mng-postgres

- **컨테이너**: `mng-pg`
- **이미지**: `postgres:17-bookworm`
- **포트**: `${POSTGRES_HOST_PORT}:${POSTGRES_PORT}` (기본 5433:5432)
- **IP**: 172.19.0.72

### 2. mng-redis  

- **컨테이너**: `mng-redis`
- **이미지**: `redis:8.4.0-bookworm`
- **포트**: 6379 (내부)
- **IP**: 172.19.0.70

### 3. RedisInsight (GUI)

- **컨테이너**: `redisinsight`
- **이미지**: `redis/redisinsight:2.70`
- **역할**: Redis 클러스터 관리 및 모니터링 GUI
- **포트**: `${REDIS_INSIGHT_PORT}` (기본 5540)
- **Traefik 통합**: `https://redisinsight.${DEFAULT_URL}`
- **인증**: Keycloak SSO (`sso-auth@file` 미들웨어)
- **볼륨**: `redisinsight-data:/db`
- **IP**: 172.19.0.68

**기능:**

- 클러스터 토폴로지 시각화
- 키 브라우저 및 검색
- CLI 인터페이스
- 쿼리 프로파일러
- Pub/Sub 모니터링

### 4. Exporters

- **pg-exporter**: 172.19.0.73
- **redis-exporter**: 172.19.0.71

## 환경 변수

```bash
POSTGRES_HOST_PORT=5433
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_DB=postgres
PGPASSWORD_SUPERUSER=<password>
REDIS_PORT=6379
```

## 사용하는 서비스

- Keycloak
- 기타 관리 서비스

## 참고 자료

- [PostgreSQL 문서](https://www.postgresql.org/docs/17/)
- [Redis 문서](https://redis.io/documentation)
