---
title: "독립 LAB 문서 정책"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
layer: "operations"
---

# 독립 LAB 문서 정책

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

독립 LAB 문서의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

##### Excluded Responsibilities

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| `0022-valkey-cluster.md` | 이 정책은 현재 source 구성을 데이터 보호, 보안, 자원, 수명주기 통제와 독립적으로 검증 가능한 운영 통제에 묶는다. 대상은 `labs/valkey-cluster/docker-compose.yml`의 LAB 전용 Valkey Cluster이다. |
| `0025-cassandra.md` | 독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다. |
| `0026-couchdb.md` | `labs/couchdb/docker-compose.yml`의 CouchDB 3노드 LAB cluster의 loopback 접근, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| `0027-mongodb.md` | `labs/mongodb/docker-compose.yml`의 MongoDB replica set LAB의 `mongodb` profile, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| `0031-postgresql-cluster.md` | `labs/postgresql-ha/docker-compose.yml`의 PostgreSQL HA LAB(etcd·Patroni·HAProxy)의 `postgres-ha` profile, 접근 경계, 백업·복구 기준을 정의한다. |
| `0057-open-webui.md` | Open WebUI LAB의 native OIDC, LAB 경계, data·secret 취급과 HOME 잔여 상태 퇴역 승인을 통제한다. |
| `0062-locust.md` | Locust는 독립 LAB capability이며, 이 정책은 test target 보호와 검토되지 않은 load·credential 수집·오해를 부르는 성능 증거를 막는다. |
| `0066-sonarqube.md` | 이 정책은 독립 LAB `labs/sonarqube/docker-compose.yml`의 SonarQube Community Build 배포를 다룬다. |
| `0069-terrakube.md` | Terrakube LAB의 기동, native OIDC, provider 권한, LAB 전용 데이터, 복구, 업그레이드, 제거를 통제한다. |
| `0070-mail.md` | Stalwart는 독립 LAB `labs/stalwart/docker-compose.yml`의 메일 서비스다. |
| `0089-jupyterlab.md` | JupyterLab LAB은 임의의 코드를 실행한다. mandatory token, loopback 게시, 단일 사용자와 work directory 보존을 통제한다. |
| `0090-dbt.md` | dbt LAB의 권한은 source 읽기와 target schema 소유로 제한하며 HOME dev-pg endpoint는 별도 승인으로만 연다. |
| `0094-lakehouse.md` | lakehouse LAB 엔진의 identity 범위, 파괴적 유지보수, 테스트 데이터 분리와 HOME catalog endpoint 승인을 통제한다. |
| `0097-superset.md` | Superset LAB의 native OIDC 로그인, role 부여, 자격 증명 처리와 HOME mng-pg endpoint 승인을 통제한다. |
| `0107-lab-promotion.md` | LAB 구조, 승격 manifest, secret, 목적지 규칙, readiness 규칙과 host reserve를 정한다. |
| `0108-kafka-cluster.md` | Kafka LAB의 cluster ID 분리, internal network, 데이터 경로와 승격 경계를 통제한다. |
| `0109-opensearch-cluster.md` | OpenSearch LAB의 LAB secret·인증서, internal network, 데이터 경로와 승격 경계를 통제한다. |

