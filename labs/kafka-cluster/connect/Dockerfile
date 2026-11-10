FROM quay.io/debezium/connect:3.7.0.Final@sha256:b9b983eda59570c526ddffa86ff73e56c53180d2676158ba5a5184cfd1b59a79 AS debezium

FROM confluentinc/cp-kafka-connect:8.3.2@sha256:1bc06f60d7d2958f0030c4f31df7ba66151f5d542455fb84fc785d5f670f81da

USER root

COPY --from=debezium \
    /kafka/connect/debezium-connector-postgres \
    /usr/share/confluent-hub-components/debezium-connector-postgres

USER appuser
