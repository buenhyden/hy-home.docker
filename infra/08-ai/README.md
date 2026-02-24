# AI (08-ai)

This category manages local LLM inference engines and RAG (Retrieval-Augmented Generation) interfaces.

## Services

| Service     | Profile  | Path           | Purpose                            |
| ----------- | -------- | -------------- | ---------------------------------- |
| Ollama      | `ollama` | `./ollama`     | Local LLM inference server         |
| Open WebUI  | `ollama` | `./open-webui` | User interface for Chat and RAG    |

## Dependencies

- **Vector DB**: Open WebUI connects to Qdrant (`infra/04-data/qdrant`).
- **GPU**: Requires NVIDIA Container Toolkit on the host for acceleration.

## File Map

| Path          | Description                         |
| ------------- | ----------------------------------- |
| `ollama/`     | Ollama server and metrics exporter. |
| `open-webui/` | Open WebUI application and backend. |
| `README.md`   | Category overview.                  |
