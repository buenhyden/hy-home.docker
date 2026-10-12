---
title: "보안과 비밀값 가이드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 보안과 비밀값 가이드

## Overview

보안과 비밀값의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [`SENSITIVE_ENV_VARS.md.example` vs `SENSITIVE_ENV_VARS.md` Comparison](0010-sensitive-env-vars-comparison.md) | `GDE-0010` | 이 가이드는 공개 secret registry 예제와 로컬 registry의 메타데이터를 비교하는 기준과 방법을 설명한다. |
| [OpenBao Guide](0085-openbao.md) | `GDE-0085` | OpenBao는 HOME secret control plane이다. 레거시 Vault runtime/data는 2026-09-25 폐기된 역사적 대상이며 현재 migration/rollback 입력으로 사용할 수 없다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
