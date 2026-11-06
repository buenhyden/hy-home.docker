---
title: "공통 운영 정책"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 공통 운영 정책

## Overview

공통 운영의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Common Optimizations Template Exceptions Policy](0001-common-optimizations-template-exceptions.md) | `POL-0001` | 이 문서는 `infra/common-optimizations.yml` 적용 시 허용되는 예외 목록과 승인 기준을 정의한다. |
| [Harness / Agent-first Engineering Operations Policy](0004-harness-agent-first-engineering.md) | `POL-0004` | 이 운영 정책은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약을 유지하기 위한 통제 기준을 정의한다. |
| [Infrastructure Optimization Governance Policy](0006-infrastructure-optimization-governance.md) | `POL-0006` | 이 정책은 root Compose가 include하는 정상 서비스와 `labs/*/docker-compose.yml`의 LAB 서비스에 대한 공통 운영 통제와 개선 백로그를 소유한다. |
| [Compose Profile Vocabulary Policy](0078-compose-profile-vocabulary.md) | `POL-0078` | 추적된 Compose profile의 이름·분류·목적을 소유하며, 여러 profile 선택은 합집합이고 보안 격리를 제공하지 않는다. |

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
