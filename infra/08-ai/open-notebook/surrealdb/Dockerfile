FROM surrealdb/surrealdb:v3.3.5@sha256:3db515b88e79737aa828c05fbf1515748004ba57495ff89a013851cc3f1ad4b9 AS surreal

FROM debian:bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates bash \
  && rm -rf /var/lib/apt/lists/*

COPY --from=surreal /surreal /usr/local/bin/surreal
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
