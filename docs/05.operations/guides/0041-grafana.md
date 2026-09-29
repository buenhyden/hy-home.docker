---
title: "Grafana Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "operations"
artifact_id: "GDE-0041"
parent_ids:
- "POL-0041"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - grafana
  - grafana-db-provision
created: "2026-05-10"
---

# Grafana Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Grafana 사용 맥락과 설정 확인 방법을 설명한다. Grafana는 [grafana/grafana image declaration](../../../infra/06-observability/docker-compose.yml)으로 실행되는 visualization hub이며 provisioned datasources, provisioned dashboards, Keycloak OAuth role mapping, protected route를 통해 metrics, logs, traces, alerts, profiles를 한 화면에서 탐색한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Grafana compose service, provisioning mounts, datasource UID, dashboard provider, Keycloak role mapping, protected route boundary를 빠르게 파악한다.
- Grafana Explore와 dashboards에서 Prometheus, Loki, Tempo, Alertmanager, Pyroscope 연결을 확인한다.
- 장애 대응, restart, provisioning rollback, SSO/datasource triage는 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/grafana/provisioning`과 `infra/06-observability/grafana/dashboards`를 읽을 수 있는 권한.
- Docker Secret IDs `grafana_admin_password`, `grafana_client_secret`가 준비되어 있어야 한다. Secret 값은 문서, 로그, task evidence에 기록하지 않는다.
- Keycloak groups `/admins`, `/editors` role mapping 정책을 변경하지 않는다.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:|container_name: infra-grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|traefik.http.routers.grafana.middlewares: gateway-standard-chain@file' infra/06-observability/docker-compose.yml
   ```

2. Datasource provisioning boundary를 확인한다.

   ```bash
   rg -n 'uid: Prometheus|url: http://prometheus:9090|uid: Loki|url: http://loki:3100|uid: Tempo|url: http://tempo:3200|uid: alertmanager|url: http://alertmanager:9093|type: grafana-pyroscope-datasource|url: http://pyroscope:4040|tracesToLogsV2|datasourceUid: .Loki.' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

3. Dashboard provisioning boundary를 확인한다.

   ```bash
   rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml
   find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l
   ```

4. UI에서 주요 탐색 경로를 확인한다.

   - UI: `https://grafana.${DEFAULT_URL}`
   - Metrics: datasource `Prometheus`
   - Logs: datasource `Loki`
   - Traces: datasource `Tempo`, `Loki`로의 `tracesToLogsV2` link
   - Alerts: datasource `Alertmanager`
   - Profiles: datasource `Pyroscope`

5. Role mapping 기준을 확인한다.

   - `/admins` group: `Admin`
   - `/editors` group: `Editor`
   - `/viewers` group: `Viewer`
   - 그 외 realm 사용자: 거부 (`ROLE_ATTRIBUTE_STRICT=true`, catch-all 없음)
   - 익명 접근은 비활성화되어 있으며, 신규 사용자는 기본값으로 `Viewer`가 된다.
   - hy-home.k8s Kiali는 Viewer 서비스 계정 `k8s-kiali`의 토큰으로 Grafana를
     읽으며, [RUN-0096](../runbooks/0096-k8s-integration.md)이 이를 발급/재발급한다.
   - OAuth 호출은 마운트된 local root CA로 Keycloak을 검증한다
     (`TLS_SKIP_VERIFY_INSECURE=false`).
   - 이를 활성화하는 승인된 recreate 전에 Keycloak에서 owner 계정이
     `/admins`에 있고 읽기 전용 사용자를 위한 `/viewers` group이 존재하는지
     확인한다. 그렇지 않으면 해당 사용자들이 접근 권한을 잃는다. rollback은
     이전 Compose 값과 recreate이며, Grafana 데이터는 초기화되지 않는다.

### Common Pitfalls

- **Provisioning drift**: UI에서만 바꾼 dashboard나 datasource는 JSON/YAML로 export해 커밋하기 전까지 current truth가 되지 않는다.
- **Datasource identity drift**: dashboard는 provisioned UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`, `Pyroscope`, `n8n-db`, `airflow-db` 또는 datasource 변수를 참조해야 한다. 이미 있는 datasource의 UID는 Grafana가 제자리에서 바꾸지 못하므로 `deleteDatasources`로 지우고 다시 만든다(SPEC-0193에서 Pyroscope).
- **Dashboard identity**: 이미 provision된 dashboard의 `uid`를 바꾸거나, 지운 파일과 같은 경로에 다른 `uid`의 파일을 두면 Grafana 13이 `deprecatedInternalID ... is already in use`로 저장을 거부한다. 기존 dashboard는 `uid`를 유지하고, 교체하는 dashboard는 새 경로에 둔다.
- **Secret evidence**: `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, 렌더링된 secret 값을 증거에 복사해서는 안 된다.
- **Role mapping drift**: `/admins`와 `/editors` mapping은 `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`가 제어한다.
- **Dashboard edit lock**: provider `editable: false`가 provisioned dashboard를 code-owned 상태로 유지한다.

