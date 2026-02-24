# vault

HashiCorp Vault provides secure secret storage and management.

## Services

| Service | Image                  | Role           | Resources         |
| :------ | :--------------------- | :------------- | :---------------- |
| `vault` | `hashicorp/vault:latest`| Secret Engine  | 0.5 CPU / 1GB RAM |

## Networking

Exposed via Traefik at `vault.${DEFAULT_URL}` with TLS.

## Persistence

- **Storage**: Filesystem backend (default) or shared PostgreSQL.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `config/`   | Vault policies and config files.    |
| `README.md` | Service overview and policy docs.   |
