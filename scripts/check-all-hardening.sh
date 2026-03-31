#!/usr/bin/env bash
# Unified Infrastructure Hardening Verification Script
# Consolidates checks for all 11 tiers into a single execution and report.

set -euo pipefail

# Source the library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_PATH="${SCRIPT_DIR}/lib/hardening-lib.sh"

if [[ ! -f "$LIB_PATH" ]]; then
    echo "Error: Hardening library not found at $LIB_PATH"
    exit 1
fi

# shellcheck source=lib/hardening-lib.sh
source "$LIB_PATH"

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
    check_contains "$nginx_compose" "service: template-infra-readonly-low" "nginx compose template mismatch"
    check_contains "$nginx_conf" "server_tokens off;" "nginx server_tokens off missing"
}

# --- Tier 02: Auth ---
check_02_auth() {
    local tier="02-auth"
    start_tier "$tier"

    local keycloak_compose="infra/02-auth/keycloak/docker-compose.yml"
    local oauth_compose="infra/02-auth/oauth2-proxy/docker-compose.yml"
    local oauth_cfg="infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg"

    check_file "$keycloak_compose"
    check_file "$oauth_compose"
    check_file "$oauth_cfg"

    check_contains "$keycloak_compose" "service: template-infra-high" "keycloak compose template mismatch"
    check_contains "$oauth_compose" "service: template-infra-readonly-med" "oauth2-proxy compose template mismatch"
    check_contains "$oauth_cfg" "cookie_secure = true" "oauth2-proxy cookie_secure missing"
}

# --- Tier 03: Security ---
check_03_security() {
    local tier="03-security"
    start_tier "$tier"

    local compose_file="infra/03-security/vault/docker-compose.yml"
    local agent_hcl="infra/03-security/vault/config/vault-agent.hcl"
    local spec_file="docs/04.specs/03-security/spec.md"

    check_file "$compose_file"
    check_file "$agent_hcl"
    check_file "$spec_file"

    check_contains "$compose_file" "service: template-stateful-med" "vault compose template inheritance missing"
    check_contains "$compose_file" "vault-agent:" "vault-agent service missing"
    check_contains "$spec_file" "../../01.prd/2026-03-28-03-security-optimization-hardening.md" "tier 03 spec trace link missing"
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

# --- Tier 11: Laboratory ---
check_11_laboratory() {
    local tier="11-laboratory"
    start_tier "$tier"

    local portainer_compose="infra/11-laboratory/portainer/docker-compose.yml"
    check_file "$portainer_compose"
    check_contains "$portainer_compose" "sso-auth@file" "portainer sso missing"
}

# Main Execution
main() {
    local exit_code=0

    check_01_gateway
    check_02_auth
    check_03_security
    check_04_data
    check_05_messaging
    check_06_observability
    check_07_workflow
    check_08_ai
    check_09_tooling
    check_11_laboratory

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


# k3s 전환 준비: Docker Compose 설정을 Kubernetes(k3s)로 옮기기 위한 리소스 및 네트워크 정책 최적화
