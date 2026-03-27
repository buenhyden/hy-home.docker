# Operational Policies: 04-data

> Operational policies for shared data management services.

## Overview

이 디렉토리는 `04-data` 티어의 운영 계층 서비스(Management DB 등)에 대한 거버넌스 및 정책 문서를 포함한다. 각 문서는 통제 기준과 검증 방법을 정의한다.

## Audience

이 README의 주요 독자:
- 플랫폼 운영팀, SRE, AI 에이전트

## Scope

### In Scope
- [Management Database (mng-db)](./mng-db.md)
- [PostgreSQL HA Cluster (postgresql-cluster)](./postgresql-cluster.md)
- [Supabase Platform (supabase)](./supabase.md)
 운영 정책
- 관리 계층 데이타 접근 및 보안 통제 기준

### Out of Scope
- NoSQL 또는 Cache Cluster 정책 (데이터 티어 타 폴더 참조)

## Structure

```text
operational/
├── mng-db.md              # Management DB Operations Policy
├── postgresql-cluster.md  # PostgreSQL HA Cluster Policy
├── supabase.md            # Supabase Operations Policy
└── README.md              # This file
```

## Related References

- [04-data Operations](../README.md)
- [Operational Guides](../../../07.guides/04-data/operational/README.md)
- [Operational Runbooks](../../../09.runbooks/04-data/operational/README.md)
