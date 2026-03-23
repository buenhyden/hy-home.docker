# vault-agent.hcl
pid_file = "/tmp/vault-agent.pid"

vault {
  address = "http://vault:8200"
}

auto_auth {
  method "approle" {
    mount_path = "auth/approle"

    config = {
      role_id_file_path   = "/vault/agent/role_id"
      secret_id_file_path = "/vault/agent/secret_id"
      remove_secret_id_file_after_reading = false
    }
  }

  sink "file" {
    config = {
      path = "/vault/agent/token"
      mode = 0600
    }
  }
}

cache {
  # use_auto_auth_token = true
}

listener "tcp" {
  address     = "0.0.0.0:8100"
  tls_disable = true
}

api_proxy {
  use_auto_auth_token = true
}

template {
  source      = "/vault/config/templates/postgres_password.ctmpl"
  destination = "/vault/out/postgres/postgres_password"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/keycloak_db_password.ctmpl"
  destination = "/vault/out/keycloak/kc_db_password"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/keycloak_admin_username.ctmpl"
  destination = "/vault/out/keycloak/admin_username"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/keycloak_admin_password.ctmpl"
  destination = "/vault/out/keycloak/admin_password"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/oauth2_proxy_client_secret.ctmpl"
  destination = "/vault/out/oauth2-proxy/client_secret"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/oauth2_proxy_cookie_secret.ctmpl"
  destination = "/vault/out/oauth2-proxy/cookie_secret"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/grafana_admin_password.ctmpl"
  destination = "/vault/out/grafana/admin_password"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/grafana_db_password.ctmpl"
  destination = "/vault/out/grafana/db_password"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/grafana_oauth_client_secret.ctmpl"
  destination = "/vault/out/grafana/oauth_client_secret"
  perms       = 0600
}

template {
  source      = "/vault/config/templates/app_env.ctmpl"
  destination = "/vault/out/app/app.env"
  perms       = 0600
}

template_config {
  static_secret_render_interval = "5m"
  exit_on_retry_failure         = false
}
