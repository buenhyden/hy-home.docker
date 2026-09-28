---
title: "Pact Broker Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0093"
parent_ids:
- "POL-0093"
implementation_services:
  infra/09-tooling/pact-broker/docker-compose.yml:
  - pact-broker
  - pact-broker-db-provision
created: "2026-09-23"
---

# Pact Broker Usage Guide

## Usage

### Purpose and classification

Pact Broker는 `contract-testing`으로 선택되는 OPTIONAL 계약 저장소다.
소비자 테스트가 pact를 여기에 게시하고, 프로바이더 빌드가 이를 가져와
검증하며, `can-i-deploy`는 기록된 검증 결과로 답한다. 브로커는 실제
프로바이더와 스텁을 비교 검증하지 않는 WireMock을 보완한다.

### Current implementation

- [Pact Broker Compose](../../../infra/09-tooling/pact-broker/docker-compose.yml)는
  `mng-pg`에 기능 전용 역할과 데이터베이스를 생성하는
  `pact-broker-db-provision`과 `pact-broker`를 정의한다.
- 브로커는 `PACT_BROKER_DB_USER`가 소유한 `PACT_BROKER_DB_NAME`
  데이터베이스에 pact, 버전, 태그, 검증 결과를 저장한다. 컨테이너는
  디스크에 아무것도 남기지 않으며 읽기 전용 루트 파일시스템으로
  실행된다.
- Basic 인증이 UI와 전체 API를 보호하며, 헬스체크용
  `/diagnostic/status/heartbeat`만 공개되어 있다. 이미지는 자격 증명을
  환경 변수에서만 읽으므로, 서비스 엔트리포인트가 두 비밀번호를 Docker
  secret에서 브로커 프로세스로 내보낸다.
- 호스트 포트 `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}`는 루프백
  전용이다. 평문 HTTP 위의 basic 인증이 호스트 밖으로 나가서는 안 된다.
  Traefik 라우트나 OIDC 클라이언트는 없다.
- `PACT_DO_NOT_TRACK`은 이미지의 분석 핑을 비활성화한다.

### Publishing and verifying

| Command | Effect |
| --- | --- |
| `docker compose --profile core --profile contract-testing up -d pact-broker` | 데이터베이스를 프로비저닝하고 브로커 시작 |
| `curl -s http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}/diagnostic/status/heartbeat` | 자격 증명 없는 생존 확인 |
| `pact-broker publish <dir> --consumer-app-version <sha> --broker-base-url http://127.0.0.1:${PACT_BROKER_HOST_PORT:-19292} --broker-username ${PACT_BROKER_BASIC_AUTH_USERNAME:-pact} --broker-password <secret>` | 소비자 버전에 대한 pact를 기록 |
| `pact-broker can-i-deploy --pacticipant <name> --version <sha> …` | 검증 결과를 읽음; 아무것도 쓰지 않음 |

자격 증명은 `pact_broker_basic_auth_password` 시크릿이다. 명령줄이 아니라
클라이언트 환경 변수(`PACT_BROKER_PASSWORD`)로 전달한다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=contract-testing bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`

## Runbook Handoff

프로비저닝 실패, 비정상 브로커, 인증 오류, 자격 증명 교체는
[runbook](../runbooks/0093-pact-broker.md)을 사용한다.

## Traceability

- [Policy](../policies/0093-pact-broker.md) (`POL-0093`)
- [Runbook](../runbooks/0093-pact-broker.md) (`RUN-0093`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Pact Broker package README](../../../infra/09-tooling/pact-broker/README.md) and [derived version projection](../../../infra/tech-stack.versions.json)
- [WireMock guide](0092-wiremock.md)
- [Pact Broker Docker configuration](https://docs.pact.io/pact_broker/docker_images/pactfoundation)