###### Current Items
<!-- core-payload-level:4 -->

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Valkey Cluster Operations Policy](0022-valkey-cluster.md) | `POL-0022` | 이 정책은 현재 source 구성을 데이터 보호, 보안, 자원, 수명주기 통제와 독립적으로 검증 가능한 운영 통제에 묶는다. 대상은 `labs/valkey-cluster/docker-compose.yml`의 LAB 전용 Valkey Cluster이다. |
| [Cassandra Operations Policy](0025-cassandra.md) | `POL-0025` | 독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다. |
| [CouchDB Operations Policy](0026-couchdb.md) | `POL-0026` | `labs/couchdb/docker-compose.yml`의 CouchDB 3노드 LAB cluster의 loopback 접근, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| [MongoDB Operations Policy](0027-mongodb.md) | `POL-0027` | `labs/mongodb/docker-compose.yml`의 MongoDB replica set LAB의 `mongodb` profile, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| [PostgreSQL Cluster Operations Policy](0031-postgresql-cluster.md) | `POL-0031` | `labs/postgresql-ha/docker-compose.yml`의 PostgreSQL HA LAB(etcd·Patroni·HAProxy)의 `postgres-ha` profile, 접근 경계, 백업·복구 기준을 정의한다. |
| [Open WebUI Operations Policy](0057-open-webui.md) | `POL-0057` | Open WebUI LAB의 native OIDC, LAB 경계, data·secret 취급과 HOME 잔여 상태 퇴역 승인을 통제한다. |
| [Locust Operations Policy](0062-locust.md) | `POL-0062` | Locust는 독립 LAB capability이며, 이 정책은 test target 보호와 검토되지 않은 load·credential 수집·오해를 부르는 성능 증거를 막는다. |
| [SonarQube Operations Policy](0066-sonarqube.md) | `POL-0066` | 이 정책은 독립 LAB `labs/sonarqube/docker-compose.yml`의 SonarQube Community Build 배포를 다룬다. |
| [Terrakube Operations Policy](0069-terrakube.md) | `POL-0069` | Terrakube LAB의 기동, native OIDC, provider 권한, LAB 전용 데이터, 복구, 업그레이드, 제거를 통제한다. |
| [Stalwart Mail Operations Policy](0070-mail.md) | `POL-0070` | Stalwart는 독립 LAB `labs/stalwart/docker-compose.yml`의 메일 서비스다. |
| [JupyterLab Operations Policy](0089-jupyterlab.md) | `POL-0089` | JupyterLab LAB은 임의의 코드를 실행한다. mandatory token, loopback 게시, 단일 사용자와 work directory 보존을 통제한다. |
| [dbt Operations Policy](0090-dbt.md) | `POL-0090` | dbt LAB의 권한은 source 읽기와 target schema 소유로 제한하며 HOME dev-pg endpoint는 별도 승인으로만 연다. |
| [Lakehouse Operations Policy](0094-lakehouse.md) | `POL-0094` | lakehouse LAB 엔진의 identity 범위, 파괴적 유지보수, 테스트 데이터 분리와 HOME catalog endpoint 승인을 통제한다. |
| [Superset Operations Policy](0097-superset.md) | `POL-0097` | Superset LAB의 native OIDC 로그인, role 부여, 자격 증명 처리와 HOME mng-pg endpoint 승인을 통제한다. |
| [LAB Promotion Policy](0107-lab-promotion.md) | `POL-0107` | LAB 구조, 승격 manifest, secret, 목적지 규칙, readiness 규칙과 host reserve를 정한다. |
| [Kafka Cluster LAB Operations Policy](0108-kafka-cluster.md) | `POL-0108` | Kafka LAB의 cluster ID 분리, internal network, 데이터 경로와 승격 경계를 통제한다. |
| [OpenSearch Cluster LAB Operations Policy](0109-opensearch-cluster.md) | `POL-0109` | OpenSearch LAB의 LAB secret·인증서, internal network, 데이터 경로와 승격 경계를 통제한다. |

###### Classification
<!-- core-payload-level:4 -->

이 폴더의 문서는 모두 정책 역할이며 `POL-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

##### Owners

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [문서 작성 계약](../../../00.workspace/03.process/documentation-protocol.md)
- [README 템플릿](../../../99.templates/02.templates/93.common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

이동 대상은 LAB 관련 운영 문서다. 서비스 소스는 저장소 루트 `labs/`가 소유한다.
문서 이동은 LAB 서비스 기동, 배포, 비밀번호 변경, 데이터 이동·삭제 또는 복구 실행을 뜻하지 않는다.

###### Transition and Exit
<!-- core-payload-level:4 -->

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. superseded 또는 retired에 이른 문서는 [은퇴 전제 조건](../../../00.workspace/03.process/documentation-protocol.md#retirement-preconditions)을 모두 충족할 때에만 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
