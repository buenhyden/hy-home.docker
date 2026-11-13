---
title: "OpenSearch Cluster LAB Operations Policy"
version: "0.1.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0109"
parent_ids:
- "AD-0026"
created: "2026-11-05"
---

# OpenSearch Cluster LAB Operations Policy

## Purpose

### Objective

이 정책은 `labs/opensearch-cluster/docker-compose.yml`의 LAB 전용 세 node OpenSearch cluster와
Dashboards를 격리, secret·인증서, 데이터, 자원과 승격 통제에 묶는다.

### Authority

- Runtime source: [OpenSearch LAB Compose](../../../../labs/opensearch-cluster/docker-compose.yml).
- Artifact: `POL-0109`; parent: `AD-0026`.
- Version projection: [tech-stack versions](../../../../infra/tech-stack.versions.json)는 Compose에서 파생된 drift 증거이며 정확한 pin은 Compose가 소유한다.

## Scope

### Applies To

LAB 전용 `opensearch-cluster` profile과 project `hy-home-lab-opensearch`에 적용된다.

### Exclusions

HOME 단일 node를 대체하거나 승격하는 것은 승인하지 않는다. 승격은 [POL-0107](0107-lab-promotion.md)을 따르는 별도 Task다.

## Rules

### Requirements

- 독립 Compose project와 정확한 `opensearch-cluster` profile로만 선택한다. root include에는 넣지 않는다.
- secret은 `secrets/labs/opensearch-cluster/`의 LAB 사본(LAB-012부터 LAB-015)만 쓴다. HOME
  `secrets/data/opensearch/` 값을 읽거나 재사용하지 않는다. 값은 Compose, Markdown, evidence에 두지 않는다.
- 인증서는 `${LAB_OPENSEARCH_CERT_DIR}`의 LAB 전용 CA와 node 인증서를 읽기 전용으로 mount한다.
  Dashboards에는 `rootCA.pem`만 준다. node 개인키를 다른 서비스에 전달하지 않는다.
- `lab_opensearch_core_net`은 internal로 유지한다. host port, Traefik route, HOME `edge_net`·`obs_net`
  연결을 추가하지 않는다. 인증은 내부 basic 인증만 쓴다.
- 네 data 경로를 `${LAB_DATA_DIR}/opensearch-cluster/` 아래에 분리해 유지한다. 선언된 limit,
  `pids_limit`, healthcheck를 유지한다. 세 node가 한 host에 있으므로 host 가용성을 주장하지 않는다.
- 기동·정지는 `scripts/operations/lab.py`만 쓰며 `down -v`와 volume prune을 쓰지 않는다.
- 데이터 보존과 삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)과 별도 승인을
  따른다.

### Enforcement

[RUN-0109](../../runbooks/15-labs/0109-opensearch-cluster.md)의 정적 render와
`lab.py check opensearch-cluster`로 검증한다. 현재 HOME 입력의 render와 runtime은 `NOT_RUN`이다.
2026-11-05 controller 보고에 따르면 `labs/.env`에 `LAB_OPENSEARCH_CERT_DIR`가 없으며, agent는 그 파일을 읽지 않았다.

## Exceptions

### Exception Conditions

명명된 실험이 없을 때 LAB은 정지 상태로 둘 수 있다. transport hostname 검증을 끄는 것은 container IP가
매번 바뀌기 때문이며, CA와 `nodes_dn` 검증으로 대신한다. 예외는 HOME secret 재사용이나 host 노출을
승인하지 않는다.

### Approval and Review

image, 인증서, secret, network, 데이터 경로, 승격 manifest가 바뀔 때와 승격 Task를 열기 전에 검토한다.

## Ownership

### Responsibilities

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Change and Adoption

- [OpenSearch LAB guide](../../guides/15-labs/0109-opensearch-cluster.md)
- [OpenSearch LAB runbook](../../runbooks/15-labs/0109-opensearch-cluster.md)
- [LAB promotion policy](0107-lab-promotion.md)
- [Domain catalog](../../README.md)
