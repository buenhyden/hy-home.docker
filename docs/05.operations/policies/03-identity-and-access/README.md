---
title: "인증과 접근 정책"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 인증과 접근 정책

## Stage Responsibility

### Purpose and Readers

인증과 접근의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

### Inputs and Outputs

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Contents

### Current Items

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [02-Auth Keycloak Operations Policy](0014-keycloak.md) | `POL-0014` | 이 문서는 `02-auth` Keycloak 운영 정책을 정의한다. DB/관리자 시크릿 처리, readiness 검증, 변경 통제 기준을 명시한다. |
| [02-Auth OAuth2 Proxy Operations Policy](0015-oauth2-proxy.md) | `POL-0015` | 이 문서는 `02-auth` OAuth2 Proxy 운영 정책을 정의한다. 시크릿 주입 경로, 세션/쿠키 표준, fail-closed 및 degraded-mode 운영 통제를 명시한다. |
| [Application Authentication Integration Policy](0079-application-auth-integration.md) | `POL-0079` | 이 정책은 Keycloak을 중앙 IdP로 사용하면서 OAuth2 Proxy ForwardAuth와 application-native OIDC를 선택·운영하는 기준을 정의한다. |

### Classification

이 폴더의 문서는 모두 정책 역할이며 `POL-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 같은 번호와 slug로 다른 역할 폴더에 있다.

## Workflow

### Create and Review

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

### Transition and Exit

문서를 이동·삭제하면 이 목록의 행과 링크를 같은 변경에서 갱신하며, 문서의 원래 식별자와 생성일은 바뀌지 않는다.

## Related Documents

### Upstream and Downstream

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)

### Policy and Templates

- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
- [README 템플릿](../../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본
