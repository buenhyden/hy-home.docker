---
title: "GitHub Control Surface"
version: "1.0.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
created: "2026-02-14"
---

# GitHub Control Surface

## Overview

`.github` holds the tracked definitions GitHub itself reads: workflows, the
typed gate registry they run, code ownership, contribution templates, and the
branch-protection proposal. This document is the folder's entry point and routes
readers to each definition, its canonical governance owner, and the local
command that verifies it.

The file is named `repository-surface.md` rather than `README.md` on purpose.
GitHub resolves a repository's displayed README from the root, `.github/`, and
`docs/` in that order, so a `.github/README.md` would compete with the root
[README](../README.md) for the repository landing page.

## Audience

- Maintainers changing a workflow, ruleset, or ownership rule.
- Agents that must locate the authority for a GitHub-side behavior before
  editing it.
- Reviewers confirming that a change to CI matches its declared contract.

## Scope

This surface owns the tracked GitHub definitions and the routes to their
authority. It owns no policy of its own.

- Owned: the inventory below, and the mapping from each definition to its
  canonical owner and its verification command.
- Not owned: GitHub governance policy, which lives in
  [github-governance.md](../docs/00.agent-governance/policies/github-governance.md);
  gate composition, which lives in
  [workflow-contract.yml](./workflow-contract.yml); server-side branch
  protection, which lives in the GitHub project settings and is only proposed
  here.

## Structure

| Path | Role |
| :--- | :--- |
| `workflows/` | Workflow definitions GitHub Actions executes |
| `workflow-contract.yml` | Typed registry of jobs, gate nodes, and public suites |
| `rulesets/` | Branch-protection proposals, applied by hand in project settings |
| `ISSUE_TEMPLATE/` | Issue forms |
| `PULL_REQUEST_TEMPLATE.md` | Pull request body template |
| `CODEOWNERS` | Review routing by path |
| `dependabot.yml` | Dependency update schedule |
| `labeler.yml` | Pull request label routing |
| `SECURITY.md` | Vulnerability reporting route |

## Navigation / Inventory

- [CI quality workflow](./workflows/ci-quality.yml)
- [Typed workflow and gate registry](./workflow-contract.yml)
- [Contributor greeting workflow](./workflows/greetings.yml)
- [Pull request labeler workflow](./workflows/pr-labeler.yml)
- [Stale-thread workflow](./workflows/stale.yml)
- [Release changelog workflow](./workflows/generate-changelog.yml)
- [Tech-stack version sync workflow](./workflows/tech-stack-version-sync.yml)
- [Code ownership](./CODEOWNERS)
- [Pull request template](./PULL_REQUEST_TEMPLATE.md)
- [Label routing](./labeler.yml)

## Verification and Quality Gates

Run these from the repository root before proposing a change to this surface.

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
python3 scripts/validation/check-github-workflow-contract.py
```

- [Typed gate CLI](../scripts/validation/run-ci-gate.py) executes the public
  suites a profile selects.
- [Focused workflow checker](../scripts/validation/check-github-workflow-contract.py)
  validates `workflow-contract.yml` against every tracked workflow definition.
- [Typed local QA gate](../scripts/validation/run-ci-gate.py)
  renders the selected suite-to-validator mapping with `--explain`.

## How to Work in This Area

1. Change the canonical owner first. Edit
   [github-governance.md](../docs/00.agent-governance/policies/github-governance.md)
   when the behavior itself changes → the policy states the new rule.
2. Declare the change in [workflow-contract.yml](./workflow-contract.yml) when
   it adds, removes, or reroutes a job or gate node → the contract names the
   new shape.
3. Edit the workflow definition to match the declaration → the workflow and the
   contract agree field for field.
4. Run `python3 scripts/validation/check-github-workflow-contract.py` → exit
   status `0`.
5. Add the new definition to the inventory above → every tracked file in this
   folder is reachable from this document.

A branch-protection change is proposed in
[rulesets/main-protection.md](./rulesets/main-protection.md) and applied by a
maintainer in GitHub project settings; this repository cannot apply it.

## Related Documents

- [Canonical GitHub governance](../docs/00.agent-governance/policies/github-governance.md)
- [Local main-protection proposal](./rulesets/main-protection.md)
- [Agent governance overview](../docs/00.agent-governance/README.md)
- [Current Stage 00 task checklist](../docs/00.agent-governance/policies/task-checklists.md)
- [Workspace governance authority](../docs/02.architecture/decisions/0029-workspace-governance-authority.md)
- [Repository README](../README.md)
