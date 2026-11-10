FROM grafana/tempo:3.1.1@sha256:64e2fbd56d9c2b3412a4b430a58ea59e91a670b1e75f920a0c702213ad145044 AS upstream

FROM alpine:3.24.3@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /tempo /usr/bin/tempo
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/tempo.yaml", "-config.expand-env=true"]
