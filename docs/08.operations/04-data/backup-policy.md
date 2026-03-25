# Backup Policy

Standard backup requirements for data infrastructure.

## 1. Frequency & Retention

| Database Tier | Frequency | Retention | Verification |
| :--- | :--- | :--- | :--- |
| **Critical** (PG, Supabase) | Daily | 30 Days | Monthly |
| **Cache** (Valkey) | None | N/A | N/A |
| **Object** (MinIO) | Weekly | 90 Days | Quarterly |

## 2. Tools

- **Native Utilities**: `pg_dump`, `mongodump`.
- **Restic**: Encrypted off-site snapshots to remote S3.
- **Rclone**: Syncing SeaweedFS volumes to secondary storage.

## 3. Verification

Backups are useless if they cannot be restored. Quarterly "Fire Drills" are mandatory for the **Critical** tier.
