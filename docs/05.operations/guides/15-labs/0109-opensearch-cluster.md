---
title: "OpenSearch Cluster LAB Usage Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "operations"
artifact_id: "GDE-0109"
parent_ids:
- "POL-0109"
implementation_services:
  labs/opensearch-cluster/docker-compose.yml:
  - opensearch-node1
  - opensearch-node2
  - opensearch-node3
  - lab-opensearch-dashboards
created: "2026-11-05"
---

# OpenSearch Cluster LAB Usage Guide

## Overview

[`labs/opensearch-cluster/docker-compose.yml`](../../../../labs/opensearch-cluster/docker-compose.yml)은
독립 Compose project `hy-home-lab-opensearch`의 세 node OpenSearch cluster와 Dashboards LAB이다.
정상 root는 이 파일을 include하지 않는다. 같은 host의 세 node는 host 고가용성이 아니다.

## Scope

### Audience and Goal

대상 독자: 운영자, 개발자, AI Agent.

목적: OpenSearch LAB의 구성, 인증서·secret·network 경계, 정적 검증과 승격 계획을 현재 Compose와
맞춰 이해한다. HOME 단일 node는 [GDE-0019](../05-databases-and-storage/0019-opensearch.md)가 다룬다.

## Concepts

`opensearch-cluster` profile이 네 서비스를 선택한다.

| 서비스 | 역할 | 준비 상태 판단 |
| --- | --- | --- |
| `opensearch-node1`, `opensearch-node2`, `opensearch-node3` | cluster-manager 겸 data node; 저장소의 OpenSearch Dockerfile로 build | admin 인증 `_cluster/health?wait_for_status=yellow` healthcheck |
| `lab-opensearch-dashboards` | LAB node만 쓰는 Dashboards | `/api/status`가 200 또는 401 |

| 경계 | LAB 계약 |
| --- | --- |
| 상태 | `${LAB_DATA_DIR}/opensearch-cluster/{node1,node2,node3,dashboards}` bind volume |
| 네트워크 | internal `lab_opensearch_core_net`만 사용; HOME `edge_net`·`obs_net`에 접속하지 않음 |
| 노출 | host port와 Traefik router 없음; 9200, 9600, 5601은 내부 expose만 |
| 비밀 | `${LAB_SECRET_DIR}/opensearch-cluster/`의 admin, dashboard, exporter password와 security cookie |
| 인증서 | `${LAB_OPENSEARCH_CERT_DIR}`의 CA와 node 인증서를 읽기 전용 mount; Dashboards는 `rootCA.pem`만 받는다 |
| 인증 | 내부 basic 인증만; HOME Keycloak/OIDC와 gateway route를 쓰지 않음 |

- node 인증서 subject는 `CN=opensearch-node*`(`plugins.security.nodes_dn`)에 맞아야 한다. container
  IP가 매번 바뀌므로 transport hostname 검증은 끈다.
- node build·설정 mount는 `../../infra/04-data/opensearch/...`를 재사용한다. Dashboards는
  [`opensearch-cluster-dashboards.config`](../../../../labs/opensearch-cluster/opensearch-cluster-dashboards.config)를
  설정 파일로 읽는다.
- 정확한 image pin, limit과 template은 Compose와
  [공통 template](../../../../infra/common-optimizations.yml)이 소유한다.
- host disk가 OpenSearch high watermark(90%)를 넘으면 security index를 배치하지 못한다.

## Usage

### Operator input

`LAB_OPENSEARCH_CERT_DIR`는 필수이며 값이 없으면 정적 render도 실패한다. 2026-11-05 현재
`labs/.env`에 이 값이 없어 이 LAB은 현재 HOME 입력으로 render되지 않았다. owner가 LAB 전용 인증서
디렉터리를 준비하고 `labs/.env`에 넣어야 HOME render, `lab.py check`와 readiness 검사를 실행할 수 있다.
LAB README는 SPEC-0215 TSK-0002의 이전 기동 기록을 담고 있으나, 이 가이드는 현재 layout에서 그
결과를 다시 관찰하지 않았다.

### Static check

repository root에서 합성 경로로 render한다. 이 경로는 정적 render용이며 실제 secret·인증서가 아니다.

```bash
LAB_DATA_DIR=/tmp/synthetic-lab-data LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet
```

기동과 정지는 [RUN-0109](../../runbooks/15-labs/0109-opensearch-cluster.md)의 `lab.py` 절차만 쓴다.

### Promotion

[promotion manifest](../../../../labs/opensearch-cluster/promotion.yaml)는 `replace-same`이며 목적지는
`infra/04-data/opensearch/`, profile `opensearch`이다. HOME `opensearch`와 `opensearch-dashboards`를
은퇴시킨다. LAB secret 사본 LAB-012부터 LAB-015는 승격되지 않고, 서비스는
`secrets/data/opensearch/`의 `infra` secret을 쓴다. 문서 목적지는 `05-databases-and-storage` 역할
폴더다. 승격 절차는 [RUN-0107](../../runbooks/15-labs/0107-lab-promotion.md)이 소유한다.

### Common Checks

profile, 네 data 경로, internal network, 읽기 전용 인증서 mount, secret 경로가
`secrets/labs/opensearch-cluster/` 아래인지 render로 확인한다. 정적 통과는 configuration 증거일 뿐이다.

### Runbook Handoff

정적 점검, 기동·정지, 진단과 복구 계획은 [RUN-0109](../../runbooks/15-labs/0109-opensearch-cluster.md)를 따른다.

### Traceability

- Artifact: `GDE-0109`; governing policy: `POL-0109`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.
- Runtime authority: `labs/opensearch-cluster/docker-compose.yml`.

## Troubleshooting

- render가 `set isolated LAB certificate directory`로 실패하면 `LAB_OPENSEARCH_CERT_DIR`가 없다.
- node가 서로를 거부하면 인증서 subject와 `nodes_dn`을 확인한다.
- node가 bind 디렉터리에 쓰지 못하면 그 LAB 경로만 uid 1000(`opensearch`) 소유로 맞춘다.

## Related Documents

- [Operations policy](../../policies/15-labs/0109-opensearch-cluster.md)
- [OpenSearch LAB README](../../../../labs/opensearch-cluster/README.md)
- [OpenSearch LAB runbook](../../runbooks/15-labs/0109-opensearch-cluster.md)
- [LAB promotion policy](../../policies/15-labs/0107-lab-promotion.md)
- [HOME OpenSearch guide](../05-databases-and-storage/0019-opensearch.md)
- [OpenSearch Docker](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/)
