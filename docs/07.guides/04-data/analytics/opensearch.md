<!-- Target: docs/07.guides/04-data/analytics/opensearch.md -->

# OpenSearch System Guide

> Distributed search and analytics engine with Dashboards.

---

## Overview (KR)

이 문서는 OpenSearch 시스템에 대한 가이드다. 검색 엔진의 구조, API 사용법, Dashboards를 통한 시각화 및 문제 해결 방법을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- AI Agents

## Purpose

OpenSearch 클러스터의 아키텍처를 이해하고, 검색 API 및 시각화 도구를 효과적으로 활용하는 것을 돕는다.

## Prerequisites

- `hy-home.docker` 인프라 네트워크 (`infra_net`) 지식.
- Docker Secrets 및 기본 HTTPS 통신 이해.
- `opensearch-admin_password` 시크릿 접근 권한.

## Step-by-step Instructions

### 1. API Access (REST)

OpenSearch는 `9200` 포트를 통해 검색 API를 제공한다.

```bash
# 클러스터 헬스 체크
curl -X GET "https://opensearch:9200/_cluster/health" -u admin:<password> --insecure
```

### 2. Dashboards Usage

데이터 시각화 및 매니지먼트를 위해 Dashboards UI에 접속한다.

- URL: `https://opensearch-dashboard.${DEFAULT_URL}`
- 기본 계정: `admin`

### 3. Index Management

매핑 설정 및 인덱스 생성을 수행한다.

```bash
curl -X PUT "https://opensearch:9200/my-index" -u admin:<password> --insecure -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 2
    }
  }
}'
```

## Common Pitfalls

- **Memory Lock Fail**: `bootstrap.memory_lock=true` 설정에도 불구하고 호스트 시스템의 `ulimit` 제한으로 인해 메모리 락이 실패할 수 있다.
- **Certificate Mismatch**: 커스텀 인증서 적용 시 도메인 이름 불일치로 인한 통신 오류가 발생할 수 있다.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [opensearch.md](../../../08.operations/04-data/analytics/opensearch.md)
- **Runbook**: [opensearch.md](../../../09.runbooks/04-data/analytics/opensearch.md)
