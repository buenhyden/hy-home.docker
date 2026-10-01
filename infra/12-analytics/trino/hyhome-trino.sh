#!/bin/bash
# Export the lakehouse S3 secret into this process only; the catalog file
# reads it with ${ENV:...}. Then start the requested Trino command.
set -euo pipefail
secret=/run/secrets/seaweedfs_s3_lakehouse_secret_key
[[ -f "$secret" && ! -L "$secret" ]] || { echo "trino: lakehouse S3 secret missing" >&2; exit 64; }
AWS_SECRET_ACCESS_KEY="$(tr -d '\r\n' <"$secret")"
[[ -n "$AWS_SECRET_ACCESS_KEY" ]] || { echo "trino: lakehouse S3 secret empty" >&2; exit 64; }
export AWS_SECRET_ACCESS_KEY
: "${LAKEHOUSE_CATALOG_URI:?}" "${LAKEHOUSE_S3_ENDPOINT:?}" "${AWS_REGION:?}" "${AWS_ACCESS_KEY_ID:?}"
exec "$@"
