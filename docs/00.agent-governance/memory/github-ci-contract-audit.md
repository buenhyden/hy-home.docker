---
layer: agentic
---

# Memory: GitHub CI Contract Audit

- Date: 2026-05-09
- Layer: infra
- Status: active
- Applies To: `.github/workflows/`, `.github/rulesets/`, CI contract checks
- Tags: #github #ci #qa #governance
- Retrieval Keywords: GitHub CI contract, workflow permissions, branch ruleset, compose profile validation
- Last Verified: 2026-05-10

## Problem

The `.github/` audit found no duplicate workflow, job, or step definitions, but
the local governance policy assumed protected `main` branch enforcement that was
not represented by a local ruleset proposal. CI also validated the default
`core` Compose profile but did not prove that every declared profile could be
resolved by Docker Compose.

## Context

- `.github/workflows/ci-quality.yml` is the canonical QA gate workflow.
- Community workflows for greetings, stale threads, and PR labeling are triage
  automation, not QA gates.
- The pre-change remote audit observed no repository rulesets and no `main`
  branch protection.
- Full-profile Compose config validation passed, while full-profile QuickWin
  and security baselines still have known hardening gaps.

## Resolution

- Added all-profile Compose config validation to CI without promoting
  full-profile hardening baselines to required checks.
- Added a local `main` branch ruleset proposal under `.github/rulesets/`.
- Required top-level workflow permissions and the expected CI job inventory in
  `scripts/check-repo-contracts.sh`.
- Kept community automation workflows and made their default token permissions
  explicit.

## Prevention

- Keep `.github/workflows/ci-quality.yml` as the CI/QA job inventory source.
- Do not add GitHub-native agent instruction files unless repository governance
  explicitly adopts that layer.
- Apply remote branch protection or rulesets only after explicit owner approval.
- Treat all-profile QuickWin/security failures as separate infra hardening work,
  not as hidden CI contract drift.

## Evidence

- `.github/workflows/ci-quality.yml`
- `.github/rulesets/`
- `scripts/check-repo-contracts.sh`
- `scripts/validate-docker-compose.sh`
