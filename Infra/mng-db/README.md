# Management Database Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 다른 인프라 서비스들이 공통으로 사용하거나 관리 목적으로 필요한 데이터베이스(PostgreSQL, Redis)를 정의합니다. 또한 Redis 데이터를 시각적으로 관리하기 위한 RedisInsight를 포함합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **mng-pg** | PostgreSQL Database | n8n, Keycloak 등 관리형 서비스들이 사용하는 메타데이터 저장소입니다. |
| **mng-pg-exporter**| Metrics Exporter | PostgreSQL의 상태와 성능 메트릭을 수집하여 Prometheus에 제공합니다. |
| **mng-redis** | In-Memory Store | n8n 큐 관리 등 빠른 데이터 처리가 필요한 서비스들이 사용하는 공용 Redis입니다. |
| **mng-redis-exporter**| Metrics Exporter | Redis 메트릭을 수집합니다. |
| **redisinsight** | Redis GUI | Redis 데이터를 웹 브라우저에서 조회하고 관리할 수 있는 도구입니다. SSO 인증이 적용되어 있습니다. |

## 3. 구성 및 설정 (Configuration)

### PostgreSQL (`mng-pg`)
- **초기화**: `./init/init_users_dbs.sql` 스크립트를 통해 초기 데이터베이스와 유저를 생성합니다.
- **포트**: 호스트 포트매핑을 통해 외부 접근이 가능합니다. (`POSTGRES_HOST_PORT`)

### Redis (`mng-redis`)
- **보안**: Docker Secret(`redis_password`)을 통해 비밀번호를 안전하게 관리합니다.
- **설정**: AOF(Append Only File)가 활성화되어 데이터 내구성을 높였습니다.

### RedisInsight
- **접속**: `https://redisinsight.${DEFAULT_URL}`
- **보안**: `sso-auth` 미들웨어가 적용되어 있어 로그인 후 접근 가능합니다.

### 네트워크
- `infra_net`을 통해 다른 서비스들과 통신합니다.
