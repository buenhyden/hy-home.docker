---
title: "Valkey Cluster LAB 대시보드"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-11-05"
---

# Valkey Cluster LAB 대시보드

## Purpose

### Service Role

이 LAB 전용 Grafana 대시보드 JSON과 그 출처를 보관합니다. HOME Grafana는
`infra/06-observability/grafana/dashboards/`만 provisioning하므로 이 파일들은
HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지 않습니다.

#### Audience

LAB source 관리자와 관측 연결을 검토하는 운영자입니다.

#### Scope

대시보드 JSON과 출처 기록만 소유합니다. HOME Grafana provisioning, HOME
Prometheus scrape·alert rule, LAB 관측 stack의 기동·연결은 범위 밖입니다.

#### Structure

- [valkey-cluster.json](valkey-cluster.json): UID `hyhome-valkey-cluster`, grafana.com dashboard 21914 revision 1 (2024-09-14)

### Supported Environment

없음: 이 디렉터리는 Grafana 대시보드 JSON만 보관하므로 실행 환경이 없다. LAB 관측 연결 계약이 승인되면 그 LAB의 Grafana가 파일을 읽는다.

## Interfaces

### Inputs and Outputs

입력은 위 Structure 목록의 출처에서 가져온 대시보드 JSON이다. HOME Grafana provisioning 경로 `infra/06-observability/grafana/dashboards/`에는 연결되지 않는다.

### Security Boundary

이 디렉터리는 대시보드 JSON과 출처 기록만 소유하며 secret, 포트, network를 선언하지 않는다. HOME Grafana와 HOME Prometheus에서 분리되어 있다.

## Development

### Local Workflow

LAB 관측을 연결하는 별도 계약이 승인되면 그 LAB의 Prometheus·Grafana가 이
파일을 읽도록 구성합니다. HOME provisioning 경로로 옮기지 않습니다.

### Checks

없음: 이 디렉터리에는 실행 가능한 검증 명령이 없다. 파일의 UID와 출처는 Structure 목록이 기록한다.

## Operations

### Runbook Links

- [상위 LAB source](../README.md)
- [Grafana README](../../../infra/06-observability/grafana/README.md)

### Observability and Recovery

없음: HOME Prometheus가 LAB 서비스를 수집하지 않으므로 이 대시보드로 관측되는 데이터가 아직 없다. LAB 운영은 [상위 LAB README](../README.md)와 [Valkey Cluster Runbook](../../../docs/05.operations/runbooks/15-labs/0022-valkey-cluster.md)를 따른다.
