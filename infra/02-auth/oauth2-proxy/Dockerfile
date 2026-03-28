FROM quay.io/oauth2-proxy/oauth2-proxy:v7.14.2 AS src

# Avoid pulling a new base image in restricted environments by reusing an image
# that's already part of this stack.
FROM valkey/valkey:9.0.2-alpine

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN addgroup -S oauth2proxy \
    && adduser -S -D -H -s /sbin/nologin -G oauth2proxy oauth2proxy \
    && chmod +x /docker-entrypoint.sh \
    && chown oauth2proxy:oauth2proxy /docker-entrypoint.sh /bin/oauth2-proxy

USER oauth2proxy:oauth2proxy

ENTRYPOINT ["/docker-entrypoint.sh"]
