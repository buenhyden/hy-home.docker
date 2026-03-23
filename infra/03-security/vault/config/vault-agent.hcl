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
  use_auto_auth_token = true
}

template {
  source      = "/vault/config/templates/example.ctmpl"
  destination = "/vault/agent/rendered-example.txt"
  perms       = 0600
}

template_config {
  static_secret_render_interval = "5m"
  exit_on_retry_failure         = false
}
