# Keycloak Identity Provider (IdP) Guide

> **Component**: `keycloak`
> **Internal Port**: `8080`
> **Administrative Path**: `https://keycloak.${DEFAULT_URL}`

## 1. Technical Specification

Keycloak serves as the primary OIDC/SAML provider with PostgreSQL persistence.

| Attribute | Value |
| --- | --- |
| **Internal Host** | `keycloak` |
| **External URL** | `https://keycloak.${DEFAULT_URL}` |
| **Static IP** | `172.19.0.29` |
| **Main Port** | `8080` |
| **Management Port**| `9000` |

### Database Persistence

- **Connectivity**: Managed via `pg-router` forwarding to the Patroni cluster.
- **Verification**: `docker exec keycloak curl -f http://localhost:9000/health/ready`

## 2. Bootstrapping a New Environment

Upon initial deployment (`docker compose up -d`), Keycloak initializes with the credentials specified in the infra secrets (`KEYCLOAK_ADMIN`).

### Mandatory First Steps

1. **Create Realm**: Navigate to the Master realm and create a new realm (e.g., `internal-dev`) for application users to isolate them from the administrative realm.
2. **Configure OIDC Client**:
   - Name: `oauth2-proxy`
   - Access Type: Confidential
   - Valid Redirect URIs: `https://auth.${DEFAULT_URL}/oauth2/callback`
3. **User Provisioning**: Add a standard user with the `admin` role mapping for testing.

## 3. High-Availability State

Keycloak is configured to utilize the Management PostgreSQL instance (`mng-pg`) for persistent state and a distributed Infinispan cache (integrated) for session clustering.

## 4. Maintenance & Integration

| Action | Reference | Link |
| --- | --- | --- |
| **Recovery** | Lockout Flow | [Runbook](../../../runbooks/02-auth/auth-lockout.md) |
| **Usage**    | Secrets Access | [Onboarding](../../../examples/README.md#secrets) |
| **App Link** | OAuth2 Proxy | [Guide](sso-oauth2-proxy-guide.md) |

## 5. Troubleshooting

### "Admin User Locked"

If the administrative user is locked out due to invalid attempts, use the bootstrap runbook: `../../../runbooks/02-auth/auth-lockout.md`.

### "Token Signature Invalid"

Ensure the system time across all Docker nodes is synchronized. OIDC flows are highly sensitive to clock drift.
