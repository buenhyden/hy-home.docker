FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.3 AS src

FROM alpine:3.24.1

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY --chmod=0555 docker-entrypoint.sh /docker-entrypoint.sh

RUN addgroup -S -g 101 oauth2proxy \
    && adduser -S -D -H -u 100 -s /sbin/nologin -G oauth2proxy oauth2proxy \
    && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER 100:101

ENTRYPOINT ["/docker-entrypoint.sh"]
