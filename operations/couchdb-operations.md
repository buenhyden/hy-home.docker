# CouchDB Operations

> **Component**: `influxdb`
> **Profile**: `compose-file` (Standard)
> **Profile**: `compose-file` (Standard)

## Usage

### 1. Web UI (Fauxton)

Access the management dashboard at `https://couchdb.${DEFAULT_URL}/_utils`.

### 2. API Access

```bash
# Check cluster status
curl -u ${COUCHDB_USERNAME}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/_membership

# Create a database
curl -X PUT -u ${COUCHDB_USERNAME}:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/my_new_db
```

## Troubleshooting

### "Cluster not fully joined"

Check the logs of the initialization container:

```bash
docker logs couchdb-cluster-init
```

### "Consistency Issues"

Ensure your client supports HTTP cookies to take advantage of Traefik's sticky sessions, or target a specific node alias if performing cluster maintenance.
