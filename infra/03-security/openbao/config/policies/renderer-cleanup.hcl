# Exact renderer accessors only; the reconciler matches nonce and creation window.
path "auth/approle/role/hy-home-renderer/secret-id" {
  capabilities = ["list"]
}
path "auth/approle/role/hy-home-renderer/secret-id-accessor/lookup" {
  capabilities = ["update"]
  required_parameters = ["secret_id_accessor"]
  allowed_parameters = { "secret_id_accessor" = [] }
}
path "auth/approle/role/hy-home-renderer/secret-id-accessor/destroy" {
  capabilities = ["update"]
  required_parameters = ["secret_id_accessor"]
  allowed_parameters = { "secret_id_accessor" = [] }
}

# Self-identity probe only: prove exact policy, no default and short nonrenewable TTL.
path "auth/token/lookup-self" {
  capabilities = ["read"]
}
