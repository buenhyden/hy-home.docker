FROM grafana/loki:3.6.6 AS upstream

FROM alpine:3.21

RUN apk add --no-cache bash busybox wget ca-certificates

COPY --from=upstream /usr/bin/loki /usr/bin/loki
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/loki/loki-config.yaml", "-config.expand-env=true"]
