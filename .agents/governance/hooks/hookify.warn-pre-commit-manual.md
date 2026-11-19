---
title: "WARNING: manual pre-commit execution"
version: "1.1.6"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-19"
action: "warn"
enabled: true
event: "bash"
name: "warn-pre-commit-manual"
pattern: "pre-commit\\s+run"
---

# Manual Pre-commit Execution Warning

## Purpose

### Objective

**Manual `pre-commit run` detected (project rule)**

### Authority

Owning policy: [Quality standards execution boundary](../../../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary).

## Scope

### Applies To

Bash commands matching the frontmatter pattern.

### Exclusions

None.

## Rules

### Requirements

Agents never run `pre-commit run` directly. Use the observed installed hooks
for an ordinary commit. When installed delivery is unconfirmed or diagnosis is
needed, use `scripts/validation/run-ci-precommit.sh --mode local-staged`. Server
PR checks use the authenticated `--mode pr-merge` route.

**Project pre-commit policy:**

- Manual runs can create inconsistent evidence.
- Installed commit-hook delivery must be observed separately; this warning does
  not claim it ran automatically for a particular commit.
- Remote candidate validation uses the registered read-only changed-style
  controller; routine CI does not run an all-files formatter.

**Detected forms and normal commit path:**

```bash
# WARNING: manual pre-commit execution is prohibited for agents
pre-commit run --all-files
pre-commit run --files myfile.py

# Let the installed hooks check the reviewed index and message.
git commit -m "feat(scope): My change"
```

If lint or format issues exist, fix the affected files directly before committing.

### Enforcement

The declared Bash event and unchanged native pattern identify matching commands.

## Exceptions

### Exception Conditions

An explicitly approved all-files gate uses only its controlled route and conditions.

### Approval and Review

That gate needs explicit approval under the execution boundary.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

None.
