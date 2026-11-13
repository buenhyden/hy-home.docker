---
title: "WARNING: manual pre-commit execution"
version: "1.1.3"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
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

Owning policy: [Quality standards execution boundary](../quality-standards.md#4-execution-boundary).

## Scope

### Applies To

The `warn-pre-commit-manual` rule applies on the `bash` event. `.agents/governance/quality-standards.md#4-execution-boundary` owns this
boundary: agents never run `pre-commit run` directly. An explicitly approved
all-files gate uses only its controlled route and conditions. The admitted
scoped route immediately before local commit is
`scripts/validation/run-ci-precommit.sh --mode local-staged`; server PR checks
use its authenticated `--mode pr-merge` route.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

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

# Check the reviewed index immediately before an ordinary commit.
scripts/validation/run-ci-precommit.sh --mode local-staged
git commit -m "feat(scope): My change"
```

If lint or format issues exist, fix the affected files directly before committing.

### Enforcement

The declared Bash event and unchanged native pattern identify matching commands.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None: this document states no separate approval or review step.

## Ownership

### Responsibilities

The rule owner is `@buenhyden`.

### Change and Adoption

None: this document states no separate change or adoption step.
