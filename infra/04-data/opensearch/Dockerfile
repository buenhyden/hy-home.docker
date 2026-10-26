# Reference:
# - https://docs.opensearch.org/latest/install-and-configure/plugins/
# - https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/

ARG OPENSEARCH_BASE_IMAGE=opensearchproject/opensearch:3.8.0
FROM ${OPENSEARCH_BASE_IMAGE}

LABEL version="0.1" description="OpenSearch with custom plugins and secret-based internal users injection"

SHELL ["/bin/bash", "-c"]

# 시스템 경로 수정, 플러그인 설치, entrypoint 복사를 위해 root 사용
USER 0

# Build-time plugin installation
# ordered to leverage cache if plugins don't change
# 필수/유지 플러그인
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch \
  ingest-attachment \
  analysis-nori \
  mapper-annotated-text \
  mapper-murmur3 \
  mapper-size

# The exporter release must equal the OpenSearch base version, or the
# install fails; update both together.
ARG OPENSEARCH_EXPORTER_VERSION=3.8.0.0
RUN /usr/share/opensearch/bin/opensearch-plugin install \
  "https://github.com/opensearch-project/opensearch-prometheus-exporter/releases/download/${OPENSEARCH_EXPORTER_VERSION}/prometheus-exporter-${OPENSEARCH_EXPORTER_VERSION}.zip"


COPY ./opensearch/opensearch-entrypoint.sh /usr/local/bin/opensearch-entrypoint.sh
RUN chmod 755 /usr/local/bin/opensearch-entrypoint.sh

RUN test "$(id -u opensearch)" = "1000" && \
  test "$(id -g opensearch)" = "1000"

USER 1000
