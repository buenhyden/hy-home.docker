# NoSQL Database Operations (04-data/nosql)

> Operational policies and maintenance standards for Cassandra, CouchDB, and MongoDB.

## Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 플랫폼의 안정적인 운영을 위한 정책, 백업 전략, 보안 표준 및 모니터링 가이드라인을 포함한다.

## Audience

이 README의 주요 독자:

- **Operators (SRE/DBA)**: 정기 점검 및 운영 자동화 수행
- **Security Officers**: 데이터 보호 정책 및 접근 제어 검토
- **AI Agents**: 장애 감지 및 자동 복구 로직 구현

## Scope

### In Scope

- Service Level Objectives (SLO) 정의
- Backup & Retention 정책
- Cluster Scaling 가이드라인
- 정기 패치 및 업데이트 절차

### Out of Scope

- 기술적 시스템 구조 (07.guides/04-data/nosql 참조)
- 긴급 장애 복구 (09.runbooks/04-data/nosql 참조)
- 인프라 배포 코드 (infra/04-data/nosql 참조)

## Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra Operation Policy
├── couchdb.md            # CouchDB Operation Policy
└── mongodb.md            # MongoDB Operation Policy
```

## How to Work in This Area

1. **Templates**: 새 운영 정책 추가 시 `docs/99.templates/operation.template.md`를 사용한다. (현재 template.md 부재 시 Guide 형식을 준용하되 운영 관점에 집중)
2. **Review**: 모든 정책 변경은 인프라 팀의 승인을 거쳐야 한다.
3. **Traceability**: 정책 위반 발생 시 대응할 수 있는 `Runbook` 링크를 반드시 포함한다.

## Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../infra/04-data/nosql/README.md)
- **Guides**: [NoSQL Technical Guides](../../../07.guides/04-data/nosql/README.md)
- **Runbooks**: [NoSQL Runbooks](../../../09.runbooks/04-data/nosql/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
