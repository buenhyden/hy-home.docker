FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.6@sha256:c3415e8660af553f5e18f5d90db050614c02493c0ac6260ac59442f6d9b12048 AS src

FROM alpine:3.24.4@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY --chmod=0555 docker-entrypoint.sh /docker-entrypoint.sh

RUN addgroup -S -g 101 oauth2proxy \
    && adduser -S -D -H -u 100 -s /sbin/nologin -G oauth2proxy oauth2proxy \
    && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER 100:101

ENTRYPOINT ["/docker-entrypoint.sh"]
