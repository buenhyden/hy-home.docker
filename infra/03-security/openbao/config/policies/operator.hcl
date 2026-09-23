# Owner-approved human operations: two existing values, renderer credentials,
# backup reads, authenticated quorum recovery, the hy-home.k8s cluster
# rebuild steps (Kubernetes auth and bootstrap token), the Prometheus API
# credential rotation and the Kiali Grafana token reissue. No secret deletion
# or wildcards.
path "secret/data/hy-home/02-auth/keycloak" {
  capabilities = ["read", "update"]
}

path "secret/data/hy-home/06-observability/grafana" {
  capabilities = ["read", "update"]
}

path "secret/metadata/hy-home/02-auth/keycloak" {
  capabilities = ["read"]
}

path "secret/metadata/hy-home/06-observability/grafana" {
  capabilities = ["read"]
}

path "auth/approle/role/hy-home-renderer/secret-id" {
  capabilities = ["update"]
}

path "sys/storage/raft/snapshot" {
  capabilities = ["read", "sudo"]
}

# Cancel removes only an in-progress root-generation attempt, never secret data.
path "sys/generate-root-token/attempt" {
  capabilities = ["read", "update", "delete", "sudo"]
}

path "sys/generate-root-token/update" {
  capabilities = ["update", "sudo"]
}

# hy-home.k8s Prometheus API credential: rotate it together with OBS-013 and
# INFRA-007, without a root session.
path "secret/data/platform/prometheus-api" {
  capabilities = ["create", "read", "update"]
}

path "secret/metadata/platform/prometheus-api" {
  capabilities = ["read"]
}

# hy-home.k8s Kiali Grafana token (Viewer service account `k8s-kiali`): reissue
# it before expiry without a root session.
path "secret/data/platform/grafana-api" {
  capabilities = ["create", "read", "update"]
}

path "secret/metadata/platform/grafana-api" {
  capabilities = ["read"]
}

# hy-home.k8s rebuild: point Kubernetes auth at the new API server and CA,
# then issue a bootstrap token through its role (policy k8s-bootstrap only).
path "auth/kubernetes/config" {
  capabilities = ["read", "update"]
}

path "auth/token/create/k8s-bootstrap" {
  capabilities = ["update"]
}
