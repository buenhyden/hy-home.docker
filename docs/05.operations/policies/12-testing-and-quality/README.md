---
title: "시험과 품질 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
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
| [k6 Operations Policy](0061-k6.md) | `POL-0061` | k6는 명시적으로 선택되는 `testing` job이다. root Compose service는 `version`만 실행하는 inventory/render 경계이고, 트래픽 실행 인터페이스는 승인된 `quality_run.py` isolated exe |
| [Performance Testing Operations Policy](0064-performance-testing.md) | `POL-0064` | 이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다. ### Policy  |
| [SonarQube Operations Policy](0066-sonarqube.md) | `POL-0066` | 이 정책은 추적 중인 SonarQube Community Build 배포를 다루며 유료 에디션 기능, 네이티브 Keycloak 통합, 범용 CI 게이트는 가정하지 않는다. |
| [WireMock Operations Policy](0092-wiremock.md) | `POL-0092` | WireMock은 추적되는 stub으로 HTTP 요청에 응답한다. 기능 모드는 bounded request journal을 기록하고, load override 모드는 journal을 기록하지 않는다. admin API에는 인증이 없으므로 노출과 stu |
| [Pact Broker Operations Policy](0093-pact-broker.md) | `POL-0093` | 브로커의 검증 결과가 어떤 버전을 배포할 수 있는지 정하므로, 누가 publish와 verify를 할 수 있는지, 그리고 어디까지 도달할 수 있는지가 통제 대상이다. |
| [Conftest Operations Policy](0095-conftest.md) | `POL-0095` | `infra/11-quality/conftest/policy/` 아래의 Rego 규칙은 저장소 컨테이너 baseline의 실행 가능한 부분집합이다. 새 규칙을 추가하지 않으며 각 규칙은 다른 정책이 이미 소유한 통제를 그대로 다시 적은 것이다. |

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
