# Specialized Data Runbooks

> Recovery and operational runbooks for specialized database engines within the `04-data` tier.

## Runbooks

- [Neo4j Recovery Runbook](./neo4j.md)

## Related Documents

- [Storage Exhaustion Runbook](../storage-exhaustion.md)
- [ARD](../../../02.ard/0004-data-architecture.md)

---

## Overview

`docs/09.runbooks/04-data/specialized`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

## Structure

```text
docs/09.runbooks/04-data/specialized/
├── neo4j.md  # 문서
├── qdrant.md  # 문서
└── README.md  # This file
```

## How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
