---
title: "독립 LAB source"
version: "0.3.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-10-12"
---

# 독립 LAB source

## Purpose

### Service Role

이 디렉터리는 정상 root Compose와 분리된 LAB entrypoint, 공개 안내와
LAB 전용 build·bind source를 보관합니다. LAB 운영 문서는
`docs/05.operations/`의 역할별 `15-labs/` 폴더에 있으며 이 runtime source family와 구분합니다.
승격 통제와 절차는 `15-labs`의 LAB 승격 정책과 런북(OPS-0107)이 소유하며,
각 LAB의 Guide와 Runbook도 같은 폴더에 있습니다. [운영 문서 탐색](../docs/05.operations/README.md)에서 찾습니다.

#### Audience

LAB source 관리자, 운영자와 정적 검토자입니다.

#### Scope

source 경로와 공개 구성의 탐색입니다. 실제 기동, 이미지 업데이트, 비밀값 이관,
부하 생성, 데이터 삭제·복구를 문서 이동으로 승인하거나 완료로 처리하지 않습니다.

#### Structure

모든 LAB은 `labs/<name>/` 폴더 하나입니다(SPEC-0263). 폴더에는 진입점
`docker-compose.yml`, 서비스 `README.md`, 승격 manifest `promotion.yaml`과 LAB이 쓰는
build source·설정·helper·Grafana 대시보드가 함께 있습니다. `labs/` root에는 이 README와
공유 `.env.example`만 둡니다. Supabase LAB은 2026-11-06 owner 결정으로 제거했습니다(SPEC-0263 W8).

| LAB | Entry point와 안내 | 승격 manifest | Source 자산 |
| --- | --- | --- | --- |
| PostgreSQL HA | [Compose](postgresql-ha/docker-compose.yml), [안내](postgresql-ha/README.md) | [promotion.yaml](postgresql-ha/promotion.yaml) | config·wrapper·초기화 SQL·etcd·HAProxy 대시보드 |
| Valkey Cluster | [Compose](valkey-cluster/docker-compose.yml), [안내](valkey-cluster/README.md) | [promotion.yaml](valkey-cluster/promotion.yaml) | config·scripts·대시보드 |
| Locust | [Compose](locust/docker-compose.yml), [안내](locust/README.md) | [promotion.yaml](locust/promotion.yaml) | build source |
| Cassandra | [Compose](cassandra/docker-compose.yml), [안내](cassandra/README.md) | [promotion.yaml](cassandra/promotion.yaml) | 대시보드 |
| CouchDB | [Compose](couchdb/docker-compose.yml), [안내](couchdb/README.md) | [promotion.yaml](couchdb/promotion.yaml) | [initializer](couchdb/couchdb-cluster-init.sh) |
| MongoDB | [Compose](mongodb/docker-compose.yml), [안내](mongodb/README.md) | [promotion.yaml](mongodb/promotion.yaml) | 대시보드 |
| Kafka | [Compose](kafka-cluster/docker-compose.yml), [안내](kafka-cluster/README.md) | [promotion.yaml](kafka-cluster/promotion.yaml) | Schema Registry·Connect(Debezium) build·대시보드 |
| OpenSearch | [Compose](opensearch-cluster/docker-compose.yml), [안내](opensearch-cluster/README.md) | [promotion.yaml](opensearch-cluster/promotion.yaml) | [Dashboards 설정](opensearch-cluster/opensearch-cluster-dashboards.config) |
| Lakehouse | [Compose](lakehouse/docker-compose.yml), [안내](lakehouse/README.md) | [promotion.yaml](lakehouse/promotion.yaml) | [Spark](lakehouse/spark/README.md), [Trino](lakehouse/trino/README.md), [Flink](lakehouse/flink/README.md), [GX](lakehouse/great-expectations/README.md), [table bucket job](lakehouse/seaweedfs-table-bucket.sh) |
| dbt | [Compose](dbt/docker-compose.yml), [안내](dbt/README.md) | [promotion.yaml](dbt/promotion.yaml) | build·project |
| Superset | [Compose](superset/docker-compose.yml), [안내](superset/README.md) | [promotion.yaml](superset/promotion.yaml) | build·설정 |
| JupyterLab | [Compose](jupyterlab/docker-compose.yml), [안내](jupyterlab/README.md) | [promotion.yaml](jupyterlab/promotion.yaml) | build |
| SonarQube | [Compose](sonarqube/docker-compose.yml), [안내](sonarqube/README.md) | [promotion.yaml](sonarqube/promotion.yaml) | 독립 Compose source |
| Stalwart | [Compose](stalwart/docker-compose.yml), [안내](stalwart/README.md) | [promotion.yaml](stalwart/promotion.yaml) | 설정 helper |
| Open WebUI | [Compose](open-webui/docker-compose.yml), [안내](open-webui/README.md) | [promotion.yaml](open-webui/promotion.yaml) | OIDC entrypoint |

