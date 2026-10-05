---
title: "품질 계층 (11-quality)"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-10-01"
---

# 품질 계층 (11-quality)

## Overview

소프트웨어·설정·계약·성능과 테스트 메일을 검증하는 패키지를 모았습니다.
데이터 품질 검증인 Great Expectations는 [12 Analytics](../12-analytics/README.md)에
남습니다. 폴더 이름은 profile·기동 순서·network 격리를 대신하지 않습니다.

## Audience

개발자, 품질·성능 검증 담당자와 플랫폼 운영자를 위한 인덱스입니다.

## Scope

- [k6](k6/README.md)는 root의 1회성 기본 부하 작업입니다.
- [Locust](locust/README.md)는 [독립 LAB](../../labs/locust.md)가 사용할 image
  source만 소유하며 root와 HOME 상태를 공유하지 않습니다.
- [WireMock](wiremock/README.md)은 추적 합성 HTTP stub을 제공합니다. 기능 모드는
  loopback에만 게시하고 부하 모드는 같은 서비스를 override하여 host port와 요청
  journal을 제거합니다.
- [Pact Broker](pact-broker/README.md)는 pact와 검증 결과를 기능 전용 management
  DB에 저장합니다.
- [SonarQube](sonarqube/README.md), [Conftest](conftest/README.md),
  [Mailpit](mailpit/README.md)은 각 package 문서의 권한·상태 경계를 따릅니다.

## Structure

~~~text
11-quality/
├── k6/
├── locust/
├── wiremock/
├── pact-broker/
├── sonarqube/
├── conftest/
└── mailpit/
~~~

## Tech Stack

| Package | 선택 profile 또는 진입점 | 실행·상태 경계 |
| --- | --- | --- |
| [k6](k6/) | **testing** | root는 비트래픽 버전 확인; 승인된 격리 runner가 부하 실행 |
| [locust](locust/) | **labs/locust.yml** | 독립 LAB 진입점; root include와 HOME 상태를 공유하지 않음 |
| [wiremock](wiremock/) | **api-mock**, load override | 한 Compose model에 기능·부하 중 한 모드만 존재 |
| [pact-broker](pact-broker/) | **contract-testing** | 기능 전용 DB provisioner와 Broker |
| [sonarqube](sonarqube/) | **tooling**, **sast** | management DB와 data·log volume |
| [conftest](conftest/) | **policy-check** | 읽기 전용 infra 검증, network 없음 |
| [mailpit](mailpit/) | **dev**, **local**, **mail-dev** | 테스트 메시지 SQLite capture |

## Configuration

각 package의 Compose/Dockerfile이 image, profile, network, volume과 health
계약을 소유합니다. Locust 전용 공개 입력은 **labs/.env.example**의
**LAB_LOCUST_***를 사용합니다. WireMock load 모드는 root Compose와
**wiremock/wiremock.load.yml**을 같은 명령에서 결합합니다.

## Validation

- **bash scripts/hardening/check-all-hardening.sh 11-quality**
- **bash scripts/validation/validate-docker-compose.sh**
- **python3 -m unittest tests.validation.test_quality_mock_lab -v**

정적 통과는 실제 부하 생성, image build, target 승인 또는 결과 완전성의 증거가
아닙니다.

## Usage

1. 대상 소유자, network, 자원과 종료 조건을 승인받은 뒤에만 트래픽을 생성합니다.
2. WireMock fixture에는 합성 데이터만 사용하고 admin API를 공용 route에 연결하지
   않습니다.
3. Locust는 독립 LAB entrypoint로만 render하며 root profile에 다시 추가하지
   않습니다.
4. 운영 문서는 [문서 진입점](../../docs/README.md)의 해당 Guide, Policy,
   Runbook을 따릅니다.

## Related Documents

- [인프라 인덱스](../README.md)
- [Platform Operations](../09-platform-ops/README.md)
- [Communication](../10-communication/README.md)
- [문서 진입점](../../docs/README.md)
