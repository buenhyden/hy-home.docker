# Agent templates consume only these two KV v2 data endpoints.
# Health reads only their exact version metadata; no list or sibling access.
path "secret/data/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/data/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}
