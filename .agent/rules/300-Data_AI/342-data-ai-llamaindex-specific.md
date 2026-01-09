---
trigger: always_on
glob: "**/*.py"
description: "LlamaIndex: RAG Pipelines, Modularity, and Settings specific rules."
---
# LlamaIndex Specific Rules

## 1. Modularity

- **No Monoliths**: Break down RAG pipelines into data loading, indexing, and querying functions.
- **Workflow API**: Use the `Workflow` API for complex, event-driven agentic patterns.

## 2. Configuration

- **Global Settings**: Use `Settings` (e.g., `Settings.llm`, `Settings.embed_model`) to configure models globally at app startup.
- **Environment**: Load API keys `OPENAI_API_KEY` etc. from environment variables.

### Example: Configuration

#### Good (Example)

```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

def configure():
    Settings.llm = OpenAI(model="gpt-4", temperature=0)
    Settings.chunk_size = 512
```

## 3. Data Ingestion

- **LlamaParse**: Use LlamaParse for complex documents (PDFs with tables).
- **Vector Store**: For production, use a persistent vector store (Qdrant, Pinecone) rather than in-memory `VectorStoreIndex` alone.

## 4. Coding Standards

- **Type Hints**: Type annotations are mandatory (`List[Document]`, `BaseQueryEngine`).
- **Async**: Prefer `async` methods for IO-bound operations (indexing, querying).

### Example: Async Ingestion

#### Good (Example)

```python
async def build_index(docs: List[Document]):
    return await asyncio.to_thread(VectorStoreIndex.from_documents, docs)
```
