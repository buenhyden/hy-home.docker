#!/bin/bash
# Iceberg table bucket for the REST catalog (SPEC-0180 S12), only under the
# lakehouse profile so the object-bucket job other profiles wait on never
# depends on the S3 Tables API. Admin owns the bucket; the policy grants the
# table identity the catalog and table actions an engine needs, and neither
# policy changes nor bucket deletion. That identity's S3 actions are scoped to
# the same bucket in s3-identities.conf. Every run rewrites the policy.
set -euo pipefail
secret=/run/secrets/seaweedfs_s3_admin_secret_key
[[ -f "$secret" && ! -L "$secret" ]] || { echo "seaweedfs-table-bucket: admin secret missing" >&2; exit 64; }
[[ -n "${AWS_ACCESS_KEY_ID:-}" ]] || { echo "seaweedfs-table-bucket: SEAWEEDFS_S3_ADMIN_ACCESS_KEY unset" >&2; exit 64; }
AWS_SECRET_ACCESS_KEY="$(tr -d '\r\n' <"$secret")"
[[ -n "$AWS_SECRET_ACCESS_KEY" ]] || { echo "seaweedfs-table-bucket: admin secret empty" >&2; exit 64; }
export AWS_SECRET_ACCESS_KEY
s3t() { aws --endpoint-url "$S3_ENDPOINT" s3tables "$@"; }

bucket=lakehouse
identity=lakehouse
arn="$(s3t list-table-buckets --query "tableBuckets[?name=='${bucket}'].arn | [0]" --output text)"
if [[ -z "$arn" || "$arn" == None ]]; then
    arn="$(s3t create-table-bucket --name "$bucket" --query arn --output text)"
    echo "table bucket $bucket created"
else
    echo "table bucket $bucket exists"
fi
actions='"s3tables:GetTableBucket","s3tables:ListNamespaces","s3tables:CreateNamespace","s3tables:GetNamespace","s3tables:DeleteNamespace","s3tables:ListTables","s3tables:CreateTable","s3tables:GetTable","s3tables:UpdateTable","s3tables:DeleteTable"'
s3t put-table-bucket-policy --table-bucket-arn "$arn" --resource-policy \
    "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":{\"AWS\":\"${identity}\"},\"Action\":[${actions}],\"Resource\":[\"$arn\",\"$arn/*\"]}]}"
for namespace in dev test; do
    if s3t get-namespace --table-bucket-arn "$arn" --namespace "$namespace" >/dev/null 2>&1; then
        echo "namespace $namespace exists"
    else
        s3t create-namespace --table-bucket-arn "$arn" --namespace "$namespace" >/dev/null
        echo "namespace $namespace created"
    fi
done
