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
  # Group 1000 read lets Keycloak (UID 1000, group 1000) consume it (P06).
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/grafana_admin_password.ctmpl"
  destination = "/openbao/out/observability/grafana_admin_password.txt"
  # Group 1000 read lets Grafana (UID 472, group 1000) consume it (P06 W49).
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/grafana_client_secret.ctmpl"
  destination = "/openbao/out/observability/grafana_client_secret.txt"
  # Grafana reads it at every start as its Keycloak OIDC client secret (P06).
  perms       = 0640
}

# P06 OIDC client secret; only the oauth2-proxy consumer binds this directory.
template {
  source      = "/openbao/config/templates/oauth2_proxy_client_secret.ctmpl"
  destination = "/openbao/out/oauth2-proxy/oauth2_proxy_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/oauth2_proxy_client_secret_version.ctmpl"
  destination = "/openbao/out/oauth2-proxy/oauth2_proxy_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the kafbat consumer binds this directory.
template {
  source      = "/openbao/config/templates/kafbat_client_secret.ctmpl"
  destination = "/openbao/out/kafbat/kafbat_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/kafbat_client_secret_version.ctmpl"
  destination = "/openbao/out/kafbat/kafbat_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the dozzle consumer binds this directory.
template {
  source      = "/openbao/config/templates/dozzle_client_secret.ctmpl"
  destination = "/openbao/out/dozzle/dozzle_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/dozzle_client_secret_version.ctmpl"
  destination = "/openbao/out/dozzle/dozzle_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the gatus consumer binds this directory.
template {
  source      = "/openbao/config/templates/gatus_oidc_client_secret.ctmpl"
  destination = "/openbao/out/gatus/gatus_oidc_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/gatus_oidc_client_secret_version.ctmpl"
  destination = "/openbao/out/gatus/gatus_oidc_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the airflow consumer binds this directory.
template {
  source      = "/openbao/config/templates/airflow_client_secret.ctmpl"
  destination = "/openbao/out/airflow/airflow_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/airflow_client_secret_version.ctmpl"
  destination = "/openbao/out/airflow/airflow_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the open-webui consumer binds this directory.
template {
  source      = "/openbao/config/templates/openwebui_oidc_client_secret.ctmpl"
  destination = "/openbao/out/open-webui/openwebui_oidc_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/openwebui_oidc_client_secret_version.ctmpl"
  destination = "/openbao/out/open-webui/openwebui_oidc_client_secret.version"
  perms       = 0600
}

# P06 OIDC client secret; only the superset consumer binds this directory.
template {
  source      = "/openbao/config/templates/superset_oidc_client_secret.ctmpl"
  destination = "/openbao/out/superset/superset_oidc_client_secret.txt"
  perms       = 0640
}

template {
  source      = "/openbao/config/templates/superset_oidc_client_secret_version.ctmpl"
  destination = "/openbao/out/superset/superset_oidc_client_secret.version"
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
# certificate; the port is never published, so peers on obs_net and secrets_net
# and the host itself can reach it.
listener "tcp" {
  address     = "0.0.0.0:8100"
  role        = "metrics_only"
  tls_disable = true
}

telemetry {
  prometheus_retention_time = "24h"
  disable_hostname          = true
}
