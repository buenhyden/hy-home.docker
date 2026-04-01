# Standardize `infra_net` Technical Specification

## Overview (KR)

이 문서는 모든 인프라 서비스에 `infra_net` 네트워크를 적용하고 서브넷을 `172.19.0.0/16`으로 고정하기 위한 상세 지침을 정의한다. 이는 PRD의 요구사항을 구체적인 Docker Compose 설정값으로 변환한 명세다.

## Strategic Boundaries & Non-goals

- **SPEC Owns**:
  - 루트 `docker-compose.yml`의 `networks` IPAM 설정.
  - 각 서비스별 `networks` 블록에 `infra_net` 추가.
  - 기존 서비스의 고정 IP 할당값 유지.
- **SPEC Does Not Own**:
  - `project_net` 등 다른 네트워크의 IPAM 변경.
  - 컨테이너 내부의 `/etc/hosts` 직접 수정 (Docker DNS 활용 권장).

## Related Inputs

- **PRD**: `[../../01.prd/2026-04-01-standardize-infra-net.md]`
- **ARD**: `[../../02.ard/0026-standardize-infra-net.md]`
- **Related ADRs**: `[../../03.adr/0026-standardize-infra-net.md]`

## Contracts

- **Config Contract**:
  - `networks.infra_net.ipam.config.subnet` == `172.19.0.0/16`
  - `services.*.networks` list must contain `infra_net`.
- **Governance Contract**:
  - `include`된 파일의 모든 서비스는 전역 `infra_net`을 참조해야 함.
  - `k3d-hyhome` 설정이 있는 경우 절대 삭제하지 않음.

## Core Design

- **Component Boundary**: Docker Compose 런타임 환경.
- **Key Dependencies**: Docker Compose V2.20+ (`include` 지원).
- **Tech Stack**: YAML, Docker Engine.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Docker Compose `networks` 및 `services.networks` 스키마 준수.
- **Transition Plan**:
  1. 루트 파일의 IPAM 설정 확인/수정.
  2. 개별 서비스 파일 순차 수정.
  3. `docker compose config`로 병합 결과 검증.

## Interfaces & Data Structures

### Network Definition Example (Root)

```yaml
networks:
  infra_net:
    name: infra_net
    driver: bridge
    ipam:
      config:
        - subnet: ${INFRA_SUBNET:-172.19.0.0/16}
          gateway: ${INFRA_GATEWAY:-172.19.0.1}
```

### Assigned IP Mapping Table (Authoritative)

| IP Address | Service Name / Group | Folder Path |
| :--- | :--- | :--- |
| `172.19.0.5` | oauth2-proxy-valkey | `infra/02-auth/oauth2-proxy` |
| `172.19.0.7` | registry | `infra/09-tooling/registry` |
| `172.19.0.11-16` | Relational / Mng DB Core | `infra/04-data/relational`, `operational` |
| `172.19.0.20-28` | Observability Stack | `infra/06-observability` |
| `172.19.0.30-38` | Kafka Stack | `infra/05-messaging/kafka` |
| `172.19.0.50-59` | PostgreSQL Cluster | `infra/04-data/relational/postgresql-cluster` |
| `172.19.0.61` | Neo4j | `infra/04-data/specialized/neo4j` |
| `172.19.0.80-85` | n8n Workflow | `infra/07-workflow/n8n` |
| `172.19.0.90-100` | Airflow Workflow | `infra/07-workflow/airflow` |
| `172.19.0.120` | Terraform / Atlantis | `infra/09-tooling/terraform` |
| `172.19.0.121` | RedisInsight | `infra/11-laboratory/redisinsight` |
| `172.19.0.150-151` | Cassandra | `infra/04-data/nosql/cassandra` |
| `172.19.0.160-163` | CouchDB | `infra/04-data/nosql/couchdb` |
| `172.19.0.170-175` | MongoDB | `infra/04-data/nosql/mongodb` |
| `172.19.0.179-191` | Supabase Stack | `infra/04-data/operational/supabase` |
| `172.19.0.200` | RabbitMQ | `infra/05-messaging/rabbitmq` |
| `172.19.0.201` | Ollama | `infra/08-ai/ollama` |
| `172.19.0.202` | Qdrant | `infra/04-data/specialized/qdrant` |
| `172.19.0.211` | Ollama Exporter | `infra/08-ai/ollama` |
| `172.19.0.220` | Portainer | `infra/11-laboratory/portainer` |
| `172.19.0.221` | Dozzle | `infra/11-laboratory/dozzle` |
| `172.19.0.222` | Homer Dashboard | `infra/11-laboratory/dashboard` |
| `172.19.0.223` | SonarQube | `infra/09-tooling/sonarqube` |
| `172.19.0.224` | Syncthing | `infra/09-tooling/syncthing` |
| `172.19.0.225-227` | Terrakube API/UI/Executor | `infra/09-tooling/terrakube` |
| `172.19.0.250` | Locust Master | `infra/09-tooling/locust` |
| `172.19.0.251` | Open-WebUI | `infra/08-ai/open-webui` |
| `172.19.0.253` | Locust Worker | `infra/09-tooling/locust` |
| `172.19.0.260-261` | Stalwart Mail / MailHog | `infra/10-communication/mail` |

### Service Assignment Example

```yaml
services:
  example-service:
    networks:
      infra_net:
        ipv4_address: 172.19.0.X # Existing or Auto
      k3d-hyhome: # Must be preserved if exists
        ipv4_address: 172.18.0.X
```

## Edge Cases & Error Handling

- **Error 1: IP Conflict**: 이미 할당된 정적 IP가 새 서브넷 범위를 벗어날 경우 수정 필요.
- **Error 2: Multiple Default Networks**: 네트워크를 명시적으로 지정하지 않은 서비스가 `infra_net`에 합류할 때 기존 default 네트워크와의 통신 확인.

## Verification

```bash
# 전체 설정의 무결성 검사
docker compose config
# infra_net 서브넷 확인
docker compose config | grep -A 5 "infra_net:"
# k3d-hyhome 유지 확인
docker compose config | grep "k3d-hyhome"
```

## Related Documents

- **Plan**: `[../../05.plans/2026-04-01-standardize-infra-net.md]`
- **Tasks**: `[../../06.tasks/2026-04-01-standardize-infra-net.md]`
- **Runbook**: `[../../09.runbooks/0012-standardize-infra-net.md]`
