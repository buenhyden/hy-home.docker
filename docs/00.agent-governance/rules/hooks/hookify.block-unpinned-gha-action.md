---
name: block-unpinned-gha-action
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.github/workflows/.*\.ya?ml$
  - field: new_text
    operator: regex_match
    pattern: uses:\s+\S+@(latest|main|master|develop|dev)\b
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**Floating GitHub Actions reference blocked (project rule)**

`docs/00.agent-governance/rules/github-governance.md` — GitHub Actions Security Contract: the workflow uses a floating branch or tag reference.

**Detected pattern:** `uses: owner/action@latest` / `@main` / `@master` / `@develop`

**Why this is risky:**

- External actions can change without review.
- Floating refs increase supply-chain attack exposure.
- Builds are not reproducible.

**Safe alternative:**

```yaml
# BLOCKED: floating reference
- uses: actions/checkout@main
- uses: actions/setup-python@latest

# ALLOWED: pinned version or commit SHA
- uses: actions/checkout@v4.2.2
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Commit SHA pinning is safest. If a version tag is used, prefer digest verification.

## Related Documents

- `docs/00.agent-governance/README.md`