### Source-backed operating contract

- **Purpose/classification/source**: `grafana`는 여러 observability profile이 선택하는 `HOME` observability UI이며, [Compose](../../../infra/06-observability/docker-compose.yml)와 provisioning 파일이 권위 있는 정의다.
- **State flow**: 현재 source는 `GF_DATABASE_*` 외부 데이터베이스 변수를 설정하지 않으므로, Grafana는 `grafana-data:/var/lib/grafana`의 기본 SQLite 데이터베이스를 plugin, runtime 상태와 함께 사용한다. datasource/dashboard는 추적되는 파일에서 읽기 전용으로 provision된다.
- **Secrets/auth/dependencies**: `grafana_admin_password`와 `grafana_client_secret`가 admin bootstrap과 native Keycloak OAuth에 공급된다. 익명 접근은 현재 source(2026-09-21)에서 비활성화되어 있다. 이전에는 로그인 없이 모든 dashboard가 노출되었다. Traefik, Keycloak, root CA, datasource, `obs_net`이 의존성이며, 익명 접근은 OAuth 관리와 별개로 평가한다.
- **Resources/normal use**: Compose 제한은 source 값일 뿐 측정된 여유 용량이 아니다. root에서 렌더링하고 `/api/health`, OAuth 로그인, 익명 거부, datasource health, provisioned dashboard 로드를 확인한다.
- **Lifecycle**: SQLite/`grafana-data`를 복사하기 전에 Grafana를 중지한다. provisioning과 대응하는 secret을 보존한다. plugin/schema 호환성을 검토하고, 핀된 버전을 하나씩 업그레이드하고, 재개 전에 users/teams/dashboards/alerts/datasources/OAuth를 확인한다.
- **Upstream/license**: 공식 [installation/database default](https://grafana.com/docs/grafana/latest/setup-grafana/installation/), [backup](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/), [upgrade](https://grafana.com/docs/grafana/latest/upgrade-guide/when-to-upgrade/) 안내를 따른다. Grafana OSS는 AGPL-3.0 라이선스다.

### Dashboard catalog (SPEC-0193)

- **Coverage**: [Grafana README](../../../infra/06-observability/grafana/README.md)의 Service Coverage 표가 Compose 서비스 전체(정지·OPTIONAL·LAB 포함)를 한 줄씩 나열하고, 서비스마다 메트릭 소스(scrape job)와 대시보드를 적는다. 메트릭 소스가 없는 서비스(ComfyUI, Open WebUI, Dozzle 등)는 `Infrastructure/containers`(cAdvisor)와 Logs Drilldown으로 본다.
- **One role per dashboard**: 같은 소스를 같은 목적으로 그리는 대시보드는 하나만 둔다. 계약 테스트가 두 대시보드의 쿼리가 절반 이상 겹치면 실패한다.
- **External first**: 서비스가 방출하는 메트릭 이름과 맞는 벤더 저장소, monitoring-mixins, grafana.com 대시보드가 있으면 그것을 쓴다. 파일에 넣을 때 `__inputs`를 provisioned UID로 풀고, `hyhome-*` UID를 붙이고, `description`에 출처와 revision(또는 commit)을 남긴다. README의 Dashboard Sources 표가 전체 출처 목록이다. 로컬 대시보드는 맞는 외부 대시보드가 없을 때만 둔다(Ollama, OAuth2 Proxy, Flower, Pyroscope, Airflow Runs (DB)).
- **Label contract**: 모든 scrape target에 `cluster="hy-home"`, `namespace="hy-home"`가 붙는다. mixin 대시보드의 `cluster`/`namespace` 변수가 이 라벨로 채워진다. Kafka job 이름 `kafka-broker`, `kafka-connect`, `schema-registry`와 `kafka_connect_cluster_id`, `env` 라벨은 Confluent 대시보드가 그대로 동작하도록 맞춘 값이다.
- **Single-binary exception**: Loki와 Tempo mixin 대시보드는 microservice마다 job을 나눠 고른다(`job=~"($namespace)/(querier|...)"`). 여기서는 둘 다 단일 바이너리이므로 이 두 계열만 job selector를 `job="loki"`, `job="tempo"`로 바꿔 넣었다.

### Signal correlation and Drilldown

| 경로 | 설정 | 비고 |
| --- | --- | --- |
| Metrics → Traces | Prometheus `exemplarTraceIdDestinations` (`traceID` → Tempo) | Prometheus가 `--enable-feature=exemplar-storage`로 exemplar를 저장한다 |
| Logs → Traces | Loki `derivedFields` (`traceID`/`trace_id` → Tempo) | 로그 본문에 trace ID가 있을 때만 링크가 생긴다 |
| Traces → Logs | Tempo `tracesToLogsV2` (`service.name` → `service_name`) | Alloy가 Compose 서비스 이름을 `service_name`으로 붙인다 |
| Traces → Metrics | Tempo `tracesToMetrics` (span metrics) | `traces_spanmetrics_*`의 `service` 라벨 |
| Traces → Profiles | Tempo `tracesToProfiles` (`service.name` → Pyroscope `service_name`) | pprof를 수집하는 서비스에만 해당 |

- **Metrics Drilldown**: Prometheus datasource의 `timeInterval`이 scrape 간격(30 s)과 같아 `$__rate_interval`이 샘플 네 개를 덮는다.
- **Logs Drilldown**: Loki의 `volume_enabled`, `pattern_ingester`, `discover_log_levels`가 서비스별 볼륨, 패턴, 레벨 보기를 채운다.
- **Traces Drilldown**: Tempo 3.0.3은 TraceQL metrics를 기본으로 답한다. trace를 보내는 서비스는 Traefik, Keycloak, Grafana, Airflow(apiserver, worker, DAG processor, triggerer)이며 샘플링은 10%다. Airflow scheduler는 제외한다(RUN-0050).
- **Profiles Drilldown**: Alloy `pyroscope.scrape "go_services"`가 `/debug/pprof`을 제공하는 Go 서비스 11개(Prometheus, Alertmanager, Loki, Tempo, Alloy, Pyroscope, Grafana:6060, node-exporter, SeaweedFS S3, `mng-pg-exporter`, registry)에서 30초마다 가져온다. eBPF는 쓰지 않는다.
- **SQL datasources**: `n8n-db`, `airflow-db`는 `grafana-db-provision`이 만든 `grafana_reader`로 접속한다. 이 role은 n8n `execution_entity`·`workflow_entity`와 Airflow `dag`·`dag_run`·`task_instance`만 `SELECT`하며, 세션은 읽기 전용이고 statement timeout 30 s, 연결 4개로 제한된다.

### External dashboard survey (2026-09-29)

외부 후보는 벤더 저장소, [monitoring-mixins](https://monitoring.mixins.dev/), [grafana.com dashboards](https://grafana.com/grafana/dashboards/)에서 찾았다. 후보마다 JSON을 받아 PromQL의 메트릭 이름을 핀된 exporter가 방출하는 이름과 대조했다.

| 판단 | 서비스와 근거 |
| --- | --- |
| 벤더 대시보드 채택 | Traefik(`contrib/grafana`), Keycloak(`keycloak-grafana-dashboard`의 troubleshooting·capacity planning), SeaweedFS(`other/metrics`), Kafka·Connect·Schema Registry(Confluent `jmx-monitoring-stacks`), Gatus(예제), NVIDIA DCGM, redis_exporter contrib |
| mixin 채택 | Prometheus, Alertmanager, Grafana, Alloy, Loki, Tempo, Airflow, etcd, OpenSearch |
| grafana.com 채택 | Node Exporter Full 1860, cAdvisor 19792, PostgreSQL 9628, Qdrant 24603, HAProxy 12693, Valkey Cluster 21914, MongoDB 16490, Cassandra 6400, Kafka consumer lag 7589, k6 19665, OpenBao 23725, Docker Registry 9621, n8n 24474·24475 |
| 맞는 것 없음 | OAuth2 Proxy(`oauth2_proxy_*`를 쓰는 대시보드가 없다), Ollama(lucabecker42 exporter와 다른 exporter를 가정), Pyroscope(공식 대시보드가 Kubernetes 라벨 전용), Supabase(Cloud 전용 메트릭), InfluxDB 3(mixin은 InfluxDB 2 이름) |
| 버림 | Keycloak 14390(Keycloak 26이 방출하지 않는 `base_*` 이름), Qdrant 공식 대시보드(Kubernetes·Cloud 전용), Neo4j 12046(Community 판에 메트릭 endpoint가 없다), vLLM 24756(vLLM 서비스가 없다) |

Airflow mixin은 `airflow_dagrun_*`, `airflow_pool_*` 같은 이름을 쓰는데, 기존 statsd mapping은 DAG 파일 이름을 메트릭 이름에 넣었다. mapping을 DAG, task, pool, 파일 이름을 라벨로 옮기도록 바꾸고, 알 수 없는 긴 이름은 버린다.

## Common Checks

- `docker compose --profile obs ps grafana`
- `docker logs --tail=100 infra-grafana`
- `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `python3 -m unittest tests.validation.test_compose_baseline_gates.ObservabilityDashboardContractTests`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0041-grafana.md)을 따른다.

## Traceability

- Declared parent: [Grafana Operations Policy](../policies/0041-grafana.md) (`POL-0041`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0041-grafana.md) (`POL-0041`), [Runbook](../runbooks/0041-grafana.md) (`RUN-0041`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0041-grafana.md)
- [Recovery runbook](../runbooks/0041-grafana.md)
