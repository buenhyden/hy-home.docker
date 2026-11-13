---
title: "디자인 시스템 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 디자인 시스템 가이드

## Stage Responsibility

### Purpose and Readers

디자인 시스템의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

### Inputs and Outputs

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Contents

### Current Items

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Shared Storybook Usage Guide](0101-storybook.md) | `GDE-0101` | 공유 Storybook은 `projects/storybook/nextjs`의 UI story와 문서를 읽기 전용 정적 origin(`storybook`)과 문서 MCP(`storybook-mcp`)로 제공하는 선택형 `experience` 서비스다.  |

### Classification

이 폴더의 문서는 모두 가이드 역할이며 `GDE-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 같은 번호와 slug로 다른 역할 폴더에 있다.

## Workflow

### Create and Review

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

### Transition and Exit

문서를 이동·삭제하면 이 목록의 행과 링크를 같은 변경에서 갱신하며, 문서의 원래 식별자와 생성일은 바뀌지 않는다.

## Related Documents

### Upstream and Downstream

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)

### Policy and Templates

- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
- [README 템플릿](../../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본
