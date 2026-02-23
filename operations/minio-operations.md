# MinIO Storage Operations Blueprint

> Standard operating procedures for the S3-compatible MinIO object storage cluster.

## 1. Description

MinIO serves as the primary artifact and blob storage utility for the applications and infrastructure deployments (e.g., Loki logs, database backups) routed through `infra/04-data/minio/docker-compose.yml`.

## 2. Bucket Provisioning

MinIO relies on the `mc` (MinIO Client) utility to interact with the backend API reliably. Initial buckets and users are constructed natively by the `minio-createbuckets` sidecar container upon fresh compose startups.

If you need to add new buckets manually in runtime:

```bash
docker exec -it minio-createbuckets sh

# Inside the container, point alias to local minio instance
mc alias set myminio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}

# Make bucket
mc mb myminio/new-custom-bucket

# Assign policy
mc anonymous set download myminio/new-custom-bucket
```

## 3. Storage Scalability and Limits

MinIO binds directly to the host filesystem at `${DEFAULT_DATA_DIR}/minio/data`.
To migrate or increase the host filesystem without compromising data:

1. Halt the MinIO stack.

```bash
docker compose -f infra/04-data/minio/docker-compose.yml down
```

1. Re-mount or transition the underlying host volume pointing to `${DEFAULT_DATA_DIR}/minio/data`.
2. Restart the container. Single-node MinIO configurations gracefully adopt existing disk states without strict re-indexing constraints.

## 4. Web Console Interface

Administrative operations (User management, Access Keys, direct file uploads) should primarily be executed via the Console.

- Access the Console through `https://minio-console.${DEFAULT_URL}` over the Traefik router.
- Login exclusively utilizing `${MINIO_ROOT_USER}` mapped credentials.

> [!TIP]
> MinIO's console runs on port `9001` internally, while the strict S3 API runs on `9000`. Ensure Traefik labels distinctively port-balance these domains (`minio.${DEFAULT_URL}` vs `minio-console.${DEFAULT_URL}`).
