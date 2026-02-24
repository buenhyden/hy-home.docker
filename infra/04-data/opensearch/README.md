# OpenSearch Cluster

OpenSearch is a distributed search and analytics engine.

## Services

| Service                | Image                                      | Role           | Resources       |
| :--------------------- | :----------------------------------------- | :------------- | :-------------- |
| `opensearch`           | `opensearchproject/opensearch:2.11.0`      | Search Engine  | 1 CPU / 4GB RAM |
| `opensearch-dashboards`| `opensearchproject/opensearch-dashboards:2.11.0` | Visualization  | 0.5 CPU / 1GB RAM |

## Networking

| Endpoint                 | Port | Purpose                |
| :----------------------- | :--- | :--------------------- |
| `search.${DEFAULT_URL}`  | 9200 | REST API               |
| `kibana.${DEFAULT_URL}`  | 5601 | Dashboards Web UI      |

## Persistence

- **Data**: `/usr/share/opensearch/data` (mounted to `opensearch-data` volume).

## Configuration

- **Security**: Basic Auth (credentials in `secrets/opensearch_auth.txt`).
- **Cluster**: Single-node configuration for development (`discovery.type=single-node`).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and cluster notes. |
