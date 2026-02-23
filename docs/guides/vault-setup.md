# HashiCorp Vault Setup Guide

> Comprehensive guide on initializing, unsealing, and utilizing HashiCorp Vault for local infrastructure secrets.

## 1. Introduction

HashiCorp Vault operates within the `infra/03-security/vault/docker-compose.yml` stack. It provides a secure mechanism for managing tokens, passwords, certificates, and encryption keys across the `infra_net` environment.

## 2. Server Initialization

> [!IMPORTANT]
> A fresh Vault deployment starts in an **Unitialized** state. You must initialize it to generate the master keys and initial root token.

1. Deploy the stack:

```bash
docker compose -f infra/03-security/vault/docker-compose.yml up -d
```

1. Exec into the running Vault container:

```bash
docker exec -it vault sh
```

1. Initialize the server:

```bash
vault operator init
```

🚨 **CRITICAL**: The console will output `Unseal Key 1..5` and the `Initial Root Token`. Copy these immediately and store them in a secure offline password manager. They will NOT be shown again.

## 3. Unsealing Workflow

Vault enters a **Sealed** state upon initialization and every subsequent restart. It cannot serve requests until unsealed.

1. Run the unseal command inside the container:

```bash
vault operator unseal <Unseal Key 1>
vault operator unseal <Unseal Key 2>
vault operator unseal <Unseal Key 3>
```

Once the threshold (usually 3 of 5 keys) is reached, Vault becomes unsealed.

## 4. Basic Operation via UI

To interact graphically with Vault:

1. Navigate to the designated endpoint routed via Traefik (e.g., `https://vault.${DEFAULT_URL}`).
2. Wait for the Traefik middleware to successfully redirect.
3. Authenticate to the Vault UI utilizing the `Initial Root Token` or an identity provider method if configured.
4. Enable Secret Engines (e.g., KV v2) within the Secrets tab.

## 5. Connecting Services to Vault

Applications deployed in `infra_net` can access Vault internally via `http://vault:8200` utilizing the appropriate `VAULT_TOKEN` environment variable passed into the respective docker-compose files.
