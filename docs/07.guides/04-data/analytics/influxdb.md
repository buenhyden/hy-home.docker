<!-- Target: docs/07.guides/04-data/analytics/influxdb.md -->

# InfluxDB (TSDB) Guide

> Comprehensive guide for managing InfluxDB 3.x and 2.x in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 InfluxDB 시계열 데이터베이스에 대한 가이드다. 시스템의 아키텍처, V3(Core)와 V2(Legacy)의 차이점, 그리고 Telegraf/Grafana와의 연동 방법을 설명한다. 플랫폼 성능 지표 및 비즈니스 매트릭 수집의 핵심 진입점을 다룬다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

이 가이드는 운영자가 인프라 내 InfluxDB 구성을 이해하고, 개발자가 성능 모니터링 및 분석을 위해 데이터베이스와 상호작용하는 방법을 익히도록 돕는다.

## Prerequisites

- `infra_net` 네트워크 접근 권한.
- Docker 및 Docker Compose 설치 완료.
- `secrets/influxdb_api_token` 내 유효한 API 토큰.

## Step-by-step Instructions

### 1. 버전 선택 (Version Selection)

환경은 다음 두 가지 버전을 지원한다:

- **v3 (Core)**: 고성능 및 SQL 지원을 위해 선호됨. `docker-compose.yml` 사용.
- **v2 (Legacy)**: 기존 Flux 스크립트 호환성을 위해 사용. `docker-compose.v2.yml` 사용.

### 2. 기본 버킷 관리 (Basic Bucket Management)

버킷은 특정 보존 정책을 가진 데이터를 저장하는 단위다.

```bash
# InfluxDB 3.x (via influx3 CLI)
influx3 bucket create --name my-metrics --retention 90d

# InfluxDB 2.x (via influx CLI)
influx bucket create -n my-metrics -r 90d
```

### 3. 검증 및 상태 확인 (Verification & Health Check)

```bash
# Endpoint: http://influxdb:8181 (v3) or http://influxdb:8086 (v2)
curl -i http://influxdb:8181/health
```

## Common Pitfalls

- **토큰 불일치 (Token Mismatch)**: Telegraf나 k6에서 사용하는 토큰이 Docker Secrets에 저장된 토큰과 일치하는지 확인한다.
- **포트 충돌 (Port Conflict)**: v3는 `8181`, v2는 `8086`을 기본값으로 사용한다. 애플리케이션 연결 정보를 확인한다.
- **보존 제약 (Retention Limits)**: 보존 정책 없이 대량의 데이터를 수집할 경우 `${DEFAULT_DATA_DIR}`의 디스크 공간이 고갈될 수 있다.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [influxdb.md](../../../08.operations/04-data/analytics/influxdb.md)
- **Runbook**: [influxdb.md](../../../09.runbooks/04-data/analytics/influxdb.md)
