#!/bin/sh
# Export the S3 secret key from its Docker secret for -config.expand-env;
# the access key ID arrives as S3_ACCESS_KEY.
set -eu

secret_file="${S3_SECRET_KEY_FILE:?S3_SECRET_KEY_FILE is not set}"
[ -r "$secret_file" ] || {
  echo "missing secret: $secret_file" >&2
  exit 1
}

S3_SECRET_KEY="$(tr -d '\r\n' <"$secret_file")"
[ -n "$S3_SECRET_KEY" ] || {
  echo "empty secret: $secret_file" >&2
  exit 1
}
export S3_SECRET_KEY

exec /usr/bin/tempo "$@"
