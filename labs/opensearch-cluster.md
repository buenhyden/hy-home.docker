---
title: "OpenSearch Cluster LAB"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-10-03"
---

# OpenSearch 3-node LAB

## Overview

`labs/opensearch-cluster.yml`은 정상 root Compose가 include하지 않는 학습용
OpenSearch 클러스터입니다. 이 파일 자체를 별도 Compose entrypoint로 사용하고
`opensearch-cluster` profile로 node1–3과 `lab-opensearch-dashboards`를
함께 선택합니다. 같은 호스트의 세 노드는 호스트 고가용성이 아닙니다.

## Audience

독립 검색 LAB의 설정과 보안 경계를 검토하는 개발자와 운영자.

## Scope

별도 세 노드·Dashboard의 상태·인증서·비밀 참조를 다룬다. 실제 기동과 기존 데이터 복구는 별도 승인이다.

## Structure

`opensearch-cluster.yml`이 서비스 선언을, 이 문서가 실행 전제와 정적 검증을 소유한다.

| 경계 | LAB 계약 |
| --- | --- |
| 상태 | `lab-opensearch-node1-data`, `node2-data`, `node3-data`, `dashboards-data`의 프로젝트별 새 named volume |
| 네트워크 | `lab_opensearch_core_net`만 사용; 정상 `edge_net`·`obs_net`·`lab_net`에 접속하지 않음 |
| 노출 | 호스트 publish 포트와 Traefik 라우터 없음; API 9200, 모니터링 9600, Dashboards 5601은 내부 expose만 |
| 비밀 | `${LAB_SECRET_DIR}/opensearch-cluster/`의 `lab_opensearch_admin_password`, `lab_opensearch_dashboard_password`, `lab_opensearch_exporter_password`, `lab_opensearch_security_cookie`; 정상 비밀을 재사용하지 않음 |
| 인증서 | `${LAB_OPENSEARCH_CERT_DIR}`의 별도 CA/node 인증서를 읽기 전용 mount; 값이 없으면 정적 render도 실패 |
| 인증 | LAB 노드는 내부 basic 인증만 구성하고, LAB Dashboards는 LAB 노드만 사용; 정상 Keycloak/OIDC와 게이트웨이 라우트를 사용하지 않음 |

LAB Dashboard에는 검증용 `rootCA.pem`만 파일로 mount하고 node 개인키는
전달하지 않습니다. LAB node는 저장소의 custom OpenSearch Dockerfile과 내부 사용자 렌더러를
재사용합니다. 렌더러가 기대하는 컨테이너 내부 secret 이름에는 LAB secret을
alias로 연결하지만 호스트 secret과 데이터는 별개입니다. 모든 빌드·설정 mount
경로는 `labs/` 기준 `../infra/04-data/opensearch/...`를 사용합니다. LAB
Dashboard는 정상 Dashboard 설정 파일을 mount하지 않으며 LAB backend를
환경 입력으로 지정합니다.

LAB node healthcheck는 Docker secret을 curl 설정 stdin으로 전달하며, 비밀번호를
명령 인자에 넣지 않습니다. Node 시작 스크립트는 Bash 단일 인자로 렌더합니다.

현재 Dockerfile은 OpenSearch 기본 이미지와 exporter plugin의 선언 버전 호환성이 검증되지 않아
이미지 빌드 호환성은 해결되지 않았습니다. LAB 인증서의 SAN, node DN,
서로의 신뢰, 관리자 DN, Dashboards 인증 및 클러스터 결성도 실제 검증 전입니다.
따라서 소스 분리의 정적 검사를 통과해도 LAB 기동·건강·복구는 `NOT_RUN`이고
runtime 승인은 막혀 있습니다. 이 LAB의 데이터 보존과 삭제는 정상 HOME의
데이터와 별도로 승인받아야 합니다.

## Usage

정적 검사는 저장소 루트에서 별도 LAB entrypoint를 대상으로 합니다. 아래
절대 경로는 **정적 render용 합성 참조**이며 실제 비밀·인증서를 뜻하지 않습니다.
기동에는 승인된 LAB 전용 경로를 별도로 지정합니다.

```bash
LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --quiet
LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --services
```

기동 전 Docker context, 별도 프로젝트 이름, 모든 내부/호스트 포트, 네트워크,
볼륨, 인증서·secret 참조, 호스트 CPU/메모리/디스크와 정확한 정리 범위를
재확인합니다. 기존 HOME나 LAB 컨테이너의 중지·재시작·삭제, 백업·복구 및
비밀 발급은 별도 승인입니다. 운영 정책은 [문서 진입점](../docs/README.md)에서
찾습니다. 공식 자료: [OpenSearch Docker 설치](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/),
[Dashboards Docker 설정](https://docs.opensearch.org/latest/install-and-configure/install-dashboards/docker/).

## Related Documents

- [OpenSearch LAB Compose](opensearch-cluster.yml)
- [운영 가이드 목록](../docs/05.operations/guides/README.md)
