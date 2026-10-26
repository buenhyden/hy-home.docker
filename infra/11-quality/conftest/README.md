---
title: "Conftest"
version: "1.0.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-27"
created: "2026-09-23"
---

<!-- [ID:11-quality:conftest] -->
# Conftest

> `infra/` 하위 Compose 파일과 Dockerfile에 대한 온디맨드 **OPTIONAL** 정책 테스트(Open Policy Agent Rego)입니다.

## Overview

Conftest는 `policy-check` profile로 선택되는 **OPTIONAL** one-shot 작업입니다.
공개 `infra/`와 `labs/`를 읽기 전용으로 마운트하고 network 없이 실행합니다.
호스트 wrapper가 Git 추적 소스 목록과 POL-0078에서 검증한 overlay의 상속
profile만 준비한 뒤, 정책 단위 테스트와 해당 Compose·Dockerfile 소스를 검사합니다.
`deny`는 실패, `warn`은 출력만 합니다. 무시된 설치 산출물은 읽지 않으며,
무시되지 않은 미추적 소스 후보는 Docker 호출 전에 실패합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Compose leaf와 Dockerfile을 위한 Rego 정책과 그 단위 테스트.
- 이를 추적 중인 인프라 소스에 대해 실행하는 작업.

### Out of Scope

- 컨테이너, 이미지, Docker 데몬의 런타임 검사.
- 시크릿, `.env`, `infra/` 밖의 모든 것.

## Structure

```text
conftest/
├── README.md            # This file
├── docker-compose.yml   # One-shot job
├── run.sh               # verify, then test the required prepared source lists
└── policy/
    ├── compose.rego         # namespace compose
    ├── compose_test.rego
    ├── dockerfile.rego      # namespace dockerfile
    └── dockerfile_test.rego
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Tool** | Conftest (`openpolicyagent/conftest`) | Rego v1 정책 |
| **Access** | 공개 `infra/`, `labs/`, 임시 파생 입력 읽기 전용 | 네트워크 없음, UID 1000, 읽기 전용 root |

## Configuration

환경 변수나 시크릿이 없습니다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `bash scripts/validation/check-conftest-policy.sh` | 준비된 버전 관리 소스에 대해 정책 단위 테스트와 corpus 검사를 실행합니다. |
| `bash scripts/validation/check-conftest-policy.sh --mode corpus` | 준비된 Compose·Dockerfile corpus만 검사합니다. |
| `bash scripts/validation/check-conftest-policy.sh --mode verify` | 정책 단위 테스트만 실행합니다. |

## Validation

- CI: `leaf.conftest-policy`가 `scripts/validation/check-conftest-policy.sh`를 실행합니다.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

`corpus`와 기본 `all`은 wrapper가 만든 두 NUL 경로 목록·digest와 검증된
부분 overlay 입력을 요구합니다. 파생 입력은 서비스의 상속 `profiles`만 추가하며
다른 Rego 입력은 유지합니다. 실행용 Compose 원본을 고치거나 profile 권한을
새로 만들지 않습니다. wrapper는 읽기 전용 임시 입력만 job에 추가하고 종료 후
정리합니다. 준비 실패에는 raw 입력으로 되돌아가는 경로가 없습니다.
직접 선언된 job의 `verify`는 사용할 수 있으나, 준비되지 않은 `corpus`·기본 실행은
wrapper가 필요하다는 오류로 종료합니다.

## Troubleshooting

- `FAIL - <file> - <namespace> - …`는 선언과 규칙을 가리키므로 해당 선언을 수정합니다.
- `verify`가 실패하면 규칙과 그 테스트가 서로 어긋난다는 뜻입니다.

## Related Documents

- **Guide**: Conftest Usage Guide (`docs/05.operations/guides/12-testing-and-quality/0095-conftest.md`)
- **Policy**: Conftest Operations Policy (`docs/05.operations/policies/12-testing-and-quality/0095-conftest.md`)
- **Runbook**: Conftest Recovery Runbook (`docs/05.operations/runbooks/12-testing-and-quality/0095-conftest.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `11-quality`의 Conftest 작업 leaf; 서비스: `conftest`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/conftest/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml`, `run.sh`, `policy/*.rego` |
| Config values | 프로필: `policy-check` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/conftest/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | 없음 (`network_mode: none`) |
| Volumes | `../..:/project/infra:ro`, `../../../labs:/project/labs:ro` |
| Ports | 게시되지 않음 |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | 선언되지 않음 (1회성 작업) |
| Operations | Guide (`docs/05.operations/guides/12-testing-and-quality/0095-conftest.md`), Policy (`docs/05.operations/policies/12-testing-and-quality/0095-conftest.md`), Runbook (`docs/05.operations/runbooks/12-testing-and-quality/0095-conftest.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 작업을 실행하고 처음 실패한 선언을 수정합니다. 런북을 참고합니다. |

## Usage

1. 새 규칙에는 같은 디렉터리에 통과·실패 테스트를 함께 추가한다.
2. 현재 소스가 통과하지 못하는 규칙은 `warn`으로 시작한다.
3. allowlist 항목은 서비스와 사유를 정책 파일에 적는다.

런타임 이미지와 프로필의 권위는 [docker-compose.yml](docker-compose.yml)에 있으며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 근거입니다.
