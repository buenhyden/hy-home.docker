#!/usr/bin/env bash
set -euo pipefail

failures=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "missing file: $file"
    return 1
  fi
  return 0
}

check_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -Fq -- "$pattern" "$file"; then
    fail "$label (file: $file, expected: $pattern)"
  fi
}

keycloak_compose="infra/02-auth/keycloak/docker-compose.yml"
oauth_compose="infra/02-auth/oauth2-proxy/docker-compose.yml"
oauth_cfg="infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg"
oauth_dockerfile="infra/02-auth/oauth2-proxy/Dockerfile"
oauth_entrypoint="infra/02-auth/oauth2-proxy/docker-entrypoint.sh"

check_file "$keycloak_compose" || true
check_file "$oauth_compose" || true
check_file "$oauth_cfg" || true
check_file "$oauth_dockerfile" || true
check_file "$oauth_entrypoint" || true

if [[ "$failures" -eq 0 ]]; then
  # Keycloak baseline checks.
  check_contains "$keycloak_compose" "service: template-infra-high" "keycloak compose template mismatch"
  check_contains "$keycloak_compose" "KC_DB_PASSWORD_FILE: /run/secrets/keycloak_db_password" "keycloak db password file contract missing"
  check_contains "$keycloak_compose" 'KC_BOOTSTRAP_ADMIN_PASSWORD="$$(tr -d '\''\r\n'\'' </run/secrets/keycloak_admin_password)"' "keycloak admin secret injection missing"
  check_contains "$keycloak_compose" "/health/ready HTTP/1.1" "keycloak readiness healthcheck missing"
  check_contains "$keycloak_compose" "keycloak_db_password" "keycloak db secret wiring missing"
  check_contains "$keycloak_compose" "keycloak_admin_password" "keycloak admin secret wiring missing"

  # OAuth2 Proxy compose/runtime checks.
  check_contains "$oauth_compose" "service: template-infra-readonly-med" "oauth2-proxy compose template mismatch"
  check_contains "$oauth_compose" "OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://mng-valkey:6379" "oauth2-proxy redis endpoint contract missing"
  check_contains "$oauth_compose" "OAUTH2_PROXY_OIDC_ISSUER_URL=https://keycloak.\${DEFAULT_URL}/realms/hy-home.realm" "oauth2-proxy dynamic oidc issuer missing"
  check_contains "$oauth_compose" "OAUTH2_PROXY_REDIRECT_URL=https://auth.\${DEFAULT_URL}/oauth2/callback" "oauth2-proxy dynamic redirect url missing"
  check_contains "$oauth_compose" "OAUTH2_PROXY_COOKIE_DOMAINS=.\${DEFAULT_URL}" "oauth2-proxy cookie domains env missing"
  check_contains "$oauth_compose" "OAUTH2_PROXY_WHITELIST_DOMAINS=*.\${DEFAULT_URL}" "oauth2-proxy whitelist domains env missing"
  check_contains "$oauth_compose" "/ping >/dev/null 2>&1 || exit 1" "oauth2-proxy /ping healthcheck missing"
  check_contains "$oauth_compose" "start_period: 20s" "oauth2-proxy healthcheck start_period missing"
  check_contains "$oauth_compose" "oauth2_proxy_cookie_secret" "oauth2-proxy cookie secret wiring missing"
  check_contains "$oauth_compose" "oauth2_proxy_client_secret" "oauth2-proxy client secret wiring missing"
  check_contains "$oauth_compose" "mng_valkey_password" "oauth2-proxy valkey secret wiring missing"

  # OAuth2 Proxy image hardening checks.
  check_contains "$oauth_dockerfile" "adduser -S -D -H -s /sbin/nologin -G oauth2proxy oauth2proxy" "oauth2-proxy non-root user creation missing"
  check_contains "$oauth_dockerfile" "USER oauth2proxy:oauth2proxy" "oauth2-proxy USER directive missing"

  # OAuth2 Proxy entrypoint secret handling checks.
  check_contains "$oauth_entrypoint" "read_secret()" "oauth2-proxy read_secret helper missing"
  check_contains "$oauth_entrypoint" "OAUTH2_PROXY_REDIS_PASSWORD" "oauth2-proxy redis password export missing"
  check_contains "$oauth_entrypoint" "set -- --config /etc/oauth2-proxy.cfg" "oauth2-proxy default command fallback missing"

  # OAuth2 Proxy config security/session defaults.
  check_contains "$oauth_cfg" "provider = \"keycloak-oidc\"" "oauth2-proxy provider mismatch"
  check_contains "$oauth_cfg" "cookie_secure = true" "oauth2-proxy cookie_secure missing"
  check_contains "$oauth_cfg" "cookie_httponly = true" "oauth2-proxy cookie_httponly missing"
  check_contains "$oauth_cfg" "cookie_samesite = \"lax\"" "oauth2-proxy cookie_samesite mismatch"
  check_contains "$oauth_cfg" "cookie_refresh = \"1h\"" "oauth2-proxy cookie_refresh mismatch"
  check_contains "$oauth_cfg" "cookie_expire = \"12h\"" "oauth2-proxy cookie_expire mismatch"
  check_contains "$oauth_cfg" "client_secret_file = \"/run/secrets/oauth2_proxy_client_secret\"" "oauth2-proxy client secret file contract missing"
  check_contains "$oauth_cfg" "cookie_secret_file = \"/run/secrets/oauth2_proxy_cookie_secret\"" "oauth2-proxy cookie secret file contract missing"
fi

echo "Auth hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 02-auth hardening baseline enforced"
