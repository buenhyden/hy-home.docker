# Agent templates consume only these two KV v2 data endpoints.
path "secret/data/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/data/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}
