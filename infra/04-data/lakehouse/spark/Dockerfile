FROM apache/spark:4.1.3-scala2.13-java21-python3-ubuntu

# Iceberg runtime and the AWS bundle (S3FileIO and SigV4 for the SeaweedFS
# REST catalog), pinned by checksum so a rebuild cannot fetch other bytes.
# Maven Central publishes SHA-1 only; these SHA-256 values were computed from
# files whose SHA-1 matched the published one. Update both jars together.
ADD --chmod=0644 --checksum=sha256:d6ea6c5d099288daeb7d5a92061bd3d7d8f296492632b42378e5f2f0e3066242 \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-4.1_2.13/1.11.0/iceberg-spark-runtime-4.1_2.13-1.11.0.jar \
    /opt/spark/jars/
ADD --chmod=0644 --checksum=sha256:38f01da7e96850cdd05e6616d758b77b43314b712a8808e3f9a824d56976162f \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/1.11.0/iceberg-aws-bundle-1.11.0.jar \
    /opt/spark/jars/
