FROM quay.io/oauth2-proxy/oauth2-proxy:v7.14.2 AS src

# Avoid pulling a new base image in restricted environments by reusing an image
# that's already part of this stack.
FROM valkey/valkey:9.0.2-alpine

COPY --from=src /bin/oauth2-proxy /bin/oauth2-proxy
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
