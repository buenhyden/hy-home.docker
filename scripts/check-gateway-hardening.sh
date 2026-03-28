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

traefik_compose="infra/01-gateway/traefik/docker-compose.yml"
traefik_middleware="infra/01-gateway/traefik/dynamic/middleware.yml"
nginx_compose="infra/01-gateway/nginx/docker-compose.yml"
nginx_conf="infra/01-gateway/nginx/config/nginx.conf"

check_file "$traefik_compose" || true
check_file "$traefik_middleware" || true
check_file "$nginx_compose" || true
check_file "$nginx_conf" || true

if [[ "$failures" -eq 0 ]]; then
  # Traefik compose: template/healthcheck/middleware chain
  check_contains "$traefik_compose" "service: template-infra-readonly-med" "traefik compose template mismatch"
  check_contains "$traefik_compose" "traefik.http.routers.dashboard.middlewares: dashboard-auth@file,gateway-standard-chain@file" "traefik dashboard middleware chain mismatch"
  check_contains "$traefik_compose" "traefik', 'healthcheck', '--ping'" "traefik healthcheck ping missing"

  # Traefik middleware definitions
  check_contains "$traefik_middleware" "req-rate-limit:" "missing req-rate-limit"
  check_contains "$traefik_middleware" "req-retry:" "missing req-retry"
  check_contains "$traefik_middleware" "attempts: 2" "retry attempts mismatch"
  check_contains "$traefik_middleware" "initialInterval: 100ms" "retry initial interval mismatch"
  check_contains "$traefik_middleware" "req-circuit-breaker:" "missing req-circuit-breaker"
  check_contains "$traefik_middleware" "NetworkErrorRatio() > 0.30" "circuit breaker rule mismatch"
  check_contains "$traefik_middleware" "gateway-standard-chain:" "missing gateway-standard-chain"
  check_contains "$traefik_middleware" "- req-rate-limit" "gateway chain missing req-rate-limit"
  check_contains "$traefik_middleware" "- req-retry" "gateway chain missing req-retry"
  check_contains "$traefik_middleware" "- req-circuit-breaker" "gateway chain missing req-circuit-breaker"

  # Nginx compose: readonly template/tmpfs/healthcheck
  check_contains "$nginx_compose" "service: template-infra-readonly-low" "nginx compose template mismatch"
  check_contains "$nginx_compose" "- /var/cache/nginx" "nginx tmpfs missing /var/cache/nginx"
  check_contains "$nginx_compose" "- /var/log/nginx" "nginx tmpfs missing /var/log/nginx"
  check_contains "$nginx_compose" "- /var/run" "nginx tmpfs missing /var/run"
  check_contains "$nginx_compose" "/ping || exit 1" "nginx healthcheck /ping missing"

  # Nginx config: security/timeouts/failover/cache policy
  check_contains "$nginx_conf" "server_tokens off;" "nginx server_tokens off missing"
  check_contains "$nginx_conf" "proxy_connect_timeout" "nginx proxy_connect_timeout missing"
  check_contains "$nginx_conf" "proxy_send_timeout" "nginx proxy_send_timeout missing"
  check_contains "$nginx_conf" "proxy_read_timeout" "nginx proxy_read_timeout missing"
  check_contains "$nginx_conf" "proxy_next_upstream" "nginx proxy_next_upstream policy missing"
  check_contains "$nginx_conf" "max_fails=" "nginx upstream max_fails missing"
  check_contains "$nginx_conf" "fail_timeout=" "nginx upstream fail_timeout missing"
  check_contains "$nginx_conf" "location ~* \\.(?:css|js|mjs|map|jpg|jpeg|png|gif|svg|ico|woff|woff2|ttf|eot)$" "nginx static cache location missing"
  check_contains "$nginx_conf" "Cache-Control \"public, max-age=604800, immutable\"" "nginx static cache header missing"
fi

echo "Gateway hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 01-gateway hardening baseline enforced"
