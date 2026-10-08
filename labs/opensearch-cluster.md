---
title: "OpenSearch Cluster LAB"
version: "0.1.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
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
| 상태 | `node1`, `node2`, `node3`, `dashboards` 상태를 `${LAB_DATA_DIR}/opensearch-cluster/` 아래에 bind. 이전 project named volume은 이동·삭제하지 않음 (SPEC-0215) |
| 네트워크 | `lab_opensearch_core_net`만 사용; 정상 `edge_net`·`obs_net`에 접속하지 않음 |
| 노출 | 호스트 publish 포트와 Traefik 라우터 없음; API 9200, 모니터링 9600, Dashboards 5601은 내부 expose만 |
| 비밀 | `${LAB_SECRET_DIR}/opensearch-cluster/`의 `lab_opensearch_admin_password`, `lab_opensearch_dashboard_password`, `lab_opensearch_exporter_password`, `lab_opensearch_security_cookie`; 정상 비밀을 재사용하지 않음 |
| 인증서 | `${LAB_OPENSEARCH_CERT_DIR}`의 별도 CA/node 인증서를 읽기 전용 mount; 값이 없으면 정적 render도 실패 |
| Project | `hy-home-lab-opensearch` |
| Services | `opensearch-node1`, `opensearch-node2`, `opensearch-node3`, `lab-opensearch-dashboards` |
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

exporter plugin은 OpenSearch 기본 이미지와 같은 `3.8.0.0`이어야 이미지가 빌드됩니다.
node 인증서 subject는 `CN=opensearch-node*`에 맞아야 합니다(`plugins.security.nodes_dn`).
LAB 인증서가 IP SAN만 가질 수 있어 transport hostname 검증은 끕니다.
Dashboards는 `labs/opensearch-cluster-dashboards.config`를 설정 파일로 읽습니다.
이미지의 env→옵션 변환을 거치지 않으므로 비밀번호는 환경 변수 참조로만 들어가고
명령 인자에 남지 않습니다. node healthcheck는 비밀번호를 curl 설정 문법에 맞게
escape하므로 특수문자가 있어도 동작합니다. 빈 값과 줄바꿈만 거부합니다.
SPEC-0215 TSK-0002에서 HOME 호스트로 기동해 green, node 3개, Dashboards healthy를
확인했고, `down` 뒤 container·network는 0개였습니다. 호스트 디스크가 OpenSearch
high watermark(90%)를 넘으면 보안 index를 배치하지 못하므로 디스크 여유를 먼저 확인합니다. 이 LAB의 데이터 보존과 삭제는 정상 HOME의
데이터와 별도로 승인받아야 합니다.

## Usage

정적 검사는 저장소 루트에서 별도 LAB entrypoint를 대상으로 합니다. 아래
절대 경로는 **정적 render용 합성 참조**이며 실제 비밀·인증서를 뜻하지 않습니다.
기동에는 승인된 LAB 전용 경로를 별도로 지정합니다.

```bash
LAB_DATA_DIR=/tmp/synthetic-lab-data LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --quiet
LAB_DATA_DIR=/tmp/synthetic-lab-data LAB_SECRET_DIR=/tmp/synthetic-lab-secrets LAB_OPENSEARCH_CERT_DIR=/tmp/synthetic-lab-certs \
  docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --services
```

기동과 종료는 `python3 scripts/operations/lab.py up opensearch-cluster --purpose "<목적>" --lease <기간>`과 `lab.py down opensearch-cluster`로 하며, 충돌·예산 검사와 정리 대상 ledger는 `POL-0078`을 따른다.

기동 전 Docker context, 별도 프로젝트 이름, 모든 내부/호스트 포트, 네트워크,
볼륨, 인증서·secret 참조, 호스트 CPU/메모리/디스크와 정확한 정리 범위를
재확인합니다. 기존 HOME나 LAB 컨테이너의 중지·재시작·삭제, 백업·복구 및
비밀 발급은 별도 승인입니다. 운영 정책은 [문서 진입점](../docs/README.md)에서
찾습니다. 공식 자료: [OpenSearch Docker 설치](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/),
[Dashboards Docker 설정](https://docs.opensearch.org/latest/install-and-configure/install-dashboards/docker/).

## Bind State Ownership

`lab.py up`은 `${LAB_DATA_DIR}` 아래 bind 디렉터리를 실행 사용자 소유로 만든다. 이 LAB의 데이터 프로세스는 uid 1000 (`opensearch`)로 쓰므로, 디렉터리 소유권이 맞지 않으면 기동이 실패할 수 있다. 실패하면 해당 LAB 경로만 그 uid로 소유권을 맞추고 HOME 경로는 건드리지 않는다.

## Related Documents

- [OpenSearch LAB Compose](opensearch-cluster.yml)
- [운영 가이드 목록](../docs/05.operations/guides/README.md)
