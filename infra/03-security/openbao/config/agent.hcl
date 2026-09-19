pid_file = "/tmp/openbao-agent.pid"

vault {
  address = "http://openbao:8200"
}

auto_auth {
  method "approle" {
    mount_path = "auth/approle"

    config = {
      role_id_file_path   = "/openbao/agent/role_id"
      secret_id_file_path = "/openbao/agent/secret_id"

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
  destination = "/openbao/rendered/auth/keycloak_admin_password.txt"
  perms       = 0600
}

template {
  source      = "/openbao/config/templates/grafana_admin_password.ctmpl"
  destination = "/openbao/rendered/observability/grafana_admin_password.txt"
  perms       = 0600
}

template_config {
  static_secret_render_interval = "5m"
  exit_on_retry_failure         = false
}