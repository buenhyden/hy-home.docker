# OpenSearch Cluster

OpenSearch is a distributed search and analytics engine.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `opensearch` | `build: ./Dockerfile` | Search engine | 1GB heap / 1GB shm |
| `dashboards` | `opensearchproject/opensearch-dashboards:3.4.0` | Analytics GUI | Default |
| `exporter` | `prometheuscommunity/elasticsearch-exporter:v1.10.0`| Metrics exporter | Default |

## Networking

- **API Access**: `opensearch.${DEFAULT_URL}` via Traefik (Internal port 9200).
- **Dashboard**: `opensearch-dashboard.${DEFAULT_URL}` via Traefik (Internal port 5601).
- **Security**: Traefik handles TLS terminating, but backend communication also uses HTTPS with verification skip.

## Persistence

- **Data**: `opensearch-data` volume mapped to `${DEFAULT_DATA_DIR}/opensearch/opensearch1-data`.
- **Certs**: `opensearch_certs` volume mapped to `${DEFAULT_DOCKER_PROJECT_PATH}/secrets/certs`.

## Configuration

- **Auth**: Uses `opensearch_admin_password` and `opensearch_dashboard_password` secrets.
- **Plugins**: Custom build includes `analysis-nori` and `repository-s3`.
- **Cluster**: Single-node configuration for development (`discovery.type=single-node`).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and cluster notes. |
