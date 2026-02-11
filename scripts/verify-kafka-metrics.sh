#!/usr/bin/env bash
set -euo pipefail

PROM_CONTAINER="${PROM_CONTAINER:-infra-prometheus}"
QUERY_URL='http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22kafka%22%7D'

response="$(docker exec "${PROM_CONTAINER}" wget -qO- "${QUERY_URL}")"

if ! echo "${response}" | grep -q '"job":"kafka"'; then
  echo "Kafka JMX metrics not found in Prometheus (job=\"kafka\")." >&2
  echo "Response: ${response}" >&2
  exit 1
fi

echo "Kafka JMX metrics are present in Prometheus (job=\"kafka\")."
