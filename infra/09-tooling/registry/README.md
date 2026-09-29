---
title: "Docker Registry"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
created: "2026-03-19"
---

<!-- [ID:09-tooling:registry] -->
# Docker Registry

> **HOME** OCI 이미지 저장소이며 호스트 엔드포인트는 loopback 전용 인증되지 않은 HTTP입니다.

## Overview

이 서비스는 승인된 신뢰 네트워크에서 비민감 OCI 이미지를 저장·배포하는 **HOME** Registry입니다. 현재 Compose는 호스트 포트 `${REGISTRY_PORT:-5000}`을 `127.0.0.1`에만 게시하며, Registry TLS·인증·Traefik route를 선언하지 않습니다. 같은 network의 컨테이너는 `registry:5000`에 인증 없이 접근할 수 있습니다.

`registry` 서비스는 민감하지 않은 아티팩트를 위한 로컬 OCI 저장소입니다. 호스트 엔드포인트는 `127.0.0.1`에 바인딩되어 있으며 인증 없는 HTTP입니다. 같은 네트워크의 컨테이너도 인증 없이 접근할 수 있습니다. TLS와 접근 제어가 구현되고 테스트되기 전까지는 독점적이거나 민감한 이미지를 저장하지 말고 승인된 신뢰 네트워크 밖으로 엔드포인트를 노출하지 않습니다.

## Audience

이 README의 주요 독자:

- Operators
- CI/CD Developers
- AI Agents

## Scope

### In Scope

- Docker Registry v2 핵심 서비스.
- 로컬 이미지 영속화 및 배포.
- 기본적인 헬스 모니터링.

### Out of Scope

- TLS, 인증, 접근 제어 (추적 중인 서비스에는 구현되어 있지 않음).
- 고가용성(HA) 영속화 (현재는 단일 노드 바인딩).
- 이미지 보안 스캔 (SonarQube나 Trivy에서 별도로 처리).

## Structure

```text
registry/
├── README.md          # This file
└── docker-compose.yml # Service definition
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | Registry v2 | 이미지 배포 |
| **Port** | `127.0.0.1:${REGISTRY_PORT:-5000}` → `5000` | Loopback 전용 호스트 게시 |
| **Storage** | Bind Mount | `${DEFAULT_REGISTRY_DIR}` |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `REGISTRY_PORT` | No | Loopback 호스트 포트(기본값: 5000); 컨테이너는 항상 5000에서 수신합니다. |
| `DEFAULT_REGISTRY_DIR` | Yes | 이미지 영속화를 위한 로컬 경로. |

## Available Scripts

저장소 루트에서 다음 읽기 전용 확인 명령을 실행합니다. Registry를 시작하거나 변경하려면 런타임 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile registry config --services` | 선택된 root-project 서비스를 확인합니다. |
| `docker compose --profile registry logs --tail=200 registry` | 승인된 실행 중인 Registry 서비스를 점검합니다. |

## Validation

- Registry에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 09-tooling`을 실행합니다.
- Registry 문서를 준비 완료로 표시하기 전에 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- registry 네트워크, 볼륨, 레이블 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- 저장소나 접근 설정을 변경하기 전에 registry 로그와 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: Registry Guide (`docs/05.operations/guides/0065-registry.md`)
- **Policy**: Registry Operations (`docs/05.operations/policies/0065-registry.md`)
- **Runbook**: Registry Runbook (`docs/05.operations/runbooks/0065-registry.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `09-tooling`의 Docker Registry 서비스 leaf; 서비스: `registry`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/registry/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml` |
| Config values | 프로필: `tooling`, `registry` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/registry/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | project default |
| Volumes | `registry-data-volume:/var/lib/registry:rw`, `registry-data-volume` |
| Ports | `127.0.0.1:${REGISTRY_PORT:-5000}:5000` |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | `registry`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0065-registry.md`), Policy (`docs/05.operations/policies/0065-registry.md`), Runbook (`docs/05.operations/runbooks/0065-registry.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 이미지와 프로필의 권위는 [docker-compose.yml](docker-compose.yml)에 있으며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 근거입니다.
