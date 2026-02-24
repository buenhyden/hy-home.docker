# HashiCorp Vault Security Guide

> **Component**: `vault`
> **Tier**: `03-security`
> **Internal Port**: `8200`

## 1. Role and Security Posture

Vault provides a unified secret storage backend for the entire platform. It handles identity-based access to tokens, passwords, and certificates.

- **Storage Backend**: Integrated Raft storage or external Consul.
- **API Access**: `http://vault:8200` (Internal).
- **Web UI**: `https://vault.${DEFAULT_URL}`.

## 2. Bootstrapping & Unsealing

Vault starts in an **Uninitialized** state. This is a one-time operation per environment.

### Initialization Workflow

1. Exec into container: `docker exec -it infra-vault sh`.
2. Run: `vault operator init`.
3. **Save**: Record the 5 unseal keys and root token securely.

### Unsealing After Restart

Vault seals itself after every container restart. You MUST unseal it before any dependent application (like Keycloak or App APIs) can fetch secrets.

```bash
vault operator unseal [Key 1]
vault operator unseal [Key 2]
vault operator unseal [Key 3]
```

## 3. Storage Integration

Applications retrieve secrets via the `VAULT_TOKEN` and the KV (Key-Value) v2 secret engine. Use the UI to enable engines and define policies.
