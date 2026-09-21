FROM python:3.12-slim-bookworm

ARG DBT_CORE_VERSION=1.11.15
ARG DBT_POSTGRES_VERSION=1.11.0

RUN pip install --no-cache-dir \
    "dbt-core==${DBT_CORE_VERSION}" \
    "dbt-postgres==${DBT_POSTGRES_VERSION}"

WORKDIR /workspace

COPY docker-entrypoint.sh /usr/local/bin/dbt-entrypoint

RUN chmod 0755 /usr/local/bin/dbt-entrypoint

ENTRYPOINT ["/usr/local/bin/dbt-entrypoint"]