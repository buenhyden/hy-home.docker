---
title: "Docker Registry"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
created: "2026-03-19"
---

<!-- [ID:09-tooling:registry] -->
# Docker Registry

> On-demand OPTIONAL OCI image store; the tracked endpoint is unauthenticated HTTP.

## Overview

이 서비스는 승인된 신뢰 네트워크에서 비민감 OCI 이미지를 임시로 저장·배포하는 **OPTIONAL** Registry입니다. 현재 Compose는 `${REGISTRY_PORT:-5000}`을 bind address 없이 게시하며, Registry TLS·인증·Traefik route를 선언하지 않습니다. 외부 firewall 또는 Docker daemon 정책은 tracked source로 확인되지 않으므로 보호 수단으로 가정하지 않습니다.

The `registry` service is an on-demand local OCI store for non-sensitive artifacts. Its current all-interface endpoint is unauthenticated HTTP. Do not store proprietary or sensitive images, or expose the endpoint beyond the approved trusted network, until TLS and access control are implemented and tested.

## Audience

이 README의 주요 독자:

- Operators
- CI/CD Developers
- AI Agents

## Scope

### In Scope

- Docker Registry v2 core service.
- Local image persistence and distribution.
- Basic health monitoring.

### Out of Scope

- TLS, authentication, and access control (not implemented in the tracked service).
- High Availability (HA) persistence (currently single-node binding).
- Image security scanning (handled by SonarQube or Trivy separately).

## Structure

```text
registry/
├── README.md          # This file
└── docker-compose.yml # Service definition
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | Registry v2 | Image Distribution |
| **Port** | `5000` | Standard OCI port |
| **Storage** | Bind Mount | `${DEFAULT_REGISTRY_DIR}` |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `REGISTRY_PORT` | No | Registry listening port (default: 5000). |
| `DEFAULT_REGISTRY_DIR` | Yes | Local path for image persistence. |

## Available Scripts

Run these read-only checks from the repository root. Starting or changing Registry requires runtime approval.

| Command | Description |
| :--- | :--- |
| `docker compose --profile registry config --services` | Confirm the selected root-project services. |
| `docker compose --profile registry logs --tail=200 registry` | Inspect an approved running Registry service. |

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 09-tooling` after README or Compose reference changes that affect the registry.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` before marking registry documentation ready.

## Troubleshooting

- Start with the hardening check to confirm registry network, volume, and label references stay declared.
- Check registry logs and the linked runbook before changing storage or access settings.

## Related Documents

- **Guide**: Registry Guide (`docs/05.operations/catalog/09-tooling/0065-registry/guide.md`)
- **Policy**: Registry Operations (`docs/05.operations/catalog/09-tooling/0065-registry/policy.md`)
- **Runbook**: Registry Runbook (`docs/05.operations/catalog/09-tooling/0065-registry/runbook.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Docker Registry service leaf in `09-tooling`; services: `registry`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/registry/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profiles: `tooling`, `registry` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/registry/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `registry-data-volume:/var/lib/registry:rw`, `registry-data-volume` |
| Ports | `${REGISTRY_PORT:-5000}:${REGISTRY_PORT:-5000}` |
| Labels | `hy-home.tier` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `registry` |
| Operations | Guide (`docs/05.operations/catalog/09-tooling/0065-registry/guide.md`), Policy (`docs/05.operations/catalog/09-tooling/0065-registry/policy.md`), Runbook (`docs/05.operations/catalog/09-tooling/0065-registry/runbook.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence in an approved runtime context. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

Runtime image and profile authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../tech-stack.versions.json) is drift evidence.
