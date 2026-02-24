# Runbook: Vault Sealed / Key Loss

> Incident response procedure for when HashiCorp Vault is sealed, locked, or keys are inaccessible.

## Context

Vault mandates its storage backend is completely encrypted. The decryption keys exist only in memory, created by providing a quorum of "Unseal Keys". If the container restarts or crashes, it purges memory, falling back into a "Sealed" state rejecting all API traffic.

## Symptoms

- HTTP 503 "Vault is sealed" responses from the Vault API `/v1/sys/health`.
- Applications throwing 500 error codes complaining about inaccessible credentials.
- Vault UI only displays an unseal prompt rather than a login page.

## Resolution Steps

### Method 1: Standard Quorum Unseal

1. Log in to the Host / WSL running the infrastructure.
2. Formulate an execution loop using the stored unseal keys.

```bash
docker exec -it vault vault operator unseal
# Paste Key 1 when prompted

docker exec -it vault vault operator unseal
# Paste Key 2 when prompted

docker exec -it vault vault operator unseal
# Paste Key 3 when prompted
```

1. Run `docker exec -it vault vault status` and ensure `Sealed` reads `false`.

### Method 2: Handling Unknown / Lost Keys

> [!CAUTION]
> If all Unseal keys are irretrievably lost while Vault is sealed, **your data is permanently cryptographically destroyed.**

There is no backdoor recovery mechanism. You must re-initialize the server fresh:

1. Stop the active stack.

```bash
docker compose -f infra/03-security/vault/docker-compose.yml down
```

1. Identify the local volume mapped to Vault data (`vault-data:/vault/file`) and purge it:

```bash
docker volume rm infra_vault-data
```

1. Restart the container stack and execute Step 2 from `vault-setup.md` to run `vault operator init` and record the generated keys correctly this time.
2. Redeposit the lost secrets from a trusted external backup source.
