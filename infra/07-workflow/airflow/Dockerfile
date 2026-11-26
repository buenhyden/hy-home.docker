ARG AIRFLOW_VERSION=3.4.0
ARG PYTHON_VERSION=3.13
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}@sha256:a8d9d19c563c768b2bc605ef26440f28a9164ea886064e99c599b057432ff572

ARG AIRFLOW_VERSION=3.4.0
ARG PYTHON_VERSION=3.13
ARG KEYCLOAK_PROVIDER_VERSION=0.13.0
ARG COMMON_COMPAT_PROVIDER_VERSION=1.23.1
ARG CELERY_PROVIDER_VERSION=3.26.0

USER airflow

# Preserve the upstream shell contract explicitly for pipeline failure detection.
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "nounset", "-o", "nolog", "-c"]

# Public upstream constraints are retained byte-for-byte for review/provenance.
# Three direct providers have an explicit reviewed overlay. Resolve the complete
# dependency set against the other upstream pins, then fail on incompatibility.
COPY --chown=airflow:root infra/07-workflow/airflow/constraints-upstream-3.4.0-python3.13.txt /tmp/constraints-upstream.txt
RUN test "${AIRFLOW_VERSION}" = 3.4.0 && test "${PYTHON_VERSION}" = 3.13 && \
    echo '698d3d1ffc27385c8b69c511bed71123d126bddad66dcad054ef0bcc3398e12c  /tmp/constraints-upstream.txt' | sha256sum -c - && \
    test "$(grep -c '^apache-airflow-providers-keycloak==' /tmp/constraints-upstream.txt)" = 1 && \
    sed -e "s/^apache-airflow-providers-keycloak==0.11.2$/apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}/" \
      -e "s/^apache-airflow-providers-common-compat==1.23.0$/apache-airflow-providers-common-compat==${COMMON_COMPAT_PROVIDER_VERSION}/" \
      -e "s/^apache-airflow-providers-celery==3.26.0$/apache-airflow-providers-celery==${CELERY_PROVIDER_VERSION}/" \
      /tmp/constraints-upstream.txt > /tmp/constraints-reviewed.txt && \
    pip install --no-cache-dir \
      "apache-airflow==${AIRFLOW_VERSION}" \
      "apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}" \
      "apache-airflow-providers-common-compat==${COMMON_COMPAT_PROVIDER_VERSION}" \
      "apache-airflow-providers-celery==${CELERY_PROVIDER_VERSION}" \
      --constraint /tmp/constraints-reviewed.txt && \
    pip check && \
    python -c 'import sys; from importlib.metadata import version; assert sys.version_info[:2] == tuple(map(int, sys.argv[1].split("."))); assert version("apache-airflow") == sys.argv[2]; assert version("apache-airflow-providers-keycloak") == sys.argv[3]; assert version("apache-airflow-providers-common-compat") == sys.argv[4]; assert version("apache-airflow-providers-celery") == sys.argv[5]' \
      "${PYTHON_VERSION}" "${AIRFLOW_VERSION}" "${KEYCLOAK_PROVIDER_VERSION}" "${COMMON_COMPAT_PROVIDER_VERSION}" "${CELERY_PROVIDER_VERSION}"

# The supported _CMD readers call this read-only, dependency-free URI renderer.
# BuildKit gives the created bin directory the same mode, so it must be searchable.
COPY --chown=0:0 --chmod=0555 infra/07-workflow/airflow/connection_uri.py /opt/airflow/bin/connection_uri.py

# Install dependencies during image build; runtime pip changes are unsupported.
ENV _PIP_ADDITIONAL_REQUIREMENTS=
