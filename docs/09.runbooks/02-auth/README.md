# Auth Tier Runbook (02-auth)

<!-- [ID:docs:09:02-auth:README] -->
: Maintenance and emergency recovery procedures.

---

## Troubleshooting Procedures

### 1. Admin Account Lockout
If the admin account is locked due to MFA or password loss:
1. Access the container shell: `docker exec -it keycloak /bin/bash`.
2. Use the JBoss/Keycloak admin CLI to reset the user or disable MFA.
3. Refer to the internal **[Lockout Guide]** (Legacy) if available.

### 2. Database Connection Failure
Symptoms: Keycloak stays in "starting" state or logs `Failed to obtain JDBC connection`.
1. Check `mng-pg` status: `docker compose ps mng-pg`.
2. Verify credentials in `keycloak_db_password` secret match the database setup.
3. Check network connectivity: `docker exec keycloak nc -zv mng-pg 5432`.

### 3. OAuth2 Proxy Redirect Loops
Symptoms: Browser infinite redirect between application and Keycloak.
1. Clear browser cookies.
2. Verify `redirect_uri` in Keycloak client settings matches `https://auth.${DEFAULT_URL}/oauth2/callback`.
3. Check if `OAUTH2_PROXY_COOKIE_DOMAIN` is correctly scoped.

## Routine Maintenance

### Certificate Rotation
When `rootCA.pem` or service certs are updated:
1. Reload Traefik.
2. OAuth2 Proxy might need a restart if it caches the cert: `docker compose restart oauth2-proxy`.

### Metrics & Observability
- **Keycloak metrics**: `http://keycloak:9000/metrics`.
- **Alerting**: Trigger if the count of 4xx responses in Traefik exceeds 5% of gateway traffic.
