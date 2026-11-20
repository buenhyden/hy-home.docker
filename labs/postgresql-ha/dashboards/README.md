---
title: "PostgreSQL HA LAB 대시보드"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-11-05"
---

# PostgreSQL HA LAB 대시보드

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

이 LAB 전용 Grafana 대시보드 JSON과 그 출처를 보관합니다. HOME Grafana는
`infra/06-observability/grafana/dashboards/`만 provisioning하므로 이 파일들은
HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지 않습니다.

###### Audience
<!-- core-payload-level:4 -->

LAB source 관리자와 관측 연결을 검토하는 운영자입니다.

###### Scope
<!-- core-payload-level:4 -->

대시보드 JSON과 출처 기록만 소유합니다. HOME Grafana provisioning, HOME
Prometheus scrape·alert rule, LAB 관측 stack의 기동·연결은 범위 밖입니다.

###### Structure
<!-- core-payload-level:4 -->

- [etcd-cluster.json](etcd-cluster.json): UID `hyhome-etcd`, monitoring-mixins etcd/etcd.json (2026-09-24)
- [haproxy-overview.json](haproxy-overview.json): UID `hyhome-haproxy`, grafana.com dashboard 12693 revision 14 (2026-04-11)

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

입력은 위 Structure 목록의 출처에서 가져온 대시보드 JSON이다. HOME Grafana provisioning 경로 `infra/06-observability/grafana/dashboards/`에는 연결되지 않는다.

###### Security Boundary
<!-- core-payload-level:4 -->

이 디렉터리는 대시보드 JSON과 출처 기록만 소유하며 secret, 포트, network를 선언하지 않는다. HOME Grafana와 HOME Prometheus에서 분리되어 있다.

#### Usage

##### Prerequisites

없음: 이 디렉터리는 Grafana 대시보드 JSON만 보관하므로 실행 환경이 없다. LAB 관측 연결 계약이 승인되면 그 LAB의 Grafana가 파일을 읽는다.

##### Selected Start

LAB 관측을 연결하는 별도 계약이 승인되면 그 LAB의 Prometheus·Grafana가 이
파일을 읽도록 구성합니다. HOME provisioning 경로로 옮기지 않습니다.

#### Checks

##### Readiness

없음: 이 디렉터리에는 실행 가능한 검증 명령이 없다. 파일의 UID와 출처는 Structure 목록이 기록한다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [상위 LAB source](../README.md)
- [Grafana README](../../../infra/06-observability/grafana/README.md)

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: HOME Prometheus가 LAB 서비스를 수집하지 않으므로 이 대시보드로 관측되는 데이터가 아직 없다. LAB 운영은 [상위 LAB README](../README.md)와 [15-labs runbooks](../../../docs/05.operations/03.runbooks/15.labs/README.md)의 RUN-0031 PostgreSQL 클러스터 Runbook를 따른다.

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
