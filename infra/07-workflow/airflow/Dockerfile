ARG AIRFLOW_VERSION=3.3.1
FROM apache/airflow:${AIRFLOW_VERSION}

ARG AIRFLOW_VERSION=3.3.1
ARG PYTHON_VERSION=3.13
ARG KEYCLOAK_PROVIDER_VERSION=0.9.0

USER airflow

# 3.3.1 constraints에 맞는 provider 의존성 설치
RUN pip install --no-cache-dir \
    "apache-airflow-providers-common-compat>=1.18.0" \
    "python-keycloak>=5.0.0" \
    --constraint \
    "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# constraints의 keycloak-provider=0.8.2 pin만 우회
RUN pip install --no-cache-dir --no-deps \
    "apache-airflow-providers-keycloak==${KEYCLOAK_PROVIDER_VERSION}"