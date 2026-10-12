---
title: "시험과 품질 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
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
| [k6 Load Test Recovery Runbook](0061-k6.md) | `RUN-0061` | 승인된 isolated k6 실행이 잘못된 endpoint를 대상으로 하거나 한도를 넘거나 비정상 종료할 때 부하를 멈추고 정리하는 절차다. root Compose의 `k6`는 `version`만 실행하므로 이 절차의 대상이 아니다. |
| [Performance Testing Incident Runbook](0064-performance-testing.md) | `RUN-0064` | 공유 서비스에 영향을 주는 k6·Locust LAB 부하 시험을 중단하고 진단하는 공통 절차다. 부하를 먼저 멈추고, root `k6` 작업 또는 독립 Locust LAB의 정확한 프로젝트를 확인한 뒤 대상 회복과 증거 완전성을 판정한다. |
| [SonarQube Runbook](0066-sonarqube.md) | `RUN-0066` | SonarQube(`sonarqube` service)의 health·DB 연결 장애, 검색 인덱스 복구, 토큰 사고, DB 복원, 업그레이드 절차다. |
| [WireMock Recovery Runbook](0092-wiremock.md) | `RUN-0092` | WireMock의 모드 이상, 스텁 404, 매핑 로드 실패, 메모리 한계 도달을 다루는 런북이다. |
| [Pact Broker Recovery Runbook](0093-pact-broker.md) | `RUN-0093` | Pact Broker의 프로비저닝 실패, 비정상 상태, 401 오류, 데이터베이스 손실, 크리덴셜 교체를 다루는 복구 런북이다. |
| [Conftest Recovery Runbook](0095-conftest.md) | `RUN-0095` | `conftest` 정책 검사 작업이 실패했을 때 원인을 찾고 수정하는 런북이다. |

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
