<!-- Target: docs/03.specs/093-docs-taxonomy-agent-first-migration/README.md -->

# docs-taxonomy-agent-first-migration Specifications

> 문서 택소노미 에이전트-퍼스트 마이그레이션 사양

## Overview

`docs/03.specs/093-docs-taxonomy-agent-first-migration`는 문서 디렉토리 구조를 에이전트-퍼스트 택소노미로 마이그레이션한 변경 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Documentation Writers
- Repository Maintainers
- AI Agents

## Status

이 사양 폴더는 완료된 문서 택소노미 마이그레이션의 설계 사양을 보존합니다. 마이그레이션은 P0–P15 기간에 완료되었으며, 현재 단계 경로(`docs/01.requirements`–`docs/05.operations`, `docs/90.references`, `docs/99.templates`)가 기준입니다.

## Scope

### In Scope

- 완료된 docs taxonomy migration 구현 계약 보존
- canonical stage path, validator, runtime catalog migration 기준
- 후속 agent가 taxonomy 변경 이력을 추적하기 위한 관련 문서 링크

### Out of Scope

- 새 taxonomy 변경 제안
- 실행 계획 또는 작업 evidence 작성
- Docker Compose runtime 변경

## Structure

```text
docs-taxonomy-agent-first-migration/
├── spec.md      # Migration specification (completed)
└── README.md    # This file
```

## How to Work in This Area

1. 새 작업을 시작하기 전에 [spec.md](./spec.md)에서 완료된 migration contract를 확인합니다.
2. 새 taxonomy 변경이 필요하면 이 문서를 덮어쓰지 말고 새 PRD/ARD/ADR/Spec/Plan 흐름으로 제안합니다.
3. 현재 stage 경로는 [docs/03.specs/README.md](../README.md)와 [docs/README.md](../../README.md)를 기준으로 확인합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 완료된 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [docs/00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
