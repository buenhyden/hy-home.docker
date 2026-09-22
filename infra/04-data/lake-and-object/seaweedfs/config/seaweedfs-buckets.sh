#!/bin/bash
# Create the consumer buckets once; existing buckets are left untouched.
set -euo pipefail
secret=/run/secrets/seaweedfs_s3_admin_secret_key
[[ -f "$secret" && ! -L "$secret" ]] || { echo "seaweedfs-buckets: admin secret missing" >&2; exit 64; }
[[ -n "${AWS_ACCESS_KEY_ID:-}" ]] || { echo "seaweedfs-buckets: SEAWEEDFS_S3_ADMIN_ACCESS_KEY unset" >&2; exit 64; }
AWS_SECRET_ACCESS_KEY="$(tr -d '\r\n' <"$secret")"
export AWS_SECRET_ACCESS_KEY
for bucket in ${BUCKETS:?}; do
    if aws --endpoint-url "$S3_ENDPOINT" s3api head-bucket --bucket "$bucket" >/dev/null 2>&1; then
        echo "bucket $bucket exists"
    else
        aws --endpoint-url "$S3_ENDPOINT" s3api create-bucket --bucket "$bucket" >/dev/null
        echo "bucket $bucket created"
    fi
done
