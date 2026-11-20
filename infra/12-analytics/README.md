---
title: "12 Analytics"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-10-01"
---

# 12 Analytics

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

#### Service

##### Purpose

이 tier에는 현재 root Compose가 include하는 패키지가 없습니다. 데이터 처리·SQL
조회·품질 검증·BI·변환·notebook 패키지는 SPEC-0262에서 독립 LAB entrypoint로
옮겼습니다. ADR-0062 capability tier 이름은 유지합니다.

###### Audience
<!-- core-payload-level:4 -->

데이터 엔지니어, 분석 사용자와 패키지 운영자를 위한 안내입니다.

###### Scope
<!-- core-payload-level:4 -->

분석 패키지의 현재 위치 안내만 소유합니다. 공유 저장소는 [04 Data](../04-data/README.md),
MLflow는 [08 AI](../08-ai/README.md)에 남습니다.

###### Structure
<!-- core-payload-level:4 -->

| LAB | Entry point | 서비스 | Source 자산 |
| --- | --- | --- | --- |
| Lakehouse | [labs/lakehouse/docker-compose.yml](../../labs/lakehouse/docker-compose.yml) | `seaweedfs-table-bucket`, `spark`, `trino`, `great-expectations`, `flink-jobmanager`, `flink-taskmanager` | `labs/lakehouse/` |
| dbt | [labs/dbt/docker-compose.yml](../../labs/dbt/docker-compose.yml) | `dbt-db-provision`, `dbt` | `labs/dbt/` |
| Superset | [labs/superset/docker-compose.yml](../../labs/superset/docker-compose.yml) | `superset-db-provision`, `superset-init`, `superset` | `labs/superset/` |
| JupyterLab | [labs/jupyterlab/docker-compose.yml](../../labs/jupyterlab/docker-compose.yml) | `jupyterlab` | `labs/jupyterlab/` |

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

없음: 이 tier는 입출력을 제공하지 않는다. LAB이 쓰는 HOME SeaweedFS·mng-pg·dev-pg·MLflow endpoint는 `labs/.env.example`의 입력으로만 지정한다.

###### Security Boundary
<!-- core-payload-level:4 -->

이 tier는 secret, 포트, network를 선언하지 않는다. LAB은 HOME network에 연결되지 않으며 도달 가능한 HOME endpoint는 별도 승인 대상이다.

#### Usage

##### Prerequisites

없음: 이 tier에는 root Compose가 include하는 패키지가 없어 지원 런타임이 없다. 분석 패키지의 런타임은 독립 LAB이 각자 선언한다.

##### Selected Start

- LAB은 HOME network에 연결되지 않습니다. HOME SeaweedFS·mng-pg·dev-pg·MLflow는
  `labs/.env.example`의 endpoint 입력으로만 지정하며, 도달 가능한 endpoint는 별도 승인 대상입니다.
- tier 정적 점검: `bash scripts/hardening/check-all-hardening.sh 12-analytics`
  (LAB source를 점검합니다).

#### Checks

##### Readiness

tier 정적 점검은 `bash scripts/hardening/check-all-hardening.sh 12-analytics`이며 통과는 LAB 실행을 증명하지 않는다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [LAB source](../../labs/README.md)
- [인프라 인덱스](../README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 tier에는 실행 서비스가 없다. LAB 운영은 [LAB Runbook 목록](../../docs/05.operations/03.runbooks/15.labs/README.md)을 따른다.

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
