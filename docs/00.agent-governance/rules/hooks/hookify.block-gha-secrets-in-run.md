---
name: block-gha-secrets-in-run
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/.*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: (echo|print)\s+.*\$\{\{\s*secrets\.|run:\s+env\s*$|\$\{\{\s*secrets\.[^}]+\}\}\s*>>\s*\$GITHUB_(OUTPUT|ENV|STEP_SUMMARY)
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**GitHub Actions secret exposure pattern blocked (project rule)**

`docs/00.agent-governance/rules/github-governance.md` — GitHub Actions Security Contract: this pattern can expose secrets in workflow logs.

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

## Related Documents

- `docs/00.agent-governance/README.md`
