# Data Tier Guides (04-data)

> Persistence, Caching, and Storage Services 가이드

## Overview

이 디렉터리는 `hy-home.docker` 데이터 인프라 계층(04-data)을 위한 기술 가이드를 포함합니다. 각 가이드는 데이터베이스 유형별로 정리되어 효율적인 시스템 이해와 운영을 돕습니다.

## Audience

이 README의 주요 독자:

- 시스템을 사용하는 **Developers**
- 인프라를 관리하는 **Operators**
- 문서 구조를 학습하는 **AI Agents**

## Scope

### In Scope

- 관계형 데이터베이스(PostgreSQL) 사용 가이드
- 캐시 및 Key-Value 저장소(Valkey) 사용 가이드
- NoSQL 및 오브젝트 스토리지 가이드

## Structure

```text
04-data/
├── cache-and-kv/         # 분산 캐시 및 KV 저장소 가이드 (Valkey Cluster)
├── lake-and-object/       # 데이터 레이크 및 오브젝트 스토리지 가이드
├── nosql/                 # NoSQL 데이터베이스 가이드
├── operational/           # 운영 및 관리용 데이터베이스 가이드
├── relational/            # 관계형 데이터베이스(PostgreSQL) 가이드
└── README.md              # This file
```

## How to Work in This Area

1. 전반적인 데이터 아키텍처는 [Architecture](../../02.ard/0004-data-architecture.md) 문서를 먼저 확인합니다.
2. 특정 엔진의 구현 세부 사항은 `infra/04-data/` 경로의 소스 코드를 참조합니다.
3. 새로운 가이드 추가 시 `docs/99.templates/guide.template.md`를 사용합니다.

## Related References

- **Operations**: [Data Operations Policy](../../08.operations/04-data/README.md)
- **Runbooks**: [Data Recovery Runbooks](../../09.runbooks/04-data/README.md)
- **Source**: [Infrastructure Source](../../../infra/04-data/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
