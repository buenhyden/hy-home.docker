ARG AIRFLOW_VERSION=3.3.1

FROM apache/airflow:${AIRFLOW_VERSION}

ARG AIRFLOW_VERSION=3.3.1
ARG PYTHON_VERSION=3.13
ARG KEYCLOAK_PROVIDER_VERSION=0.8.2

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}" \
    --constraint \
    "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"