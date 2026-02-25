# System Architecture

이 문서는 `hy-home.docker` 저장소의 전역 아키텍처 제약과 변경 규칙을 정의합니다.
서비스별 상세 설계는 [`docs/context/`](docs/context/), 실행 절차는 [`runbooks/`](runbooks/) 및 [`OPERATIONS.md`](OPERATIONS.md)를 기준으로 합니다.

## 1. Scope

- 대상: 루트 [`docker-compose.yml`](docker-compose.yml) + [`infra/**/docker-compose*.yml|yaml`](infra/)로 구성된 인프라 스택
- 목표: 로컬/홈랩 환경에서 재현 가능한 멀티 서비스 인프라 제공
- 제외: 개별 서비스 내부 비즈니스 로직, 앱 코드 구현 세부 ([`specs/`](specs/)에서 별도 정의)

## 2. Architectural Invariants

아래 항목은 기본 규칙이며, 예외는 ADR/Spec에 명시되어야 합니다.

- **Root Orchestration**: `docker-compose.yml`이 단일 진입점이며, 서비스 스택은 `include`로 조립합니다.
- **Modular Boundaries**: 서비스별 Compose는 `infra/<tier>/<service>/`에 분리하고, 공통 정책은 루트에서 관리합니다.
- **Secrets-First**: 비밀번호/토큰은 `.env`가 아닌 `secrets/**/*.txt` + Docker secrets로 주입합니다.
- **Port Policy**: 호스트 노출 포트는 `*_HOST_PORT`, 컨테이너 포트는 `*_PORT`를 사용합니다. Compose 파일에는 `${VAR:-default}`로 기본 포트를 명시합니다.
- **Security Baseline**: 기본적으로 `security_opt: [no-new-privileges:true]`, `cap_drop: [ALL]`를 적용합니다.
- **Docs Separation**: 아키텍처/배경은 [`docs/`](docs/), 구현 계획은 [`specs/`](specs/), 실행 절차는 [`runbooks/`](runbooks/)에 분리합니다.

## 3. Runtime Topology

### 3.1 Network Model

| Network | Type | Purpose |
| :--- | :--- | :--- |
| `infra_net` | bridge (internal) | 서비스 간 기본 통신망 |
| `project_net` | external | 외부 프로젝트 연동용 |
| `kind` | external | Kubernetes(kind) 연동용 |

`infra_net`의 대역/게이트웨이는 `.env`의 `INFRA_SUBNET`, `INFRA_GATEWAY`로 관리합니다.

### 3.2 Layered Service Map

| Tier | Role | 대표 서비스 |
| :--- | :--- | :--- |
| `01-gateway` | Ingress / Edge Routing | Traefik, Nginx |
| `02-auth` | Identity / Access Proxy | Keycloak, OAuth2 Proxy |
| `03-security` | Secret Vault | Vault |
| `04-data` | DB / Cache / Object / Search | PostgreSQL, Valkey, MinIO, OpenSearch, Qdrant, Supabase |
| `05-messaging` | Event / Queue | Kafka, ksqlDB, RabbitMQ |
| `06-observability` | Metrics / Logs / Traces | Prometheus, Grafana, Loki, Tempo, Alloy, Pyroscope |
| `07-workflow` | Orchestration | Airflow, n8n |
| `08-ai` | Inference / AI UI | Ollama, Open-WebUI |
| `09-tooling` | QA / DevOps Tools | SonarQube, Terrakube, Syncthing, Locust |
| `10-communication` | Mail / Relay | Stalwart, Mailhog |

### 3.3 Stack Modes

- **Core Include Stack**: 루트 `docker-compose.yml`에 활성 `include`된 서비스 세트
- **Optional Stack**: 프로파일 또는 주석 해제로 선택 활성화하는 서비스 세트
- **Standalone Stack**: 루트 `include` 없이 별도 Compose로 운영 가능한 서비스(예: Supabase)

## 4. Change Governance

아키텍처 변경 시 아래 체크리스트를 충족해야 합니다.

| Check | Requirement | Mandatory |
| :--- | :--- | :--- |
| Boundary Impact | 어떤 tier/서비스 경계를 바꾸는지 명시 | Yes |
| Network Impact | `infra_net`/external network 영향 분석 | Yes |
| Secret Impact | 신규/변경 secret 파일 경로 및 주입 방식 명시 | Yes |
| Port Impact | `*_HOST_PORT`/`*_PORT` 변수 및 기본값 영향 반영 | Yes |
| Security Baseline | 권한 상승(cap_add/privileged) 필요 시 근거 문서화 | Yes |
| Ops Impact | 관련 runbook/OPERATIONS 업데이트 | Yes |
| Validation | `bash scripts/validate-docker-compose.sh` 통과 | Yes |
| Traceability | ADR/Spec/Runbook 상호 링크 | Yes |

## 5. Architecture References

- 인프라 개요 ARD: [`docs/ard/infra-overview.md`](docs/ard/infra-overview.md)
- 메시징 ARD: [`docs/ard/messaging-requirements.md`](docs/ard/messaging-requirements.md)
- 기술 컨텍스트 허브: [`docs/context/README.md`](docs/context/README.md)
- 운영 정책: [`OPERATIONS.md`](OPERATIONS.md)
