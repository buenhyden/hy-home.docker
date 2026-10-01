FROM flink:2.1.3-scala_2.12-java21

# Iceberg Flink runtime, the AWS bundle (S3FileIO and SigV4 for the SeaweedFS
# REST catalog), the Kafka SQL connector and the Hadoop client the Iceberg
# runtime loads its Configuration class from. Pinned by checksum so a rebuild
# cannot fetch other bytes; Maven Central publishes SHA-1 only, and these
# SHA-256 values were computed from files whose SHA-1 matched the published one.
ADD --chmod=0644 --checksum=sha256:39e658d876f253815b4b17c6676bebf6a24d517afe93a21298106d1d7fa97331 \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-2.1/1.11.0/iceberg-flink-runtime-2.1-1.11.0.jar \
    /opt/flink/lib/
ADD --chmod=0644 --checksum=sha256:38f01da7e96850cdd05e6616d758b77b43314b712a8808e3f9a824d56976162f \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.11.0/iceberg-aws-bundle-1.11.0.jar \
    /opt/flink/lib/
ADD --chmod=0644 --checksum=sha256:11cbbcd1163c4fae0d23f9e2c55b4ff57a719a39fe96fc780001cd21a4e5ba15 \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/5.0.0-2.1/flink-sql-connector-kafka-5.0.0-2.1.jar \
    /opt/flink/lib/
ADD --chmod=0644 --checksum=sha256:cc59446ec9ebaceae56fdb8d8c21477766dc5d426325642151c796bec5c4e6b7 \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-api/3.5.0/hadoop-client-api-3.5.0.jar \
    /opt/flink/lib/
ADD --chmod=0644 --checksum=sha256:b7db3e60c5df1cd37c2995b3e0142e57487260706834e5325bbe0a5e683eedf1 \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-runtime/3.5.0/hadoop-client-runtime-3.5.0.jar \
    /opt/flink/lib/
