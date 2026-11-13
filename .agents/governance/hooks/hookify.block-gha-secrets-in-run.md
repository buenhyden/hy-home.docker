---
title: "BLOCKED: prints a secret to logs"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.github/workflows/.*\\.ya?ml$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "(echo|print)\\s+.*\\$\\{\\{\\s*secrets\\.|run:\\s+env\\s*$|\\$\\{\\{\\s*secrets\\.[^}]+\\}\\}\\s*>>\\s*\\$GITHUB_(OUTPUT|ENV|STEP_SUMMARY)"
enabled: true
event: "file"
name: "block-gha-secrets-in-run"
---

# BLOCKED: prints a secret to logs

## Purpose

### Objective

Apply the declared `block` action for block-gha-secrets-in-run.

### Authority

Owning policy: [GitHub governance](../github-governance.md).

## Scope

### Applies To

The `block-gha-secrets-in-run` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: prints a secret to logs"). The frontmatter owns the exact matcher.

### Exclusions

None.

## Rules

### Requirements

**GitHub Actions secret exposure pattern blocked (project rule)**

`.agents/governance/github-governance.md` — GitHub Actions Security Contract: this pattern can expose secrets in workflow logs.

**Detected risky patterns:**

- `echo ${{ secrets.* }}` — prints secrets to logs
- `run: env` — dumps all environment variables, including secrets
- direct writes of secrets to `$GITHUB_OUTPUT` or `$GITHUB_ENV`

**Why this rule blocks:**

- GitHub Actions logs are retained.
- Exposed secrets can bypass masking.
- `github-governance.md` prohibits secrets in log output.

**Safe alternative:**

```yaml
# BLOCKED: prints a secret to logs

- run: echo ${{ secrets.API_KEY }}

# ALLOWED: passes the secret as a masked environment variable
- run: ./script.sh
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

Prefer OIDC-based cloud credentials over long-lived repository secrets.

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
