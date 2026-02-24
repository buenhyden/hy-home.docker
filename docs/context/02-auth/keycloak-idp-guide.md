# Keycloak Identity Provider (IdP) Guide

> **Component**: `keycloak`
> **Internal Port**: `8080`
> **Administrative Path**: `https://keycloak.${DEFAULT_URL}`

## 1. Identity & Access Management Core

Keycloak serves as the primary OIDC and SAML identity provider for the entire platform. It manages user lifecycles, roles, and client authentication.

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

## 4. Troubleshooting

### "Admin User Locked"

If the administrative user is locked out due to invalid attempts, use the bootstrap runbook: `runbooks/02-auth/auth-lockout.md`.

### "Token Signature Invalid"

Ensure the system time across all Docker nodes is synchronized. OIDC flows are highly sensitive to clock drift.
