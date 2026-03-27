# Relational Data Guides

> 관계형 데이터베이스(RDB) 시스템 기술 가이드

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼에서 사용하는 관계형 데이터베이스 서비스의 기술적 세부 사항, 아키텍처, 그리고 연결 방법을 설명하는 가이드를 포함한다. 단순히 설정을 나열하는 것이 아니라, 클러스터링 원리와 장애 대응 논리를 기술적으로 기술하여 개발자와 운영자가 시스템을 깊이 이해하도록 돕는 것을 목적으로 한다.

## Audience

이 README의 주요 독자:

- 데이터베이스 연결 및 쿼리 작성이 필요한 **Developers**
- 클러스터 상태 및 설정을 관리하는 **Operators**
- 시스템 구조를 분석하고 검증하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster`(Patroni/HA) 아키텍처 및 연결 방법
- 관계형 데이터베이스의 고가용성 설계 원칙
- 데이터 복제 및 일관성 보장 메커니즘

### Out of Scope

- 캐시 및 NoSQL 기술 가이드 (-> `../cache-and-kv/`, `../nosql/`)
- 개별 애플리케이션의 비즈니스 도메인 모델 설계
- 단순 운영 작업 절차 (-> `docs/09.runbooks/04-data/relational/`)

## Structure

```text
relational/
├── postgresql-cluster.md     # HA PostgreSQL 클러스터 기술 가이드
└── README.md                 # This file
```

## How to Work in This Area

1. 새 가이드를 작성할 때는 `docs/99.templates/guide.template.md`를 사용한다.
2. 모든 가이드는 추적 가능성을 위해 `infra/04-data/relational/` 하위의 실제 구현과 연결되어야 한다.
3. 운영 정책이나 복구 절차는 각각 `08.operations/`와 `09.runbooks/` 디렉터리를 참조하도록 작성한다.

## Related References

- **Operations**: [Operations Policy](../../08.operations/04-data/relational/README.md)
- **Runbooks**: [Recovery Runbooks](../../09.runbooks/04-data/relational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
