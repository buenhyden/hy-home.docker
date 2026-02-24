# Security (03-security)

This category manages secret storage, encryption-as-a-service, and security auditing.

## Services

| Service | Profile | Path      | Purpose                                     |
| ------- | ------- | --------- | ------------------------------------------- |
| Vault   | `vault` | `./vault` | Central secret management and transit encryption |

## Dependencies

- **Consul/Storage**: Vault requires a storage backend (configured to use internal filesystem or shared DB).
- **Gateway**: Exposed via Traefik at `vault.${DEFAULT_URL}`.

## File Map

| Path        | Description                               |
| ----------- | ----------------------------------------- |
| `vault/`    | Vault service and configuration policies. |
| `README.md` | Category overview.                        |
