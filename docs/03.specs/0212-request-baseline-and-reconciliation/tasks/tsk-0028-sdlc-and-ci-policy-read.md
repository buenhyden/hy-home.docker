---
title: "SDLC and CI Policy Read Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0028"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# SDLC and CI Policy Read Task

## Overview

### Objective

Execute W44: read the SDLC policy and the CI/QA policy against the code and
workflows that enforce them, and apply the owner's choice on the one naming
gap found. This Task owns criterion 39 only.

## Inputs and Authorization

On 2026-10-29 the owner asked for the SDLC area and then the CI/QA area to be
read after the archive read in TSK-0027, and chose to rename the release
workflow. The input is `main` at merged PR #625. The authorization covers the
rename and its current references, this branch, its pull request, and merge.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0028 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0028 | ready | in-progress | #objective |
| SPEC-0212-TSK-0028 | in-progress | completed | #evidence |

### SDLC read

| Statement in `.agents/governance/sdlc.md` | Checked against | Result |
| --- | --- | --- |
| Family lifecycle states for requirements, architecture descriptions, operational guidance, ADRs, Specs, Plans, Tasks, navigation READMEs, and route records | Registry `lifecycles` | Matches |
| Evidence `Required` is `required` or `optional` | `spec_packages.py` evidence parser | Matches |
| Current Result vocabulary | Registry `result_domain` | Matches; the `DEFER` set is the generation-5 reader only |
| Acceptance decisions | Registry `acceptance_domain` | Matches |
| A Plan is never ahead of or terminal before its Spec; a Task runs only while both parents are `approved` | `spec_packages.py` parent-order checks | Matches |
| A multi-item Task has at least two rows, covers its Work Units, and declares no frontmatter `status` | `spec_packages.py` item checks | Matches |

### CI/QA read

| Statement | Source | Checked against | Result |
| --- | --- | --- | --- |
| One PR candidate job with no path skip; main push is a separate security observation | `quality-standards.md` delivery matrix | `ci-quality.yml` triggers and job conditions | Matches |
| One main-only SemVer release producer with `v` tags | `git-workflow.md`, runbook 0009 | Release workflow and `release.py` tag function | Matches |
| Commit checks never rewrite; fixers are manual | `quality-standards.md` §10 | `.pre-commit-config.yaml` hook stages and arguments | Matches |
| Every formatter has a `files` selector; `ruff.toml` pins Python; `.prettierignore` states the Prettier boundary | `quality-standards.md` §10 | Hooks, `ruff.toml`, `.prettierignore` | Matches |
| Use a merge commit or fast-forward for referenced commits | `github-governance.md` | Repository merge settings (TSK-0018) | Matches |

### Release workflow rename

The release producer was named `generate-changelog.yml` while it publishes a
release and generates no changelog, which suggested the automatic changelog
that policy forbids. It is now `.github/workflows/publish-release.yml`. The
current references in `.github/repository-surface.md`,
`.github/workflow-contract.yml`, `scripts/manifest.yaml`, runbook 0009, and two
tests use the new name, and the workflow records stay path-sorted. Completed
Task bodies, the dated research pack, and frozen archive bodies keep the old
name as history. GitHub tracks run history per workflow file, so earlier runs
stay under the old name.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Workflow contract | 39 | W44 | `check-github-workflow-contract.py` | This branch | PASS | 5 workflows, 7 jobs, 9 actions | required | - |
| Gate and release tests | 39 | W44 | `python3 -m unittest tests.lib.gate.test_github_workflow_contract tests.validation.test_ci_gate_plan tests.validation.test_agent_governance_ci_routing tests.lib.gate.test_ci_gate_adapters tests.validation.test_release` | This branch | PASS | 237 tests OK | required | - |
| Script manifest | 39 | W44 | `check-script-manifest.py` | This branch | PASS | Valid | required | - |
| Metadata contracts | 39 | W44 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 39 | accepted | Workflow contract, Gate and release tests, Script manifest, Metadata contracts | The SDLC and CI/QA policy text matches its code; the release workflow name now matches what it does. | SPEC-0212 TSK-0028 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
