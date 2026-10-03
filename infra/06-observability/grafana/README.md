---
title: "Grafana 시각화와 대시보드"
version: "1.1.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-01-12"
---

# Grafana 시각화와 대시보드

## Overview

`infra/06-observability/grafana`에는 `06-observability` 티어의 Grafana 구현이 들어 있습니다. Grafana는 compose 서비스 `grafana`, 컨테이너 `infra-grafana`, 이미지 [declared runtime image](../../tech-stack.versions.json)로 실행되며 런타임 상태를 `grafana-data`에 저장하고 프로비저닝 및 대시보드 트리를 읽기 전용으로 마운트하며 접근 제어에는 Keycloak Generic OAuth 역할 매핑을 사용합니다.

## Audience

- 메트릭, 로그, 트레이스, 알림, 프로파일을 탐색하는 Developers
- 데이터소스와 대시보드 프로비저닝을 유지 관리하는 SREs
- SSO, 대시보드, 데이터소스 장애를 처리하는 Operators
- 시크릿이나 토큰을 노출하지 않고 마스킹된 근거를 수집하는 AI Agents

## Scope

### In Scope

- Grafana compose 서비스와 보호된 라우트 `https://grafana.${DEFAULT_URL}`
- `provisioning/datasources/datasource.yml`의 데이터소스 프로비저닝
- `provisioning/dashboards/dashboards.yml`의 대시보드 프로비저닝
- `dashboards/`의 대시보드 JSON 파일
- Keycloak Generic OAuth 역할 매핑과 Docker Secret 파일 참조

### Out of Scope

- JSON으로 내보내지 않은 UI 전용 대시보드 변경
- Grafana compose 경계 밖의 Keycloak realm/client 변경
- Prometheus, Loki, Tempo, Pyroscope가 관리하는 백엔드 텔레메트리 저장소
- 운영 근거 없이 이루어지는 런타임 역할 매핑, 시크릿, 라우트, 이미지, 프로비저닝 정책 변경

## Structure

```text
grafana/
├── dashboards/       # Provisioned dashboard JSON tree
├── provisioning/
│   ├── dashboards/   # Dashboard provider YAML
│   └── datasources/  # Datasource provisioning YAML
└── README.md         # This file
```

## Service Boundary

