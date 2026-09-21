#!/bin/bash
# MLflow artifact store provisioning on MinIO (feature-owned).
#
# Creates the MLflow bucket and a dedicated MinIO identity whose policy covers
# only that bucket, so the tracking server never holds the shared application
# credential that can read every bucket. Credentials reach mc through stdin,
# never argv. Every input is validated before the first MinIO call.
set -euo pipefail

fail() {
  printf 'mlflow-artifacts: %s\n' "$1" >&2
  exit 64
}

read_secret() {
  [ -f "$1" ] && [ ! -L "$1" ] || fail "secret is not a regular file: $1"
  local value
  value="$(cat "$1")"
  [ -n "$value" ] || fail "secret is empty: $1"
  case "$value" in
    *$'\r'* | *$'\n'* | *'"'* | *'\'*) fail "secret contains a line break, quote or backslash: $1" ;;
  esac
  [ "${#value}" -le 512 ] || fail "secret exceeds 512 characters: $1"
  printf '%s' "$value"
}

bucket="${MLFLOW_ARTIFACT_BUCKET:-}"
user="${MLFLOW_S3_USER:-}"
policy="${bucket}-rw"
[[ "$bucket" =~ ^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$ ]] || fail "MLFLOW_ARTIFACT_BUCKET is not a valid bucket name"
[[ "$user" =~ ^[A-Za-z0-9._-]{3,64}$ ]] || fail "MLFLOW_S3_USER must match ^[A-Za-z0-9._-]{3,64}$"
[[ "${MINIO_ENDPOINT:-}" =~ ^https?://[A-Za-z0-9.-]+(:[0-9]+)?$ ]] || fail "MINIO_ENDPOINT is not an http(s) origin"

root_user="$(read_secret /run/secrets/minio_root_username)"
root_pass="$(read_secret /run/secrets/minio_root_password)"
user_pass="$(read_secret /run/secrets/mlflow_s3_password)"
[ "${#user_pass}" -ge 8 ] || fail "mlflow_s3_password must be at least 8 characters"

export MC_CONFIG_DIR=/tmp/.mc
printf '{"url":"%s","accessKey":"%s","secretKey":"%s","api":"s3v4","path":"auto"}' \
  "$MINIO_ENDPOINT" "$root_user" "$root_pass" | mc alias import root >/dev/null

mc mb --ignore-existing "root/${bucket}"

# Read/write objects in this bucket only; no bucket administration.
mc admin policy create root "$policy" /dev/stdin >/dev/null <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetBucketLocation", "s3:ListBucket", "s3:ListBucketMultipartUploads"],
      "Resource": ["arn:aws:s3:::${bucket}"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"],
      "Resource": ["arn:aws:s3:::${bucket}/*"]
    }
  ]
}
POLICY

# Adding an existing user updates its secret, so this also applies rotation.
printf '%s\n%s\n' "$user" "$user_pass" | mc admin user add root >/dev/null
mc admin policy attach root "$policy" --user "$user" >/dev/null
printf 'mlflow-artifacts: bucket=%s user=%s policy=%s ready\n' "$bucket" "$user" "$policy"
