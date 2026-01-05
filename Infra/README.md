# Infrastructure Platform

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 개발 및 운영에 필요한 핵심 인프라 서비스들을 Docker Compose 기반으로 통합 관리하는 플랫폼입니다. 인증, 모니터링, 데이터베이스, 메시징 큐 등 모듈화된 마이크로서비스 아키텍처를 제공합니다.

**주요 기능 (Key Features)**:
- **Modular Architecture**: Docker Compose의 `include` 기능을 사용하여 서비스별 독립적 관리 및 유연한 조합 가능.
- **Unified Gateway**: Traefik을 통한 단일 진입점 및 자동 SSL/TLS 종단.
- **Centralized Auth**: Keycloak 및 OAuth2 Proxy를 이용한 통합 인증 (SSO).
- **Observability**: LGTM 스택(Loki, Grafana, Tempo, Prometheus)으로 전체 시스템 관측성 확보.

**기술 스택 (Tech Stack)**:
- **Orchestration**: Docker Compose v2.20+
- **Gateway**: Traefik v3
- **Observability**: Grafana, Prometheus, Loki, Tempo
- **Backing Services**: PostgreSQL, Redis, Kafka, MinIO

## 2. 아키텍처 및 워크플로우 (Architecture & Workflow)
**시스템 구조도**:
```mermaid
graph TD
    User[사용자] -->|HTTPS/443| Traefik[Traefik Gateway]
    Traefik -->|Auth Check| OAuth2[OAuth2 Proxy]
    OAuth2 -->|Validate| Keycloak[Keycloak IAM]
    Traefik -->|Route| App[애플리케이션 서비스]
    Traefik -->|Route| Tools[운영 도구 (Grafana/Kibana 등)]
    
    subgraph Observability
        App -->|Metrics| Prometheus
        App -->|Logs| Loki
        App -->|Traces| Tempo
        Prometheus & Loki & Tempo --> Grafana
    end

    subgraph Data Layer
        App --> Postgres[PostgreSQL Cluster]
        App --> Redis[Redis Cluster]
        App --> Kafka[Kafka Cluster]
    end
```

**네트워크**:
- 모든 서비스는 `infra_net` 브리지 네트워크(172.19.0.0/16)를 통해 상호 통신합니다.

## 3. 시작 가이드 (Getting Started)
**사전 요구사항 (Prerequisites)**:
- **Docker**: v24.0.0 이상
- **Docker Compose**: v2.20.0 이상 (`include` 문법 지원 필수)
- **SSL 인증서**: 로컬 개발 시 `mkcert` 설치 권장

**초기 설정 (Initial Setup)**:
1. **네트워크 생성**:
   ```bash
   docker network create infra_net
   ```
2. **환경 변수 구성**:
   `Infra/` 루트의 `.env.example`을 `.env`로 복사하고 환경에 맞게 수정합니다.
   ```bash
   cp .env.example .env
   ```
3. **인증서 발급**:
   각 서비스(Traefik 등)에서 참조하는 인증서 경로(`cis/certs` 등)에 인증서를 배치합니다.

**실행 방법 (Deployment)**:
전체 인프라를 한 번에 실행하거나 개별적으로 실행할 수 있습니다.
```bash
# 전체 실행 (Infra/ 폴더에서)
docker compose up -d

# 개별 서비스 실행 (예: DB만)
docker compose -f mng-db/docker-compose.yml up -d
```

## 4. 환경 설정 명세 (Configuration Reference)
**주요 환경 변수 (Environment Variables)**:
| 변수명 | 설명 | 기본값 예시 |
|---|---|---|
| `DEFAULT_URL` | 서비스 기본 도메인 | `localhost` |
| `HTTP_PORT` | Traefik HTTP 포트 | `80` |
| `HTTPS_PORT` | Traefik HTTPS 포트 | `443` |
| `TZ` | 시스템 타임존 | `Asia/Seoul` |

**볼륨 마운트 (Volume Mapping)**:
- 데이터 영속성이 필요한 서비스(DB, Prometheus 등)는 `volumes` 섹션에 정의된 명명된 볼륨(Named Volume)을 사용합니다.
- 예: `mng-pg-data`, `prometheus-data`, `kafka-1-data`

## 5. 통합 및 API 가이드 (Integration Guide)
**인증 전략 (Auth Strategy)**:
- 대부분의 관리 도구(Grafana, Airflow 등)는 **Keycloak SSO**와 연동되어 있습니다.
- API 접근 시 OAuth2 Proxy를 경유하거나 Bearer Token을 사용해야 합니다.

**주요 엔드포인트**:
- **Traefik Dashboard**: `https://dashboard.${DEFAULT_URL}`
- **Keycloak**: `https://keycloak.${DEFAULT_URL}`
- **Grafana**: `https://grafana.${DEFAULT_URL}`
- **Portainer**: `https://portainer.${DEFAULT_URL}` (선택 사항)

## 6. 가용성 및 관측성 (Availability & Observability)
**상태 확인 (Health Check)**:
- 각 모듈의 `docker-compose.yml`에는 `healthcheck` 블록이 정의되어 있습니다.
- `docker compose ps` 명령어로 전체 서비스 상태(`healthy`)를 확인할 수 있습니다.

**모니터링**:
- **Metrics**: `https://prometheus.${DEFAULT_URL}`
- **Unified View**: `https://grafana.${DEFAULT_URL}` (대시보드를 통해 통합 모니터링)

## 7. 백업 및 복구 (Backup & Disaster Recovery)
**백업 정책**:
- **Database**: PostgreSQL(`pg_dump`), Redis(`RDB/AOF`) 데이터는 주기적으로 백업해야 합니다.
- **Volume**: Docker Volume 데이터(`var/lib/docker/volumes/...`)를 백업 솔루션을 통해 스냅샷 하십시오.

## 8. 보안 및 강화 (Security Hardening)
**필수 체크리스트**:
1. **Secrets 관리**: `.env` 파일에 비밀번호를 평문으로 저장하지 말고, Docker Secrets 기능을 적극 활용하십시오.
2. **네트워크 격리**: 외부 노출이 필요 없는 DB 등의 포트는 호스트에 매핑하지 말고 내부 네트워크만 사용하십시오.
3. **TLS 적용**: 프로덕션 환경에서는 Let's Encrypt 또는 공인 인증서를 사용하여 HTTPS를 강제하십시오.

## 9. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Bind for 0.0.0.0:80 failed**: 호스트의 80포트가 이미 사용 중인지 확인하십시오 (`netstat -ano`).
- **Service Unhealthy**: `docker logs [컨테이너명]`으로 상세 로그를 확인하십시오. DB 연결 지연이 주원인일 수 있습니다.

**진단 명령어**:
```bash
# 전체 컨테이너 상태 요약
docker compose ps -a

# 특정 서비스 로그 확인 (실시간)
docker compose logs -f traefik
```

---

### 하위 서비스 문서 (Sub-Service Documentation)
- [**Auth**](./keycloak/README.md): Keycloak, OAuth2 Proxy
- [**Gateway**](./traefik/README.md): Traefik
- [**Databases**](./mng-db/README.md): Postgres, Redis, MinIO...
- [**Messaging**](./kafka/README.md): Kafka, Airflow
- [**Observability**](./observability/README.md): LGTM, Ollama
