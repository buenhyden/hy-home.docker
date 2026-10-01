FROM python:3.12-slim-bookworm

# dbt debug checks for git and dbt deps needs it for git packages.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Pins live in requirements.txt, the single file Renovate updates.
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /workspace

COPY docker-entrypoint.sh /usr/local/bin/dbt-entrypoint

RUN chmod 0755 /usr/local/bin/dbt-entrypoint

ENTRYPOINT ["/usr/local/bin/dbt-entrypoint"]
