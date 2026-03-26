# Qdrant Infrastructure README

Qdrant is the vector database engine for the `04-data` tier, used by AI services for embedding storage and retrieval.

## Deployment Details
- **Network**: `infra_net`
- **Persistence**: `${DEFAULT_DATA_DIR}/qdrant`
- **Interface**: gRPC / HTTP API

## Related Documents
- [ARD](../../docs/02.ard/0004-data-architecture.md)
- [Guide](../../docs/07.guides/04-data/03.nosql-dbs.md)
