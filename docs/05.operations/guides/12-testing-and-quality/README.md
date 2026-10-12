---
title: "시험과 품질 가이드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
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
| [k6 Usage Guide](0061-k6.md) | `GDE-0061` | k6는 `infra/11-quality/k6/`의 **DEV** one-shot 부하 생성기다. `testing` profile에서만 선택되며 root Compose의 `k6` service는 `version`만 실행하는 inventory/render |
| [Performance Testing Usage Guide](0064-performance-testing.md) | `GDE-0064` | 성능 시험은 `k6`(기본 부하 발생기), WireMock(외부 HTTP 의존성 모의 서버), Locust(독립 LAB 선택 도구)로 수행한다. 이 가이드는 세 도구의 역할과 시험 입력, 결과 판정 기준을 정리한다. |
| [SonarQube Usage Guide](0066-sonarqube.md) | `GDE-0066` | SonarQube Community Build는 `infra/11-quality/sonarqube/`의 `sonarqube` service로 운영하는 코드 품질·SAST 도구다. `tooling`과 `sast` profile에서만 선택되며 HOME에서 |
| [WireMock Usage Guide](0092-wiremock.md) | `GDE-0092` | WireMock은 기능 검사와 mock 자체 부하 측정에 공통 `api-mock` profile로 선택되는 OPTIONAL HTTP 스텁 서버다. 개발과 테스트 중 외부 HTTP 의존성을 대신해 실제 서비스를 호출하지 않고도 소비자를 테스트할 수 있게 |
| [Pact Broker Usage Guide](0093-pact-broker.md) | `GDE-0093` | Pact Broker는 `contract-testing`으로 선택되는 OPTIONAL 계약 저장소다. 소비자 테스트가 pact를 여기에 게시하고, 프로바이더 빌드가 이를 가져와 검증하며, `can-i-deploy`는 기록된 검증 결과로 답한다. 브로커 |
| [Conftest Usage Guide](0095-conftest.md) | `GDE-0095` | Conftest는 `policy-check`로 선택되는 OPTIONAL 일회성 정책 테스트다. 실행 중인 컨테이너가 아니라 인프라 소스에 대해 Open Policy Agent(Rego) 규칙을 평가하므로, 시작 전에 잘못된 선언을 잡아낸다. |

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
