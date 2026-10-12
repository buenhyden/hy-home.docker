---
title: "메일과 통지 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 메일과 통지 정책

## Overview

메일과 통지의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Stalwart Mail Operations Policy](0070-mail.md) | `POL-0070` | Stalwart는 OPTIONAL 내부 메일 서비스다. 프로토콜 리스너, relay 규칙, 메일박스 데이터는 관리 UI 경로 이상의 통제가 필요하다. 이 정책은 그 통제를 정의한다. |
| [Mailpit Policy](0084-mailpit.md) | `POL-0084` | Mailpit은 개발용 이메일을 캡처한다. 일부러 느슨하게 둔 SMTP 설정은 현재 DEV 분류와 loopback/internal 네트워크 경계 안에서만 허용된다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
