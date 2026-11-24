FROM grafana/tempo:3.1.1@sha256:64e2fbd56d9c2b3412a4b430a58ea59e91a670b1e75f920a0c702213ad145044 AS upstream

FROM alpine:3.24.4@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /tempo /usr/bin/tempo
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/tempo.yaml", "-config.expand-env=true"]
