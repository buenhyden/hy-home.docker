---
title: "OpenSearch Cluster LAB Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
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
next_review_at: "2027-05-13"
---

# OpenSearch Cluster LAB Usage Guide

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Audience

세 node OpenSearch cluster와 Dashboards LAB의 구성, 인증서·secret·network 경계와 정적 검증을 이해하려는 운영자, 개발자, AI Agent가 읽는다.

##### Outcome

[`labs/opensearch-cluster/docker-compose.yml`](../../../../labs/opensearch-cluster/docker-compose.yml)은
독립 Compose project `hy-home-lab-opensearch`의 세 node OpenSearch cluster와 Dashboards LAB이다.
정상 root는 이 파일을 include하지 않는다. 같은 host의 세 node는 host 고가용성이 아니다.

대상 독자: 운영자, 개발자, AI Agent.

목적: OpenSearch LAB의 구성, 인증서·secret·network 경계와 정적 검증을 현재 Compose와
맞춰 이해한다. HOME 단일 node는 [GDE-0019](../05.databases-and-storage/0019-opensearch.md)가 다룬다.

###### Traceability
<!-- core-payload-level:4 -->

- Artifact: `GDE-0109`; governing policy: `POL-0109`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.
- Runtime authority: `labs/opensearch-cluster/docker-compose.yml`.

###### Related Documents
<!-- core-payload-level:4 -->

- [Operations policy](../../02.policies/15.labs/0109-opensearch-cluster.md)
- [OpenSearch LAB README](../../../../labs/opensearch-cluster/README.md)
- [OpenSearch LAB runbook](../../03.runbooks/15.labs/0109-opensearch-cluster.md)
- [LAB promotion policy](../../02.policies/15.labs/0107-lab-promotion.md)
- [HOME OpenSearch guide](../05.databases-and-storage/0019-opensearch.md)
- [OpenSearch Docker](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/)

#### Prerequisites

##### Environment

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

##### Authority

실제 secret·인증서는 문서에 적지 않으며 합성 경로로만 render한다. LAB secret 사본 LAB-012부터 LAB-015는 승격되지 않았다.

#### Procedure

##### Steps

###### Operator input
<!-- core-payload-level:4 -->

`LAB_OPENSEARCH_CERT_DIR`는 필수이며 값이 없으면 정적 render도 실패한다. 현재 HOME
입력의 render는 `NOT_RUN`이다. 2026-11-05 controller 보고에 따르면 `labs/.env`에 이 값이 없다(agent는
그 파일을 읽지 않는다). owner가 LAB 전용 인증서
디렉터리를 준비하고 `labs/.env`에 넣어야 HOME render, `lab.py check`와 readiness 검사를 실행할 수 있다.
LAB README는 SPEC-0215 TSK-0002의 이전 기동 기록을 담고 있으나, 이 가이드는 현재 layout에서 그
결과를 다시 관찰하지 않았다.

###### Static check
<!-- core-payload-level:4 -->

repository root에서 합성 경로로 render한다. 이 경로는 정적 render용이며 실제 secret·인증서가 아니다.

```bash
LAB_DATA_DIR=/tmp/synthetic-lab-data LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet
```

기동과 정지는 [RUN-0109](../../03.runbooks/15.labs/0109-opensearch-cluster.md)의 `lab.py` 절차만 쓴다.

###### Promotion
<!-- core-payload-level:4 -->

[ADR-0062](../../../02.architecture/02.decisions/0062-home-lab-membership.md#decision)는 검색 실험을
이 LAB에 두고 HOME 단일 node의 별도 퇴역을 결정했다. 현행 root에는 선택형 단일 node와
Dashboards가 남아 있다. [promotion manifest](../../../../labs/opensearch-cluster/promotion.yaml)의
`replace-same`은 HOME 대체 검토용 후보이며 실행 승인을 담지 않는다. HOME 대체를 다시
검토하려면 현행 구조 결정의 변경을 승인받고 [POL-0107](../../02.policies/15.labs/0107-lab-promotion.md)의
별도 Task 절차를 따른다. LAB secret 사본 LAB-012부터 LAB-015는 LAB에 남는다.

###### Exceptions
<!-- core-payload-level:4 -->

이 가이드는 Troubleshooting에 적은 내용 외의 예외를 따로 기록하지 않는다.

##### Expected Results

profile, 네 data 경로, internal network, 읽기 전용 인증서 mount, secret 경로가
`secrets/labs/opensearch-cluster/` 아래인지 render로 확인한다. 정적 통과는 configuration 증거일 뿐이다.

#### Troubleshooting

##### Symptoms

- render가 `set isolated LAB certificate directory`로 실패하면 `LAB_OPENSEARCH_CERT_DIR`가 없다.
- node가 서로를 거부하면 인증서 subject와 `nodes_dn`을 확인한다.
- node가 bind 디렉터리에 쓰지 못하면 그 LAB 경로만 uid 1000(`opensearch`) 소유로 맞춘다.

###### Runbook Handoff
<!-- core-payload-level:4 -->

정적 점검, 기동·정지, 진단과 복구 계획은 [RUN-0109](../../03.runbooks/15.labs/0109-opensearch-cluster.md)를 따른다.

##### Next Action

증상이 계속되면 [RUN-0109](../../03.runbooks/15.labs/0109-opensearch-cluster.md)를 따른다. 진단과 복구 계획도 이 runbook이 맡는다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
