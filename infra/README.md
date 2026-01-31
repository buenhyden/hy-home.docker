# Hy-Home Infrastructure (infra/)

이 디렉토리는 `Docker Compose`로 구축된 홈 서버/개발 환경 인프라의 **서비스 정의**를 관리합니다. 각 서비스는 `infra/서비스명/docker-compose.yml`에 분리되어 있으며, **저장소 루트의 `docker-compose.yml`에서 `include`** 기능으로 통합됩니다.

## 🏗️ 전체 구조

```text
infra/
├── [service]/                # 각 서비스별 설정 폴더
│   ├── docker-compose.yml    # 개별 서비스 정의
│   └── README.md             # 서비스별 상세 가이드
└── ...
```

## 🧭 실행 흐름

> **실행 진입점은 저장소 루트의 `docker-compose.yml`입니다.**

```bash
# 저장소 루트에서
cp .env.example .env
docker compose up -d
```

- `.env`와 `secrets/` 값은 루트 기준으로 관리됩니다.
- 특정 서비스만 실행하려면:

```bash
docker compose up -d traefik
```

## 🛠️ 주요 컴포넌트

현재 구성된 인프라는 다음과 같은 서비스들을 포함하고 있습니다.

### 1. Gateway & Security

- **Traefik**: 리버스 프록시 및 대시보드. SSL 종료 및 부하 분산 처리.
- **Keycloak**: 인증 및 인가 (SSO) 관리를 위한 중앙 인증 서버.
- **OAuth2 Proxy**: 인프라 서비스에 대한 통합 인증 계층 가동.
- **Nginx**: 경로 기반 라우팅/캐시가 필요한 경우 사용하는 보조 프록시 (옵션).
- **Vault**: 비밀번호, 토큰 등 민감 정보를 관리하는 보안 저장소 (옵션).

### 2. Databases (Persistence)

- **PostgreSQL Cluster**: Patroni를 사용한 고가용성 PG 클러스터.
- **Managed DB (mng-db)**: 관리용 PostgreSQL + Valkey + RedisInsight.
- **Valkey Cluster**: 고성능 인메모리 데이터 구조 저장소 클러스터.
- **Redis Cluster**: Redis 기반 클러스터 (옵션).
- **InfluxDB**: 시계열 데이터 저장소 (옵션).
- **CouchDB**: 문서형 NoSQL DB (옵션).
- **MinIO**: S3 호환 오브젝트 스토리지.
- **OpenSearch**: 검색/분석 및 대시보드.
- **Qdrant**: 벡터 데이터베이스 (RAG).
- **Supabase**: 자체 호스팅 BaaS 스택 (별도 실행).

### 3. Message Broker

- **Kafka Cluster**: 분산 스트리밍 플랫폼.
  - Kafka UI, Schema Registry, Rest Proxy, Connect, Exporter 포함.
- **ksqlDB**: Kafka 스트림 SQL 엔진.

### 4. Observability Stack

- **Prometheus**: 지표 수집 및 시계열 데이터베이스.
- **Grafana**: 지표 및 로그 시각화 대시보드.
- **Loki & Tempo**: 로그 및 분산 추적 데이터 처리.
- **Alloy**: 에이전트 기반 데이터 수집 도구.
- **Alertmanager**: 알림 정책 및 전송 관리.

### 5. AI & Workflow

- **Ollama**: 로컬 LLM 구동 엔진 및 Web UI.
- **Qdrant**: 벡터 데이터베이스 (RAG 구축용).
- **n8n / Airflow**: 워크플로우 자동화 및 데이터 파이프라인 관리.

### 6. Others

- **SonarQube**: 코드 품질 검사 도구 (옵션).
- **Storybook**: 디자인 시스템 템플릿.
- **Terraform / Terrakube**: IaC 실행 및 오케스트레이션.
- **MailHog**: 개발용 SMTP 테스트 서버 (옵션).
- **RabbitMQ**: 메시지 브로커 (구성 예정).

## 📌 서비스 인덱스

