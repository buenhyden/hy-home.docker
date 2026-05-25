# OpenSearch

> Distributed search and analytics engine with Dashboards.

## Overview (KR)

`opensearch` 스택은 로그 집계, 풀텍스트 검색 및 실시간 시각화를 위한 확장 가능한 검색 백엔드를 제공한다. 고가용성 관측성 및 분석 워크로드를 위해 설계되었다.

## Audience

이 README의 주요 독자:

- **Developers**: 검색 쿼리 및 데이터 인덱싱 설계
- **Operators**: 노드 상태 관리 및 보안 설정
- **AI Agents**: 인프라 탐색 및 검색 효율 분석

## Scope

### In Scope

- OpenSearch 2.18 및 Dashboards 3.4.0을 위한 Docker 인프라
- 자원 할당(JVM Heap) 및 볼륨 영속성 관리
- 보안 설정 (Docker Secrets, HTTPS 적용)
- 커스텀 빌드 이미지를 통한 플러그인 관리

### Out of Scope

- 상세 검색 쿼리 로직 개발 (-> 시스템 가이드 참조)
- 인덱스 보존 정책 설계 (-> 운영 정책 참조)
- 개별 노드 장애 복구 절차 (-> 런북 참조)

## Structure

```text
opensearch/
├── opensearch/             # Engine configuration
├── opensearch-dashboards/  # Visualization configuration
├── Dockerfile              # Custom build for security
├── docker-compose.yml      # Standard stack
└── README.md               # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | OpenSearch service leaf in `04-data`; services: `opensearch-node1`, `opensearch-node2`, `opensearch-node3`, `opensearch-dashboards`, `opensearch`, `opensearch-dashboards`; local compose only: `docker-compose.cluster.yml`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/opensearch/docker-compose.yml` |
| Config files | `docker-compose.cluster.yml`, `docker-compose.yml` |
| Config values | env keys: `node.name`, `cluster.name`, `discovery.seed_hosts`, `cluster.initial_cluster_manager_nodes`, `OPENSEARCH_JAVA_OPTS`, `bootstrap.memory_lock`, `node.roles`, `plugins.security.ssl.http.enabled`, plus 8 more; profiles: `data` |
| Compose linkage | local compose only: `docker-compose.cluster.yml`; root include optional/commented in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/opensearch/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `opensearch-data1:/usr/share/opensearch/data`, `../../../../secrets/certs:/usr/share/opensearch/config/certs:ro`, `./config/userdict_ko.txt:/usr/share/opensearch/config/userdict_ko.txt:ro`, `opensearch-data2:/usr/share/opensearch/data`, `opensearch-data3:/usr/share/opensearch/data`, `../../../../secrets/certs/rootCA.pem:/usr/share/opensearch-dashboards/config/rootCA.pem:ro`, `opensearch-data1`, `opensearch-data2`, plus 15 more |
| Ports | `${ES_PERFORMANCE_ANALYZER_HOST_PORT:-9600}:${ES_PERFORMANCE_ANALYZER_PORT:-9600}`, `9200`, `9600`, `5601`, `${KIBANA_PORT:-5601}` |
| Labels | `traefik.enable`, `traefik.http.routers.opensearch.rule`, `traefik.http.routers.opensearch.entrypoints`, `traefik.http.routers.opensearch.tls`, `traefik.http.services.opensearch.loadbalancer.serversTransport`, `traefik.http.services.opensearch.loadbalancer.server.port`, `traefik.http.services.opensearch.loadbalancer.server.scheme`, `traefik.http.routers.opensearch-dashboards.rule`, plus 8 more |
| Secret refs | names: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_exporter_password`, `opensearch_security_cookie`, `oauth2_proxy_client_secret`; mounts: `/run/secrets/opensearch_admin_password`, `/run/secrets/opensearch_dashboard_password`, `/run/secrets/opensearch_exporter_password`, `/run/secrets/opensearch_security_cookie`, `/run/secrets/oauth2_proxy_client_secret` |
| Healthcheck | Compose healthcheck declared for `opensearch-node1`, `opensearch-node2`, `opensearch-node3`, `opensearch-dashboards`, `opensearch`, `opensearch-dashboards` |
| Operations | [Guide](../../../../docs/05.operations/guides/04-data/analytics/opensearch.md), [Policy](../../../../docs/05.operations/policies/04-data/analytics/opensearch.md), [Runbook](../../../../docs/05.operations/runbooks/04-data/analytics/opensearch.md) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 아키텍처 컨텍스트는 [시스템 가이드](../../../../docs/05.operations/guides/04-data/analytics/opensearch.md)를 참조한다.
2. 자원 거버넌스는 [운영 정책](../../../../docs/05.operations/policies/04-data/analytics/opensearch.md)을 확인한다.
3. 유지보수 및 복구 절차는 [복구 런북](../../../../docs/05.operations/runbooks/04-data/analytics/opensearch.md)을 사용한다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect OpenSearch.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking OpenSearch documentation ready.
- `docker-compose.cluster.yml` includes node and dashboard healthchecks; validate it from this service directory with `docker compose --env-file ../../../../.env.example -f docker-compose.cluster.yml config --services`.

## Troubleshooting

- Start with `docker compose config` from this service directory to verify OpenSearch, Dashboards, network, certificate, and secret references render.
- If the cluster does not form or Dashboards cannot connect, inspect `docker compose logs opensearch` and `docker compose logs opensearch-dashboards` before changing JVM, OIDC, or certificate settings.

## Related Documents

- **System Guide**: [docs/05.operations/04-data/analytics/opensearch.md](../../../../docs/05.operations/guides/04-data/analytics/opensearch.md)
- **Policy**: [docs/05.operations/policies/04-data/analytics/opensearch.md](../../../../docs/05.operations/policies/04-data/analytics/opensearch.md)
- **Runbook**: [docs/05.operations/runbooks/04-data/analytics/opensearch.md](../../../../docs/05.operations/runbooks/04-data/analytics/opensearch.md)
- **Monitoring**: `opensearch-exporter:9114/metrics`

## AI Agent Guidance

1. OpenSearch 설정 변경 시 JVM Heap 메모리 설정을 신중히 확인한다.
2. HTTPS 및 보안 플러그인 설정을 수정할 때 인증서 경로를 누락하지 않도록 주의한다.
3. 인덱스 생성 및 삭제 작업을 자동화하기 전에 운영 정책의 데이터 보존 주기를 먼저 읽는다.

---
Copyright (c) 2026. Analytics Tier Infrastructure.