| Field | Evidence |
| --- | --- |
| Purpose | `06-observability` 티어의 메트릭, 로그, 트레이스, 알림, 프로파일 시각화 허브 |
| Compose service | `infra/06-observability/docker-compose.yml`의 `grafana` |
| Compose linkage | `infra/06-observability/docker-compose.yml`에 선언됨 |
| Container | `infra-grafana` |
| Image | [declared runtime image](../../tech-stack.versions.json) |
| Config files | `provisioning/datasources/datasource.yml`, `provisioning/dashboards/dashboards.yml`, 대시보드 JSON 파일 |
| Config values | 데이터소스 UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`; Pyroscope 데이터소스 타입 `grafana-pyroscope-datasource`; 대시보드 프로바이더 `editable: false`; `/admins`, `/editors` 역할 매핑 |
| Volumes | `./grafana/provisioning:/etc/grafana/provisioning:ro`, `./grafana/dashboards:/etc/grafana/dashboards:ro`, `grafana-data:/var/lib/grafana:rw` |
| Secret refs | `grafana_admin_password`, `grafana_client_secret` |
| Networks | `edge_net`, `obs_net` |
| Ports | `traefik.http.services.grafana-svc.loadbalancer.server.port: ${GRAFANA_PORT:-3000}` |
| Labels | `traefik.http.routers.grafana.*`, `traefik.http.routers.grafana-static.*`, `traefik.http.services.grafana-svc.*` |
| Healthcheck | `http://localhost:${GRAFANA_PORT:-3000}/api/health` |
| Operations | Guide (`docs/05.operations/guides/0041-grafana.md`), Policy (`docs/05.operations/policies/0041-grafana.md`), Runbook (`docs/05.operations/runbooks/0041-grafana.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh), [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 연결된 런북, compose 설정 렌더링, 서비스 로그, 헬스체크, 마스킹된 OAuth/데이터소스 근거로 시작합니다 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile obs up -d grafana` | 저장소 루트에서 Grafana 시작 |
| `docker compose --profile obs restart grafana` | 이미 연결된 provisioning·dashboard 파일 내용의 승인된 재적용; Compose 환경·시크릿 참조·이미지 변경에는 RUN-0041의 재생성 절차 사용 |
| `docker compose --profile obs logs -f grafana` | 저장소 루트에서 Grafana 로그 확인 |

## Tech Stack

Grafana 이미지와 데이터 소스 선언은 [Compose](docker-compose.yml)와 이 패키지의 provisioning 설정이 소유합니다.

## Configuration

### Datasources

- **Prometheus**: `uid: Prometheus`, URL `http://prometheus:9090`
- **Loki**: `uid: Loki`, URL `http://loki:3100`
- **Tempo**: `uid: Tempo`, URL `http://tempo:3200`, `tracesToLogsV2`가 `Loki`와 연결됨
- **Alertmanager**: `uid: alertmanager`, URL `http://alertmanager:9093`
- **Pyroscope**: 데이터소스 타입 `grafana-pyroscope-datasource`, URL `http://pyroscope:4040`

### Dashboards and Access

- 대시보드 프로바이더는 `/etc/grafana/dashboards/*`에서 JSON 파일을 마운트합니다.
- 프로바이더 `editable: false`는 대시보드를 코드 소유 상태로 유지합니다.
- 대시보드 보유 현황과 서비스별 매핑은 아래 Service Coverage와 Dashboard Sources 표가 기준이며, `tests/validation/test_compose_baseline_gates.py`의 대시보드 계약 테스트가 표와 파일을 대조합니다.
- Keycloak 그룹 `/admins`, `/editors`, `/viewers`는 각각 Grafana `Admin`, `Editor`, `Viewer`로 매핑됩니다. OAuth role mapping은 strict이므로 역할이 없는 사용자의 `Viewer` fallback을 보장하지 않습니다. 일반 조직 기본 역할과 OAuth 수용 조건을 구분합니다.
- `grafana_admin_password`와 `grafana_client_secret`은 Docker Secret 파일 참조를 통해 주입됩니다.

### Service Coverage

정상 root에 포함되는 모든 infra Compose 서비스가 한 번씩 나옵니다. LAB 서비스는 독립 Compose와 LAB 문서에서 확인합니다. 컨테이너 대시보드와 Logs Drilldown은 전체를 다루고, 메트릭 소스가 있는 서비스는 자기 대시보드를 따로 가집니다. Metrics source가 `none`이면 이 스택이 수집하는 메트릭이 없다는 뜻입니다(SPEC-0193).

| Layer | Service | Metrics source | Dashboards | Note |
| --- | --- | --- | --- | --- |
| 01-gateway | `nginx` | none | `Infrastructure/containers` | container metrics and logs only |
| 01-gateway | `traefik` | `traefik` | `Gateway/traefik`, `Infrastructure/containers` |  |
| 02-auth | `keycloak` | `keycloak` | `Security/keycloak-troubleshooting`, `Security/keycloak-capacity-planning`, `Infrastructure/containers` |  |
| 02-auth | `oauth2-proxy` | `oauth2-proxy` | `Gateway/oauth2-proxy`, `Infrastructure/containers` |  |
| 02-auth | `oauth2-proxy-valkey` | `oauth2-proxy-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 02-auth | `oauth2-proxy-valkey-exporter` | `oauth2-proxy-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 03-security | `openbao` | `openbao` | `Security/openbao`, `Infrastructure/containers` |  |
| 03-security | `openbao-agent` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `analytics` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `auth` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `db` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `flink-jobmanager` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `flink-taskmanager` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `functions` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `great-expectations` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `imgproxy` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `influxdb` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `kong` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `meta` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `mng-pg` | `manage-postgres` | `Infrastructure/postgresql`, `Infrastructure/containers` |  |
| 04-data | `mng-pg-exporter` | `manage-postgres` | `Infrastructure/postgresql`, `Infrastructure/containers` |  |
| 04-data | `mng-pg-init` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `mng-valkey` | `mng-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 04-data | `mng-valkey-exporter` | `mng-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 04-data | `neo4j` | none | `Infrastructure/containers` | Community edition has no metrics endpoint |
| 04-data | `opensearch` | `opensearch` | `Infrastructure/opensearch-cluster`, `Infrastructure/opensearch-node`, `Infrastructure/opensearch-search-and-index`, `Infrastructure/containers` |  |
| 04-data | `opensearch-dashboards` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `qdrant` | `qdrant` | `Infrastructure/qdrant-overview`, `Infrastructure/containers` |  |
| 04-data | `realtime` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `rest` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `seaweedfs-buckets` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `seaweedfs-filer` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `seaweedfs-master` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `seaweedfs-s3` | `seaweedfs-s3` | `Infrastructure/seaweedfs`, `Infrastructure/containers` |  |
| 04-data | `seaweedfs-table-bucket` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `seaweedfs-volume` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `spark` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `storage` | none | `Infrastructure/containers` | container metrics and logs only |
| 13-experience | `storybook` | none | `Infrastructure/containers` | 소스 선언만; 지표 scrape 미정의 |
| 04-data | `studio` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `supavisor` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `superset` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `superset-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `superset-init` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `trino` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `vector` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `dev-pg` | none | `Infrastructure/containers` | source only; metrics scrape not declared |
| 04-data | `dev-perf-provision` | none | `Infrastructure/containers` | 소스 선언만; 지표 scrape 미정의 |
| 04-data | `dev-platform-provision` | none | `Infrastructure/containers` | source only; metrics scrape not declared |
| 04-data | `dev-valkey` | none | `Infrastructure/containers` | source only; metrics scrape not declared |
| 05-messaging | `debezium-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 05-messaging | `kafbat-ui` | none | `Infrastructure/containers` | container metrics and logs only |
| 05-messaging | `kafka-1` | `kafka-broker` | `Infrastructure/kafka-cluster`, `Infrastructure/kafka-topics`, `Infrastructure/containers` |  |
| 05-messaging | `kafka-connect` | `kafka-connect` | `Infrastructure/kafka-connect`, `Infrastructure/containers` |  |
| 05-messaging | `kafka-exporter` | `kafka-exporter` | `Infrastructure/kafka-consumer-lag`, `Infrastructure/containers` |  |
| 05-messaging | `kafka-init` | none | `Infrastructure/containers` | container metrics and logs only |
| 05-messaging | `kafka-rest-proxy` | none | `Infrastructure/containers` | container metrics and logs only |
| 05-messaging | `schema-registry` | `schema-registry` | `Infrastructure/schema-registry`, `Infrastructure/containers` |  |
| 06-observability | `alertmanager` | `alertmanager` | `Observability/alertmanager-overview`, `Infrastructure/containers` |  |
| 06-observability | `alloy` | `alloy` | `Observability/alloy-controller`, `Observability/alloy-resources`, `Observability/alloy-opentelemetry`, `Observability/alloy-loki`, `Infrastructure/containers` |  |
| 06-observability | `cadvisor` | `cadvisor` | `Infrastructure/containers` |  |
| 06-observability | `dcgm-exporter` | `dcgm-exporter` | `Infrastructure/dcgm-exporter`, `Infrastructure/containers` |  |
| 06-observability | `gatus` | `gatus` | `Observability/gatus`, `Infrastructure/containers` |  |
| 06-observability | `grafana` | `grafana` | `Observability/grafana`, `Infrastructure/containers` |  |
| 06-observability | `grafana-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 06-observability | `loki` | `loki` | `Observability/loki-operational`, `Observability/loki-reads`, `Observability/loki-writes`, `Observability/loki-chunks`, `Infrastructure/containers` |  |
| 06-observability | `node-exporter` | `node-exporter` | `Infrastructure/node-exporter`, `Infrastructure/containers` |  |
| 06-observability | `prometheus` | `prometheus` | `Observability/prometheus-overview`, `Infrastructure/containers` |  |
| 06-observability | `pushgateway` | none | `Infrastructure/containers` | container metrics and logs only |
| 06-observability | `pyroscope` | `pyroscope` | `Observability/pyroscope`, `Infrastructure/containers` |  |
| 06-observability | `tempo` | `tempo` | `Observability/tempo-operational`, `Observability/tempo-reads`, `Observability/tempo-writes`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-apiserver` | `airflow-monitor` | `Applications/airflow`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-dag-processor` | `airflow-monitor` | `Applications/airflow`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-init` | none | `Infrastructure/containers` | container metrics and logs only |
| 07-workflow | `airflow-scheduler` | `airflow-monitor` | `Applications/airflow`, `Applications/airflow-db`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-statsd-exporter` | `airflow-monitor` | `Applications/airflow`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-triggerer` | `airflow-monitor` | `Applications/airflow`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-valkey` | `airflow-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-valkey-exporter` | `airflow-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 07-workflow | `airflow-worker` | `airflow-monitor` | `Applications/airflow`, `Infrastructure/containers` |  |
| 07-workflow | `flower` | `flower` | `Applications/flower`, `Infrastructure/containers` |  |
| 07-workflow | `n8n` | `n8n-monitor` | `Applications/n8n-system-health`, `Applications/n8n-workflow-analytics`, `Infrastructure/containers` |  |
| 07-workflow | `n8n-task-runner` | none | `Infrastructure/containers` | container metrics and logs only |
| 07-workflow | `n8n-task-runner-worker` | none | `Infrastructure/containers` | container metrics and logs only |
| 07-workflow | `n8n-valkey` | `n8n-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 07-workflow | `n8n-valkey-exporter` | `n8n-valkey-exporter` | `Infrastructure/redis`, `Infrastructure/containers` |  |
| 07-workflow | `n8n-worker` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `comfyui` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `crawl4ai` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `ollama` | `ollama-exporter` | `Applications/ollama`, `Infrastructure/containers` |  |
| 08-ai | `ollama-exporter` | `ollama-exporter` | `Applications/ollama`, `Infrastructure/containers` |  |
| 08-ai | `open-webui` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `backup-sqlite-export` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `conftest` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `dbt` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `dbt-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `k6` | k6 remote write | `Infrastructure/k6`, `Infrastructure/containers` |  |
| 09-platform-ops | `opentofu` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `pact-broker` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `pact-broker-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `registry` | `registry` | `Infrastructure/docker-registry`, `Infrastructure/containers` |  |
| 09-platform-ops | `renovate` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `restic` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `restic-offsite` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `sonarqube` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `terrakube-api` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `terrakube-executor` | none | `Infrastructure/containers` | container metrics and logs only |
| 09-platform-ops | `terrakube-ui` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `wiremock` | none | `Infrastructure/containers` | container metrics and logs only |
| 11-quality | `mailpit` | none | `Infrastructure/containers` | container metrics and logs only |
| 10-communication | `stalwart` | none | `Infrastructure/containers` | container metrics and logs only |
| 10-communication | `stalwart-config` | none | `Infrastructure/containers` | container metrics and logs only |
| 06-observability | `dozzle` | none | `Infrastructure/containers` | container metrics and logs only |
| 12-analytics | `jupyterlab` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `mlflow` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `mlflow-db-provision` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `open_notebook` | none | `Infrastructure/containers` | container metrics and logs only |
| 04-data | `redisinsight` | none | `Infrastructure/containers` | container metrics and logs only |
| 08-ai | `surrealdb` | none | `Infrastructure/containers` | container metrics and logs only |

### LAB Dashboard Coverage

독립 LAB Compose에 속한 다음 대시보드는 파일을 보존하지만 정상 root의 Prometheus는
해당 LAB 서비스들을 수집하지 않습니다. LAB 관측 연결과 실행 검증은 별도 계약입니다:
`Infrastructure/cassandra`, `Infrastructure/etcd-cluster`,
`Infrastructure/haproxy-overview`, `Infrastructure/mongodb`,
`Infrastructure/valkey-cluster`.

`hy-home-lab-locust` 프로젝트의 `lab-locust-master`와
`lab-locust-worker`도 정상 root 서비스 표에서 제외합니다. HOME Alloy
Docker discovery는 Compose 프로젝트 `hy-home-infra`만 유지하므로 이 LAB의
컨테이너 메트릭과 로그를 수집하지 않습니다. Locust LAB 관측 연결은 별도 계약과
검증 전까지 대시보드에 연결하지 않습니다.

### Dashboard Sources

프로비저닝된 대시보드마다 출처와 revision을 기록합니다. 방출되는 메트릭과 맞는 벤더·mixin·grafana.com 대시보드가 있으면 그것을 쓰고, 없을 때만 로컬 대시보드를 둡니다.

| Dashboard | UID | Source |
| --- | --- | --- |
| `Applications/airflow` | `hyhome-airflow` | monitoring-mixins apache-airflow/apache-airflow-overview.json (2026-03-26) |
| `Applications/airflow-db` | `hyhome-airflow-db` | Local dashboard: no external dashboard matches airflow metadata database (read-only) |
| `Applications/flower` | `hyhome-flower` | Local dashboard: no external dashboard matches flower |
| `Applications/n8n-system-health` | `applications-n8n-system-health` | grafana.com dashboard 24474 revision 1 (2025-11-26) |
| `Applications/n8n-workflow-analytics` | `applications-n8n-workflow-analytics` | grafana.com dashboard 24475; datasource set to the read-only n8n-db |
| `Applications/ollama` | `applications-ollama` | local: no external dashboard matches lucabecker42/ollama-exporter |
| `Gateway/oauth2-proxy` | `hyhome-oauth2-proxy` | Local dashboard: no external dashboard matches oauth2-proxy |
| `Gateway/traefik` | `gateway-traefik` | traefik/traefik contrib/grafana/traefik.json at the pinned Traefik release tag (= grafana.com 17346 revision 9) |
| `Infrastructure/cassandra` | `hyhome-cassandra` | grafana.com dashboard 6400 revision 2 (2018-06-14) |
| `Infrastructure/containers` | `hyhome-containers` | grafana.com dashboard 19792 revision 6 (2024-11-24) |
| `Infrastructure/dcgm-exporter` | `Oxed_c6Wz` | NVIDIA/dcgm-exporter grafana/dcgm-exporter-dashboard.json (2023-08-11) |
| `Infrastructure/docker-registry` | `infrastructure-docker-registry` | grafana.com dashboard 9621 revision 2 (2019-01-11); Kubernetes variables replaced by job registry |
| `Infrastructure/etcd-cluster` | `hyhome-etcd` | monitoring-mixins etcd/etcd.json (2026-09-24) |
| `Infrastructure/haproxy-overview` | `hyhome-haproxy` | grafana.com dashboard 12693 revision 14 (2026-04-11) |
| `Infrastructure/k6` | `infrastructure-k6` | grafana.com dashboard 19665 revision 3 (2024-04-30); SPEC-0203에서 `project_id`/`run_id`/`attempt` 필터와 기존 `testid` 계열을 유지하는 명시적 `All=.*` 호환값을 로컬 적용 |
| `Infrastructure/kafka-cluster` | `hyhome-kafka-cluster` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/kafka-cluster-kraft.json |
| `Infrastructure/kafka-connect` | `hyhome-kafka-connect` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/kafka-connect-cluster.json |
| `Infrastructure/kafka-consumer-lag` | `hyhome-kafka-consumer-lag` | grafana.com dashboard 7589 revision 5 (2018-08-21) |
| `Infrastructure/kafka-topics` | `hyhome-kafka-topics` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/kafka-topics-kraft.json |
| `Infrastructure/mongodb` | `hyhome-mongodb` | grafana.com dashboard 16490 revision 1 (2022-06-24) |
| `Infrastructure/node-exporter` | `rYdddlPWk` | grafana.com dashboard 1860 revision 45 (2026-04-11) |
| `Infrastructure/opensearch-cluster` | `hyhome-opensearch-cluster` | monitoring-mixins opensearch/opensearch-cluster-overview.json (2026-06-11) |
| `Infrastructure/opensearch-node` | `hyhome-opensearch-node` | monitoring-mixins opensearch/opensearch-node-overview.json (2026-06-11) |
| `Infrastructure/opensearch-search-and-index` | `hyhome-opensearch-search` | monitoring-mixins opensearch/opensearch-search-and-index-overview.json (2026-06-11) |
| `Infrastructure/postgresql` | `hyhome-postgres` | grafana.com dashboard 9628 revision 8 (2024-12-06) |
| `Infrastructure/qdrant-overview` | `hyhome-qdrant` | grafana.com dashboard 24603 revision 1 (2025-12-25) |
| `Infrastructure/redis` | `hyhome-redis` | oliver006/redis_exporter contrib/grafana_prometheus_redis_dashboard.json (= grafana.com 763 revision 6) |
| `Infrastructure/schema-registry` | `hyhome-schema-registry` | confluentinc/jmx-monitoring-stacks@f376263fc6d7 jmxexporter-prometheus-grafana/assets/grafana/provisioning/dashboards/schema-registry-cluster.json |
| `Infrastructure/seaweedfs` | `hyhome-seaweedfs` | seaweedfs/seaweedfs other/metrics/grafana_seaweedfs.json (2026-09-01) |
| `Infrastructure/valkey-cluster` | `hyhome-valkey-cluster` | grafana.com dashboard 21914 revision 1 (2024-09-14) |
| `Observability/alertmanager-overview` | `hyhome-alertmanager` | monitoring-mixins alertmanager/alertmanager-overview.json (2026-06-20) |
| `Observability/alloy-controller` | `hyhome-alloy-controller` | grafana/alloy@5f45ab2e5a0a operations/alloy-mixin/rendered/dashboards/alloy-controller.json |
| `Observability/alloy-loki` | `hyhome-alloy-loki` | grafana/alloy@5f45ab2e5a0a operations/alloy-mixin/rendered/dashboards/alloy-loki.json |
| `Observability/alloy-opentelemetry` | `hyhome-alloy-opentelemetry` | grafana/alloy@5f45ab2e5a0a operations/alloy-mixin/rendered/dashboards/alloy-opentelemetry.json |
| `Observability/alloy-resources` | `hyhome-alloy-resources` | grafana/alloy@5f45ab2e5a0a operations/alloy-mixin/rendered/dashboards/alloy-resources.json |
| `Observability/gatus` | `hyhome-gatus` | TwiN/gatus .examples/docker-compose-grafana-prometheus gatus.json (2025-10-25) |
| `Observability/grafana` | `hyhome-grafana` | grafana/grafana grafana-mixin/dashboards/grafana-overview.json (2025-08-25) |
| `Observability/loki-chunks` | `hyhome-loki-chunks` | grafana/loki production/loki-mixin-compiled loki-chunks.json; job selectors set to the single-binary job |
| `Observability/loki-operational` | `hyhome-loki-operational` | grafana/loki production/loki-mixin-compiled loki-operational.json; job selectors set to the single-binary job |
| `Observability/loki-reads` | `hyhome-loki-reads` | grafana/loki production/loki-mixin-compiled loki-reads.json; job selectors set to the single-binary job |
| `Observability/loki-writes` | `hyhome-loki-writes` | grafana/loki production/loki-mixin-compiled loki-writes.json; job selectors set to the single-binary job |
| `Observability/prometheus-overview` | `hyhome-prometheus` | monitoring-mixins prometheus/prometheus.json (2026-08-27) |
| `Observability/pyroscope` | `hyhome-pyroscope` | Local dashboard: no external dashboard matches pyroscope |
| `Observability/tempo-operational` | `hyhome-tempo-operational` | grafana/tempo operations/tempo-mixin-compiled tempo-operational.json; job selectors set to the single-binary job |
| `Observability/tempo-reads` | `hyhome-tempo-reads` | grafana/tempo operations/tempo-mixin-compiled tempo-reads.json; job selectors set to the single-binary job |
| `Observability/tempo-writes` | `hyhome-tempo-writes` | grafana/tempo operations/tempo-mixin-compiled tempo-writes.json; job selectors set to the single-binary job |
| `Security/keycloak-capacity-planning` | `hyhome-keycloak-capacity` | keycloak/keycloak-grafana-dashboard dashboards/keycloak-capacity-planning-dashboard.json @f819507c13 |
| `Security/keycloak-troubleshooting` | `hyhome-keycloak-troubleshooting` | keycloak/keycloak-grafana-dashboard dashboards/keycloak-troubleshooting-dashboard.json @f819507c13 |
| `Security/openbao` | `openbao` | grafana.com dashboard 23725 revision 1 (2025-07-15); job set to openbao |

## How to Work in This Area

1. 사용법과 프로비저닝 맥락은 Grafana 가이드(`docs/05.operations/guides/0041-grafana.md`)를 따릅니다.
2. 준비 상태, SSO, 데이터소스, 대시보드 프로비저닝, 재시작, 롤백 절차는 Grafana 런북(`docs/05.operations/runbooks/0041-grafana.md`)을 따릅니다.
3. 관리자 비밀번호, OAuth 클라이언트 시크릿, 토큰, 렌더링된 시크릿 값은 문서, 로그, 태스크 근거, 커밋 메시지에 남기지 않습니다.
4. 계획/태스크 근거와 롤백 기록 없이는 역할 매핑, 데이터소스 UID, 대시보드 프로바이더 잠금, 시크릿 참조, 이미지 버전, 라우트 미들웨어를 변경하지 않습니다.

## Validation

- Compose 또는 설정 참조를 변경한 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 인프라 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.
- `docker compose --profile obs ps grafana`와 `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`로 준비 상태를 확인합니다.
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`로 데이터소스 프로비저닝을 확인합니다.
- `rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml`로 대시보드 프로비저닝을 확인합니다.
- `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`로 대시보드 보유 현황을 확인합니다.

## Troubleshooting

- 네트워크, 볼륨, 시크릿, 환경, 레이블 참조가 올바르게 렌더링되는지 `docker compose --profile obs config --quiet`로 먼저 확인합니다.
- 설정이나 시크릿 참조를 변경하기 전에 컨테이너 로그와 연결된 런북을 확인합니다.
- SSO 실패 시 마스킹된 OAuth/역할 매핑 로그를 확인하고 `/admins` 또는 `/editors` 그룹 소속을 별도로 확인합니다.
- 데이터소스 오류 시 프로비저닝 YAML에서 데이터소스 UID와 백엔드 엔드포인트를 확인합니다.
- 대시보드 로딩 오류 시 대시보드 프로바이더 경로와 대시보드 JSON 파일을 검증합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `obs-core`, `dev`, `logs`, `tracing`, `profiling`, `alerting`, `batch-metrics`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d grafana`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0041-grafana.md`; ID: `GDE-0041`, `POL-0041`, `RUN-0041`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- [infra/README.md](../../README.md)
- Operations index (`docs/05.operations/README.md`)
- Grafana guide (`docs/05.operations/guides/0041-grafana.md`)
- Grafana policy (`docs/05.operations/policies/0041-grafana.md`)
- Grafana runbook (`docs/05.operations/runbooks/0041-grafana.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 검증을 제공합니다.
