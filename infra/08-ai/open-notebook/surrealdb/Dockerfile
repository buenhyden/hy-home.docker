FROM surrealdb/surrealdb:v2.7.0@sha256:e5d7387e3727bbe2f7cd6d869e48cd34777272258572ead37c9656b25f745723 AS surreal

FROM debian:bookworm-slim@sha256:e67eeead736ff7bbe258ef088bff683635c561b1fcfefad0806c1df4ab49ce0e

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates bash \
  && rm -rf /var/lib/apt/lists/*

COPY --from=surreal /surreal /usr/local/bin/surreal
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
