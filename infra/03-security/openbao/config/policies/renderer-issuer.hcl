# Dedicated human/bootstrap issuer; never the renderer or application token.
path "auth/approle/role/hy-home-renderer/role-id" {
  capabilities = ["read"]
}
path "auth/approle/role/hy-home-renderer/secret-id" {
  capabilities = ["update"]
  min_wrapping_ttl = "30s"
  max_wrapping_ttl = "60s"
}
