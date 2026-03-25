# Mail Operations Policy

Governance and standard operating procedures for the `10-communication` tier.

## 1. Governance

- **Service Ownership**: The communication tier is managed as a shared infrastructure service.
- **Access Control**: Admin UIs for Stalwart and MailHog are protected via Traefik Middlewares (SSO/Basic Auth).
- **Relay Rules**: Unauthorized relaying is strictly prohibited and must be disabled in Stalwart configuration.

## 2. Persistence & Backups

- **Data Retention**: Stalwart data is persisted in `${DEFAULT_COMMUNICATION_DIR}`.
- **Backup Schedule**: Weekly snapshots of the `stalwart-data` volume are mandatory.
- **MailHog Data**: No data retention policy exists for MailHog; it is exclusively for transient development traffic.

## 3. Security Standards

- **TLS/SSL**: All mail traffic (IMAPS/SMTPS) MUST use valid certificates from the project's secret store.
- **Secrets Management**: Admin passwords MUST be stored in Docker secrets and never hardcoded in compose files.
- **Spam Control**: Stalwart's built-in spam filters should be kept up to date.
