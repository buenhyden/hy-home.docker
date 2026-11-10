FROM grafana/loki:3.7.8@sha256:1107dd5274e0ada47e42472b7a7e71f3b2a2fe878878108f3e2f9e51528f0193 AS upstream

FROM alpine:3.24.2@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /usr/bin/loki /usr/bin/loki
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/loki/loki-config.yaml", "-config.expand-env=true"]
