---
title: "Terrakube Usage Guide"
version: "3.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
layer: "operations"
artifact_id: "GDE-0069"
parent_ids:
- "POL-0069"
implementation_services:
  labs/terrakube/docker-compose.yml:
  - terrakube-api
  - terrakube-executor
  - terrakube-pg
  - terrakube-ui
  - terrakube-valkey
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# Terrakube Usage Guide

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

Terrakube LAB을 실험하고 HOME 퇴역을 확인하는 담당자.

##### Outcome

Terrakube는 독립 LAB인 [Terrakube LAB](../../../../labs/terrakube/README.md)(`lab-terrakube` profile)이다.
ADR-0062 item 9와 2026-11-26 owner 결정(SPEC-0263 TSK-0004)으로 HOME `09-platform-ops`에서 옮겼다.
root Compose에 포함되지 않고 HOME network에 연결되지 않으며 Traefik route가 없다. HOME의 IaC 실행은
OpenTofu가 맡는다. 장애 진단과 백업·복원은 [Terrakube Runbook](../../03.runbooks/15.labs/0069-terrakube.md)이 맡는다.

###### Boundaries
<!-- core-payload-level:4 -->

- [Policy](../../02.policies/15.labs/0069-terrakube.md) (`POL-0069`)
- [Runbook](../../03.runbooks/15.labs/0069-terrakube.md) (`RUN-0069`)
- [Platform Operations·Quality 아키텍처](../../../02.architecture/01.descriptions/0009-tooling-architecture.md)

- [Terrakube architecture](https://docs.terrakube.io/architecture)
- [Terrakube project and Apache-2.0 license](https://github.com/terrakube-io/terrakube)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)
- [Operations index](../../README.md)

#### Prerequisites

##### Environment

###### 분류와 토폴로지
<!-- core-payload-level:4 -->

Terrakube는 on-demand LAB IaC 협업 플랫폼이다. API, UI, executor와 LAB 전용 PostgreSQL·Valkey가
`lab-terrakube` profile에 속하고 `lab.py`가 lease로만 기동한다. 각 컴포넌트는 복제본 하나이며
고가용성을 제공하거나 주장하지 않는다.

###### 구현과 데이터 흐름
<!-- core-payload-level:4 -->

- [Terrakube LAB Compose](../../../../labs/terrakube/docker-compose.yml)가 서비스, 이미지, secret,
  healthcheck, loopback 게시를 정의한다.
- 브라우저 -> `${LAB_HOST_BIND_IP}:${LAB_TERRAKUBE_UI_HOST_PORT:-18097}`(UI) -> `:18096`(API);
  API는 LAB network 안의 `terrakube-executor:8090`으로 작업을 전달한다.
- 로그인은 Keycloak `hy-home.realm`의 LAB 전용 public client `lab-terrakube`이다. API는 HOME 공개
  gateway 이름으로 issuer를 조회하고 HOME root CA를 Paketo `ca-certificates` binding으로 신뢰한다.
- PostgreSQL(`terrakube-pg`)이 메타데이터를, Valkey(`terrakube-valkey`)가 작업 조정과 실시간 출력을
  맡는다. Terraform state·plan·출력은 `StorageType: LOCAL`로 `${LAB_DATA_DIR}/terrakube/state`에
  저장되며 API와 executor가 같은 volume을 쓴다.
- Secret은 `${LAB_SECRET_DIR}/terrakube/`의 네 파일(LAB-038~041)이며 Spring `configtree`로 설정
  이름과 같은 파일명에서 읽는다. 값은 증거에 넣지 않는다.
- executor에는 Docker socket이 없다(owner 결정 2026-11-26).
- health endpoint는 프로세스 준비만 증명하며 OIDC 로그인과 실제 plan 실행을 증명하지 않는다.

##### Authority

Secret 사본 생성과 Keycloak client 등록은 owner가 한다. LAB 기동은 `lab.py` lease가 필요하고 인프라
apply·destroy는 별도의 원격 변경 승인이 필요하다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | `python3 scripts/operations/lab.py check terrakube`로 render, 충돌, secret 경로를 검사한다. | 오류 없이 끝난다. | 보고된 입력이나 충돌을 고친 뒤 다시 검사한다. |
| 2 | owner가 LAB secret 네 파일과 Keycloak client `lab-terrakube`(redirect `http://localhost:18097/*`)를 준비한다. | 파일과 client가 있다. | 기동하지 않고 owner에게 넘긴다. |
| 3 | 승인된 lease로 `lab.py up terrakube`를 실행하고 다섯 container의 health를 확인한다. | 모두 healthy다. | Runbook의 진단 절차를 따른다. |
| 4 | UI에서 로그인하고 비적용 plan 하나로 executor 실행을 확인한다. | plan이 끝나고 state 디렉터리에 결과가 생긴다. | 인증 오류를 우회하지 않고 `@buenhyden`에게 보고한다. |
| 5 | 인프라를 apply하거나 destroy하려면 별도의 원격 변경 승인을 받는다. | 승인 기록이 있다. | 실행하지 않는다. |

##### Expected Results

- `python3 scripts/operations/lab.py check terrakube`
- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops`

#### Troubleshooting

##### Symptoms

위 Expected Results가 실패하거나 서비스 동작이 기대와 다르면 증상과 출력 요약을 기록하고 [Runbook](../../03.runbooks/15.labs/0069-terrakube.md)의 절차로 진단한다.

###### Runbook Handoff
<!-- core-payload-level:4 -->

실행 실패, 백업/복원, OIDC 진단, 업그레이드에는
[runbook](../../03.runbooks/15.labs/0069-terrakube.md)을 사용한다.

##### Next Action

실행 실패, 백업/복원, OIDC 진단, 업그레이드는 [runbook](../../03.runbooks/15.labs/0069-terrakube.md)을 따른다. 인증 오류는 우회하지 말고 `@buenhyden`에게 보고한다.

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
