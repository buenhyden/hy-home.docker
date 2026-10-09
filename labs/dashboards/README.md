---
title: "LAB Dashboards"
version: "0.1.0"
type: "common/readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-10-09"
---

# LAB Dashboards

## Overview

독립 LAB(`labs/*.yml`) 전용 Grafana 대시보드 JSON을 보존하는 위치입니다. HOME
Grafana는 `infra/06-observability/grafana/dashboards/`만 provisioning하므로 이
파일들은 HOME에 표시되지 않습니다. HOME Prometheus는 LAB 서비스를 수집하지 않아 HOME에서는
빈 대시보드였습니다.

## Dashboards

| Dashboard | UID | Source |
| --- | --- | --- |
| `cassandra` | `hyhome-cassandra` | grafana.com dashboard 6400 revision 2 (2018-06-14) |
| `etcd-cluster` | `hyhome-etcd` | monitoring-mixins etcd/etcd.json (2026-09-24) |
| `haproxy-overview` | `hyhome-haproxy` | grafana.com dashboard 12693 revision 14 (2026-04-11) |
| `mongodb` | `hyhome-mongodb` | grafana.com dashboard 16490 revision 1 (2022-06-24) |
| `valkey-cluster` | `hyhome-valkey-cluster` | grafana.com dashboard 21914 revision 1 (2024-09-14) |

## Usage

LAB 관측을 연결하는 별도 계약이 승인되면, 그 LAB의 Prometheus·Grafana가 이
파일을 읽도록 구성합니다. HOME provisioning 경로로 되돌려 놓지 않습니다.

## Related Documents

- [Grafana README](../../infra/06-observability/grafana/README.md)
- [Compose profile vocabulary](../../docs/05.operations/policies/0078-compose-profile-vocabulary.md)
