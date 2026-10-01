---
title: "Quality Tier (11-quality)"
version: "0.1.0"
type: "common/package-readme"
status: "review"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-10-01"
---

# Quality Tier (11-quality)

## Overview

소프트웨어·설정·계약·성능과 테스트 메일을 검증하는 기존 패키지를 모았습니다.
데이터 품질 검증인 Great Expectations는 [12 Analytics](../12-analytics/README.md)에
남습니다. 폴더 이름은 프로필·기동 순서·네트워크 격리를 대신하지 않습니다.

## Audience

개발자, 품질·성능 검증 담당자와 플랫폼 운영자를 위한 인덱스입니다.

## Scope

- [k6](k6/README.md)와 [Locust](locust/README.md)는 대상 소유자의 승인을 받은
  후에만 트래픽을 생성합니다. k6는 1회성이며 Locust는 master/worker 서비스로
  구성됩니다.
- [SonarQube](sonarqube/README.md)는 권한 정보를 PostgreSQL과 선언된
  데이터/로그 볼륨에 영속화합니다. 검색 인덱스는 파생 값이지만 데이터베이스와
  확장/설정은 일관되게 복구해야 합니다.
- [WireMock](wiremock/README.md)은 추적되는 합성 HTTP 스텁을 제공합니다.
  관리 API는 인증이 없으므로 호스트 포트는 loopback에만 바인딩됩니다.
- [Pact Broker](pact-broker/README.md)는 pact와 검증 결과를 기능 전용
  `mng-pg` 데이터베이스에 basic auth와 loopback 포트로 보호하여 저장합니다.
- [Conftest](conftest/README.md)는 `infra/` 아래의 Compose 파일과
  Dockerfile에 대해 읽기 전용, 네트워크 없이 Rego 정책 테스트를 실행합니다.

- [Mailpit](mailpit/README.md)은 개발 SMTP를 캡처합니다. UI/SMTP host 바인딩은
  loopback이며 `/data/mailpit.db`에 저장합니다. 컨테이너는 `mail_net`의 서비스
  DNS로 전송할 수 있습니다. UI SSO가 SMTP 인증을 대신하지 않으며 외부 배달용
  Stalwart와 구분합니다.

## Structure

| Package | 기존 선택 프로필 | 실행·상태 경계 |
| --- | --- | --- |
| [k6](k6/) | `testing` | 승인된 대상에만 부하를 보내는 1회성 작업 |
| [locust](locust/) | `testing` | master/worker와 같은 시나리오·빌드 소스 |
| [wiremock](wiremock/) | `api-mock` | 추적된 스텁만 소유; 메모리 변경은 재시작 시 사라짐 |
| [pact-broker](pact-broker/) | `contract-testing` | 기능 전용 DB provisioner와 Broker를 함께 보존 |
| [sonarqube](sonarqube/) | `tooling`, `sast` | management DB와 데이터·로그 볼륨 |
| [conftest](conftest/) | `policy-check` | 읽기 전용 infra 검증, 네트워크 없음 |
| [mailpit](mailpit/) | `dev`, `local`, `mail-dev` | 테스트 메시지 SQLite 캡처 |

## How to Work in This Area

- 모든 Compose 검증은 저장소 루트에서 합니다. `quality`라는 새 Compose
  프로필은 없습니다. `tooling`은 Platform Operations의 Registry와 Quality의 SonarQube를
  함께 선택하며 IaC나 부하 테스트를 시작하지 않습니다.
- 정적 검사는 `bash scripts/hardening/check-all-hardening.sh 11-quality`와
  기존 `scripts/validation/validate-docker-compose.sh`를 사용합니다.
  설정 통과는 실제 부하 생성, 이미지 빌드, 메일 수신·복원 성공의 증거가 아닙니다.
- image/build pin, host 경로, volume·secret·network 계약은 각 패키지 원본을
  따릅니다. 재분류를 이유로 `DEFAULT_TOOLING_DIR` 또는
  `DEFAULT_COMMUNICATION_DIR` 아래 데이터를 옮기지 않습니다.
- 운영 문서는 [문서 진입점](../../docs/README.md)의 Stage05 subject0061,
  0062,0064,0066,0084,0092,0093,0095에서 찾습니다. Platform Operations와 Quality의 공통 하드닝0063은
  두 tier에 걸친 지침을 유지합니다.

## Related Documents

- [인프라 인덱스](../README.md)
- [Platform Operations](../09-platform-ops/README.md)
- [Communication](../10-communication/README.md)
- [문서 진입점](../../docs/README.md)
