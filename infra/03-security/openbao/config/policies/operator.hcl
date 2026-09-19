# Owner-approved human operations: two existing values, renderer credentials,
# backup reads and authenticated quorum recovery. No secret deletion or wildcards.
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
