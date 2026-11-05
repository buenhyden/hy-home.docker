---
title: "PostgreSQL HA LAB 대시보드"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-05"
created: "2026-11-05"
---

# PostgreSQL HA LAB 대시보드

## Overview

이 LAB 전용 Grafana 대시보드 JSON과 그 출처를 보관합니다. HOME Grafana는
`infra/06-observability/grafana/dashboards/`만 provisioning하므로 이 파일들은
HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지 않습니다.

## Audience

LAB source 관리자와 관측 연결을 검토하는 운영자입니다.

## Scope

대시보드 JSON과 출처 기록만 소유합니다. HOME Grafana provisioning, HOME
Prometheus scrape·alert rule, LAB 관측 stack의 기동·연결은 범위 밖입니다.

## Structure

- [etcd-cluster.json](etcd-cluster.json): UID `hyhome-etcd`, monitoring-mixins etcd/etcd.json (2026-09-24)
- [haproxy-overview.json](haproxy-overview.json): UID `hyhome-haproxy`, grafana.com dashboard 12693 revision 14 (2026-04-11)

## Usage

LAB 관측을 연결하는 별도 계약이 승인되면 그 LAB의 Prometheus·Grafana가 이
파일을 읽도록 구성합니다. HOME provisioning 경로로 옮기지 않습니다.

## Related Documents

- [상위 LAB source](../README.md)
- [Grafana README](../../../infra/06-observability/grafana/README.md)