| 서비스 | 프로파일 | 경로 | 요약 |
| --- | --- | --- | --- |
| Traefik | - | `infra/traefik` | Edge Router, TLS, 라우팅/미들웨어 |
| Keycloak | - | `infra/keycloak` | 중앙 인증/인가 (SSO) |
| OAuth2 Proxy | - | `infra/oauth2-proxy` | ForwardAuth SSO 게이트 |
| Nginx | `nginx` | `infra/nginx` | 보조 리버스 프록시 |
| Vault | `vault` | `infra/vault` | 시크릿/키 관리 |
| mng-db | - | `infra/mng-db` | PostgreSQL + Valkey + RedisInsight |
| PostgreSQL Cluster | - | `infra/postgresql-cluster` | Patroni HA + HAProxy |
| Valkey Cluster | - | `infra/valkey-cluster` | 6노드 인메모리 클러스터 |
| Redis Cluster | `redis-cluster` | `infra/redis-cluster` | Redis 클러스터 (옵션) |
| InfluxDB | `influxdb` | `infra/influxdb` | TSDB (옵션) |
| CouchDB | `couchdb` | `infra/couchdb` | 3노드 CouchDB (옵션) |
| MinIO | - | `infra/minio` | S3 오브젝트 스토리지 |
| OpenSearch | - | `infra/opensearch` | 검색/대시보드/Exporter |
| Qdrant | - | `infra/qdrant` | 벡터 DB |
| Kafka | - | `infra/kafka` | KRaft + Confluent 스택 |
| ksqlDB | - | `infra/ksql` | 스트림 SQL (예제 데이터는 `examples` 프로파일) |
| Observability | - | `infra/observability` | Prometheus + Grafana + Loki + Tempo |
| n8n | - | `infra/n8n` | 워크플로우 자동화 (Queue) |
| Airflow | `airflow` | `infra/airflow` | 워크플로우 오케스트레이션 |
| Ollama | `ollama` | `infra/ollama` | 로컬 LLM + WebUI |
| SonarQube | `sonarqube` | `infra/sonarqube` | 코드 품질 분석 |
| Storybook | - | `infra/storybook` | 디자인 시스템 템플릿 |
| Terraform | - | `infra/terraform` | Terraform CLI 컨테이너 |
| Terrakube | `terrakube` | `infra/terrakube` | Terraform 오케스트레이션 |
| Mail | `mail` | `infra/mail` | MailHog 테스트 SMTP |
| Supabase | - | `infra/supabase` | 자체 호스팅 Supabase 스택 (별도 실행) |
| RabbitMQ | - | `infra/rabbitmq` | Placeholder (구성 예정) |

## ⚙️ 설정 가이드

### 서비스 실행

메인 디렉토리에서 아래 명령어를 사용하여 전체 인프라를 구동할 수 있습니다.

```bash
docker compose up -d
```

특정 서비스만 실행하려면 메인에서 서비스를 지정할 수 있습니다.

### 프로파일(Profiles)로 선택 실행

일부 스택은 **프로파일로 비활성화**되어 있으며 필요할 때만 켤 수 있습니다.

```bash
# 예: Airflow와 Ollama만 켜기
docker compose --profile airflow --profile ollama up -d
```

현재 사용 중인 프로파일:
- `airflow` (기본 Airflow 스택)
- `debug` (Airflow 디버그 구성)
- `flower` (Airflow 모니터링 UI)
- `influxdb`
- `couchdb`
- `mail`
- `nginx`
- `ollama`
- `sonarqube`
- `vault`
- `terrakube`
- `redis-cluster`
- `examples` (KSQL/예제 스택)

## ➕ 서비스 추가 방법

1. `infra/서비스명/` 디렉토리를 생성하고 `docker-compose.yml`을 작성합니다.
2. 필요 시 `profiles`를 지정해 선택 실행 가능한 스택으로 분리합니다.
3. 루트 `docker-compose.yml`의 `include`에 새 서비스를 추가합니다.
4. 환경 변수가 필요하면 루트 `.env.example`에 추가하고, 민감 값은 `secrets/`에 `*.txt`로 분리합니다.
5. 문서 반영: `infra/README.md`에 서비스 요약을 추가하고 `docs/README.md` 및 `docs/ops/README.md`에 관련 내용을 업데이트합니다.

## 📝 참고 사항

- **환경 파일**: `.env.example`와 `.env`는 저장소 루트에서 관리됩니다.
- **볼륨 경로**: 반드시 호스트 컴퓨터의 실제 경로를 `.env` 파일에 지정해야 데이터가 유실되지 않습니다.
- **네트워크**: `infra_net`이라는 브리지 네트워크를 통해 내부 서비스 간 통신이 이루어집니다.
  - `INFRA_SUBNET`, `INFRA_GATEWAY`로 네트워크 대역을 변경할 수 있습니다.

### 운영 헬퍼 스크립트 (PowerShell)

```powershell
# 예: 프로파일 포함 기동
.\scripts\infra-compose.ps1 -Action up -Profiles airflow,ollama

# 로그 확인
.\scripts\infra-compose.ps1 -Action logs -Args "-f" -Services alertmanager

# 특정 서비스만 기동
.\scripts\infra-compose.ps1 -Action up -Profiles observability -Services prometheus,grafana
```
