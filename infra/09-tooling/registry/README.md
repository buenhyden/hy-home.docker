<!-- [ID:09-tooling:registry] -->
# Docker Registry

> Private OCI-compliant image distribution service.

## Overview

이 서비스는 컨테이너 이미지를 내부 네트워크에서 관리하고 배포하는 **프라이빗 도커 레지스트리**입니다. 외부 네트워크 의존성을 줄이고 보안이 강화된 이미지 저장소로 활용됩니다.

The `registry` service acts as the internal repository for container images in `hy-home.docker`. It enables fast, local pulls for internal infrastructure and avoids dependency on external public registries for proprietary or sensitive images.

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

- External authentication (handled via proxy or basic auth if needed).
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

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Start the registry service. |
| `docker pause registry` | Pause the registry service. |

## Related References

- **Guide**: [Registry Guide](../../../docs/07.guides/09-tooling/registry.md)
- **Operation**: [Registry Operations](../../../docs/08.operations/09-tooling/registry.md)
- **Runbook**: [Registry Runbook](../../../docs/09.runbooks/09-tooling/registry.md)
