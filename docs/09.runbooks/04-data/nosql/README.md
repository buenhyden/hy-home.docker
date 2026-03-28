# NoSQL Database Runbooks (04-data/nosql)

> Step-by-step recovery procedures and troubleshooting guides for NoSQL infrastructure.

## Overview

이 디렉터리는 `hy-home.docker` NoSQL 데이터 계층에서 발생할 수 있는 주요 장애 상황(데이터 유실, 노드 다운, 성능 저하 등)에 대한 구체적인 대응 절차(Runbooks)를 포함한다.

## Audience

이 README의 주요 독자:

- **On-call Engineers**: 장애 발생 시 긴급 복구 수행
- **SRE**: 장애 대응 프로세스 자동화 및 개선
- **AI Agents**: 장애 상황 감지 후 초기 대응 및 복구 보조

## Scope

### In Scope

- Service Down 복구 절차
- Backup 데이터 기반 Restoration (복원) 가이드
- Cluster Quorum 장애 해결
- Replication Lag 해소 방법

### Out of Scope

- 일상적 운영 정책 (08.operations/04-data/nosql 참조)
- 기술적 상세 구조 (07.guides/04-data/nosql 참조)
- 인프라 초기 배포 (infra/04-data/nosql 참조)

## Structure

```text
nosql/
├── README.md             # This file
├── cassandra.md          # Cassandra Recovery Runbook
├── couchdb.md            # CouchDB Recovery Runbook
└── mongodb.md            # MongoDB Recovery Runbook
```

## How to Work in This Area

1. **Templates**: 새 런북 추가 시 `docs/99.templates/runbook.template.md`를 사용한다. (현재 template.md 부재 시 Step-by-step 형식을 준용하여 행동 위주로 작성)
2. **Actionable**: 런북은 생각할 필요 없이 바로 명령어를 복사/붙여넣기 할 수 있을 정도로 구체적이어야 한다.
3. **Traceability**: 장애 원인 분석을 위해 관련 `Guide`와 `Operation` 문서를 링크한다.

## Related References

- **Infrastructure**: [NoSQL Infrastructure](../../../../infra/04-data/nosql/README.md)
- **Guides**: [NoSQL Technical Guides](../../../07.guides/04-data/nosql/README.md)
- **Operations**: [NoSQL Operations](../../../08.operations/04-data/nosql/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
