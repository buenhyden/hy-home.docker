---
title: "Superset Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0097"
parent_ids:
- "GDE-0097"
created: "2026-09-23"
---

# Superset Runbook

## When to Use

First setup, a login that fails, the web server not becoming healthy, or an
upgrade.

## Procedure

1. First setup (each step approved; values never enter a log or a document):
   1. Keycloak realm `hy-home.realm`: create the confidential client
      `home-superset` with standard flow only, PKCE `S256`, redirect URI
      `https://superset.${DEFAULT_URL}/oauth-authorized/keycloak` and web
      origin `https://superset.${DEFAULT_URL}`.
   2. Store its client secret as `secrets/auth/superset_oidc_client_secret.txt`
      (IAM-013, one line, mode `0640`).
   3. `bash scripts/operations/gen-secrets.sh --sync-metadata`, then
      `bash scripts/operations/gen-secrets.sh` to create PG-028 and AUTO-020.
   4. `docker compose --profile bi build superset`, then
      `docker compose --profile bi up -d superset`.
   5. Before the first login of the administrator:
      `docker compose --profile bi exec superset superset fab create-admin --username <keycloak username> --firstname <first> --lastname <last> --email <email> --password "$(openssl rand -base64 24)"`.
      The generated password is unusable (there is no form login) and is not
      kept; OIDC matches the user name.
2. Inspect: `docker compose --profile bi logs --tail=100 superset-db-provision superset-init superset`.
3. `superset: secret … must be one non-empty line`: the named secret file is
   empty or has several lines.
4. Login returns to Superset with an error: check the redirect URI and client
   secret in Keycloak, then that `keycloak.${DEFAULT_URL}` resolves to Traefik
   from the container and that `${DEFAULT_CERT_DIR}/rootCA.pem` is mounted.
5. A logged-in user sees no data: the user is `Gamma`; an Admin grants a role.
6. Upgrade: rebuild, `docker compose --profile bi run --rm superset-init`,
   then recreate `superset`.

## Evidence

Record client ID, role names, user names granted Admin, exit codes and the
source commit; never a secret, token or session cookie.

## Rollback or Recovery

The metadata database is part of the `mng-pg` pgBackRest set (RUN-0021).
Before an upgrade, take a backup; a failed migration is recovered by restoring
it and starting the previous image.

## Escalation

Stop on any request to enable form login, grant `Admin` on registration,
publish a host port or put a credential in the environment.

## Traceability

- [Guide](../guides/0097-superset.md) (`GDE-0097`)
- [Policy](../policies/0097-superset.md) (`POL-0097`)
- [Keycloak runbook](0014-keycloak.md)

## Related Documents

- [Superset package README](../../../infra/04-data/analytics/superset/README.md)
- [Superset Compose source](../../../infra/04-data/analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Backup and restore runbook](0021-backup-and-restore.md)
