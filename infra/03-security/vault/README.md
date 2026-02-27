# vault

# Vault

HashiCorp Vault is an identity-based secrets and encryption management system.

## Services

| Service | Image | Role | Resources | Profile |
| :--- | :--- | :--- | :--- | :--- |
| `vault` | `hashicorp/vault:1.21.2` | Secret Management | Default | `vault` |

## Networking

- **Port**: `${VAULT_PORT}` (internal) / `${VAULT_HOST_PORT}` (host)
- **External URL**: `https://vault.${DEFAULT_URL}` (via Traefik, if included/routed)

## Security

- **Hardening**: `no-new-privileges:true`, `read_only: false` (due to local file backend).
- **Capabilities**: `IPC_LOCK` added to prevent sensitive data from being swapped to disk.

## Persistence

- **Data**: `vault-data` volume mapped to `/vault/file`.
- **Config**: Local `./config` mapped to `/vault/config`.

## File Map

| Path | Description |
| :--- | :--- |
| `config/` | Vault policies and config files. |
| `README.md` | Service overview and policy docs. |
