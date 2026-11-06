---
title: "시험과 품질 가이드"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 시험과 품질 가이드

## Overview

시험과 품질의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [k6 Usage Guide](0061-k6.md) | `GDE-0061` | root `k6` inventory job과 `quality_run.py` 격리 executor의 경계, OTLP 지표 경로와 결과 해석 |
| [Performance Testing Usage Guide](0064-performance-testing.md) | `GDE-0064` | k6·WireMock·Locust LAB의 역할, 실행 전 입력, 결과 판정과 `perf_db` 적재 기준 |
| [WireMock Usage Guide](0092-wiremock.md) | `GDE-0092` | `api-mock` 기능·부하 모드, 추적 stub, admin API 노출 경계 |
| [Pact Broker Usage Guide](0093-pact-broker.md) | `GDE-0093` | `contract-testing` 계약 저장소의 게시·검증 흐름, 인증, 준비 상태 |
| [Conftest Usage Guide](0095-conftest.md) | `GDE-0095` | `policy-check` Rego 정책 검사의 규칙, 명령, 검사 범위 |

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
