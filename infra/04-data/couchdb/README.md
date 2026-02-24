# CouchDB

Apache CouchDB is an open-source document-oriented NoSQL database, implemented in Erlang.

## Services

| Service | Image | Role | Profile |
| :--- | :--- | :--- | :--- |
| `couchdb-1, 2, 3` | `couchdb:3.5.1` | DB Nodes | `couchdb` |
| `couchdb-init` | `curlimages/curl` | Cluster Setup | `couchdb` |

## Networking

- **URL**: `couchdb.${DEFAULT_URL}` via Traefik.
- **Load Balancing**: Sticky sessions enabled (`couchdb_sticky` cookie).
- **Internal Ports**: `5984` (API), `4369` (Epmd), `9100` (Distribution).

## Persistence

- **Volumes**: `couchdb1-data`, `couchdb2-data`, `couchdb3-data`.
- **Mount Point**: `/opt/couchdb/data`.

## Configuration

- **Admin User**: `${COUCHDB_USERNAME}`
- **Secrets**: Uses `couchdb_password` and `couchdb_cookie` Docker secrets.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and cluster docs.  |
