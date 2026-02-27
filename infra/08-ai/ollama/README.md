# Ollama & Open WebUI

This stack provides local LLM inference and a powerful chat interface.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `ollama` | `ollama/ollama:0.13.5` | LLM Engine | 4.0 CPU / 8GB RAM / GPU |
| `exporter`| `ollama-exporter:1.0.1` | Metrics | Default |

## Networking

- **Internal DNS**: `ollama:${OLLAMA_PORT:-11434}` (within `infra_net`)
- **External URL**: `https://ollama.${DEFAULT_URL}` (via Traefik)
- **Metrics**: `ollama-exporter:${OLLAMA_EXPORTER_PORT:-11435}` (within `infra_net`)

## Security

- **SSO**: Protected by `sso-auth@file` middleware (Keycloak).
- **Hardening**: `no-new-privileges:true`.

## Persistence

- **Models**: `ollama-data` volume mapped to `${DEFAULT_AI_MODEL_DIR}/ollama` on the host.
- **GPU**: Enable GPU passthrough on the host (Compose uses a `deploy.resources.reservations.devices` block).

## File Map

| Path             | Description                         |
| ---------------- | ----------------------------------- |
| `ollama/`        | Ollama service and data persistence.|
| `open-webui/`    | Open WebUI service.                 |
| `README.md`      | Service overview and model guides.  |
