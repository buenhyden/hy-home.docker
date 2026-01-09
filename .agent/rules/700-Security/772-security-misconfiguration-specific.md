---
trigger: always_on
glob: "**/*.{py,js,ts,go,java,json,yaml,yml}"
description: "Security Misconfiguration (OWASP A05): Secure headers, debug modes, and configurations."
---
# Security Misconfiguration Standards (OWASP A05)

## 1. Debug Mode

- **Production**: NEVER run with `DEBUG=True` or `development` mode in production.
- **Error Messages**: Do not expose stack traces to end-users. Log them internally; show a generic error page.

## 2. Security Headers

Enforce the following headers on all responses:

- **HSTS**: `Strict-Transport-Security: max-age=31536000; includeSubDomains` (Force HTTPS).
- **CSP**: `Content-Security-Policy`. strict whitelisting of scripts/styles/images.
- **Frame**: `X-Frame-Options: DENY` (Prevent Clickjacking).
- **Content Type**: `X-Content-Type-Options: nosniff`.

## 3. Cookie Configuration

- **Attributes**: `Secure`, `HttpOnly`, `SameSite=Strict` (or `Lax`).
- **Scope**: Scope cookies to the specific domain/path.

## 4. Permissions & Ports

- **Least Privilege**: Run applications as a non-root user.
- **Files**: Restrict file permissions (e.g., `chmod 600` for config secrets).
- **Ports**: Close unnecessary ports. Expose only the required application port (e.g., 443/80).

## 5. Dependency Management

- **Updates**: Keep frameworks and libraries updated.
- **Unused**: Remove unused features, endpoints, and libraries to reduce attack surface.
