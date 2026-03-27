# Relational Data Operations

> 관계형 데이터베이스(RDB) 시스템 운영 정책 및 거버넌스

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼의 관계형 데이터베이스 서비스 운영 시 준수해야 하는 정책, 제어 항목, 그리고 검증 기준을 정의한다. 데이터의 무결성, 보안, 그리고 가용성을 보장하기 위한 최소한의 가드레일을 설정하여 안전한 운영 환경을 유지하는 것을 목적으로 한다.

## Audience

이 README의 주요 독자:

- 시스템 운영 및 정책을 수립하는 **Operators / SRE**
- 정책 준수 여부를 감사하는 **Security Compliance Officers**
- 운영 자동화 로직을 수행하는 **AI Agents**

## Scope

### In Scope

- `postgresql-cluster` 운영 제어 정책 (Required/Allowed/Disallowed)
- 데이터 액세스 권한 및 보안 거버넌스
- 클러스터 변경 관리 및 백업 정책 지침

### Out of Scope

- 캐시 및 NoSQL 운영 정책 (-> `../cache-and-kv/`, `../nosql/`)
- 인프라 직접 코드 설정 (-> `infra/04-data/relational/`)
- 긴급 복구 실행 지침 (-> `docs/09.runbooks/04-data/relational/`)

## Structure

```text
relational/
├── postgresql-cluster.md     # HA PostgreSQL 클러스터 운영 정책
└── README.md                 # This file
```

## How to Work in This Area

1. 새 정책을 작성할 때는 `docs/99.templates/operation.template.md`를 사용한다.
2. 모든 정책 항목은 `07.guides/`의 기술적 배경과 `09.runbooks/`의 실행 절차 사이의 연결 고리 역할을 해야 한다.
3. 정책 변경 시에는 반드시 관련 인프라 설정의 정합성을 재검토해야 한다.

## Related References

- **Guides**: [Technical Guides](../../07.guides/04-data/relational/README.md)
- **Runbooks**: [Recovery Runbooks](../../09.runbooks/04-data/relational/README.md)
- **Infra**: [Relational Infra Source](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