[공개 환경 예시](.env.example)는 정적 구성 입력이며 실제 비밀값을 저장하지 않습니다.

### Supported Environment

각 LAB은 `labs/<name>/docker-compose.yml`의 독립 Docker Compose project로 실행하며 `scripts/operations/lab.py`가 정확한 LAB 이름으로 선택한다. image, network, 상태 경로는 각 LAB 폴더가 선언한다.

## Interfaces

### Inputs and Outputs

데이터 LAB의 역할과 선택 경계는 다음과 같습니다. 각 LAB 폴더의 Compose와 안내가
실제 profile·source·권한 계약을 소유합니다.

| LAB | 역할 | Profile·진입점 | 실행·상태 경계 |
| --- | --- | --- | --- |
| [PostgreSQL HA](postgresql-ha/README.md) | Patroni·etcd·HAProxy 토폴로지 | `postgres-ha` | HOME mng-pg와 별개 |
| [Valkey Cluster](valkey-cluster/README.md) | 6노드 캐시·KV 토폴로지 | `valkey-cluster` | HOME mng-valkey와 별개 |
| [Cassandra](cassandra/README.md) | wide-column 저장소 | `cassandra` | 독립 LAB |
| [CouchDB](couchdb/README.md) | 문서 동기화 저장소 | `couchdb` | 독립 LAB |
| [MongoDB](mongodb/README.md) | 문서 저장소·replica set | `mongodb` | 독립 LAB |
| [OpenSearch Cluster](opensearch-cluster/README.md) | 세 노드 검색 토폴로지 | `opensearch-cluster` | HOME 단일 노드와 별개 |
| [Locust](locust/README.md) | 독립 부하 검증 image source | `labs/locust/docker-compose.yml` | root include와 HOME 상태를 공유하지 않음 |

SPEC-0262와 ADR-0062 개정으로 root에서 옮긴 LAB은 다음과 같습니다. LAB은 HOME network에
연결되지 않으므로 HOME SeaweedFS·mng-pg·dev-pg·MLflow가 필요한 LAB은
[.env.example](.env.example)의 `LAB_*` endpoint 입력으로만 대상을 지정합니다.
HOME은 이 서비스들을 LAB network에 기본으로 게시하지 않으므로 도달 가능한
endpoint는 별도 owner 승인 대상이며, 그 전까지 이 LAB들은 render 검증만 합니다.
Secret은 다른 데이터 LAB처럼 `LAB_SECRET_DIR` 아래 LAB 전용 파일이며, HOME 값의 LAB 사본
준비는 별도 승인 대상입니다.

