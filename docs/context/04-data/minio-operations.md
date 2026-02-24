# MinIO Operations

> **Component**: `minio`

## Usage

### 1. Web Console

- **URL**: `https://minio-console.${DEFAULT_URL}`
- **Login**: Use credentials from `.env` (or secrets).

### 2. S3 Access (Clients)

- **Endpoint**: `https://minio.${DEFAULT_URL}`
- **Region**: `us-east-1` (MinIO default)

### 3. CLI (mc)

You can interact with MinIO using the official client.

**Alias Configuration:**

```bash
mc alias set local http://localhost:${MINIO_HOST_PORT} ROOT_USER ROOT_PASSWORD
```

**Commands:**

```bash
# List buckets
mc ls local

# Upload file
mc cp my-file.txt local/cdn-bucket/

# Set bucket public
mc anonymous set public local/cdn-bucket
```

## Troubleshooting

### "Bucket already owned by you"

The init container prints "ignore-existing" warnings if buckets already exist. This is normal and indicates idempotency.

### "Init container fails"

If `minio-create-buckets` fails:

1. Check if `minio` service is healthy.
2. Verify secrets are correctly populated in `/run/secrets/`.
3. Check logs: `docker compose logs minio-create-buckets`
