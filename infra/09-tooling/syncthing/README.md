# Syncthing

Syncthing is a continuous file synchronization program that synchronizes files and directories between two or more devices in real time.

## Services

| Service     | Image                        | Role                    | Resources               |
| :---        | :---                         | :---                    | :---                    |
| `syncthing` | `syncthing/syncthing:2.0.13` | File sync daemon         | med (0.5 CPU / 512 MB) |

## Networking

- **Web GUI**: `https://syncthing.${DEFAULT_URL}` via Traefik (internal port `${SYNCTHING_GUI_PORT:-8384}`).
- **Sync Protocol**: TCP+UDP on `${SYNCTHING_SYNC_HOST_PORT:-22000}` (data transfer).
- **Discovery**: UDP on `${SYNCTHING_BROADCASTS_HOST_PORT:-21027}` (local peer discovery broadcasts).

## Persistence

- **Config Volume**: `syncthing-volume` → `${DEFAULT_TOOLING_DIR}/syncthing` (Syncthing database and certificates).
- **Sync Directory**: `resources-contents-volume` → `${DEFAULT_RESOURCES_DIR}` (data to be synchronized, available at `/Sync` in container).

## Secrets

| Secret               | Description                                    |
| :---                 | :---                                           |
| `syncthing_password` | Web GUI admin password (Docker secret mount). |

## Configuration

Key environment variables (from `.env`):

| Variable                      | Default | Description                          |
| :---                          | :---    | :---                                 |
| `SYNCTHING_SYNC_HOST_PORT`    | `22000` | Host port for sync protocol (TCP+UDP).|
| `SYNCTHING_BROADCASTS_HOST_PORT` | `21027` | Host port for local discovery (UDP). |
| `SYNCTHING_GUI_PORT`          | `8384`  | Internal port for the Web GUI.       |
| `SYNCTHING_USERNAME`          | —       | Web GUI admin username.              |
| `DEFAULT_RESOURCES_DIR`       | —       | Host path mounted as sync target.    |
| `PUID` / `PGID`               | `1000`  | UID/GID for file ownership.          |

## File Map

| Path                | Description                                  |
| ------------------- | -------------------------------------------- |
| `docker-compose.yml`| Service definition with volumes and Traefik. |
| `README.md`         | Service overview (this file).                |
