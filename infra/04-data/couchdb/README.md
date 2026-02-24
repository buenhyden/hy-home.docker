# CouchDB

Apache CouchDB is an open-source document-oriented NoSQL database, implemented in Erlang.

## Services

| Service   | Image               | Role           | Resources         | Port       |
| :-------- | :------------------ | :------------- | :---------------- | :--------- |
| `couchdb` | `couchdb:3.3`       | Document DB    | 0.5 CPU / 1GB RAM | 5984 (Int) |

## Networking

| Endpoint                   | Port | Purpose                 |
| :------------------------- | :--- | :---------------------- |
| `couchdb.${DEFAULT_URL}`   | 5984 | Web UI (Fauxton) / API  |

## Persistence

- **Data**: `/opt/couchdb/data` (mounted to `couchdb-data` volume).

## Configuration

- **Admin**: Configured via `COUCHDB_USER` and `COUCHDB_PASSWORD`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and cluster docs.  |
