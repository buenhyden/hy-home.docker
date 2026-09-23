#!/bin/bash
# Write the lakehouse catalog configuration to tmpfs, export the S3 secret
# into this process only, then run the requested Spark command. Every command
# (`spark-sql`, `spark-submit`, `pyspark`) gets the same catalog this way.
set -euo pipefail
secret=/run/secrets/seaweedfs_s3_lakehouse_secret_key
[[ -f "$secret" && ! -L "$secret" ]] || { echo "spark: lakehouse S3 secret missing" >&2; exit 64; }
AWS_SECRET_ACCESS_KEY="$(tr -d '\r\n' <"$secret")"
[[ -n "$AWS_SECRET_ACCESS_KEY" ]] || { echo "spark: lakehouse S3 secret empty" >&2; exit 64; }
export AWS_SECRET_ACCESS_KEY
: "${LAKEHOUSE_CATALOG_URI:?}" "${LAKEHOUSE_S3_ENDPOINT:?}" "${LAKEHOUSE_WAREHOUSE:?}" "${AWS_REGION:?}"

export SPARK_CONF_DIR=/tmp/spark-conf
mkdir -p "$SPARK_CONF_DIR"
cat >"$SPARK_CONF_DIR/spark-defaults.conf" <<CONF
spark.sql.extensions org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalogImplementation in-memory
spark.sql.defaultCatalog lakehouse
spark.sql.catalog.lakehouse org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.lakehouse.type rest
spark.sql.catalog.lakehouse.uri ${LAKEHOUSE_CATALOG_URI}
spark.sql.catalog.lakehouse.warehouse ${LAKEHOUSE_WAREHOUSE}
spark.sql.catalog.lakehouse.rest.auth.type sigv4
spark.sql.catalog.lakehouse.rest.signing-region ${AWS_REGION}
spark.sql.catalog.lakehouse.rest.signing-name s3
spark.sql.catalog.lakehouse.io-impl org.apache.iceberg.aws.s3.S3FileIO
spark.sql.catalog.lakehouse.s3.endpoint ${LAKEHOUSE_S3_ENDPOINT}
spark.sql.catalog.lakehouse.s3.path-style-access true
spark.local.dir /tmp
spark.ui.enabled false
CONF
exec "$@"
