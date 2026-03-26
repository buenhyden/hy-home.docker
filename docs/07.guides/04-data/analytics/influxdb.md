<!-- Target: docs/07.guides/04-data/analytics/influxdb.md -->

# InfluxDB (TSDB) Guide

> Comprehensive guide for managing InfluxDB 3.x and 2.x in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 InfluxDB 시계열 데이터베이스에 대한 가이드다. 시스템의 아키텍처, V3와 V2의 차이점, 그리고 Telegraf/Grafana와의 연동 방법을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

This guide helps operators and developers understand how InfluxDB is configured within the infrastructure and how to interact with it for performance monitoring.

## Prerequisites

- Access to `infra_net` network.
- Docker and Docker Compose installed.
- Valid API Token in `secrets/influxdb_api_token`.

## Step-by-step Instructions

### 1. Version Selection
The environment supports two versions:
- **v3 (Core)**: Preferred for high performance and SQL support. Use `docker-compose.yml`.
- **v2 (Legacy)**: Used for compatibility with older Flux scripts. Use `docker-compose.v2.yml`.

### 2. Basic Bucket Management
Buckets are used to store data with specific retention policies.

```bash
# InfluxDB 3.x (via influx3 CLI)
influx3 bucket create --name my-metrics --retention 90d

# InfluxDB 2.x (via influx CLI)
influx bucket create -n my-metrics -r 90d
```

### 3. Verification & Health Check

```bash
# Endpoint: http://influxdb:8181 (v3) or http://influxdb:8086 (v2)
curl -i http://influxdb:8181/health
```

## Common Pitfalls

- **Token Mismatch**: Ensure the token used in Telegraf or k6 matches the one stored in Docker Secrets.
- **Port Conflict**: V3 defaults to `8181`, while V2 defaults to `8086`. Check your application URLs.
- **Retention Limits**: Large datasets without retention policies can deplete `${DEFAULT_DATA_DIR}` disk space.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [influxdb.md](../../../08.operations/04-data/analytics/influxdb.md)
- **Runbook**: [influxdb.md](../../../09.runbooks/04-data/analytics/influxdb.md)
