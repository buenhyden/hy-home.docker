# Operational Guides: 04-data

> Guides for operational data services and management databases.

## Overview

이 디렉토리는 `04-data` 티어 중 운영 및 관리 서비스(Management Database 등)와 관련된 가이드 문서를 포함한다. 각 문서는 시스템 구조 이해 및 사용자 가이드를 제공한다.

## Audience

이 README의 주요 독자:
- 개발자, 운영자, AI 에이전트

## Scope

### In Scope
- [Management Database (mng-db)](./mng-db.md)
- [PostgreSQL HA Cluster (postgresql-cluster)](./postgresql-cluster.md)
- [Supabase Platform (supabase)](./supabase.md)
 가이드
- 운영 데이타 서비스 활용 지침

### Out of Scope
- NoSQL 또는 캐시 전용 가이드 (다른 하위 디렉토리 참조)

## Structure

```text
operational/
├── mng-db.md              # Management Database Guide
├── postgresql-cluster.md  # PostgreSQL HA Cluster Guide
├── supabase.md            # Supabase Platform Guide
└── README.md              # This file
```

## Related References

- [04-data Guides](../README.md)
- [Operational Operations](../../../08.operations/04-data/operational/README.md)
- [Operational Runbooks](../../../09.runbooks/04-data/operational/README.md)
