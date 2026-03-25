# AI Infrastructure (08-ai)

Local LLM inference engines and RAG (Retrieval-Augmented Generation) interfaces.

## 0. Context & SSoT

- **Documentation**: [docs/07.guides/08-ai/README.md](../../docs/07.guides/08-ai/README.md)
- **Operations**: [docs/08.operations/08-ai/README.md](../../docs/08.operations/08-ai/README.md)
- **Runbooks**: [docs/09.runbooks/08-ai/README.md](../../docs/09.runbooks/08-ai/README.md)
- **Secrets**: [secrets/08-ai/](../../secrets/) (Managed via Keycloak SSO)

## 1. Structure & Services

| Service | Directory | Description |
| :--- | :--- | :--- |
| **Ollama** | [`./ollama/`](./ollama/) | Local LLM inference server (Go-based) |
| **Open WebUI** | [`./open-webui/`](./open-webui/) | Web interface for chat and RAG (Svelte-based) |

## 2. Tech Stack

- **Inference**: Ollama (supports GGUF, PyTorch, etc.)
- **Interface**: Open WebUI (formerly Ollama WebUI)
- **Vector Search**: Qdrant (Targeted at `infra/04-data/qdrant`)
- **Acceleration**: NVIDIA CUDA (Requires NVIDIA Container Toolkit)

## 3. Configuration & Sockets

- **Internal Network**: `infra_net`
- **DNS Endpoints**:
  - Ollama: `ollama:11434`
  - Open WebUI: `open-webui:8080`
- **Traefik Entrypoints**:
  - `ollama.${DEFAULT_URL}`
  - `chat.${DEFAULT_URL}`

## 4. Persistence

- **AI Models**: Hosted on `${DEFAULT_AI_MODEL_DIR}/ollama` to ensure persistence across container updates.
- **App Data**: Open WebUI configuration stored in `${DEFAULT_AI_MODEL_DIR}/open-webui`.

## 5. Operational Status

> [!IMPORTANT]
> GPU acceleration requires `nvidia-container-toolkit` installed on the host. Check status via `nvidia-smi` inside the ollama container.

> [!NOTE]
> All services are protected by Keycloak SSO auth middleware via Traefik.
