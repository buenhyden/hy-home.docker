pid_file = "/tmp/openbao-agent.pid"

vault {
  # VAULT_ADDR and VAULT_CACERT from Compose own the TLS endpoint/trust.
  tls_skip_verify = false
}

auto_auth {
  method "approle" {
    mount_path = "auth/approle"

    config = {
      role_id_file_path   = "/openbao/agent/role_id"
      secret_id_file_path = "/openbao/agent/secret_id"

      secret_id_response_wrapping_path = "auth/approle/role/hy-home-renderer/secret-id"
      remove_secret_id_file_after_reading = true
    }
  }

  sink "file" {
    config = {
      path = "/openbao/agent/token"
      mode = 0600
    }
  }
}

template {
  source      = "/openbao/config/templates/keycloak_admin_password.ctmpl"
  destination = "/openbao/out/auth/keycloak_admin_password.txt"
  perms       = 0600
}

template {
  source      = "/openbao/config/templates/grafana_admin_password.ctmpl"
  destination = "/openbao/out/observability/grafana_admin_password.txt"
  perms       = 0600
}

template {
  source      = "/openbao/config/templates/keycloak_admin_password_version.ctmpl"
  destination = "/openbao/out/auth/keycloak_admin_password.version"
  perms       = 0600
}

template {
  source      = "/openbao/config/templates/grafana_admin_password_version.ctmpl"
  destination = "/openbao/out/observability/grafana_admin_password.version"
  perms       = 0600
}

template_config {
  static_secret_render_interval = "5m"
  exit_on_retry_failure         = false
}

# Metrics for the Prometheus `openbao-agent` job (SPEC-0239). A metrics_only
# listener serves /agent/v1/metrics and nothing else: no API proxy, cache or
# quit route, no token, no secret. Plain HTTP because the Agent holds no server
# certificate; the port is never published and only obs_net and secrets_net
# peers can reach it.
listener "tcp" {
  address     = "0.0.0.0:8100"
  role        = "metrics_only"
  tls_disable = true
}

telemetry {
  prometheus_retention_time = "24h"
  disable_hostname          = true
}
