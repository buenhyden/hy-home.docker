# Ollama & Open WebUI

This stack provides local LLM inference and a powerful chat interface.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `ollama` | `ollama/ollama:0.13.5` | LLM Engine | 4.0 CPU / 8GB RAM / GPU |
| `exporter`| `ollama-exporter:1.0.1` | Metrics | Default |

## Networking

- **Static IP**: `172.19.0.40`
- **URL**: `ollama.${DEFAULT_URL}` via Traefik.
- **Port**: `11434` (Internal).

## Security

- **SSO**: Protected by `sso-auth@file` middleware (Keycloak).
- **Hardening**: `no-new-privileges:true`.

## Persistence

- **Models**: `ollama-data` volume mapped to `/root/.ollama`.
 is installed on the host and `deploy: resources: reservations: devices` is configured in `docker-compose.yml`.

## File Map

| Path             | Description                         |
| ---------------- | ----------------------------------- |
| `ollama/`        | Ollama service and data persistence.|
| `open-webui/`    | Open WebUI service.                 |
| `README.md`      | Service overview and model guides.  |
