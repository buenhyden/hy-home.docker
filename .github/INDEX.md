---
profile_id: github-navigation-index
---

# GitHub Control Surface Index

## Purpose

This navigation-only index routes readers to the tracked GitHub definitions,
their canonical governance owner, local verification, and dated observation
evidence.

## Surface Map

- [CI quality workflow](./workflows/ci-quality.yml)
- [Typed workflow and gate registry](./workflow-contract.yml)
- [Document corpus lifecycle workflow](./workflows/document-corpus-lifecycle.yml)
- [Contributor greeting workflow](./workflows/greetings.yml)
- [Pull request labeler workflow](./workflows/pr-labeler.yml)
- [Stale-thread workflow](./workflows/stale.yml)
- [Release changelog workflow](./workflows/generate-changelog.yml)
- [Tech-stack version sync workflow](./workflows/tech-stack-version-sync.yml)
- [Code ownership](./CODEOWNERS)
- [Pull request template](./PULL_REQUEST_TEMPLATE.md)
- [Label routing](./labeler.yml)

## Authority and Change Routes

- [Canonical GitHub governance](../docs/00.agent-governance/policies/github-governance.md)
- [Local main-protection proposal](./rulesets/main-protection.md)
- [Dated GitHub Actions observation](../docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml)

## Verification

- [Typed gate CLI](../scripts/validation/run-ci-gate.py)
- [Local QA profile wrapper](../scripts/validation/run-local-qa-gates.sh)
- [Repository contract checker](../scripts/validation/check-repo-contracts.sh)
- [Focused workflow checker](../scripts/validation/check-github-workflow-contract.py)

## Related Documents

- [Agent governance overview](../docs/00.agent-governance/README.md)
- [Current Stage 00 task evidence](../docs/03.specs/0153-workspace-governance-simplification/tasks/tsk-0004-stage00.md)
- [Active convergence task](../docs/03.specs/0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md)
