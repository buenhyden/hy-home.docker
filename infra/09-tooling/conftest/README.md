---
title: "Conftest"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:09-tooling:conftest] -->
# Conftest

> On-demand OPTIONAL policy test (Open Policy Agent Rego) over the Compose files and Dockerfiles under `infra/`.

## Overview

Conftest는 `policy-check` profile로 선택되는 **OPTIONAL** one-shot 작업입니다.
`infra/`만 read-only로 mount하고 network 없이 실행하며, 먼저 정책 자체의
단위 테스트(`conftest verify`)를 돌린 뒤 모든 `docker-compose*.yml`과
`Dockerfile*`을 검사합니다. `deny`는 실패, `warn`은 출력만 합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Rego policies for Compose leaves and Dockerfiles, with their unit tests.
- A job that runs them against the tracked infrastructure source.

### Out of Scope

- Runtime inspection of containers, images or the Docker daemon.
- Secrets, `.env` and anything outside `infra/`.

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
| **Tool** | Conftest (`openpolicyagent/conftest`) | Rego v1 policies |
| **Access** | `infra/` read-only | No network, UID 1000, read-only root |

## Configuration

No environment variables or secrets.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose --profile policy-check run --rm conftest` | Verify the policies and test all Compose files and Dockerfiles. |

## Validation

- CI: `leaf.conftest-policy` runs `scripts/validation/check-conftest-policy.sh`.
- `HYHOME_COMPOSE_PROFILES=policy-check bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- `FAIL - <file> - <namespace> - …` names the declaration and rule; fix the declaration.
- A failing `verify` summary means a rule and its test disagree.

## Related Documents

- **Guide**: Conftest Usage Guide (`docs/05.operations/catalog/09-tooling/0095-conftest/guide.md`)
- **Policy**: Conftest Operations Policy (`docs/05.operations/catalog/09-tooling/0095-conftest/policy.md`)
- **Runbook**: Conftest Recovery Runbook (`docs/05.operations/catalog/09-tooling/0095-conftest/runbook.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Conftest job leaf in `09-tooling`; services: `conftest`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/conftest/docker-compose.yml` |
| Config files | `docker-compose.yml`, `run.sh`, `policy/*.rego` |
| Config values | profiles: `policy-check` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/conftest/docker-compose.yml` |
| Networks | none (`network_mode: none`) |
| Volumes | `../..:/project/infra:ro` |
| Ports | Not published |
| Labels | `hy-home.tier` |
| Secret refs | Not declared |
| Healthcheck | Not declared (one-shot job) |
| Operations | Guide (`docs/05.operations/catalog/09-tooling/0095-conftest/guide.md`), Policy (`docs/05.operations/catalog/09-tooling/0095-conftest/policy.md`), Runbook (`docs/05.operations/catalog/09-tooling/0095-conftest/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Run the job and fix the first failing declaration; see the runbook. |

## How to Work in This Area

1. 새 규칙에는 같은 디렉터리에 통과·실패 테스트를 함께 추가한다.
2. 현재 소스가 통과하지 못하는 규칙은 `warn`으로 시작한다.
3. allowlist 항목은 서비스와 사유를 정책 파일에 적는다.

Runtime image and profile authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../tech-stack.versions.json) is drift evidence.
