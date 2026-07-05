---
status: active
---

<!-- Target: docs/90.references/audits/README.md -->

# Audit References

> stable audit reports, comparison reports, and audit-reference indexes

## Overview

`docs/90.references/audits`는 active stage 문서를 보조하는 audit reference 공간입니다. 이 폴더는 특정 시점의 조사·비교·감사 결과 중 반복 참조할 가치가 있는 안정적 요약을 보관합니다.

Audit reference는 task evidence나 incident timeline을 대체하지 않습니다. 실행 중인 작업 증거는 `docs/04.execution/tasks/`, 운영 incident와 postmortem은 `docs/05.operations/incidents/`가 담당합니다.

## Category Role

`docs/90.references/audits`는 audit 결과를 장기 reference로 재사용할 수 있게 분리합니다. 이 category는 audit findings, comparison matrix, implementation-status snapshots, follow-up gap indexes를 담을 수 있지만, approval gate나 runtime source of truth가 아닙니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 안정화된 audit report 또는 comparison report
- 구현 현황 snapshot과 gap summary
- audit source, command, evidence path를 연결하는 reference index
- active stage 문서가 반복해서 참조하는 audit-derived facts

### Out of Scope

- 현재 실행 중인 task evidence
- incident timeline 또는 postmortem 본문
- active approval gate, policy, runbook procedure
- secret 값, credential, token, private key, shell history, raw log

## Structure

```text
audits/
├── 2026-07-03-workspace-document-contract-audit-pack/ # Workspace document contract audit reports
├── 2026-07-04-document-restructure-audit-contract-archive/ # Document restructure audit, archive, contract, and QA reports
├── 2026-07-05-agentic-engineering-implementation-audit-pack/ # Agentic engineering implementation-status audit reports
└── README.md # This file
```

## Current References

- [Workspace document contract audit references](./2026-07-03-workspace-document-contract-audit-pack/README.md)
- [Document restructure audit references](./2026-07-04-document-restructure-audit-contract-archive/README.md)
- [Agentic engineering implementation audit references](./2026-07-05-agentic-engineering-implementation-audit-pack/README.md)

## Naming Rules

- SDLC-linked audit packs live under `<date>-<sdlc_key>/`.
- Pack-level report files use descriptive names such as `gap-register.md` or `implementation-overview.md`.
- Do not use `part-*.md` prefixes for finalized report files.

## How to Work in This Area

1. 새 audit reference가 active task evidence를 대체하지 않는지 확인합니다.
2. 새 non-README reference는 [reference.template.md](../../99.templates/templates/common/reference.template.md)의 필수 섹션을 따릅니다.
3. audit source, checked date, command, evidence path, and known gaps를 명시합니다.
4. 새 audit reference를 추가하면 이 README와 [90.references](../README.md)를 함께 갱신합니다.
5. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.

## Related Documents

- [90.references](../README.md)
- [reference data](../data/README.md)
- [research references](../research/README.md)
- [reference template](../../99.templates/templates/common/reference.template.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
