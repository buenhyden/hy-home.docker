FROM grafana/loki:3.6.6 AS upstream

FROM alpine:3.21

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /usr/bin/loki /usr/bin/loki
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/loki/loki-config.yaml", "-config.expand-env=true"]
