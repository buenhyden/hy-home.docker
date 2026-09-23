# hy-home.k8s External Secrets Operator: read-only on the platform KV v2
# entries it syncs. Bound to auth/kubernetes/role/eso-read-platform.
path "secret/data/platform/argocd" {
  capabilities = ["read"]
}

path "secret/metadata/platform/argocd" {
  capabilities = ["read"]
}

path "secret/data/platform/postgres-app" {
  capabilities = ["read"]
}

path "secret/metadata/platform/postgres-app" {
  capabilities = ["read"]
}

path "secret/data/platform/notifications" {
  capabilities = ["read"]
}

path "secret/metadata/platform/notifications" {
  capabilities = ["read"]
}

path "secret/data/platform/prometheus-api" {
  capabilities = ["read"]
}

path "secret/metadata/platform/prometheus-api" {
  capabilities = ["read"]
}
