---
title: "BLOCKED: prints a secret to logs"
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
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

## Overview

Apply the declared `block` action for block-gha-secrets-in-run.

## Scope

`file` 이벤트의 `block-gha-secrets-in-run` 규칙에 적용한다. 정확한 matcher는 이 문서의 frontmatter가 소유한다.

## Rules

**GitHub Actions secret exposure pattern blocked (project rule)**

`.agents/governance/github-governance.md` — GitHub Actions Security Contract: this pattern can expose secrets in workflow logs.

**Detected risky patterns:**

- `echo ${{ secrets.* }}` — prints secrets to logs
- `run: env` — dumps all environment variables, including secrets
- direct writes of secrets to `$GITHUB_OUTPUT` or `$GITHUB_ENV`

**Why this is BLOCK-severity:**

- GitHub Actions logs are retained.
- Exposed secrets can bypass masking.
- This is an explicit BLOCK-severity violation in `github-governance.md`.

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

## Exceptions

No exception is declared by this rule.

## Verification

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
