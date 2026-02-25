# OpenSearch Cluster

OpenSearch is a distributed search and analytics engine.

## Services

| Service | Image | Role | Resources | IP |
| :--- | :--- | :--- | :--- | :--- |
| `opensearch` | `build: ./Dockerfile` | Search Engine | 1GB Heap / 1GB SHM | `172.19.0.44` |
| `dashboards` | `opensearchproject/...:3.4.0` | Analytics GUI | Default | `172.19.0.47` |
| `exporter` | `elasticsearch-exporter:v1.10.0`| Metrics | Default | `172.19.0.48` |

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
s/opensearch_auth.txt`).
- **Cluster**: Single-node configuration for development (`discovery.type=single-node`).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and cluster notes. |
