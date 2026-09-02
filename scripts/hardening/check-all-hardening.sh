#!/usr/bin/env bash
# Unified Infrastructure Hardening Verification Script
# Consolidates checks for all 11 tiers into a single execution and report.

set -euo pipefail

_verified_repository_root() {
  local entrypoint direct_root candidate direct_identity candidate_identity
  entrypoint="$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || true)"
  if [[ -z "$entrypoint" || ! -f "$entrypoint" ]] ||
    ! direct_root="$(cd "$(dirname "$entrypoint")/../.." && pwd -P)"; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  if [[ -z "${HYHOME_CI_GATE_ROOT+x}" ]]; then
    printf '%s\n' "$direct_root"
    return 0
  fi
  candidate="$HYHOME_CI_GATE_ROOT"
  if [[ ! "$candidate" =~ ^/proc/self/fd/(0|[1-9][0-9]*)$ ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  direct_identity="$(stat -Lc '%d:%i' -- "$direct_root" 2>/dev/null || true)"
  candidate_identity="$(stat -Lc '%d:%i' -- "$candidate" 2>/dev/null || true)"
  if [[ -z "$direct_identity" || "$candidate_identity" != "$direct_identity" || ! -d "$candidate" ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  printf '%s\n' "$candidate"
}

# Source the library. The typed gate runner supplies a verified descriptor
# root; direct execution retains the script-relative fallback.
REPO_ROOT="$(_verified_repository_root)"
SCRIPT_DIR="${REPO_ROOT}/scripts/hardening"
LIB_PATH="${SCRIPT_DIR}/../lib/hardening-lib.sh"
TECH_STACK_REGISTRY="${REPO_ROOT}/infra/tech-stack.versions.json"

if [[ ! -f "$LIB_PATH" ]]; then
  echo "Error: Hardening library not found at $LIB_PATH"
  exit 1
fi

# shellcheck source=../lib/hardening-lib.sh
source "$LIB_PATH"

registry_component_image() {
  local component="$1"

  python3 - "$TECH_STACK_REGISTRY" "$component" <<'PY'
import json
import pathlib
import sys

registry_path = pathlib.Path(sys.argv[1])
component = sys.argv[2]
registry = json.loads(registry_path.read_text(encoding="utf-8"))
matches = [
    entry
    for entry in registry.get("entries", [])
    if entry.get("component") == component
]
if len(matches) != 1:
    raise SystemExit(
        f"FAIL: expected exactly one {component} entry in {registry_path}"
    )
images = matches[0].get("images")
if not isinstance(images, list) or len(images) != 1 or not isinstance(images[0], str):
    raise SystemExit(
        f"FAIL: expected exactly one {component} image in {registry_path}"
    )
print(images[0])
PY
}

compose_service_image() {
  local compose_file="$1"
  local service="$2"

  python3 - "$compose_file" "$service" <<'PY'
import os
import re
import stat
import sys

MAX_COMPOSE_BYTES = 1024 * 1024
FAILURE = "FAIL: invalid compose service image contract"
SERVICE_NAME_RE = re.compile(r"[A-Za-z0-9_.-]+\Z")
SERVICE_KEY_RE = re.compile(
    r"""^  (?:(?P<plain>[A-Za-z0-9_.-]+)|"""
    r"""'(?P<single>[A-Za-z0-9_.-]+)'|"""
    r'''"(?P<double>[A-Za-z0-9_.-]+)")[ \t]*:[ \t]*(?:#.*)?$'''
)
IMAGE_RE = re.compile(
    r"(?=.{1,255}\Z)"
    r"(?:[a-z0-9]+(?:[._-][a-z0-9]+)*(?::[0-9]{1,5})?/)*"
    r"[a-z0-9]+(?:[._-][a-z0-9]+)*"
    r"(?::[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}|@sha256:[0-9a-f]{64})?"
    r"\Z"
)


def reject() -> None:
    print(FAILURE, file=sys.stderr)
    raise SystemExit(2)


def service_key(line):
    if not line.strip() or line.lstrip().startswith("#"):
        return None
    if line.startswith("    "):
        return None
    if not line.startswith("  "):
        reject()
    match = SERVICE_KEY_RE.fullmatch(line)
    if match is None:
        reject()
    return next(value for value in match.groupdict().values() if value is not None)


compose_path = sys.argv[1]
service = sys.argv[2]
if not SERVICE_NAME_RE.fullmatch(service):
    reject()

flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK
try:
    descriptor = os.open(compose_path, flags)
except OSError:
    reject()

try:
    metadata = os.fstat(descriptor)
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_COMPOSE_BYTES:
        reject()
    payload = bytearray()
    while len(payload) <= MAX_COMPOSE_BYTES:
        chunk = os.read(
            descriptor,
            min(65536, MAX_COMPOSE_BYTES + 1 - len(payload)),
        )
        if not chunk:
            break
        payload.extend(chunk)
    if len(payload) > MAX_COMPOSE_BYTES or b"\0" in payload:
        reject()
finally:
    os.close(descriptor)

try:
    lines = bytes(payload).decode("utf-8").splitlines()
except UnicodeDecodeError:
    reject()

top_level_services_re = re.compile(
    r"""^(?:services|'services'|"services")[ \t]*:"""
)
exact_services_re = re.compile(r"^services:[ \t]*(?:#.*)?$")
services_keys = [
    index
    for index, line in enumerate(lines)
    if top_level_services_re.match(line)
]
if len(services_keys) != 1:
    reject()
services_index = services_keys[0]
if not exact_services_re.fullmatch(lines[services_index]):
    reject()

services_end = len(lines)
for index in range(services_index + 1, len(lines)):
    line = lines[index]
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if not line.startswith(" "):
        services_end = index
        break

service_keys = [
    (index, key)
    for index in range(services_index + 1, services_end)
    if (key := service_key(lines[index])) is not None
]
service_names = [key for _index, key in service_keys]
if len(service_names) != len(set(service_names)):
    reject()
target_keys = [index for index, key in service_keys if key == service]
if len(target_keys) != 1:
    reject()
target_index = target_keys[0]

target_end = services_end
for index, _key in service_keys:
    if index > target_index:
        target_end = index
        break

image_key_re = re.compile(r"""^    (?:image|'image'|"image")[ \t]*:""")
exact_image_re = re.compile(r"^    image:(.*)$")
image_keys = [
    index
    for index in range(target_index + 1, target_end)
    if image_key_re.match(lines[index])
]
if len(image_keys) != 1:
    reject()
image_match = exact_image_re.fullmatch(lines[image_keys[0]])
if image_match is None:
    reject()

scalar = image_match.group(1).lstrip(" ")
if not scalar or scalar.startswith("#"):
    reject()
quoted = scalar[0] in {"'", '"'}
if quoted:
    quote = scalar[0]
    closing_index = scalar.find(quote, 1)
    if closing_index == -1:
        reject()
    image = scalar[1:closing_index]
    trailer = scalar[closing_index + 1 :]
    if not re.fullmatch(r"[ \t]*(?:#.*)?", trailer):
        reject()
else:
    scalar_match = re.fullmatch(r"([^ \t#]+)[ \t]*(?:#.*)?", scalar)
    if scalar_match is None:
        reject()
    image = scalar_match.group(1)
    if (
        image.lower() in {"null", "true", "false"}
        or image == "~"
        or re.fullmatch(
            r"[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)",
            image,
        )
    ):
        reject()

if not IMAGE_RE.fullmatch(image):
    reject()
print(image)
PY
}

resolve_compose_service_image_cli() {
  if [[ "$#" -ne 2 ]]; then
    echo "FAIL: invalid compose service image contract" >&2
    return 2
  fi
  compose_service_image "$1" "$2"
}

usage() {
  cat <<'EOF'
Usage: bash scripts/hardening/check-all-hardening.sh [TIER...]

Run infrastructure hardening checks.

Without arguments, all supported tiers are checked. With arguments, only the
requested tiers are checked.

Supported tiers:
  01-gateway, 02-auth, 03-security, 04-data, 05-messaging,
  06-observability, 07-workflow, 08-ai, 09-tooling,
  10-communication, 11-laboratory
EOF
}

# --- Tier 01: Gateway ---
check_01_gateway() {
  local tier="01-gateway"
  start_tier "$tier"

  local traefik_compose="infra/01-gateway/traefik/docker-compose.yml"
  local traefik_middleware="infra/01-gateway/traefik/dynamic/middleware.yml"
  local nginx_compose="infra/01-gateway/nginx/docker-compose.yml"
  local nginx_conf="infra/01-gateway/nginx/config/nginx.conf"

  check_file "$traefik_compose"
  check_file "$traefik_middleware"
  check_file "$nginx_compose"
  check_file "$nginx_conf"

  check_contains "$traefik_compose" "service: template-infra-readonly-med" "traefik compose template mismatch"
  check_contains "$traefik_compose" "traefik.http.routers.dashboard.middlewares: dashboard-auth@file,gateway-standard-chain@file" "traefik dashboard middleware chain mismatch"
  check_contains "$traefik_middleware" "gateway-standard-chain:" "missing gateway-standard-chain"
  check_contains "$traefik_middleware" "average: 100 # requests per second" "gateway rate limit average mismatch"
  check_contains "$traefik_middleware" "burst: 50" "gateway rate limit burst mismatch"
  check_contains "$nginx_compose" "service: template-infra-readonly-low" "nginx compose template mismatch"
  check_contains "$nginx_conf" "server_tokens off;" "nginx server_tokens off missing"
}

# --- Tier 02: Auth ---
check_02_auth() {
  local tier="02-auth"
  start_tier "$tier"

  local keycloak_compose="infra/02-auth/keycloak/docker-compose.yml"
  local oauth_dev_compose="infra/02-auth/oauth2-proxy/docker-compose.dev.yml"
  local oauth_full_compose="infra/02-auth/oauth2-proxy/docker-compose.yml"
  local oauth_dockerfile="infra/02-auth/oauth2-proxy/Dockerfile"
  local oauth_dev_dockerfile="infra/02-auth/oauth2-proxy/dev.Dockerfile"
  local oauth_entrypoint="infra/02-auth/oauth2-proxy/docker-entrypoint.sh"
  local oauth_dev_entrypoint="infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh"
  local oauth_cfg="infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg"
  local keycloak_image
  local keycloak_compose_image

  check_file "$TECH_STACK_REGISTRY"
  check_file "$keycloak_compose"
  check_file "$oauth_dev_compose"
  check_file "$oauth_full_compose"
  check_file "$oauth_dockerfile"
  check_file "$oauth_dev_dockerfile"
  check_file "$oauth_entrypoint"
  check_file "$oauth_dev_entrypoint"
  check_file "$oauth_cfg"
  keycloak_image="$(registry_component_image "Keycloak")"
  keycloak_compose_image="$(compose_service_image "$keycloak_compose" "keycloak")"

  check_contains "$keycloak_compose" "service: template-infra-high" "keycloak compose template mismatch"
  if [[ "$keycloak_compose_image" != "$keycloak_image" ]]; then
    fail "keycloak image tag mismatch"
  fi
  check_contains "$keycloak_compose" "KC_DB_PASSWORD_FILE: /run/secrets/keycloak_db_password" "keycloak db password secret file missing"
  check_contains "$keycloak_compose" "/run/secrets/keycloak_admin_password" "keycloak admin secret injection mismatch"
  check_contains "$keycloak_compose" "/run/secrets/keycloak_db_password" "keycloak db secret injection mismatch"
  check_contains "$keycloak_compose" "traefik.http.routers.keycloak.middlewares: gateway-standard-chain@file" "keycloak gateway chain mismatch"
  check_contains "$keycloak_compose" "ipv4_address: 172.19.0.3" "keycloak infra_net IP mismatch"

  check_contains "$oauth_dev_compose" "service: template-infra-readonly-med" "root-active oauth2-proxy compose template mismatch"
  check_contains "$oauth_dev_compose" "dockerfile: dev.Dockerfile" "root-active oauth2-proxy must build dev Dockerfile"
  check_contains "$oauth_dev_compose" "OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://mng-valkey:6379" "root-active oauth2-proxy session store mismatch"
  check_contains "$oauth_dev_compose" "- mng_valkey_password" "root-active oauth2-proxy mng valkey secret missing"
  check_contains "$oauth_dev_compose" "traefik.http.routers.oauth2-proxy.middlewares: gateway-standard-chain@file" "root-active oauth2-proxy gateway chain mismatch"
  check_contains "$oauth_dev_compose" "ipv4_address: 172.19.0.4" "root-active oauth2-proxy infra_net IP mismatch"
  check_not_contains "$oauth_dev_compose" "v7.14.2" "root-active oauth2-proxy stale image reference"

  check_contains "$oauth_full_compose" "service: template-infra-readonly-med" "local/full oauth2-proxy compose template mismatch"
  check_contains "$oauth_full_compose" "dockerfile: Dockerfile" "local/full oauth2-proxy must build production Dockerfile"
  check_contains "$oauth_full_compose" "OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://oauth2-proxy-valkey:6379" "local/full oauth2-proxy session store mismatch"
  check_contains "$oauth_full_compose" "- oauth2_valkey_password" "local/full oauth2-proxy valkey secret missing"
  check_contains "$oauth_full_compose" "image: valkey/valkey:9.1.0-alpine" "oauth2-proxy valkey image tag mismatch"
  check_contains "$oauth_full_compose" "image: oliver006/redis_exporter:v1.86.0-alpine" "oauth2-proxy valkey exporter image tag mismatch"
  check_contains "$oauth_full_compose" "ipv4_address: 172.19.0.4" "local/full oauth2-proxy infra_net IP mismatch"
  check_contains "$oauth_full_compose" "ipv4_address: 172.19.0.5" "oauth2-proxy valkey infra_net IP mismatch"
  check_contains "$oauth_full_compose" "ipv4_address: 172.19.0.6" "oauth2-proxy valkey exporter infra_net IP mismatch"
  check_not_contains "$oauth_full_compose" "v7.14.2" "local/full oauth2-proxy stale image reference"

  check_contains "$oauth_dockerfile" "FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.3 AS src" "oauth2-proxy source image tag mismatch"
  check_contains "$oauth_dev_dockerfile" "FROM quay.io/oauth2-proxy/oauth2-proxy:v7.15.3 AS src" "oauth2-proxy dev source image tag mismatch"
  check_contains "$oauth_dockerfile" "USER oauth2proxy:oauth2proxy" "oauth2-proxy non-root user missing"
  check_contains "$oauth_dev_dockerfile" "USER oauth2proxy:oauth2proxy" "oauth2-proxy dev non-root user missing"
  check_contains "$oauth_entrypoint" "/run/secrets/oauth2_valkey_password" "oauth2-proxy local/full valkey secret injection mismatch"
  check_contains "$oauth_dev_entrypoint" "/run/secrets/mng_valkey_password" "oauth2-proxy root-active valkey secret injection mismatch"
  check_contains "$oauth_entrypoint" "set -- --config /etc/oauth2-proxy.cfg" "oauth2-proxy default config argument missing"
  check_contains "$oauth_dev_entrypoint" "set -- --config /etc/oauth2-proxy.cfg" "oauth2-proxy dev default config argument missing"

  check_contains "$oauth_cfg" "cookie_secure = true" "oauth2-proxy cookie_secure missing"
  check_contains "$oauth_cfg" "cookie_httponly = true" "oauth2-proxy cookie_httponly missing"
  check_contains "$oauth_cfg" "cookie_samesite = \"lax\"" "oauth2-proxy cookie_samesite mismatch"
  check_contains "$oauth_cfg" "client_secret_file = \"/run/secrets/oauth2_proxy_client_secret\"" "oauth2-proxy client secret file missing"
  check_contains "$oauth_cfg" "cookie_secret_file = \"/run/secrets/oauth2_proxy_cookie_secret\"" "oauth2-proxy cookie secret file missing"

  check_service_healthcheck "$keycloak_compose" "keycloak"
  check_service_healthcheck "$oauth_dev_compose" "oauth2-proxy"
  check_service_healthcheck "$oauth_full_compose" "oauth2-proxy"
  check_service_healthcheck "$oauth_full_compose" "oauth2-proxy-valkey"
}

# --- Tier 03: Security ---
check_03_security() {
  local tier="03-security"
  start_tier "$tier"

  local compose_file="infra/03-security/vault/docker-compose.yml"
  local vault_hcl="infra/03-security/vault/config/vault.hcl"
  local agent_hcl="infra/03-security/vault/config/vault-agent.hcl"
  local templates_dir="infra/03-security/vault/config/templates"
  local spec_file="docs/03.specs/003-security/spec.md"

  check_file "$compose_file"
  check_file "$vault_hcl"
  check_file "$agent_hcl"
  check_file "$spec_file"

  check_contains "$compose_file" "service: template-stateful-med" "vault compose template inheritance missing"
  check_contains "$compose_file" "image: hashicorp/vault:2.0.3" "vault image tag mismatch"
  check_contains "$compose_file" "vault-agent:" "vault-agent service missing"
  check_contains "$compose_file" "vault-agent-out:" "vault-agent output volume missing"
  check_contains "$compose_file" "vault-agent-out:/vault/out" "vault-agent output mount missing"
  check_contains "$compose_file" "traefik.http.routers.vault.middlewares: gateway-standard-chain@file" "vault gateway chain mismatch"
  check_contains "$compose_file" "k3d-hyhome:" "vault k3d-hyhome network missing"
  check_contains "$compose_file" "ipv4_address: 172.18.0.8" "vault k3d-hyhome IP mismatch"
  check_contains "$compose_file" "ipv4_address: 172.19.0.9" "vault infra_net IP mismatch"
  check_contains "$compose_file" "ipv4_address: 172.19.0.10" "vault-agent infra_net IP mismatch"
  check_contains "$vault_hcl" "storage \"raft\"" "vault raft storage missing"
  check_contains "$vault_hcl" "disable_mlock = true" "vault mlock runtime contract mismatch"
  check_contains "$vault_hcl" "tls_disable = 1" "vault internal HTTP listener mismatch"
  check_contains "$vault_hcl" "prometheus_retention_time = \"30s\"" "vault telemetry retention mismatch"
  check_contains "$agent_hcl" "role_id_file_path" "vault-agent AppRole role_id path missing"
  check_contains "$agent_hcl" "secret_id_file_path" "vault-agent AppRole secret_id path missing"
  check_contains "$agent_hcl" "destination = \"/vault/out" "vault-agent output destination missing"
  check_contains "$agent_hcl" "static_secret_render_interval = \"5m\"" "vault-agent static secret render interval mismatch"
  check_not_contains "$agent_hcl" "secret/data/example" "vault-agent placeholder secret path"
  check_contains "$spec_file" "../../01.requirements/015-security-optimization-hardening.md" "tier 03 spec trace link missing"

  local template_file
  for template_file in "$templates_dir"/*.ctmpl; do
    check_file "$template_file"
    check_not_contains "$template_file" "secret/data/example" "vault template placeholder secret path"
  done

  check_service_healthcheck "$compose_file" "vault"
  check_service_healthcheck "$compose_file" "vault-agent"
}

# --- Tier 04: Data ---
check_04_data() {
  local tier="04-data"
  start_tier "$tier"

  local supabase_compose="infra/04-data/operational/supabase/docker-compose.yml"
  local valkey_compose="infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml"

  check_file "$supabase_compose"
  check_file "$valkey_compose"

  check_contains "$supabase_compose" "common-optimizations.yml" "supabase template inheritance missing"
  check_contains "$valkey_compose" "common-optimizations.yml" "valkey template inheritance missing"

  check_service_healthcheck "$supabase_compose" "db"
  check_service_healthcheck "$supabase_compose" "auth"
}

# --- Tier 05: Messaging ---
check_05_messaging() {
  local tier="05-messaging"
  start_tier "$tier"

  local kafka_compose="infra/05-messaging/kafka/docker-compose.yml"
  local rabbitmq_compose="infra/05-messaging/rabbitmq/docker-compose.yml"

  check_file "$kafka_compose"
  check_file "$rabbitmq_compose"

  check_contains "$kafka_compose" "gateway-standard-chain@file" "kafka gateway chain missing"
  check_contains "$rabbitmq_compose" "gateway-standard-chain@file,sso-errors@file,sso-auth@file" "rabbitmq middleware chain mismatch"

  check_service_healthcheck "$rabbitmq_compose" "rabbitmq"
}

# --- Tier 06: Observability ---
check_06_observability() {
  local tier="06-observability"
  start_tier "$tier"

  local compose_file="infra/06-observability/docker-compose.yml"
  check_file "$compose_file"
  check_contains "$compose_file" "gateway-standard-chain@file,sso-errors@file,sso-auth@file" "observability sso middleware chain mismatch"
  check_contains "$compose_file" "condition: service_healthy" "observability health-gated dependency missing"
}

# --- Tier 07: Workflow ---
check_07_workflow() {
  local tier="07-workflow"
  start_tier "$tier"

  local airflow_compose="infra/07-workflow/airflow/docker-compose.yml"
  local n8n_compose="infra/07-workflow/n8n/docker-compose.yml"

  check_file "$airflow_compose"
  check_file "$n8n_compose"

  check_contains "$airflow_compose" "sso-auth@file" "airflow sso missing"
  check_contains "$n8n_compose" "sso-auth@file" "n8n sso missing"
}

# --- Tier 08: AI ---
check_08_ai() {
  local tier="08-ai"
  start_tier "$tier"

  local ollama_compose="infra/08-ai/ollama/docker-compose.yml"
  local webui_compose="infra/08-ai/open-webui/docker-compose.yml"

  check_file "$ollama_compose"
  check_file "$webui_compose"

  check_contains "$ollama_compose" "sso-auth@file" "ollama sso missing"
  check_contains "$webui_compose" "sso-auth@file" "open-webui sso missing"
}

# --- Tier 09: Tooling ---
check_09_tooling() {
  local tier="09-tooling"
  start_tier "$tier"

  local sonarqube_compose="infra/09-tooling/sonarqube/docker-compose.yml"
  check_file "$sonarqube_compose"
  check_contains "$sonarqube_compose" "sso-auth@file" "sonarqube sso missing"
}

# --- Tier 10: Communication ---
check_10_communication() {
  local tier="10-communication"
  start_tier "$tier"

  local mail_compose="infra/10-communication/mail/docker-compose.yml"
  check_file "$mail_compose"

  check_contains "$mail_compose" "service: template-stateful-med" "stalwart template inheritance missing"
  check_contains "$mail_compose" "service: template-infra-low" "mailhog template inheritance missing"
  check_contains "$mail_compose" "traefik.http.routers.stalwart-ui.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "stalwart admin route sso middleware mismatch"
  check_contains "$mail_compose" "traefik.http.routers.mailhog.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "mailhog route sso middleware mismatch"
  check_contains "$mail_compose" "ipv4_address: 172.19.0.228" "stalwart infra_net IP mismatch"
  check_contains "$mail_compose" "ipv4_address: 172.19.0.229" "mailhog infra_net IP mismatch"

  check_service_healthcheck "$mail_compose" "stalwart"
  check_service_healthcheck "$mail_compose" "mailhog"
}

# --- Tier 11: Laboratory ---
check_11_laboratory() {
  local tier="11-laboratory"
  start_tier "$tier"

  local dashboard_compose="infra/11-laboratory/dashboard/docker-compose.yml"
  local dozzle_compose="infra/11-laboratory/dozzle/docker-compose.yml"
  local open_notebook_compose="infra/11-laboratory/open-notebook/docker-compose.yml"
  local portainer_compose="infra/11-laboratory/portainer/docker-compose.yml"
  local redisinsight_compose="infra/11-laboratory/redisinsight/docker-compose.yml"
  local dozzle_image
  local dozzle_compose_image

  check_file "$dashboard_compose"
  check_file "$dozzle_compose"
  check_file "$open_notebook_compose"
  check_file "$portainer_compose"
  check_file "$redisinsight_compose"
  dozzle_image="$(registry_component_image "Dozzle")"
  dozzle_compose_image="$(compose_service_image "$dozzle_compose" "dozzle")"

  check_contains "$dashboard_compose" "traefik.http.routers.homer.middlewares: gateway-standard-chain@file,homer-admin-ip@docker,sso-errors@file,sso-auth@file" "homer middleware chain mismatch"
  check_not_contains "$dashboard_compose" "ports:" "homer direct host ports must stay removed"
  check_contains "$dashboard_compose" "ipv4_address: 172.19.0.222" "homer infra_net IP mismatch"

  check_contains "$dozzle_compose" "/var/run/docker.sock:/var/run/docker.sock:ro" "dozzle socket must be read-only"
  check_contains "$dozzle_compose" "traefik.http.routers.dozzle.middlewares: gateway-standard-chain@file,dozzle-admin-ip@docker,sso-errors@file,sso-auth@file" "dozzle middleware chain mismatch"
  if [[ "$dozzle_compose_image" != "$dozzle_image" ]]; then
    fail "dozzle image tag mismatch"
  fi
  check_contains "$dozzle_compose" "ipv4_address: 172.19.0.221" "dozzle infra_net IP mismatch"

  check_contains "$open_notebook_compose" "traefik.http.routers.open-notebook.middlewares: gateway-standard-chain@file,open-notebook-admin-ip@docker,large-body@file,sso-errors@file,sso-auth@file" "open-notebook middleware chain mismatch"
  check_contains "$open_notebook_compose" "condition: service_healthy" "open-notebook health-gated dependency missing"
  check_contains "$open_notebook_compose" "OPEN_NOTEBOOK_PASSWORD_FILE=/run/secrets/open_notebook_password" "open-notebook password secret file missing"
  check_contains "$open_notebook_compose" "OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE=/run/secrets/open_notebook_encryption_key" "open-notebook encryption key secret file missing"
  check_contains "$open_notebook_compose" "ipv4_address: 172.19.0.122" "surrealdb infra_net IP mismatch"
  check_contains "$open_notebook_compose" "ipv4_address: 172.19.0.123" "open-notebook infra_net IP mismatch"

  check_contains "$portainer_compose" "traefik.http.routers.portainer.middlewares: gateway-standard-chain@file,portainer-admin-ip@docker,sso-errors@file,sso-auth@file" "portainer middleware chain mismatch"
  check_contains "$portainer_compose" "image: portainer/portainer-ce:sts" "portainer image tag mismatch"
  check_contains "$portainer_compose" "ipv4_address: 172.19.0.220" "portainer infra_net IP mismatch"

  check_contains "$redisinsight_compose" "image: redis/redisinsight:3.6.0" "redisinsight image tag mismatch"
  check_contains "$redisinsight_compose" "traefik.http.routers.redisinsight.middlewares: gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file" "redisinsight middleware chain mismatch"
  check_contains "$redisinsight_compose" "traefik.http.routers.redisinsight-static.middlewares: gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file" "redisinsight static middleware chain mismatch"
  check_contains "$redisinsight_compose" "ipv4_address: 172.19.0.121" "redisinsight infra_net IP mismatch"

  check_service_healthcheck "$dashboard_compose" "homer"
  check_service_healthcheck "$dozzle_compose" "dozzle"
  check_service_healthcheck "$open_notebook_compose" "surrealdb"
  check_service_healthcheck "$open_notebook_compose" "open_notebook"
  check_service_healthcheck "$portainer_compose" "portainer"
  check_service_healthcheck "$redisinsight_compose" "redisinsight"
}

# Main Execution
run_tier() {
  local tier="$1"

  case "$tier" in
  01-gateway | gateway)
    check_01_gateway
    ;;
  02-auth | auth)
    check_02_auth
    ;;
  03-security | security)
    check_03_security
    ;;
  04-data | data)
    check_04_data
    ;;
  05-messaging | messaging)
    check_05_messaging
    ;;
  06-observability | observability | obs)
    check_06_observability
    ;;
  07-workflow | workflow)
    check_07_workflow
    ;;
  08-ai | ai)
    check_08_ai
    ;;
  09-tooling | tooling)
    check_09_tooling
    ;;
  10-communication | communication | comm)
    check_10_communication
    ;;
  11-laboratory | laboratory | lab)
    check_11_laboratory
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown hardening tier: $tier" >&2
    usage >&2
    exit 2
    ;;
  esac
}

main() {
  local exit_code=0

  if [[ "${1:-}" == "--resolve-compose-service-image" ]]; then
    shift
    resolve_compose_service_image_cli "$@"
    return
  fi

  if [[ "$#" -eq 0 ]]; then
    run_tier 01-gateway
    run_tier 02-auth
    run_tier 03-security
    run_tier 04-data
    run_tier 05-messaging
    run_tier 06-observability
    run_tier 07-workflow
    run_tier 08-ai
    run_tier 09-tooling
    run_tier 10-communication
    run_tier 11-laboratory
  else
    local tier
    for tier in "$@"; do
      run_tier "$tier"
    done
  fi

  echo ""
  echo "-----------------------------------"
  if report_status; then
    exit_code=0
  else
    exit_code=1
  fi

  exit "$exit_code"
}

main "$@"
