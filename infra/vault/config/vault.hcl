# Vault Configuration File - Production Mode
# https://developer.hashicorp.com/vault/docs/configuration

# UI Configuration
# The UI is enabled by default in dev mode, but must be explicitly enabled here.
ui = true

# Mlock Configuration
# Must be explicitly set in newer Vault versions.
# 'true' helps prevents memory swapping but requires IPC_LOCK capability.
# 'false' is safer for general container usage if swap is not an issue or properly managed.
# Given the error history, setting to true (since we have IPC_LOCK) or false (to bypass checking).
# We will use 'true' as we gave IPC_LOCK, but if it fails again, try 'false'.
disable_mlock = true

# Storage Configuration
# Using Integrated Storage (Raft) is recommended for production.
# It doesn't require an external storage backend like Consul.
storage "raft" {
  path    = "/vault/file"
  node_id = "node1"
}

# Listener Configuration
# Configures how Vault listens for API requests.
listener "tcp" {
  address     = "0.0.0.0:8200"
  
  # Note: 'https_proxy' is not a valid parameter for the listener block.
  # Proxying is handled by your Traefik setup or environment variables (http_proxy).

  # TLS Configuration
  # In a strict production environment, TLS should be enabled.
  # For internal docker networking or behind a secure reverse proxy, it might be disabled.
  # WARNING: Running without TLS is not recommended for production.
  # We MUST set this to 1 (disabled) if we do not provide certs, otherwise Vault won't start.
  tls_disable = 1

  # If you want to enable TLS, uncomment and configure paths:
  # tls_cert_file = "/vault/config/certs/cert.pem"
  # tls_key_file  = "/vault/config/certs/key.pem"
}

# Service Registration (Optional)
# service_registration "consul" {
#   address = "consul:8500"
# }

# API Address
# The address to advertise to other Vault servers in the cluster for request forwarding.
# Should be reachable by other nodes.
api_addr = "http://localhost:8200"

# Cluster Address
# The address to advertise to other Vault servers in the cluster for replication.
cluster_addr = "http://localhost:8201"

# Telemetry
# Enable telemetry to send metrics to Prometheus/Grafana (via Agent/Alloy)
telemetry {
  disable_hostname = true
  prometheus_retention_time = "30s"
}
