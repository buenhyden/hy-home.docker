---
title: "BLOCKED: secret content read"
version: "1.0.0"
type: "governance/rule"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-19"
action: "block"
enabled: true
event: "bash"
name: "block-secret-content-read"
pattern: "(?:(?:^|[;&|(`]|\\$\\()\\s*(?:sudo\\s+)?(?:cat|tac|head|tail|less|more|bat|grep|egrep|fgrep|rg|sed|awk|cut|sort|uniq|nl|xxd|od|hexdump|strings|base64|diff|cmp|jq|yq|source)\\b[^;&|\\n]*?(?<=[\\s/])(?:[^\\s;&|'\\\"<>()]*/)?(?:secrets/[^\\s;&|'\\\"<>()]*[^\\s;&|'\\\"<>()/]|\\.env(?:\\.(?!example\\b)[\\w-]+)?)(?=[\\s;&|)]|$))|(?:<\\s*(?:[^\\s;&|'\\\"<>()]*/)?(?:secrets/[^\\s;&|'\\\"<>()]*[^\\s;&|'\\\"<>()/]|\\.env(?:\\.(?!example\\b)[\\w-]+)?)(?=[\\s;&|)]|$))"
---

# BLOCKED: secret content read

## Purpose

### Objective

Apply the declared `block` action for block-secret-content-read.

### Authority

[Environment constraints](../environment-constraints.md#22-approved-secrets-work-protocol),
ENVIRONMENT-CONSTRAINTS-R34 and R164: an agent never prints or quotes a
secret value, so a shell command does not read the content of a secret
file or an environment file.

## Scope

### Applies To

The declared `bash` event and `pattern` match a command whose reader
(`cat`, `head`, `tail`, `less`, `grep`, `rg`, `sed`, `awk`, `cut`, `sort`,
`xxd`, `od`, `strings`, `base64`, `diff`, `jq`, `source` and similar) names
a file under a `secrets/` directory or a `.env` file other than
`.env.example`, or that redirects such a file into a command with `<`.

### Exclusions

Metadata stays allowed: listing, finding, `stat`, `test` and `wc -c`, a
quoted search term such as `grep -rn '.env' docs`, `.env.example`, and a
tool that reads the file itself, such as `docker compose --env-file .env`.

## Rules

### Requirements

```bash
# BLOCKED: secret or environment file content
cat secrets/db/mng-pg/password.txt
grep -n KEY .env

# ALLOWED: metadata only
ls -la secrets/db
test -s secrets/db/password.txt
```

The declared action applies when the pattern matches.

### Enforcement

The shared dispatcher evaluates the rule before a provider runs the command,
for both providers. It sees the command text only: a quoted path, a path
built at run time, a variable, a script that reads the file, or a hook
bypass is outside it. On a provider with its own read deny, that deny still
applies.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

Changes land with their Task evidence and the rule test
`tests/lib/hooks/test_secret_read_rule.py`.
