---
title: "CI Quality Version Alignment and Workflow Audit"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0006"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
- "SPEC-0180-TSK-0005"
created: "2026-09-20"
---

# CI Quality Version Alignment and Workflow Audit

## Objective

Analyze the PR #169 hosted Hadolint failure, align the Docker-image executable
with the declared pre-commit release, and record an evidence-led GitHub Actions
CI/CD review. This Task covers tracked CI configuration and documentation only.
It does not authorize a merge, deployment, GitHub setting change, credential
change, or workflow deletion.

## Inputs

- Merged main baseline `534d163784bff7d776bf1d511e2e98ce1956a37c` and isolated
  branch `codex/ci-version-alignment`.
- Failed required PR check: run `35478388330`, job `105991565187`, whose
  all-files pre-commit leaf reported Hadolint `DL3066` for the Airflow and
  ComfyUI Dockerfiles.
- `.github/workflows/ci-quality.yml`, `.github/workflow-contract.yml`,
  `.pre-commit-config.yaml`, `.hadolint.yaml`, gate adapters, and regression
  tests.
- [Hadolint v2.14.0 hook manifest](https://raw.githubusercontent.com/hadolint/hadolint/v2.14.0/.pre-commit-hooks.yaml), [GitHub pull-request event activity types](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [GitHub Actions concurrency documentation](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency), [Renovate pre-commit manager](https://docs.renovatebot.com/modules/manager/pre-commit/), and [GitHub workflow disable/enable guidance](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).
- [Task 0005](tsk-0005-current-main-convergence.md) for prior PR #169 evidence.

## Work Log

### Observed failure and root cause

- The local correction used official Hadolint `2.14.0` and passed its Dockerfile
  checks. The later hosted run used the untagged
  `ghcr.io/hadolint/hadolint` Docker image supplied by the upstream
  `hadolint-docker` hook and reported two `DL3066` findings.
- `.pre-commit-config.yaml` declared repository revision `v2.14.0`, but the
  upstream Docker-image entry was untagged. The repository revision and image
  reference are independent version selectors, so the hosted hook followed the
  image registry's current tag rather than the declared release.
- The selected repair pins the entry to
  `ghcr.io/hadolint/hadolint:v2.14.0 hadolint` and adds a regression that
  rejects absent or mismatched paired selectors. It does not ignore `DL3066` or
  change Airflow/ComfyUI user declarations merely to satisfy a later linter.
  The tag aligns release version only; no image digest is pinned, so it does not
  claim immutable image bytes or identical local/container execution.
- The main-push full run `35479017681` independently showed the same root:
  the hook pulled `ghcr.io/hadolint/hadolint:latest` at digest
  `sha256:32dac94127fd60b7b7e3fbfc65e1383b9b5e25c9bfd7b8536de7a539fe68a12d`
  and reported `DL3066` at the same two Dockerfile locations. Expected
  negative-test fixture output earlier in that log is not the failing step.

### Isolated repair evidence

- The new paired-version regression was RED before configuration: it expected
  `ghcr.io/hadolint/hadolint:v2.14.0 hadolint` and observed no explicit entry.
  It is GREEN after the alignment (1/1).
- Broader local evidence is green: CI-routing tests 29/29, workflow-contract
  tests 43/43, Ruff check and format check, pre-commit configuration validation,
  and `git diff --check`. The official local Hadolint 2.14.0 binary linted all
  13 tracked hook-matching Dockerfiles successfully. An official GHCR v2.14.0
  manifest inspection found an OCI index with four manifests without pulling or
  running an image.
- These tests validate the tracked repair and release-tag selection. They do not
  prove a GitHub-hosted container execution or immutable image bytes.

### Workflow inventory and disposition

| Surface | Current role | Disposition | Evidence boundary |
| --- | --- | --- | --- |
| `ci-quality.yml` / `validation-changed` | Pull-request changed-profile quality gate; required check on `main` | Retain; repair release-version alignment | A hosted run at the repair head is still required |
| `ci-quality.yml` / `validation-full` | Main-push/manual full profile and SARIF upload | Retain; it has different event, scope, permissions, and security output | A post-merge failure cannot retroactively block a merge |
| `workflow-contract.yml` | Typed workflow/job/gate authority | Retain; validate every structural workflow change against it | It cannot apply remote GitHub settings |
| `.pre-commit-config.yaml` | Shared hook/linter ownership | Modify only for paired Hadolint selectors and regression | A repository revision alone did not pin Docker-image execution |
| `generate-changelog.yml` | Tag-only changelog presence check | Retain; release check, not deployment | No deletion evidence exists |
| `greetings.yml` | New issue/PR greeting automation | Policy candidate for removal only if single-owner/external-contributor evidence supports it | It has write permissions; absence of a current need must be established |
| `pr-labeler.yml` | Path-based PR labels | Retain; cheap and its label rules do not depend on PR title | Any trigger expansion needs label-rule evidence |
| `stale.yml` | Daily issue/PR stale closure | Policy candidate for cadence/scope change | Daily cadence and PR closure affect contributor workflow |
| Main branch protection | Remote control plane requiring `validation-changed` | No tracked-file change proposed | Dated read-back does not prove current remote enforcement |

All five tracked workflows are active and contract-registered. Their external
actions are SHA-pinned. The CI quality workflow contains no deploy/publish job
and declares no custom deployment credential or repository-secret input.

GitHub-managed default CodeQL configuration also scans Actions, JavaScript, and
Python weekly. It is outside the five tracked workflow definitions and remains
separate from Zizmor because the two cover different security concerns.

### Consolidation and modification candidates

| Priority | Candidate | Status and rationale | Risk / required proof |
| --- | --- | --- | --- |
| P0 | Pair the Hadolint Docker-image tag with hook `rev` | Implemented in the isolated branch with anti-drift regression | Run focused/local gates and wait for hosted execution of this revision |
| P1 | Order the existing deterministic pre-commit leaf before expensive CI leaves | Proposed; main full gate started at 00:32:19, pre-commit started at 00:51:25, and Hadolint failed at 00:53:00: failure surfaced 20m41s after gate start, with pre-commit taking about 95 seconds | Preserve the same gate set, status context, and `SKIP` ownership; add an ordering regression before changing the registry |
| P1 | Design optional pre-commit update ownership | Proposed; Renovate currently excludes pre-commit while Dependabot owns only npm | Do not enable a manager alone: it must atomically maintain paired revision/tag (and any later digest) or the regression must block its update |
| P1 | Assess `pull_request.edited` for title validation | Proposed; `PR_TITLE` reaches the gate, while an edited title may not produce a new run | Confirm title validation impact; change workflow, contract, and tests together |
| P1 | Review remote protection enforcement and two orphaned active remote workflow registrations | Proposed; `enforce_admins=false`, and `governance-audit-tools.yml` (ID 350504656) plus `governance-apply-candidate.yml` (ID 350527175) are absent from the default branch | `state: active` does not prove executable/current use; require provenance, owner approval, and fresh authenticated read-back before disabling |
| P2 | Consider a Hadolint digest pin and paired update ownership | Proposed; v2.14.0 tag aligns release selection but remains mutable | Define digest rotation, tag/revision synchronization, and manager/manual ownership first |
| P2 | Keep changed/full jobs separate; clarify manual-dispatch concurrency if needed | Retain; manual dispatch on main can share a concurrency group with a push | Decide whether independent manual diagnostics justify event-qualified grouping |
| P2 | Review greetings/stale cadence and retention | Proposed; labeler is cheap/path-based, greetings and daily stale handling need owner/consumer evidence | Avoid silently removing external-contributor or maintenance controls |

## Verification Evidence

| Check | Result | Scope and limitation |
| --- | --- | --- |
| Official hook-manifest inspection | PASS | Confirms the v2.14.0 Docker-image entry is untagged |
| Hosted runs `35478388330` / `35479017681` | FAIL | PR and main-push incident evidence used `:latest` and reported the same two `DL3066` findings; neither is a repair result |
| Focused paired-version regression | PASS (1/1) | RED before entry addition; GREEN for paired v2.14.0 selectors |
| CI-routing / workflow-contract tests | PASS (29/29; 43/43) | Isolated local repair evidence |
| Config, diff, Ruff, local Hadolint, and GHCR manifest checks | PASS | Local Hadolint 2.14.0 checked 13 Dockerfiles; manifest was inspected only, not run |
| Hosted `validation-changed` at repair head | Pending | Required before any merge consideration; no rerun is claimed |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- |
| Hadolint execution uses the declared release tag | G — validators and review | Local repair and regression pass; hosted verification pending | Pre-commit configuration and regression test |
| CI/CD candidates distinguish overlap from duplication | G — validators and review | Inventory and priorities recorded; no deletion proposed | Workflow contract and GitHub governance |
| Hosted and local evidence remain separate | G — validators and review | Pending hosted verification documented | Current Task and PR checks |

## Review Evidence

- Independent whole-branch review: **SPEC/QUALITY/SECURITY APPROVED** with no
  remaining findings. Review confirmed the release-tag versus immutable-digest
  boundary, retained separate changed/full responsibilities, accurate
  GitHub-token wording, and the CodeQL/Zizmor coverage distinction.
- CI/CD review is required for the paired-version change and its regression.
  Security review must confirm the official release-pinned image is retained and
  no permission, secret, or rule suppression is introduced.
- Documentation review must confirm that this Task and GDE-0004 do not claim a
  hosted rerun, merge, or remote control-plane update.

## Commit Ledger

- Local CI repair commit
  `4255f4469958184a7c7126808f5068a46cecf335`
  (`fix(ci): Align Hadolint hook and image versions`) contains the paired hook
  selector and regression only.
- The three documentation paths are ready for the separate conventional
  documentation commit; its identity is not yet recorded.
- No push, merge, workflow deletion, or remote GitHub setting change is
  recorded by this Task.
- The implementation and documentation remain isolated on
  `codex/ci-version-alignment` until review and a separately authorized delivery
  decision.

## Rulings

| Decision | Basis | Consequence |
| --- | --- | --- |
| Pin the Docker-image entry instead of suppressing `DL3066` | Failure is selector drift; declared release is v2.14.0 | Dockerfile policy remains intact; later upgrades must update both selectors |
| Preserve two CI quality jobs | PR enforcement and post-push/manual security reporting differ | Shared setup is not grounds to merge or delete jobs |
| Require evidence before workflow deletion | No tracked workflow has obsolescence proof | Consolidation remains a proposal |

## Deferred Items

- Hosted rerun, PR state, merge, and protection read-back are outside this local
  repair scope.
- Title-event coverage, an atomic pre-commit update-owner design, digest
  maintenance, caching, remote workflow cleanup, and non-gating workflow
  retention each need a scoped follow-up.
