# Specialized Data Operations

> Operating policies for specialized database engines within the `04-data` tier.

## Policies

- [Neo4j Operations Policy](./neo4j.md)

## Related Documents

- [Backup Policy](../../../policies/04-data/backup-policy.md)
- [ARD](../../../../02.architecture/requirements/0004-data-architecture.md)

---

## Overview

`docs/05.operations/04-data/specialized`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책과 controls
- 허용/금지/예외 기준
- 검증 방법과 review cadence

### Out of Scope

- 단계별 복구 절차
- 튜토리얼 문서
- incident timeline

## Structure

```text
docs/05.operations/04-data/specialized/
├── neo4j.md  # 문서
├── qdrant.md  # 문서
└── README.md  # This file
```

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Usage

> Migrated from `docs/05.operations/04-data/specialized/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Specialized Data Usages

> Specialized database engines within the `04-data` tier.

#### Policies

- [Neo4j Operations Policy](./neo4j.md)
- [Qdrant Operations Policy](./qdrant.md)
- [Qdrant Vector Database](./qdrant.md)

#### Related Documents

- [Analytical & Specialized Databases Usage](../05.analytical-specialized-dbs.md)
- [PRD](../../../../01.requirements/2026-03-26-04-data.md)
- [ARD](../../../../02.architecture/requirements/0004-data-architecture.md)

---

#### Overview

`docs/05.operations/04-data/specialized`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

##### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

#### Structure

```text
docs/05.operations/04-data/specialized/
├── neo4j.md  # 문서
├── qdrant.md  # 문서
└── README.md  # This file
```

#### How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Procedure

> Migrated from `docs/05.operations/04-data/specialized/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Specialized Data Procedures

> Recovery and operational runbooks for specialized database engines within the `04-data` tier.

#### Procedures

- [Neo4j Recovery Procedure](./neo4j.md)

#### Related Documents

- [Storage Exhaustion Procedure](../../../runbooks/04-data/storage-exhaustion.md)
- [ARD](../../../../02.architecture/requirements/0004-data-architecture.md)

---

#### Overview

`docs/05.operations/04-data/specialized`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

##### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

#### Structure

```text
docs/05.operations/04-data/specialized/
├── neo4j.md  # 문서
├── qdrant.md  # 문서
└── README.md  # This file
```

#### How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
