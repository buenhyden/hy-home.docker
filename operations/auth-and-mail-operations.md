# Auth & Communication Operations

> **Components**: `oauth2-proxy`, `keycloak`, `mailhog`

## OAuth2 Proxy (SSO) Operations

### 1. Protecting a Service (Traefik Middleware)

To protect any service with SSO, apply the following Traefik label in its `docker-compose.yml`:

```yaml
labels:
  - 'traefik.http.routers.my-app.middlewares=sso-auth@file'
```

The `sso-auth` middleware (defined in Traefik's dynamic config) forwards requests to `http://auth.${DEFAULT_URL}/oauth2/auth`.

### 2. Manual Sign-In

- **URL**: `https://auth.${DEFAULT_URL}`
- **Action**: Redirects to the configured IdP (e.g., Keycloak).

### Troubleshooting SSO

- **"500 Internal Server Error"**: Usually indicates Redis connection failure or Misconfigured Secret.
  1. Check logs: `docker compose logs oauth2-proxy`
  2. Verify Redis connection URL in `docker-compose.yml`.
- **"x509: certificate signed by unknown authority"**: The OAuth2 Proxy container doesn't trust the IdP (Keycloak) certificate.
  - Ensure `rootCA.pem` is valid and mapped.
  - Verify `SSL_CERT_FILE` env var is set correctly.

---

## MailHog (Local SMTP)

### Configuring Applications (Internal)

To send emails from other services within the `infra_net` network:

- **Host**: `mailhog`
- **Port**: `1025`
- **Auth**: None (MailHog accepts everything)

### Accessing Web UI

- **URL**: `https://mail.${DEFAULT_URL}`
- **Login**: Authenticate via your SSO provider.
