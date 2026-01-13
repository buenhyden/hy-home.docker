# Docker Infrastructure & Enterprise Projects

## 개요 (Overview)

이 저장소는 로컬 개발, 테스트 및 소규모 운영 환경을 위한 **Docker Compose 기반의 통합 인프라 스택**입니다. 레이어드 아키텍처(Layered Architecture) 원칙에 따라 설계된 26개 이상의 엔터프라이즈급 서비스를 제공하며, 고가용성(HA), 보안(SSO), 그리고 관측성(Observability)에 최적화되어 있습니다.

## 📂 주요 구조 (Directory Structure)

- **[infra/](./infra/)**: 핵심 인프라 서비스 (Traefik, Keycloak, PostgreSQL HA, Kafka, LGTM 등)
- **[docs/](./docs/)**: 시스템 설계서, 네트워크 사양, 배포 및 운영 가이드
- **[scripts/](./scripts/)**: 대시보드 복구, 환경 설정 및 유지보수 자동화 스크립트
- **[secrets/](./secrets/)**: Docker Secrets 관리 디렉토리 (보안을 위해 Git 무시)

## 🎯 시스템 아키텍처 (System Architecture)

시스템은 상호 의존성을 최소화하고 확장성을 극대화하기 위해 8개 계층으로 분리되어 있습니다.

1. **Ingress & Security**: [Traefik](./infra/traefik/), [OAuth2 Proxy](./infra/oauth2-proxy/)
2. **Identity (IAM)**: [Keycloak SSO](./infra/keycloak/)
3. **Observability (LGTM)**: [Grafana](./infra/observability/grafana/), [Prometheus](./infra/observability/prometheus/), [Loki](./infra/observability/loki/), [Tempo](./infra/observability/tempo/)
4. **Data Persistence**: [PostgreSQL HA](./infra/postgresql-cluster/), [Valkey Cluster](./infra/valkey-cluster/), [InfluxDB](./infra/influxdb/)
5. **Messaging & Streaming**: [Kafka KRaft Cluster](./infra/kafka/)
6. **AI & Vector Ops**: [Ollama (LLM)](./infra/ollama/), [Qdrant](./infra/qdrant/)
7. **Object Storage**: [MinIO S3](./infra/minio/)
8. **DevOps & Automation**: [n8n](./infra/n8n/), [SonarQube](./infra/sonarqube/), [Harbor](./infra/harbor/)

> 📊 **상세 설계 및 서비스 의존성**: [시스템 아키텍처 명세서](./docs/architecture/system-architecture.md)

## 🚀 빠른 시작 (Quick Start)

### 1. 사전 요구사항 (Requirements)

- **OS**: Windows (Docker Desktop + WSL2) / Linux
- **Hardware**: CPU 8C / RAM 16GB (최소), 16C / 32GB (권장)
- **Tools**: Docker Compose v2.x, Git

### 2. 초기 설정 (Setup Secrets)

보안을 위해 비밀번호 파일을 직접 생성해야 합니다.

```bash
mkdir -p secrets
echo "strong_password" > secrets/postgres_password.txt
echo "another_password" > secrets/valkey_password.txt
# .env.example를 참고하여 필요한 설정을 완성하세요.
```

### 3. 기동 (Execution)

```bash
cd infra
docker compose up -d
```

## 📚 주요 문서 (Documentation Index)

| 구분 | 주요 내용 | 바로가기 |
| :--- | :--- | :--- |
| **핵심 설계** | 전체 계층 구조 및 서비스 상호 작용 | [시스템 아키텍처](./docs/architecture/system-architecture.md) |
| **네트워크** | 정적 IP 할당 및 Traefik 라우팅 규칙 | [네트워크 토폴로지](./docs/architecture/network-topology.md) |
| **운영 가이드** | 백업, 업데이트, 트러블슈팅 매뉴얼 | [유지보수 가이드](./docs/guides/maintenance.md) |
| **서비스 카탈로그** | 모든 서비스의 접속 URL 및 포트 정보 | [서비스 카탈로그](./docs/reference/service-catalog.md) |

## ⚠️ 주의사항 (Notes)

- **보안**: `secrets/` 디렉토리는 절대 Git에 커밋하지 마십시오.
- **리소스**: 전체 서비스를 동시에 가동할 경우 상당한 시스템 자원이 소모됩니다. 필요에 따라 `docker compose up -d <service_name>` 명령을 사용하여 선택적으로 기동하는 것을 권장합니다.

## 📄 라이선스 (License)

이 프로젝트는 개인 개발용 템플릿으로 제공됩니다.