| LAB | 역할 | Profile·진입점 | HOME 의존 입력 |
| --- | --- | --- | --- |
| Lakehouse | Iceberg batch·SQL·streaming·품질 검증 | `lab-lakehouse` / `labs/lakehouse/docker-compose.yml` | `LAB_LAKEHOUSE_S3_ENDPOINT`, `LAB_LAKEHOUSE_CATALOG_URI` |
| dbt | dev-pg SQL 변환 작업 | `lab-dbt` / `labs/dbt/docker-compose.yml` | `LAB_DBT_DB_HOST` |
| Superset | BI 웹, native Keycloak OIDC | `lab-superset` / `labs/superset/docker-compose.yml` | `LAB_SUPERSET_DB_HOST`, `LAB_SUPERSET_DEFAULT_URL`, `LAB_SUPERSET_CA_FILE` |
| JupyterLab | 단일 사용자 notebook | `jupyterlab` / `labs/jupyterlab/docker-compose.yml` | 선택 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI` |
| SonarQube | 정적 분석 서버 | `sast` / `labs/sonarqube/docker-compose.yml` | `LAB_SONARQUBE_DB_HOST` |
| Stalwart | 메일 서버 실험 | `mail-server` / `labs/stalwart/docker-compose.yml` | 없음(자체 완결) |
| Open WebUI | 로컬 LLM 채팅·RAG, native Keycloak OIDC(ADR-0062 개정 2026-11-10) | `lab-open-webui` / `labs/open-webui/docker-compose.yml` | `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`, `LAB_OPEN_WEBUI_DEFAULT_URL`, `LAB_OPEN_WEBUI_CA_FILE` |

Locust 전용 공개 입력은 [.env.example](.env.example)의 `LAB_LOCUST_*`를
사용합니다. Locust source는 이 독립 entrypoint용이며 root profile에 추가하지
않습니다. 실제 부하 target·권한·종료 조건은 별도 수용 입력입니다.

### Security Boundary

LAB은 HOME network, 상태, secret을 공유하지 않으며 기동은 `lab.py`의 목적·lease 검사를 거친다. 비밀값 이관은 문서 이동으로 승인되지 않는다.

## Development

### Local Workflow

각 LAB 폴더의 entrypoint는 기존 `scripts/operations/lab.py`의 exact LAB 이름으로
선택합니다. 실제 실행 전에는 목적·lease·대상·resource·권한·정리와 복구 경계를
별도로 확정해야 하며, source render는 native 성공의 증거가 아닙니다.
공유 `infra/common-optimizations.yml`의 재사용 외에 LAB 전용 build와 bind source는
그 LAB 폴더에 둡니다. 운영 데이터와 secret의 위치·값은 이번 source 이동으로 바꾸지 않습니다.
Compose는 상대 경로와 `LAB_SECRET_DIR`를 `labs/<name>/` 기준으로 해석하므로
`LAB_SECRET_DIR` 기본값은 `../../secrets/labs`입니다.

같은 호스트의 복제 노드는 호스트 장애를 격리하지 않습니다. HOME 단일 인스턴스와
LAB 클러스터를 구분하고 성능·HA를 측정 없이 보장하지 않습니다. Valkey LAB 복구에는
조율된 RDB checkpoint와 완전한 AOF set/manifest, 새로운 cluster identity가 필요합니다.
게시된 client/bus 포트의 노출 경계를 유지합니다. 이 source 정리는 복구 실행 증거가 아닙니다.

### Checks

각 LAB의 정적 render는 `docker compose --env-file labs/.env.example -f labs/<name>/docker-compose.yml --profile '*' config --quiet`로 검증하며 개별 명령은 각 LAB README에 있다. source render 통과는 native 실행 성공의 증거가 아니다.

## Operations

### Runbook Links

- [문서 탐색](../docs/README.md)
- [운영 문서 탐색](../docs/05.operations/README.md)

### Observability and Recovery

없음: 이 디렉터리는 인덱스라 직접 관측 대상이 없다. LAB 운영은 [LAB Runbook 목록](../docs/05.operations/runbooks/15-labs/README.md)을 따른다.
