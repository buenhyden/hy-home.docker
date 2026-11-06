---
title: "시험과 품질 정책"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 시험과 품질 정책

## Overview

시험과 품질의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [k6 Operations Policy](0061-k6.md) | `POL-0061` | 격리 executor 전용 트래픽, 지표 relay·token, 증거와 정리 통제 |
| [Performance Testing Operations Policy](0064-performance-testing.md) | `POL-0064` | 대상 승인, 환경 격리, 결과 이력·보존과 접근 통제 |
| [WireMock Operations Policy](0092-wiremock.md) | `POL-0092` | 모드 선택, loopback 노출, 합성 stub, request journal 통제 |
| [Pact Broker Operations Policy](0093-pact-broker.md) | `POL-0093` | 프로비저닝 권한, Basic 인증, loopback 노출, 자격 증명 경계 |
| [Conftest Operations Policy](0095-conftest.md) | `POL-0095` | 규칙·allowlist·unit test, job 접근 범위, corpus 권위 |

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
