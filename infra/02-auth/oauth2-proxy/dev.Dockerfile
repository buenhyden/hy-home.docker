FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.6@sha256:c3415e8660af553f5e18f5d90db050614c02493c0ac6260ac59442f6d9b12048 AS src

FROM alpine:3.24.3@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY --chmod=0555 docker-entrypoint.dev.sh /docker-entrypoint.sh

RUN addgroup -S oauth2proxy \
    && adduser -S -D -H -s /sbin/nologin -G oauth2proxy oauth2proxy \
  && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER oauth2proxy:oauth2proxy

ENTRYPOINT ["/docker-entrypoint.sh"]
