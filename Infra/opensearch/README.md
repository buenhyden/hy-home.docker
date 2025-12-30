# OpenSearch Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 검색 및 데이터 분석 엔진인 OpenSearch를 정의합니다. 현재는 단일 노드(`opensearch-node1`) 구성이 활성화되어 있으나, 설정상 3-Node 클러스터 확장이 가능하도록 준비되어 있습니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **opensearch-node1** | Search Engine | 데이터 저장, 검색, 인덱싱을 담당하는 메인 노드입니다. 현재 Master, Data, Ingest 역할을 모두 수행합니다. |
| **opensearch-dashboards**| Visualization | OpenSearch에 저장된 데이터를 시각화하고 대시보드를 제공하는 웹 UI(Kibana Fork)입니다. |
| **opensearch-exporter** | Metrics Exporter | OpenSearch 클러스터의 메트릭을 수집하여 Prometheus에 제공합니다. |

## 3. 구성 및 설정 (Configuration)

### 보안 (Security)
OpenSearch Security Plugin이 활성화되어 있으며 HTTPS(TLS) 통신을 강제합니다.
- **인증서**: `./certs` 디렉토리의 사설 인증서를 사용합니다.
- **통신**: 노드 간 통신 및 REST API 모두 암호화됩니다.

### 시스템 설정 (System)
- **ulimits**: `memlock`, `nofile` 설정이 최적화되어 있습니다.
- **Java Heap**: `OPENSEARCH_JAVA_OPTS` 환경 변수로 힙 메모리를 제어합니다.

### 로드밸런싱 (Traefik)
- **API**: `https://opensearch.${DEFAULT_URL}` (백엔드 통신 시 HTTPS 스킴 사용하도록 설정됨)
- **Dashboards**: `https://opensearch-dashboard.${DEFAULT_URL}`

### 참고 사항
- `opensearch-node2`, `node3`는 주석 처리되어 있어 필요 시 주석 해제로 클러스터를 확장할 수 있습니다.
