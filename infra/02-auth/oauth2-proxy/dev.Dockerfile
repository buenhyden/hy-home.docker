FROM quay.io/oauth2-proxy/oauth2-proxy:v7.14.2 AS src

FROM alpine:3.22

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY --chmod=0555 docker-entrypoint.dev.sh /docker-entrypoint.sh

RUN addgroup -S oauth2proxy \
    && adduser -S -D -H -s /sbin/nologin -G oauth2proxy oauth2proxy \
  && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER oauth2proxy:oauth2proxy

ENTRYPOINT ["/docker-entrypoint.sh"]
