---
title: "BLOCKED: plaintext secrets"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(docker-compose|compose)[^/]*\\.ya?ml$|infra/[^/]*\\.ya?ml$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "\\b(PASSWORD|SECRET_KEY|API_KEY|ACCESS_TOKEN|PRIVATE_KEY|WEBHOOK_SECRET|DB_PASS(?:WORD)?|POSTGRES_PASSWORD|MYSQL_PASSWORD|REDIS_PASSWORD|GRAFANA_PASSWORD|MARIADB_PASSWORD)(?!_FILE)\\s*[:=]\\s*(?!\\$\\{|\\$\\(\\(|/run/secrets/|[\"']?\\$|\\s*$|\\s*[\"']{2})[^\\s\\n\"']{6,}"
enabled: true
event: "file"
name: "block-plaintext-secret-compose"
---

# BLOCKED: plaintext secrets

## Purpose

### Objective

Apply the declared `block` action for block-plaintext-secret-compose.

### Authority

Owning policies:

- [Agent Bootstrap Policy](../bootstrap.md#hard-constraints)
- [Environment constraints](../environment-constraints.md)
- [Quality standards](../quality-standards.md)

## Scope

### Applies To

The `block-plaintext-secret-compose` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: plaintext secrets"). The frontmatter owns the exact matcher.

### Exclusions

**Exclusions:** `_FILE` suffixes, `${...}` variable references, `/run/secrets/`
paths, and empty values are not flagged.

## Rules

### Requirements

**Plaintext secret detected in Docker Compose file (project rule)**

`.agents/governance/bootstrap.md#hard-constraints`:

> "Never write plaintext credentials or secret values."

`.agents/governance/environment-constraints.md` — Security:

> "Deliver credentials through Docker Secrets or `secrets/` mounts, never as
> plaintext values."

`.agents/governance/quality-standards.md` — Requirements:

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

The declared action applies when the pattern matches.

### Enforcement

Native event delivery is a separate observation from the frontmatter match.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

`.agents/README.md`.
