FROM grafana/loki:3.7.9@sha256:0db216b630ae1f348a1584c67f3cead8b4c1fc839169a39501db664744158e28 AS upstream

FROM alpine:3.24.3@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /usr/bin/loki /usr/bin/loki
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/loki/loki-config.yaml", "-config.expand-env=true"]
