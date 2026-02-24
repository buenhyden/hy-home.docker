# Qdrant Vector Database Context

> **Component**: `qdrant`
> **Internal Port**: `6333` (REST), `6334` (gRPC)
> **Administrative Node**: AI-tier

## 1. RAG Infrastructure Core

Qdrant serves as the vector store for the local RAG (Retrieval-Augmented Generation) platform, enabling semantic search and long-term memory for LLMs.

- **Internal API**: `http://qdrant:6333`
- **Dashboard**: `https://qdrant.${DEFAULT_URL}`

## 2. Resource Characteristics

Qdrant performance is heavily dependent on RAM. For high-dimensional HNSW (Hierarchical Navigable Small World) indices:

- Ensure the Docker container has a minimum of 2GB RAM.
- Use `mmap_threshold` settings to optimize disk utilization vs RAM caching.

## 3. Persistent Volumes

All collection data and WAL snapshots reside in the `qdrant-data` Docker volume.

- **Backup Notice**: Qdrant supports online snapshots via its REST API. Always perform a snapshot before host-level block backups.
