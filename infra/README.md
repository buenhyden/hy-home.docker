# Hy-Home Infrastructure

이 저장소는 `Docker Compose`를 사용하여 구축된 홈 서버 및 개발 환경 인프라의 설정 파일들을 관리합니다. 각 서비스는 독립적인 폴더 내의 `docker-compose.yml`을 통해 관리되며, 메인 `infra/docker-compose.yml`에서 `include` 기능을 통해 통합됩니다.

## 🏗️ 전체 구조

```text
infra/
├── .env.example              # 공통 환경 변수 템플릿
├── docker-compose.yml        # 메인 오케스트레이션 파일 (include 기반)
├── [service]/                # 각 서비스별 설정 폴더
│   ├── docker-compose.yml    # 개별 서비스 정의
│   └── README.md             # 서비스별 상세 가이드
└── ...
```

## 🛠️ 주요 컴포넌트

현제 구성된 인프라는 다음과 같은 서비스들을 포함하고 있습니다.

### 1. Gateway & Security

- **Traefik**: 리버스 프록시 및 대시보드. SSL 종료 및 부하 분산 처리.
- **Keycloak**: 인증 및 인가 (SSO) 관리를 위한 중앙 인증 서버.
- **OAuth2 Proxy**: 인프라 서비스에 대한 통합 인증 계층 가동.
- **Vault**: 비밀번호, 토큰 등 민감 정보를 관리하는 보안 저장소.

### 2. Databases (Persistence)

- **PostgreSQL Cluster**: Patroni를 사용한 고가용성 PG 클러스터.
- **Managed DB (mng-db)**: 관리용 독립 호스트 PostgreSQL 및 Redis 인스턴스.
- **Redis & Valkey Cluster**: 고성능 인메모리 데이터 구조 저장소 클러스터.
- **InfluxDB**: 시계열 데이터 가공 및 저장소.
- **CouchDB / MongoDB**: NoSQL 문서형 데이터베이스 (필요 시 활성화).

### 3. Message Broker

- **Kafka Cluster**: 분산 스트리밍 플랫폼.
  - Kafka UI, Schema Registry, Rest Proxy, Connect, Exporter 포함.

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

- **Minio**: S3 호환 오브젝트 스토리지.
- **SonarQube**: 코드 품질 검사 도구.
- **Wiki.js**: 기술 문서 관리 및 공유 위키.

## ⚙️ 설정 가이드

### 환경 변수 설정

1. `.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.

   ```bash
   cp .env.example .env
   ```

2. `.env` 파일 내의 각 서비스별 경로 및 포트, 비밀번호 설정을 사용자의 환경에 맞게 수정합니다.
   - `DEFAULT_URL`: 서비스 접속 도메인 (기본값: `127.0.0.1.nip.io`)
   - `DEFAULT_MOUNT_VOLUME_PATH`: 볼륨 데이터가 저장될 호스트 경로

### 서비스 실행

메인 디렉토리에서 아래 명령어를 사용하여 전체 인프라를 구동할 수 있습니다.

```bash
docker compose up -d
```

특정 서비스만 실행하려면 각 서비스 폴더로 이동하거나 메인에서 서비스를 지정할 수 있습니다.

### 프로파일(Profiles)로 선택 실행

일부 스택은 **프로파일로 비활성화**되어 있으며 필요할 때만 켤 수 있습니다.

```bash
# 예: Airflow와 Ollama만 켜기
docker compose --profile airflow --profile ollama up -d
```

현재 사용 중인 프로파일:
- `airflow`
- `influxdb`
- `couchdb`
- `mail`
- `nginx`
- `ollama`
- `sonarqube`
- `vault`
- `terrakube`
- `redis-cluster`

## 📝 참고 사항

- **볼륨 경로**: 반드시 호스트 컴퓨터의 실제 경로를 `.env` 파일에 지정해야 데이터가 유실되지 않습니다.
- **네트워크**: `infra_net`이라는 브리지 네트워크를 통해 내부 서비스 간 통신이 이루어집니다.
