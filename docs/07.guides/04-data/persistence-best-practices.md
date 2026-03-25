# Persistence Best Practices

Guidelines for maintaining data integrity and performance across the `hy-home.docker` ecosystem.

## 1. Volume Management

All persistent data should reside under `${DEFAULT_DATA_DIR}`.

- **Naming**: Use service-prefixed names (e.g., `postgresql-data`).
- **Permissions**: Ensure UID/GID matches the container requirements (typically 999 or 1000).

## 2. Storage Tiers

| Tier | Services | Optimization |
| :--- | :--- | :--- |
| **Hot** | PostgreSQL, Valkey | Fast NVMe / Local Bind. |
| **Warm** | MongoDB, SeaweedFS | Balanced SSD. |
| **Cold** | MinIO (Archival) | Compression / HDD. |

## 3. Maintenance

- Regularly audit volume usage via `docker system df -v`.
- Prune unused volumes monthly.
