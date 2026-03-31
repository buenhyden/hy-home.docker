# Reference:
# - https://docs.opensearch.org/latest/install-and-configure/plugins/
# - https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/

FROM opensearchproject/opensearch:3.5.0

LABEL version="0.1" description="OpenSearch 3.5 with custom plugins and secret-based internal users injection"

SHELL ["/bin/bash", "-c"]

# 시스템 경로 수정, 플러그인 설치, entrypoint 복사를 위해 root 사용
USER root

# Build-time plugin installation
# ordered to leverage cache if plugins don't change
# 필수/유지 플러그인
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch \
  ingest-attachment \
  analysis-nori \
  mapper-annotated-text \
  mapper-murmur3 \
  mapper-size

RUN /usr/share/opensearch/bin/opensearch-plugin install \
  https://github.com/opensearch-project/opensearch-prometheus-exporter/releases/download/3.5.0.0/prometheus-exporter-3.5.0.0.zip


COPY ./opensearch/opensearch-entrypoint.sh /usr/local/bin/opensearch-entrypoint.sh
RUN chmod 755 /usr/local/bin/opensearch-entrypoint.sh

USER opensearch
