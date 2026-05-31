---
name: block-plaintext-secret-compose
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (docker-compose|compose)[^/]*\.ya?ml$|infra/[^/]*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: \b(PASSWORD|SECRET_KEY|API_KEY|ACCESS_TOKEN|PRIVATE_KEY|WEBHOOK_SECRET|DB_PASS(?:WORD)?|POSTGRES_PASSWORD|MYSQL_PASSWORD|REDIS_PASSWORD|GRAFANA_PASSWORD|MARIADB_PASSWORD)(?!_FILE)\s*[:=]\s*(?!\$\{|\$\(\(|/run/secrets/|["']?\$|\s*$|\s*["']{2})[^\s\n"']{6,}
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**Plaintext secret detected in Docker Compose file (project rule)**

`AGENTS.md` — Hard Constraints violation:

> "Never write plaintext secrets; use Docker Secrets or `secrets/` mounts."

`docs/00.agent-governance/rules/quality-standards.md` — Requirements:

> "Never commit plaintext credentials."

**Detected pattern examples:**

```yaml
# BLOCKED: plaintext secrets
environment:
  POSTGRES_PASSWORD: mysecretpassword
  MYSQL_PASSWORD: hunter2
  API_KEY: abc123xyz
```

**Safer alternatives:**

```yaml
# Option 1: Docker Secrets reference
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

# Option 2: environment variable reference, with value injected from .env or outside Compose
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

# Option 3: ignored .env file
env_file:
  - .env
```

**Exclusions:** `_FILE` suffixes, `${...}` variable references, `/run/secrets/`
paths, and empty values are not flagged.

## Related Documents

- `docs/00.agent-governance/README.md`
