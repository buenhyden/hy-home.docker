---
trigger: always_on
glob: "**/*.py"
description: "AI/Deep Learning: PyTorch, Transformers, and LlamaIndex best practices."
---
# Deep Learning & AI Standards

## 1. PyTorch Best Practices

- **Tensors**: Use specific types (e.g., `float32`).
- **Device**: Write device-agnostic code (`device = "cuda" if torch.cuda.is_available() else "cpu"`).
- **Optimization**: Use `DataLoader` with `num_workers`. Use Mixed Precision (`torch.cuda.amp`) for speed on GPU.

## 2. Transformers (Hugging Face)

- **Tokenizers**: Use the fast tokenizers (`use_fast=True`).
- **Pipelines**: Use `pipeline()` for inference when simple customization is needed.
- **Saving**: Save models using `save_pretrained()` and `safetensors` format if possible.

## 3. LlamaIndex (RAG)

- **Modularity**: Separate ingestion (loading) from querying logic.
- **Settings**: Configure global `Settings` (LLM, Embed Model) explicitly.
- **Production**: Use persistent vector stores (e.g., Qdrant, Pinecone) instead of in-memory for production.

### Example: Device Agnostic PyTorch

#### Good

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
inputs = inputs.to(device)
```

### Example: LlamaIndex Modularity

#### Good

```python
from llama_index.core import Settings

def configure_settings():
    Settings.llm = OpenAI(model="gpt-4")
    Settings.embed_model = OpenAIEmbedding()

def build_index(docs):
    return VectorStoreIndex.from_documents(docs)
```
