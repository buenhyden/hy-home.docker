FROM grafana/tempo:2.10.1 AS upstream

FROM alpine:3.21

RUN apk add --no-cache bash busybox wget ca-certificates

COPY --from=upstream /tempo /usr/bin/tempo
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/tempo.yaml", "-config.expand-env=true"]
