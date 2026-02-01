# Security (03-security)

## Overview

Secrets and security services. Currently **Vault** is provided as an optional stack to centralize secrets, encryption, and PKI.

## Services

| Service | Profile | Path      | Purpose                                |
| ------- | ------- | --------- | -------------------------------------- |
| Vault   | `vault` | `./vault` | Secret management, encryption, and PKI |

## Run

```bash
docker compose --profile vault up -d vault
```

## Notes

- Vault requires **initialization and unseal** before it can be used.
- TLS assets can be mounted from `secrets/certs` for HTTPS.

## File Map

| Path        | Description               |
| ----------- | ------------------------- |
| `vault/`    | Vault service and config. |
| `README.md` | Category overview.        |
