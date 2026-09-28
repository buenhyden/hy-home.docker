---
title: "Conftest Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0095"
parent_ids:
- "POL-0095"
implementation_services:
  infra/09-tooling/conftest/docker-compose.yml:
  - conftest
created: "2026-09-23"
---

# Conftest Usage Guide

## Usage

### Purpose and classification

Conftest는 `policy-check`로 선택되는 OPTIONAL 일회성 정책 테스트다. 실행
중인 컨테이너가 아니라 인프라 소스에 대해 Open Policy Agent(Rego) 규칙을
평가하므로, 시작 전에 잘못된 선언을 잡아낸다.

### Current implementation

- [Conftest Compose](../../../infra/09-tooling/conftest/docker-compose.yml)는
  고정된 `openpolicyagent/conftest` 이미지를 UID 1000, 읽기 전용 루트,
  네트워크 없음, `infra/`만 읽기 전용으로 마운트해 실행한다. `secrets/`나
  `.env`는 전혀 보지 않는다.
- `run.sh`는 먼저 정책 자체 테스트에 대해 `conftest verify`를 실행한 다음
  `infra/` 아래의 모든 `docker-compose*.yml`과 `Dockerfile*`을 테스트한다.
  `deny`는 job을 실패시키고 `warn`은 출력만 한다.

### Rules

| Namespace | Deny | Warn |
| --- | --- | --- |
| `compose` | 허용목록(`cadvisor`) 밖의 privileged 서비스; 프로파일 없는 서비스; `:latest` 또는 태그 없는 이미지; 리터럴 값을 가진 password, secret, token, key 변수 | 모든 인터페이스에 게시된 호스트 포트 |
| `dockerfile` | 태그 없거나 `:latest`인 `FROM`(빌드 스테이지와 `scratch`는 예외); `--checksum` 없이 URL에서 받는 `ADD` | — |

리터럴이란 빈 값, `${…}` 보간, `/run/secrets/` 경로, 불리언, URL을
제외한 모든 값을 뜻한다. `*_FILE`과 `*_CMD` 키는 시크릿 출처를 나타내므로
예외다.

### Commands

| Command | Effect |
| --- | --- |
| `docker compose --profile policy-check run --rm conftest` | 정책을 검증한 다음 모든 Compose 파일과 Dockerfile을 테스트 |
| `docker run --rm -v "$PWD/infra:/project/infra:ro" -w /project openpolicyagent/conftest:<tag> test --policy infra/09-tooling/conftest/policy --namespace compose <file>` | 파일 하나를 테스트 |

## Common Checks

- CI는 `repository-integrity` suite에서 `leaf.conftest-policy`
  (`scripts/validation/check-conftest-policy.sh`)로 이 job을 실행한다.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`

## Runbook Handoff

job이 실패하면 [runbook](../runbooks/0095-conftest.md)을 사용한다.

## Traceability

- [Policy](../policies/0095-conftest.md) (`POL-0095`)
- [Runbook](../runbooks/0095-conftest.md) (`RUN-0095`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Conftest package README](../../../infra/09-tooling/conftest/README.md)
- [Conftest documentation](https://www.conftest.dev/)
- [Rego policy language](https://www.openpolicyagent.org/docs/latest/policy-language/)
