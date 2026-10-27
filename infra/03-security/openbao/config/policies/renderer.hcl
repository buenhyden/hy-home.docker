# Agent templates consume only these KV v2 data endpoints (P06 consumers).
# Health reads only their exact version metadata; no list or sibling access.
path "secret/data/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/data/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}

path "secret/data/hy-home/02-auth/oauth2-proxy" {
  capabilities = ["read"]
}

path "secret/data/hy-home/05-messaging/kafbat" {
  capabilities = ["read"]
}

path "secret/data/hy-home/06-observability/dozzle" {
  capabilities = ["read"]
}

path "secret/data/hy-home/06-observability/gatus" {
  capabilities = ["read"]
}

path "secret/data/hy-home/07-workflow/airflow" {
  capabilities = ["read"]
}

path "secret/data/hy-home/08-ai/open-webui" {
  capabilities = ["read"]
}

path "secret/data/hy-home/12-analytics/superset" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/02-auth/oauth2-proxy" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/05-messaging/kafbat" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/06-observability/dozzle" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/06-observability/gatus" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/07-workflow/airflow" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/08-ai/open-webui" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/12-analytics/superset" {
  capabilities = ["read"]
}
