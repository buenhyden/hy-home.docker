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
| **Service** | Syncthing | v2.0.13 |
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

## Related References

- **Guide**: [Syncthing Guide](../../../docs/07.guides/09-tooling/syncthing.md)
- **Operation**: [Syncthing Operations](../../../docs/08.operations/09-tooling/syncthing.md)
- **Runbook**: [Syncthing Runbook](../../../docs/09.runbooks/09-tooling/syncthing.md)
