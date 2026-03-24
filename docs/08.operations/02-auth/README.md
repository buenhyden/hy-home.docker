# Operations Policy: Auth Tier (02-auth)

<!-- [ID:docs:08:02-auth:README] -->
: Governance and operational standards for Identity & Access.

---

## Security Controls

### Identity Provider (Keycloak)
- **Realm Lockdown**: The `master` realm must only be used for system administration. Create application-specific realms for services.
- **TLS Enforcement**: All auth traffic must be encrypted over `websecure` (port 443).
- **Password Policy**: Enforce strong password complexity and rotation for admin accounts.

### ForwardAuth (OAuth2 Proxy)
- **Cookie Security**: `OAUTH2_PROXY_COOKIE_SECURE=true` must be set in production.
- **Session Duration**: Default session life is 168h (1 week); adjust based on risk.

## Availability Targets

- **SLO**: 99.9% uptime for core authentication.
- **Dependency Map**:
  - `keycloak` -> `mng-pg`
  - `oauth2-proxy` -> `mng-valkey`

## Backup & Retention

- **Database**: Daily backups of the Keycloak PostgreSQL database are mandatory.
- **Configuration**: Theme and configuration changes must be committed to `infra/02-auth/keycloak`.

---

## Review Cadence

| Item | Frequency | Responsibility |
| :--- | :--- | :--- |
| **User Audit** | Quarterly | Admin |
| **Client Secrets Rotation** | Bi-Annually | DevOps |
| **Keycloak Version Upgrade** | Upon Patch Release | DevOps |
