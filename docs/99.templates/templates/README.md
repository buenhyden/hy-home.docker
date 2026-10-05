---
title: "Template Catalog"
version: "3.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "templates"
---

# Template Catalog

## Overview

이 디렉터리는 [`../registry.json`](../registry.json)이 등록한 복사용 원본을
담습니다. 문서 type과 template 원본의 정확한 대응은 Registry의
`template_roles`만 소유합니다. 이 README는 category 디렉터리로 가는 길만
안내하고 개별 template 파일은 목록으로 옮겨 적지 않습니다. 계약 설명은
[Stage 99 README](../README.md)에, 완성된 문서가 지켜야 할 규칙은 각 문서를
소유한 stage에 있습니다.

## Scope

- 포함: Registry `template_roles`가 가리키는 template 원본.
- 제외: 완성된 문서, 과거 template, category별 README. 과거 template은 Git
  history로만 복구하며 현재 작성에 복사하지 않습니다.

### Audience

- Documentation Writers
- Repository Maintainers
- AI Agents

## Structure

### Documents

| Path | Purpose |
| --- | --- |
| [architecture/](architecture/) | Description과 ADR source |
| [archive/](archive/) | route record source |
| [common/](common/) | README source |
| [governance/](governance/) | 공유 governance source |
| [operations/](operations/) | 운영 역할별 source |
| [references/](references/) | reference pack과 member source |
| [requirements/](requirements/) | Requirement source |
| [runtime/](runtime/) | native provider projection source |
| [specs/](specs/) | Spec·Plan·Task와 interface source |

## Usage

1. [`../registry.json`](../registry.json)의 `template_roles`에서 역할을 찾고
   등록된 `source`를 복사합니다. 디렉터리를 훑어서 template을 고르지
   않습니다.
2. Markdown의 모든 `{{UPPER_SNAKE_CASE}}` 자리 표시자를 채우고 template
   전용 HTML 작성 안내 주석을 지웁니다. 기계용 contract 원본은
   `__UPPER_SNAKE__` token을 씁니다.
3. 본문은 작성 안내 주석이 지정한 언어로 씁니다. 언어는 Registry profile의
   `language`가 소유합니다.
4. 선언된 `type`을 유지하고 profile이 식별자를 선언하면 저장된 high-water
   mark보다 큰 번호를 할당합니다.
5. 적용할 검사는 공통 agent governance의
   [verification matrix](../../../.agents/governance/quality-standards.md#5-change-type-verification-matrix)로
   고릅니다. 실행 전에 `--explain`으로 선택된 gate를 확인하고, 안전하지
   않거나 쓸 수 없는 leaf는 정확한 이유와 함께 DEFER로 기록합니다. full
   또는 all-files 실행도 Task 범위와 controlled-wrapper 승인 경계를
   따릅니다.

## Related Documents

- [Stage 99 authority](../README.md)
- [Registry](../registry.json)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md)
