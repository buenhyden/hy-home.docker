<!-- Target: docs/07.guides/04-data/analytics/warehouses.md -->

# Warehouse (StarRocks) System Guide

> High-performance analytical database for real-time analytics.

---

## Overview (KR)

이 문서는 StarRocks 데이터 웨어하우스 시스템에 대한 가이드다. OLAP 엔진의 구조(FE/BE), SQL 인터페이스 사용법, 대규모 데이터 세트의 실시간 분석 및 시각화 도구 연동 방법을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Data Engineer
- Analytics Developer
- AI Agents

## Purpose

StarRocks의 분산 분석 아키텍처를 이해하고, 대규모 데이터를 초 단위로 분석할 수 있는 SQL 환경을 구축 및 활용하는 것을 돕는다.

## Prerequisites

- `hy-home.docker` 인프라 네트워크 (`infra_net`) 지식.
- MySQL 프로토콜 및 SQL 문법 이해.
- `DEFAULT_DATA_DIR` 환경 변수 설정 확인.

## Step-by-step Instructions

### 1. Connection via MySQL Client

StarRocks는 MySQL 프로토콜과 호환된다.

```bash
# FE 노드 접속 (기본 포트 9030)
mysql -u root -h starrocks-fe -P 9030
```

### 2. Creating Tables

StarRocks는 여러 데이터 모델(Duplicate, Aggregate, Primary Key)을 지원한다.

```sql
CREATE DATABASE demo;
USE demo;

CREATE TABLE sales (
    sale_date DATE,
    product_id INT,
    amount DECIMAL(10, 2)
)
ENGINE=OLAP
DUPLICATE KEY(sale_date, product_id)
DISTRIBUTED BY HASH(product_id) BUCKETS 3;

```

### 3. Data Ingestion (Stream Load)

HTTP API를 사용하여 대량의 데이터를 빠르게 로드한다.

```bash
curl --location-trusted -u root: \
    -H "label:sales_load_1" \
    -H "column_separator:," \
    -T sales_data.csv \
    -XPUT http://starrocks-fe:8030/api/demo/sales/_stream_load
```

## Common Pitfalls

- **BE Node Alive Status**: BE 노드가 FE에 정상적으로 추가되지 않으면 쿼리가 수행되지 않는다. `SHOW BACKENDS;` 명령어로 상태를 확인해야 한다.
- **Ulimit Restrictions**: BE 노드는 고성능 처리를 위해 높은 `ulimit` 설정을 요구한다. 컨테이너 내부 또는 호스트에서 조정이 필요하다.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [warehouses.md](../../../08.operations/04-data/analytics/warehouses.md)
- **Runbook**: [warehouses.md](../../../09.runbooks/04-data/analytics/warehouses.md)
