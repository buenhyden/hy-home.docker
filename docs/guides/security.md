# Security Guide

## Secrets Management

### Docker Secrets

All sensitive credentials are stored in the `secrets/` directory as text files.

**Location**: `secrets/` (git-ignored)

**Required Secrets**:

```
secrets/
?œâ??€ postgres_password.txt
?œâ??€ redis_password.txt
?œâ??€ valkey_password.txt
?œâ??€ minio_root_user.txt
?œâ??€ minio_root_password.txt
?œâ??€ minio_app_user.txt
?”â??€ minio_app_user_password.txt
```

**Access Pattern**:

```yaml
secrets:
  postgres_password:
    file: ../secrets/postgres_password.txt
```

### Password Guidelines

**Strength Requirements**:

- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- Avoid dictionary words

**Generate Secure Passwords**:

```bash
# Linux/Mac
openssl rand -base64 32

# PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 24 | % {[char]$_})
```

### Environment Variables

Never commit `.env` to git. Use `.env.example` as template.

**Bad**:

```yaml
environment:
  DB_PASSWORD: "hardcoded_password"  # NEVER DO THIS
```

**Good**:

```yaml
environment:
  DB_PASSWORD_FILE: /run/secrets/postgres_password
```

## SSL/TLS Certificates

### Development (mkcert)

**Install mkcert**:

```bash
# Windows (Chocolatey)
choco install mkcert

# Mac
brew install mkcert

# Linux
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo mv mkcert-v*-linux-amd64 /usr/local/bin/mkcert
```

**Generate Certificates**:

```bash
# Install root CA (one-time)
mkcert -install

# Create certs directory
mkdir -p certs

# Generate wildcard certificate
mkcert -key-file certs/local-key.pem \
       -cert-file certs/local-cert.pem \
       "localhost" "127.0.0.1" "*.127.0.0.1.nip.io"

# Copy root CA for services
cp "$(mkcert -CAROOT)/rootCA.pem" ./certs/rootCA.pem
```

**Traefik Configuration**:

```yaml
- "--providers.file.filename=/etc/traefik/dynamic.yml"
```

`dynamic.yml`:

```yaml
tls:
  certificates:
    - certFile: /certs/local-cert.pem
      keyFile: /certs/local-key.pem
```

### Production (Let's Encrypt)

**Automatic with Traefik**:

```yaml
command:
  - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
  - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
  - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
```

**Per-service labels**:

```yaml
labels:
  - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
```

## Authentication & Authorization

### Keycloak Configuration

**Admin Access**:

- Initial admin credentials set via `KEYCLOAK_ADMIN` / `KEYCLOAK_ADMIN_PASSWORD`
- Change immediately after first login

**Realms**:

- Create separate realm for production (`master` is for admin only)
- Configure clients for each service requiring OAuth2

**Users**:

- Enable email verification
- Require strong passwords
- Enforce MFA for admin users

### OAuth2 Proxy

**Purpose**: Protects services without built-in authentication.

**How it works**:

1. User requests protected service (e.g., Grafana)
2. Traefik forwards auth request to OAuth2 Proxy
3. OAuth2 Proxy validates session or redirects to Keycloak
4. After login, request proceeds to service

**Protected Services** (via `sso-auth@file` middleware):

- Grafana
- n8n
- Kafka UI
- RedisInsight
- MailHog
- Storybook

**Configuration**:

```yaml
environment:
  OAUTH2_PROXY_PROVIDER: keycloak-oidc
  OAUTH2_PROXY_CLIENT_ID: oauth2-proxy
  OAUTH2_PROXY_OIDC_ISSUER_URL: https://keycloak.${DEFAULT_URL}/realms/master
  OAUTH2_PROXY_COOKIE_SECRET: <64-char-random-string>
```

**Generate Cookie Secret**:

```bash
openssl rand -base64 32 | head -c 32
```

## Network Security

### Principle: Minimize Exposure

**Exposed Ports** (should be minimal):

- 80/443: Traefik only
- 5000/5001: PostgreSQL (for external tools)
- 6379: Redis (for external tools)
- 9092-9094: Kafka (for external producers/consumers)

**Internal-Only Services**:

- Prometheus, Loki, Tempo (accessed via Grafana)
- etcd, Patroni (cluster internals)
- MinIO (accessed via services, not directly)

### Firewall Rules (Production)

```bash
# Allow only Traefik
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct database access
sudo ufw deny 5432/tcp

# Enable firewall
sudo ufw enable
```

### Container Security

**Resource Limits**:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

**Read-Only Filesystem** (where possible):

```yaml
security_opt:
  - no-new-privileges:true
read_only: true
tmpfs:
  - /tmp
```

**Drop Capabilities**:

```yaml
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE  # Only if needed
```

## Data Security

### Encryption at Rest

**PostgreSQL**:
Enable data encryption via `postgresql.conf`:

```
# Encryption
ssl = on
ssl_cert_file = '/certs/server.crt'
ssl_key_file = '/certs/server.key'
```

**MinIO**:
Enable server-side encryption:

```yaml
environment:
  MINIO_KMS_SECRET_KEY: "my-minio-key:CHANGEME32BYTESLONGCHANGEME32BYTES"
```

### Backup Security

**Encrypt backups**:

```bash
# Example: PostgreSQL dump
pg_dump -h localhost -p 5000 -U postgres dbname | \
  openssl enc -aes-256-cbc -salt -out backup.sql.enc
```

**Store offsite**:

- Use MinIO bucket with versioning
- Or external S3/Azure Blob Storage

## Security Best Practices

### Development

1. ??Change all default passwords
2. ??Use mkcert for local HTTPS
3. ??Keep secrets/ in `.gitignore`
4. ??Regularly update images

### Production

1. ??Use Let's Encrypt for TLS
2. ??Enable Keycloak MFA
3. ??Implement rate limiting (Traefik)
4. ??Regular security audits
5. ??Automated backup with encryption
6. ??Monitor security logs
7. ??Network segmentation (separate `project_net`)
8. ??Container scanning (Trivy, Snyk)

## Incident Response

**If Breach Suspected**:

1. Isolate affected containers: `docker compose stop <service>`
2. Capture logs: `docker logs <container> > incident.log`
3. Rotate all secrets immediately
4. Audit access logs in Keycloak
5. Check Traefik access logs for anomalies

## Compliance Considerations

- **GDPR**: Implement data deletion in PostgreSQL
- **PCI DSS**: If processing payments, segment network
- **HIPAA**: Encrypt all data at rest and in transit
- **SOC 2**: Enable comprehensive audit logging

## See Also

- [Deployment Guide](./deployment-guide.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [Maintenance Guide](./maintenance.md)
