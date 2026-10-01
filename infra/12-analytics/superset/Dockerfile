FROM apache/superset:6.1.0

# The metadata database driver, Authlib for Keycloak OIDC and the Trino dialect
# for the lakehouse. Pins live in requirements.txt, the file Renovate updates.
USER root
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install --no-cache --python /app/.venv/bin/python -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
USER superset
