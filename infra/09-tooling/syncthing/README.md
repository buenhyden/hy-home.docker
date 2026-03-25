<!-- [ID:09-tooling:syncthing] -->
# Syncthing

> Continuous, secure peer-to-peer file synchronization.

## 1. Overview (KR)

이 서비스는 장치 간에 실시간으로 파일을 안전하게 동기화하는 **P2P 파일 동기화 도구**입니다. 데이터의 분산 저장 및 가용성 보장을 위해 활용됩니다.

## 2. Overview

The `syncthing` service provides decentralized file synchronization for `hy-home.docker`. It replaces centralized cloud storage with secure, encrypted P2P syncing between infrastructure nodes and user devices.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **syncthing** | Syncthing 2.0 | Peer-to-Peer Sync Engine |

## 4. Networking

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `8384` | HTTP | Admin GUI (`syncthing.${DEFAULT_URL}`). |
| `22000` | TCP/UDP | Device data transfer (Sync Protocol). |
| `21027` | UDP | Local network discovery (Broadcast). |

## 5. Persistence & Secrets

- **Config Volume**: `syncthing-volume` → `${DEFAULT_TOOLING_DIR}/syncthing`.
- **Sync Directory**: `resources-contents-volume` → `${DEFAULT_RESOURCES_DIR}`.
- **Secrets**: `syncthing_password`.

## 6. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Syncthing service definition. |
| `README.md` | Service overview (this file). |

---

## Documentation References

- [DevOps Tooling Guide](../../../docs/07.guides/09-tooling/README.md)
- [Backup Policy](../../../docs/08.operations/04-data/backup-policy.md)
