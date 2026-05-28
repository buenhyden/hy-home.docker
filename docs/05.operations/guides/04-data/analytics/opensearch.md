---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/analytics/opensearch.md -->

# OpenSearch Usage Guide

## Overview (KR)

이 문서는 OpenSearch 시스템에 대한 가이드다. 검색 엔진의 구조, API 사용법, Dashboards를 통한 시각화 및 문제 해결 방법을 제공한다.

## Usage
>
> Distributed search and analytics engine with Dashboards.

---

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agents

### Purpose

OpenSearch 클러스터의 아키텍처를 이해하고, 검색 API 및 시각화 도구를 효과적으로 활용하는 것을 돕는다.

### Prerequisites

- `hy-home.docker` 인프라 네트워크 (`infra_net`) 지식.
- Docker Secrets 및 기본 HTTPS 통신 이해.
- `opensearch-admin_password` 시크릿 접근 권한.

### Step-by-step Instructions

#### 1. API Access (REST)

OpenSearch는 `9200` 포트를 통해 검색 API를 제공한다.

```bash
## 클러스터 헬스 체크
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -X GET "https://opensearch:9200/_cluster/health" -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" --insecure
unset OPENSEARCH_ADMIN_PASSWORD
```

### 2. Dashboards Usage

데이터 시각화 및 매니지먼트를 위해 Dashboards UI에 접속한다.

- URL: `https://opensearch-dashboard.${DEFAULT_URL}`
- 기본 계정: `admin`

#### 3. Index Management

매핑 설정 및 인덱스 생성을 수행한다.

```bash
read -rsp "OpenSearch admin password: " OPENSEARCH_ADMIN_PASSWORD; echo
curl -X PUT "https://opensearch:9200/my-index" -u "admin:${OPENSEARCH_ADMIN_PASSWORD}" --insecure -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 2
    }
  }
}'
unset OPENSEARCH_ADMIN_PASSWORD
```

### Common Pitfalls

- **Memory Lock Fail**: `bootstrap.memory_lock=true` 설정에도 불구하고 호스트 시스템의 `ulimit` 제한으로 인해 메모리 락이 실패할 수 있다.
- **Certificate Mismatch**: 커스텀 인증서 적용 시 도메인 이름 불일치로 인한 통신 오류가 발생할 수 있다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/analytics/opensearch.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/analytics/opensearch.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/opensearch.md)
- [Operations template](../../../../99.templates/operation.template.md)
