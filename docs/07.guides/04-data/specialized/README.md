# Specialized Data Guides

> Specialized database engines within the `04-data` tier.

## Policies

- [Neo4j Operations Policy](./neo4j.md)
- [Qdrant Operations Policy](./qdrant.md)
- [Qdrant Vector Database](./qdrant.md)

## Related Documents

- [Analytical & Specialized Databases Guide](../05.analytical-specialized-dbs.md)
- [PRD](../../../01.prd/2026-03-26-04-data.md)
- [ARD](../../../02.ard/0004-data-architecture.md)

---

## Overview

`docs/07.guides/04-data/specialized`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

## Structure

```text
docs/07.guides/04-data/specialized/
├── neo4j.md  # 문서
├── qdrant.md  # 문서
└── README.md  # This file
```

## How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
