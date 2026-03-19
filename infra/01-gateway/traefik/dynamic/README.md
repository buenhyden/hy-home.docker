# Traefik Dynamic Configuration

This directory contains configuration that Traefik watches and hot-reloads without restarts.

## Files

- `middleware.yml`: Defines reusable security and transport rules.
  - `sso-auth`: OAuth2 Proxy integration for service protection.
  - `opensearch-transport`: Configures TLS trust for OpenSearch backends.
  - `req-rate-limit`: Global rate limiting rules.
- `tls.yaml`: Configures certificates and stores.
  - Points to `/certs/cert.pem` and `/certs/key.pem` generated via `mkcert`.
