---
status: completed
---

<!-- Target: docs/03.specs/119-sdlc-document-contract-corpus-normalization/README.md -->

# SDLC Document Contract Corpus Normalization

> SDLC 문서 corpus의 남은 계약/검증/생애주기 정규화 설계

## Overview

이 폴더는 numbered PRD/Spec 경로 마이그레이션 이후에도 남아 있는 문서 계약
drift를 정리하기 위한 Stage 03 설계 계약입니다.

이 설계 wave는 Stage 04 plan/task evidence를 통해 완료되었습니다.

범위는 stale PRD/Spec 규칙 문구, validator coverage, Stage 03/04 lifecycle
decision, operations leaf naming polish, closure evidence입니다. 실제 파일 이동,
삭제, validator 수정, operations leaf rename은 후속 Stage 04 plan/task evidence
없이 이 폴더에서 직접 수행하지 않습니다.

## Audience

이 README의 주요 독자:

- Documentation Specialists
- AI Agents
- Repository Maintainers
- QA Engineers

## Scope

### In Scope

- `docs/01.requirements/`와 `docs/03.specs/`의 numbered path contract 후속 정리
- Stage 00/99 계약과 README/index 문구의 불일치 후보
- Stage 03 sibling README 정책 결정 후보
- Stage 04 plan/task lifecycle와 historical evidence 분류 후보
- Stage 05 operations leaf naming 후보
- validator와 generated index 후속 적용 방안

### Out of Scope

- Docker Compose runtime 변경
- secret, credential, token, raw log, shell history, `.env` 값 확인
- remote GitHub 설정 변경
- Stage 04 증거 없는 파괴적 move/delete
- README를 durable policy owner로 바꾸는 작업

## Structure

```text
119-sdlc-document-contract-corpus-normalization/
├── README.md
└── spec.md
```

## How to Work in This Area

1. 먼저 [spec.md](./spec.md)를 읽고 wave별 책임과 non-goal을 확인합니다.
2. 실행이 필요하면 `docs/04.execution/plans/`에 plan을 만들고,
   `docs/04.execution/tasks/`에 evidence를 남깁니다.
3. template/frontmatter/lifecycle rule은 Stage 99 support 문서를 기준으로
   확인합니다.
4. Stage 00 agent-facing rule을 바꿀 때는 bootstrap, documentation protocol,
   task checklist와 충돌하지 않는지 검증합니다.
5. path move나 delete가 필요한 경우 replacement pointer, archive/tombstone
   필요성, README sync, generated index refresh를 먼저 설계합니다.

## Related Documents

- [Spec](./spec.md)
- [Stage 03 README](../README.md)
- [Numbered SDLC path migration spec](../099-template-system-numbered-sdlc-paths/spec.md)
- [Template contract standardization spec](../100-template-system-contract-standardization/spec.md)
- [Document restructure disposition spec](../103-document-restructure-audit-contract-archive/spec.md)
- [Workspace support surface contract spec](../106-workspace-support-surface-contract/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [Document restructure gap register](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md)
