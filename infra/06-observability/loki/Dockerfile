FROM grafana/loki:3.7.10@sha256:b43c257ccfc925d4a50b8717cac61a3b51df8c48d01847936057e5c4075a24a7 AS upstream

FROM alpine:3.24.4@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

RUN apk add --no-cache busybox wget ca-certificates \
    && addgroup -S -g 10001 observability \
    && adduser -S -D -H -u 10001 -G observability observability

COPY --from=upstream /usr/bin/loki /usr/bin/loki
COPY --chmod=0755 docker-entrypoint.sh /docker-entrypoint.sh

USER 10001:10001

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-config.file=/etc/loki/loki-config.yaml", "-config.expand-env=true"]
