# RAG Stack Specification (Ollama & Open WebUI)

## 1. Context

The local AI RAG (Retrieval-Augmented Generation) infrastructure leverages a triad of open-source applications mapped under the `08-ai` layer of `infra`.

Components:

- **Ollama**: The target inference engine processing Open-Weight LLMs (e.g., Llama 3, Mistral).
- **Open WebUI**: The frontend chat interface, capable of orchestrating complex web queries and direct document ingestion.
- **Qdrant**: The Vector Database storing text embeddings locally for semantic search.

## 2. Network Topology & Profile

We run this stack optionally under the `ollama` profile to conserve resources.
All containers attach to `infra_net`.

## 3. Communication Protocols

- **Open WebUI -> Ollama**:
  Open WebUI connects to Ollama via HTTP to issue inference requests.
  `OLLAMA_BASE_URL=http://ollama:11434`
- **Open WebUI -> Qdrant**:
  When documents are uploaded, the embedding models convert the text into high-dimensional vectors. These are stored directly in Qdrant.
  `VECTOR_DB=qdrant`
  `QDRANT_URL=http://qdrant:6333`

## 4. Volume Persistence Rules

To prevent having to re-download large LLM models (~4GB to ~40GB), the `.ollama` directory MUST be mounted.

```yaml
volumes:
  - ollama-data:/root/.ollama
```

Similarly, Qdrant vectors are bound to:

```yaml
volumes:
  - qdrant-data:/qdrant/storage
```
