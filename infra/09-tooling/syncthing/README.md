<!-- [ID:09-tooling:syncthing] -->
# Syncthing

> Continuous, secure peer-to-peer file synchronization.

## Overview

The `syncthing` service provides decentralized file synchronization for `hy-home.docker`. It replaces centralized cloud storage with secure, encrypted P2P syncing between infrastructure nodes and user devices.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- System Architects
- AI Agents

## Scope

### In Scope

- Syncthing Core P2P synchronization service.
- Traefik-integrated Admin GUI.
- Local and global device discovery.
- Persistent storage for `Sync` data and internal config.

### Out of Scope

- External Relay server setup (using public relays by default).
- Client-side application installation (Desktop/Mobile).
- Individual folder permission management (managed via GUI).

## Structure

```text
syncthing/
├── README.md           # This file
└── docker-compose.yml  # Service definition
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | Syncthing | `syncthing/syncthing:2.1.1` |
| **Protocol** | BEP (Block Exchange Protocol) | P2P Sync |
| **Network** | Traefik | SSL GUI termination |
| **Data Storage** | Bind Mount | `${DEFAULT_RESOURCES_DIR}` |

## Configuration

### Networking

| Port | Protocol | Description |
| :--- | :---: | :--- |
| `8384` | HTTP | Admin GUI (internal). |
| `22000` | TCP/UDP | Data transfer (Sync). |
| `21027` | UDP | Discovery (Broadcast). |

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SYNCTHING_GUI_PORT` | No | GUI listening port (default: 8384). |
| `SYNCTHING_USERNAME` | Yes | GUI login username. |
| `SYNCTHING_SYNC_PORT`| No | Sync listening port (default: 22000). |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d` | Start the Syncthing service. |
| `docker compose logs -f` | View real-time service logs. |

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 09-tooling` after README or Compose reference changes that affect Syncthing.
- Run `bash scripts/validation/check-repo-contracts.sh` before marking Syncthing documentation ready.

## Troubleshooting

- Start with the hardening check to confirm Syncthing network, volume, and secret references stay declared.
- Check Syncthing logs and the linked runbook before changing sync folder or credential settings.

## Related Documents

- **Guide**: [Syncthing Guide](../../../docs/05.operations/guides/09-tooling/syncthing.md)
- **Policy**: [Syncthing Operations](../../../docs/05.operations/policies/09-tooling/syncthing.md)
- **Runbook**: [Syncthing Runbook](../../../docs/05.operations/runbooks/09-tooling/syncthing.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Syncthing service leaf in `09-tooling`; services: `syncthing`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/syncthing/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `PUID`, `PGID`, `FILE__USER`, `FILE__PASSWORD_FILE`; profiles: `tooling`, `sync` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/syncthing/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `syncthing-volume:/var/syncthing:rw`, `resources-contents-volume:/Sync:rw`, `syncthing-volume`, `resources-contents-volume` |
| Ports | `${SYNCTHING_SYNC_HOST_PORT:-22000}:${SYNCTHING_SYNC_PORT:-22000}/tcp`, `${SYNCTHING_SYNC_HOST_PORT:-22000}:${SYNCTHING_SYNC_PORT:-22000}/udp`, `${SYNCTHING_BROADCASTS_HOST_PORT:-21027}:${SYNCTHING_BROADCASTS_PORT:-21027}/udp`, `${SYNCTHING_GUI_PORT:-8384}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.syncthing.rule`, `traefik.http.routers.syncthing.entrypoints`, `traefik.http.routers.syncthing.tls`, `traefik.http.routers.syncthing.middlewares`, `traefik.http.services.syncthing.loadbalancer.server.port` |
| Secret refs | names: `syncthing_password`; mounts: `/run/secrets/syncthing_password` |
| Healthcheck | Compose healthcheck declared for `syncthing` |
| Operations | [Guide](../../../docs/05.operations/guides/09-tooling/syncthing.md), [Policy](../../../docs/05.operations/policies/09-tooling/syncthing.md), [Runbook](../../../docs/05.operations/runbooks/09-tooling/syncthing.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence in an approved runtime context. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
