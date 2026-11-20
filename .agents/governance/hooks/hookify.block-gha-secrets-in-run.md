---
title: "BLOCKED: prints a secret to logs"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'BLOCKED: prints a secret to logs'
  layer: agent
updated: "2026-11-20"
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

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the rule payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Objective

Apply the declared `block` action for block-gha-secrets-in-run.

##### Authority

Owning policy: [GitHub governance](../../../docs/00.workspace/03.process/github-governance.md).

#### Scope

##### Applies To

The `block-gha-secrets-in-run` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: prints a secret to logs"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**GitHub Actions secret exposure pattern blocked (project rule)**

`docs/00.workspace/03.process/github-governance.md` — GitHub Actions Security Contract: this pattern can expose secrets in workflow logs.

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

##### Enforcement

Native event delivery is a separate observation from the frontmatter match.

#### Exceptions

##### Exception Conditions

No exception is declared by this rule.

##### Approval and Review

None.

#### Ownership

##### Responsibilities

`@buenhyden`.

##### Change and Adoption

`.agents/README.md`.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
