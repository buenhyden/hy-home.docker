---
layer: infra
---

# Communication Tier: Setup & Initialization

This guide covers the initial bootstrap and configuration for the mail server stack.

## 1. Prerequisites

### Directories
Ensure the host paths for persistence exist:
```bash
mkdir -p "${DEFAULT_COMMUNICATION_DIR}/stalwart/data"
```

### Secrets
Ensure the following secret file is created:
- `secrets/common/stalwart_password.txt`

## 2. Bootstrapping Services

### Initial Startup
```bash
# Start the communication profile
docker compose --profile communication up -d
```

### Stalwart Initialization
1. Navigate to `https://mail.${DEFAULT_URL}`.
2. Log in with `admin` and your secret password.
3. Complete the SMTP relay and DKIM configuration via the web UI.

## 3. Post-Setup Verification
```bash
# Verify SMTP port is listening
docker exec -it stalwart nc -zv localhost 25
```
