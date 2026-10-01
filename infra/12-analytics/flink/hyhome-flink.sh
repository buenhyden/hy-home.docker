#!/bin/bash
# Export the lakehouse S3 secret into this process only, write the catalog
# statement (no secret) to tmpfs, then run the requested Flink command. The
# JobManager, the TaskManager and `sql-client.sh -i /tmp/lakehouse.sql` all
# start through this script, so each JVM signs with the same identity.
set -euo pipefail
secret=/run/secrets/seaweedfs_s3_lakehouse_secret_key
[[ -f "$secret" && ! -L "$secret" ]] || { echo "flink: lakehouse S3 secret missing" >&2; exit 64; }
AWS_SECRET_ACCESS_KEY="$(tr -d '\r\n' <"$secret")"
[[ -n "$AWS_SECRET_ACCESS_KEY" ]] || { echo "flink: lakehouse S3 secret empty" >&2; exit 64; }
export AWS_SECRET_ACCESS_KEY
: "${LAKEHOUSE_CATALOG_URI:?}" "${LAKEHOUSE_S3_ENDPOINT:?}" "${LAKEHOUSE_WAREHOUSE:?}" "${AWS_REGION:?}"

cat >/tmp/lakehouse.sql <<SQL
CREATE CATALOG lakehouse WITH (
  'type' = 'iceberg',
  'catalog-type' = 'rest',
  'uri' = '${LAKEHOUSE_CATALOG_URI}',
  'warehouse' = '${LAKEHOUSE_WAREHOUSE}',
  'rest.auth.type' = 'sigv4',
  'rest.signing-region' = '${AWS_REGION}',
  'rest.signing-name' = 's3',
  'io-impl' = 'org.apache.iceberg.aws.s3.S3FileIO',
  's3.endpoint' = '${LAKEHOUSE_S3_ENDPOINT}',
  's3.path-style-access' = 'true'
);
USE CATALOG lakehouse;
-- The Iceberg sink commits only on a checkpoint, and the interval is read by
-- the client that builds the job, so it is set here, not on the JobManager.
SET 'execution.checkpointing.interval' = '60s';
SQL
exec "$@"
