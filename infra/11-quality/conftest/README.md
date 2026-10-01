---
title: "Conftest"
version: "1.0.1"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-09-23"
---

<!-- [ID:11-quality:conftest] -->
# Conftest

> `infra/` 하위 Compose 파일과 Dockerfile에 대한 온디맨드 **OPTIONAL** 정책 테스트(Open Policy Agent Rego)입니다.

## Overview

Conftest는 `policy-check` profile로 선택되는 **OPTIONAL** one-shot 작업입니다.
`infra/`만 read-only로 mount하고 network 없이 실행하며 먼저 정책 자체의
단위 테스트(`conftest verify`)를 돌린 뒤 모든 `docker-compose*.yml`과
`Dockerfile*`을 검사합니다. `deny`는 실패, `warn`은 출력만 합니다.

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
├── run.sh               # verify, then test Compose files and Dockerfiles
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
| **Access** | `infra/` 읽기 전용 | 네트워크 없음, UID 1000, 읽기 전용 root |

## Configuration

환경 변수나 시크릿이 없습니다.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile policy-check run --rm conftest` | 정책을 검증하고 모든 Compose 파일과 Dockerfile을 테스트합니다. |

## Validation

- CI: `leaf.conftest-policy`가 `scripts/validation/check-conftest-policy.sh`를 실행합니다.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- `FAIL - <file> - <namespace> - …`는 선언과 규칙을 가리키므로 해당 선언을 수정합니다.
- `verify`가 실패하면 규칙과 그 테스트가 서로 어긋난다는 뜻입니다.

## Related Documents

- **Guide**: Conftest Usage Guide (`docs/05.operations/guides/0095-conftest.md`)
- **Policy**: Conftest Operations Policy (`docs/05.operations/policies/0095-conftest.md`)
- **Runbook**: Conftest Recovery Runbook (`docs/05.operations/runbooks/0095-conftest.md`)
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
| Volumes | `../..:/project/infra:ro` |
| Ports | 게시되지 않음 |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | 선언되지 않음 (1회성 작업) |
| Operations | Guide (`docs/05.operations/guides/0095-conftest.md`), Policy (`docs/05.operations/policies/0095-conftest.md`), Runbook (`docs/05.operations/runbooks/0095-conftest.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 작업을 실행하고 처음 실패한 선언을 수정합니다. 런북을 참고합니다. |

## How to Work in This Area

1. 새 규칙에는 같은 디렉터리에 통과·실패 테스트를 함께 추가한다.
2. 현재 소스가 통과하지 못하는 규칙은 `warn`으로 시작한다.
3. allowlist 항목은 서비스와 사유를 정책 파일에 적는다.

런타임 이미지와 프로필의 권위는 [docker-compose.yml](docker-compose.yml)에 있으며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 근거입니다.
