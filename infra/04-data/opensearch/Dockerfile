# Reference: https://docs.opensearch.org/1.0/opensearch/install/docker/#working-with-plugins

FROM opensearchproject/opensearch:3.4.0

LABEL version="0.1" description="OpenSearch with custom plugins"

SHELL ["/bin/bash", "-c"]

# Build-time plugin installation
# ordered to leverage cache if plugins don't change
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch ingest-attachment analysis-nori mapper-annotated-text mapper-murmur3 mapper-size repository-azure discovery-azure-classic
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch https://github.com/opensearch-project/opensearch-prometheus-exporter/releases/download/3.4.0.0/prometheus-exporter-3.4.0.0.zip

