FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.5@sha256:8498b0d0ef0a7b29686414000a08aee467f02d0299c9ed1e006a8f33fc017916 AS src

FROM alpine:3.24.2

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY --chmod=0555 docker-entrypoint.dev.sh /docker-entrypoint.sh

RUN addgroup -S oauth2proxy \
    && adduser -S -D -H -s /sbin/nologin -G oauth2proxy oauth2proxy \
  && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER oauth2proxy:oauth2proxy

ENTRYPOINT ["/docker-entrypoint.sh"]
