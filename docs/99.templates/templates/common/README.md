---
layer: agentic
---

# Common Templates

## Overview

`docs/99.templates/templates/common`은 README, Reference, Audit, Archive 역할의
복사 가능한 원본을 제공한다.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

- README 탐색 문서 형식
- 안정적인 Reference 형식과 범위가 정해진 Audit 형식
- 활성 문서 제거를 기록하는 Archive tombstone 형식

## Structure

| Need | Template |
| --- | --- |
| 경로별 탐색 README 작성 | [readme.template.md](./readme.template.md) |
| 안정적인 사실과 출처 기록 | [reference.template.md](./reference.template.md) |
| 기준, 증거, 발견사항과 처분 기록 | [audit.template.md](./audit.template.md) |
| 제거된 문서의 tombstone 기록 | [archive.template.md](./archive.template.md) |

## How to Work in This Area

1. [template selection](../../support/template-selection.md)에서 대상 역할을 확인한다.
2. 선택한 원본의 토큰을 대상에 맞는 근거 기반 내용으로 바꾼다.
3. 역할, 메타데이터, 수명주기 규칙은 원본에 복제하지 않고 support 소유자로 연결한다.
4. 변경 후 [template contract](../../support/template-contract.md)를 검증한다.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [common document contract](../../support/common-document-contract.md)
- [README profile contract](../../support/readme-profile-contract.md)
