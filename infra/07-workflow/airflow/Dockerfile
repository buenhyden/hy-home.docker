ARG AIRFLOW_VERSION=3.3.2
ARG PYTHON_VERSION=3.13
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}@sha256:e9982ad3f49a60418622e1baf80c34b0daf3fa5091a336cb5ee61f0cdd189371

ARG AIRFLOW_VERSION=3.3.2
ARG PYTHON_VERSION=3.13
ARG KEYCLOAK_PROVIDER_VERSION=0.11.0
ARG COMMON_COMPAT_PROVIDER_VERSION=1.20.0
ARG CELERY_PROVIDER_VERSION=3.24.1

USER airflow

# Preserve the upstream shell contract explicitly for pipeline failure detection.
SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-o", "nounset", "-o", "nolog", "-c"]

# Public upstream constraints are retained byte-for-byte for review/provenance.
# Three direct providers have an explicit reviewed overlay. Resolve the complete
# dependency set against the other upstream pins, then fail on incompatibility.
COPY --chown=airflow:root infra/07-workflow/airflow/constraints-upstream-3.3.2-python3.13.txt /tmp/constraints-upstream.txt
RUN test "${AIRFLOW_VERSION}" = 3.3.2 && test "${PYTHON_VERSION}" = 3.13 && \
    echo 'afc652180b9f1b94c22fe843cd0ca193ed4993585f3d8d84be1ea564536900b5  /tmp/constraints-upstream.txt' | sha256sum -c - && \
    test "$(grep -c '^apache-airflow-providers-keycloak==' /tmp/constraints-upstream.txt)" = 1 && \
    sed -e "s/^apache-airflow-providers-keycloak==0.10.0$/apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}/" \
      -e "s/^apache-airflow-providers-common-compat==1.19.0$/apache-airflow-providers-common-compat==${COMMON_COMPAT_PROVIDER_VERSION}/" \
      -e "s/^apache-airflow-providers-celery==3.24.0$/apache-airflow-providers-celery==${CELERY_PROVIDER_VERSION}/" \
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

# Install dependencies during image build; runtime pip changes are unsupported.
ENV _PIP_ADDITIONAL_REQUIREMENTS=
