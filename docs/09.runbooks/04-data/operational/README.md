# Operational Runbooks: 04-data

> Step-by-step procedures for shared data services.

## Overview

이 디렉토리는 `04-data` 티어의 운영 계층 서비스(Management DB 등)에 대한 실행 절차 문서를 포함한다. 

## Audience

이 README의 주요 독자:
- 온콜 엔지니어, 플랫폼 관리자, AI 에이전트

## Scope

### In Scope
- [Management Database (mng-db)](./mng-db.md)
- [PostgreSQL HA Cluster (postgresql-cluster)](./postgresql-cluster.md)
- [Supabase Platform (supabase)](./supabase.md)
 가동 및 복구 런북
- 초기 플랫폼 설치 시 데이타 초기화 절차

### Out of Scope
- NoSQL 또는 Cache Cluster 복정 런북 (데이터 티어 타 폴더 참조)

## Structure

```text
operational/
├── mng-db.md              # mng-db Recovery Runbook
├── postgresql-cluster.md  # postgresql-cluster Recovery Runbook
├── supabase.md            # supabase Platform Runbook
└── README.md              # This file
```

## Related References

- [04-data Runbooks](../README.md)
- [Operational Guides](../../../07.guides/04-data/operational/README.md)
- [Operational Operations](../../../08.operations/04-data/operational/README.md)
