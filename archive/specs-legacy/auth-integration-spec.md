# Authentication Integration Specification

**Identifier:** `SPEC-AUTH-01`
**Domain:** Security & Access Control
**Status:** Active

## Objective

Define the Single Sign-On (SSO) architecture leveraging Traefik default middlewares, Keycloak as the Identity Provider (IdP), and OAuth2-Proxy for protecting internal applications.

## Component Flow

1. **User requests protected route:** e.g., `https://dashboard.local.dev`.
2. **Traefik Interception:** Traefik checks the `middlewares=sso-auth@file` label.
3. **ForwardAuth:** The request is bounced to OAuth2-Proxy (`auth.local.dev`).
4. **Validation:** If a valid session cookie exists, the request proceeds. If not, OAuth2-Proxy redirects the user to Keycloak.
5. **Keycloak Authentication:** The user authenticates (credentials + optional MFA) via realm `hy-home.realm`.
6. **Callback:** Keycloak returns a token to OAuth2-Proxy which sets the user cookie and proxy-forwards identity headers to the target app.

## Security Constraints

- **Realm Configuration:** All internal services share the `hy-home.realm`.
- **RBAC Mapping:** Authorization logic relies exclusively on Keycloak `groups`.
  - For Grafana, the OAuth mapping specifically checks for `contains(groups[*], '/admins')` to grant the `Admin` role.
- **Header Forwarding:** Applications should trust the `X-Forwarded-User` or `X-Forwarded-Email` headers passed down by OAuth2-Proxy.

## Deployment Requirements

Keycloak (`02-auth`) must expose its `protocol/openid-connect` endpoints securely, with TLS termination handled by Traefik. Inter-service token validation skips insecure verifying ONLY on internal docker bridge paths, otherwise PKCE (Proof Key for Code Exchange) is strictly enforced for OAuth clients.
