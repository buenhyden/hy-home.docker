# Ollama & Open WebUI

This stack provides local LLM inference and a powerful chat interface.

## Services

| Service      | Image                      | Role           | Resources               |
| :----------- | :------------------------- | :------------- | :---------------------- |
| `ollama`     | `ollama/ollama:latest`     | Inference Engine| 4 CPU / 8GB RAM / 1 GPU |
| `open-webui` | `ghcr.io/open-webui/open-webui:main` | Chat UI        | 1 CPU / 1GB RAM         |

## Networking

- **Ollama**: `ollama.${DEFAULT_URL}`.
- **WebUI**: `chat.${DEFAULT_URL}`.

## GPU Support

Ensure the NVIDIA Container Toolkit is installed on the host and `deploy: resources: reservations: devices` is configured in `docker-compose.yml`.

## File Map

| Path             | Description                         |
| ---------------- | ----------------------------------- |
| `ollama/`        | Ollama service and data persistence.|
| `open-webui/`    | Open WebUI service.                 |
| `README.md`      | Service overview and model guides.  |
