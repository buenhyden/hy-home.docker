---
title: "시험과 품질 런북"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 시험과 품질 런북

## Overview

시험과 품질의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [k6 Load Test Recovery Runbook](0061-k6.md) | `RUN-0061` | 승인된 격리 k6 실행의 준비, 취소·정리, 지표 누락 진단 |
| [Performance Testing Incident Runbook](0064-performance-testing.md) | `RUN-0064` | 공유 서비스에 영향을 준 k6·Locust LAB 부하의 중단과 대상 회복 판정 |
| [WireMock Recovery Runbook](0092-wiremock.md) | `RUN-0092` | 모드 이상, stub 404, 매핑 로드 실패, 메모리 한계 대응 |
| [Pact Broker Recovery Runbook](0093-pact-broker.md) | `RUN-0093` | 프로비저닝 실패, 비정상 broker, 401, DB 손실, 자격 증명 교체 |
| [Conftest Recovery Runbook](0095-conftest.md) | `RUN-0095` | 정책 검사 실패 단계 분리와 선언·규칙 수정 |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
