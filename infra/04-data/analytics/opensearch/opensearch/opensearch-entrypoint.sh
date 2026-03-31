#!/usr/bin/env bash
set -euo pipefail

OS_HOME="/usr/share/opensearch"
CONFIG_DIR="${OS_HOME}/config"
SEC_DIR="${CONFIG_DIR}/opensearch-security"
TOOLS_DIR="${OS_HOME}/plugins/opensearch-security/tools"

ADMIN_SECRET_FILE="/run/secrets/opensearch_admin_password"
DASH_SECRET_FILE="/run/secrets/opensearch_dashboard_password"
EXPORTER_SECRET_FILE="/run/secrets/opensearch_exporter_password"

TEMPLATE_FILE="${SEC_DIR}/internal_users.template.yml"
TARGET_FILE="${SEC_DIR}/internal_users.yml"

read_secret() {
  local file="$1"
  [[ -f "${file}" ]] || { echo "Missing secret file: ${file}" >&2; exit 1; }
  tr -d '\r\n' < "${file}"
}

hash_password() {
  local plain="$1"
  "${TOOLS_DIR}/hash.sh" -p "${plain}" | tail -n 1
}

harden_file_if_writable() {
  local path="$1"
  local mode="$2"
  if [[ -e "${path}" && -w "${path}" ]]; then
    chmod "${mode}" "${path}" || true
  fi
}

harden_dir_if_writable() {
  local path="$1"
  local mode="$2"
  if [[ -d "${path}" && -w "${path}" ]]; then
    chmod "${mode}" "${path}" || true
  fi
}

ADMIN_PASSWORD="$(read_secret "${ADMIN_SECRET_FILE}")"
KIBANASERVER_PASSWORD="$(read_secret "${DASH_SECRET_FILE}")"
EXPORTER_PASSWORD="$(read_secret "${EXPORTER_SECRET_FILE}")"

export OPENSEARCH_INITIAL_ADMIN_PASSWORD="${ADMIN_PASSWORD}"

ADMIN_HASH="$(hash_password "${ADMIN_PASSWORD}")"
KIBANASERVER_HASH="$(hash_password "${KIBANASERVER_PASSWORD}")"
EXPORTER_HASH="$(hash_password "${EXPORTER_PASSWORD}")"

[[ -f "${TEMPLATE_FILE}" ]] || { echo "Missing template file: ${TEMPLATE_FILE}" >&2; exit 1; }
[[ -d "${SEC_DIR}" ]] || { echo "Missing security dir: ${SEC_DIR}" >&2; exit 1; }
[[ -w "${SEC_DIR}" ]] || { echo "Security dir is not writable: ${SEC_DIR}" >&2; exit 1; }

tmp_file="$(mktemp "${SEC_DIR}/internal_users.yml.tmp.XXXXXX")"

sed \
  -e "s|__ADMIN_HASH__|${ADMIN_HASH}|g" \
  -e "s|__KIBANASERVER_HASH__|${KIBANASERVER_HASH}|g" \
  -e "s|__EXPORTER_HASH__|${EXPORTER_HASH}|g" \
  "${TEMPLATE_FILE}" > "${tmp_file}"

mv "${tmp_file}" "${TARGET_FILE}"

# 권한 hardening
harden_dir_if_writable "${CONFIG_DIR}" 700
harden_dir_if_writable "${SEC_DIR}" 700
harden_dir_if_writable "${CONFIG_DIR}/certs" 700

find "${SEC_DIR}" -maxdepth 1 -type f -name "*.yml" -writable -exec chmod 600 {} \; 2>/dev/null || true
find "${CONFIG_DIR}/certs" -maxdepth 1 -type f -writable -exec chmod 600 {} \; 2>/dev/null || true

harden_file_if_writable "${CONFIG_DIR}/opensearch.yml" 600
harden_file_if_writable "${CONFIG_DIR}/userdict_ko.txt" 600
harden_file_if_writable "${TARGET_FILE}" 600

exec /usr/share/opensearch/opensearch-docker-entrypoint.sh
