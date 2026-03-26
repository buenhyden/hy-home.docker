---
tier: 07.guides
component: 06-observability
title: Loki System Guide
status: production
updated: 2026-03-26
---

# Loki System Guide

> Cloud-native log aggregation system for the LGTM stack.

## Overview (KR)

Loki는 Prometheus에서 영감을 받은 로그 집계 시스템으로, 데이터 본문 전체를 인덱싱하는 대신 레이블(Labels)만 인덱싱하여 높은 효율성을 제공한다. `hy-home.docker` 아키텍처에서 Loki는 모든 서비스의 로그를 중앙 집중화하고, Grafana를 통해 시각화 및 분석을 수행한다.

## Strategic Boundaries

- **Ingestion (Push/Pull)**: Alloy 콜렉터가 OTLP 또는 Docker 로그 드라이버를 통해 로그를 수집하여 Loki로 전송한다.
- **Storage (MinIO)**: 로그 데이터(Chunks)와 인덱스는 MinIO S3 버킷에 저장되어 데이터 영속성을 보장한다.
- **Querying (LogQL)**: Grafana Explore 메뉴에서 LogQL을 사용하여 로그를 필터링하고 분석한다.

## Core Workflows

### 1. Log Ingestion Flow

1. **Alloy Discovery**: Alloy가 Docker 엔진을 스캔하여 컨테이너 로그 소스를 찾는다.
2. **Metadata Enrichment**: 컨테이너 이름, 이미지, 레이블 정보를 로그에 주입한다.
3. **Transmission**: OTLP/HTTP를 통해 Loki 인제스터(`http://loki:3100/loki/api/v1/push`)로 전송한다.

### 2. Log Analysis (LogQL)

- **Selection**: `{app="my-app"}`
- **Filtering**: `{app="my-app"} |= "error"`
- **Aggregation**: `count_over_time({app="my-app"}[5m])`

## Step-by-step Instructions

### 1. Searching Logs in Grafana

1. `https://grafana.${DEFAULT_URL}` 접속 및 로그인.
2. 왼쪽 메뉴에서 **Explore** 선택.
3. Datasource로 **Loki** 선택.
4. `Label browser`를 사용하여 수집된 레이블 확인.

### 2. Monitoring Loki Health

- **Readiness Check**: `wget -qO- http://loki:3100/ready`
- **Dashboard**: "Loki / Reads" 및 "Loki / Writes" 대시보드를 통해 처리량 확인.

## Troubleshooting

- **"No logs found"**: 컨테이너가 표준 출력(stdout/stderr)으로 로그를 전달하고 있는지 확인한다.
- **Retention Discrepancy**: `loki-config.yaml`의 `retention_period` 설정을 확인한다.

## Related Documents

- **Infrastructure README**: `[../../../infra/06-observability/loki/README.md]`
- **Operational Policy**: `[../../08.operations/06-observability/loki.md]`
- **Recovery Runbook**: `[../../09.runbooks/06-observability/loki.md]`
- **LGTM Guide**: `[./01.lgtm-stack.md]`
