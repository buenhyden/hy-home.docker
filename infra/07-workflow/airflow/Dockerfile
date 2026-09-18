ARG AIRFLOW_VERSION=3.3.1

FROM apache/airflow:${AIRFLOW_VERSION}

ARG AIRFLOW_VERSION=3.3.1
ARG PYTHON_VERSION=3.13

USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    "apache-airflow-providers-keycloak==0.8.0" \
    --constraint \
    "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"