---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-05-harness-engineering.md -->

# Task: Workspace Harness Engineering

## Overview

This document records harness engineering implementation and verification
evidence for the `hy-home.docker` workspace. It strengthens repeatable harness
validation flow against the existing Stage 00, Compose, secrets, scripts, CI,
PR, and operations surfaces.

## Inputs

- **User Request**: Harness engineering workflow from the pasted document.
- **Governance Entry**: [AGENTS.md](../../../AGENTS.md)
- **Harness Map**: [Harness implementation map](../../00.agent-governance/harness-implementation-map.md)
- **Approval Boundaries**: [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md)

## Working Rules

- Start with investigation before implementation.
- Keep changes minimal and in existing repository surfaces.
- Do not create `.harness/`.
- Do not read secret values, tokens, private keys, or certificate contents.
- Do not change Compose runtime surfaces or restart services without explicit approval.
- Record validation evidence in this task and `memory/progress.md`.

## Goal

- Implement the current `hy-home.docker` harness engineering flow as a
  repeatable, evidence-backed workflow over existing governance, Compose,
  secrets, scripts, CI, PR, and operations surfaces.

## Non-goals

- Create a `.harness/` directory.
- Read secret values, tokens, private keys, or certificate contents.
- Change root-active Compose includes, ports, volumes, networks, or secret
  mounts.
- Restart, deploy, or otherwise mutate operational services.
- Expand GitHub Actions permissions.

## Investigation Findings

| Area | Finding | Evidence |
| --- | --- | --- |
| Control / Governance | Root shims stay thin and Stage 00 is the policy SSoT. | `AGENTS.md`, `docs/00.agent-governance/README.md`, `rules/bootstrap.md` |
| Docker Compose Runtime | Root-active, optional, standalone, and variant Compose status is documented and validated by existing Compose gates. | `docker-compose.yml`, `infra/README.md`, `scripts/validation/validate-docker-compose.sh` |
| Secrets / Credentials | Secret handling is path/registry/evidence based; value files are read-forbidden. | `secrets/README.md`, `secrets/SENSITIVE_ENV_VARS.md.example` |
| Scripts / Automation | Purpose-folder script ownership is documented; harness mode existed in the QA gate runner. | `scripts/README.md`, `scripts/validation/run-local-qa-gates.sh` |
| Verification / CI | Local script-backed gates and CI quality jobs are already separated. | `run-local-qa-gates.sh --list`, `.github/workflows/ci-quality.yml` |
| Evidence / Progress | Progress and task evidence locations are defined. | `docs/00.agent-governance/memory/progress.md`, `docs/04.execution/tasks/README.md` |
| PR / Review | Harness Impact is already present in the PR template. | `.github/PULL_REQUEST_TEMPLATE.md` |
| Operations / Runbooks | Operations docs separate guides, policies, runbooks, and incidents; service runbooks include secret redaction and escalation language. | `docs/05.operations/README.md`, service runbooks |

## Gap Analysis

| Gap | Risk | Fix |
| --- | --- | --- |
| `scripts/validation/validate-harness.sh` was missing while the requested completion gate names it directly. | Medium | Add a thin wrapper delegating to `run-local-qa-gates.sh --harness`. |
| Repo contracts did not explicitly require the wrapper. | Medium | Extend the harness surface contract checks. |
| Harness documents and PR evidence examples pointed mostly to `--harness` instead of the wrapper. | Low | Align map, approval boundary, task template, PR template, and scripts README. |

## Implementation Plan

| Step | Files | Purpose |
| --- | --- | --- |
| 1 | `scripts/validation/validate-harness.sh` | Provide the requested harness validation entrypoint without duplicating gate logic. |
| 2 | `scripts/README.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/00.agent-governance/**`, `docs/99.templates/**` | Point harness evidence to the wrapper and keep `--harness` as the underlying mode. |
| 3 | `scripts/validation/check-repo-contracts.sh` | Make the wrapper and harness evidence links contract-checked. |
| 4 | `docs/04.execution/tasks/**`, `memory/progress.md` | Record task evidence and completion status. |

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Governance / validation / templates / PR contract | User-provided pasted harness engineering task | `docs/00.agent-governance/**`, `docs/99.templates/**`, `scripts/validation/**`, `.github/PULL_REQUEST_TEMPLATE.md` | Existing harness map, approval boundaries, PR Harness Impact, and `run-local-qa-gates.sh --harness`; missing `validate-harness.sh` wrapper | Wrapper and references added; validation evidence below | `git revert` or equivalent patch; no runtime rollback | No secret values, token, private key, or certificate contents |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Investigate governance, Compose, secrets, scripts, CI, PR, and operations harness surfaces. | doc | User pasted task / Phase 1 | Investigation | Investigation Findings table | Codex | Done |
| T-002 | Add requested harness validation wrapper without duplicating existing QA logic. | impl | User pasted task / Phase 5.4 | Implementation Plan step 1 | `bash scripts/validation/validate-harness.sh` | Codex | Done |
| T-003 | Align harness evidence references and repo contract checks. | impl | User pasted task / Phase 5.5-5.6 | Implementation Plan steps 2-3 | `bash scripts/validation/check-repo-contracts.sh` via wrapper | Codex | Done |
| T-004 | Record task and progress evidence. | doc | User pasted task / Phase 7 | Implementation Plan step 4 | This task and `memory/progress.md` | Codex | Done |

## Implemented Changes

| File | Change |
| --- | --- |
| `scripts/validation/validate-harness.sh` | Added wrapper for `run-local-qa-gates.sh --harness`. |
| `scripts/validation/check-repo-contracts.sh` | Added checks for the wrapper, template, README reference, and PR evidence command. |
| `scripts/README.md` | Added wrapper to inventory, lifecycle, and examples. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Updated Harness Impact evidence command to use the wrapper. |
| `docs/00.agent-governance/harness-implementation-map.md` | Added wrapper as the harness gate surface. |
| `docs/00.agent-governance/rules/approval-boundaries.md` | Updated required harness validation entrypoint. |
| `docs/99.templates/templates/governance/harness-task-contract.template.md` | Updated required validation command. |

## Secret Handling

- No secret value files, tokens, private keys, or certificate contents were read.
- Secret-related evidence remains limited to documented paths, IDs, registries,
  and redacted validation expectations.

## Compose Impact

- None. This task did not change `docker-compose.yml`, `infra/**`, profiles,
  ports, volumes, networks, secret mounts, or backup-relevant runtime behavior.

## Operations Impact

- No operational service restart, rollout, deployment, or runtime mutation was
  performed.
- Existing operations runbooks remain the runtime evidence and escalation
  surfaces for service-specific backup, restore, credential, and restart work.

## Rollback Plan

- Revert this task's additive wrapper, documentation references, and repo
  contract additions with `git revert` or an equivalent patch. No runtime state
  rollback is required.

## Validation Results

| Command | Result |
| --- | --- |
| `bash scripts/validation/validate-harness.sh` | PASS after fixing task template normalization, LLM Wiki freshness, and new script inventory gaps. |
| `bash scripts/validation/run-local-qa-gates.sh --script-backed` | PASS. Provider surface drift, tech-stack drift, docs traceability, docs implementation alignment, Compose, hardening, template/security baseline, QuickWin, LLM Wiki freshness, and repo contracts passed. |
| `git diff --check` | PASS. |
| `gh pr list --head main --json number,state,headRefName,baseRefName,title,url,statusCheckRollup --limit 5` | PASS: no open PR exists for the current `main` head, so remote PR required-check status is not an active local-task gate. |
| `graphify update .` | Skipped: `graphify` was not available on PATH. |

## Verification Summary

- **Test Commands**:
  - `bash scripts/validation/validate-harness.sh` (PASS after remediation)
  - `bash scripts/validation/run-local-qa-gates.sh --script-backed` (PASS)
  - `git diff --check` (PASS)
  - `gh pr list --head main --json number,state,headRefName,baseRefName,title,url,statusCheckRollup --limit 5` (PASS: no matching open PR)
- **Eval Commands**: N/A for docs/script wrapper work.
- **Logs / Evidence Location**: This task document and
  `docs/00.agent-governance/memory/progress.md`.

## Remaining Risks

- Closed for this local task: no open PR exists for the current `main` head, so
  there is no remote PR required-check rollup to verify. PR-time required-check
  evidence remains governed by `.github/PULL_REQUEST_TEMPLATE.md` and
  `docs/00.agent-governance/rules/github-governance.md`.
- Closed for this change type: `validate-docker-compose.sh --preflight` is not
  required because this task did not change Compose runtime surfaces, local
  operational readiness, secret files, ports, volumes, networks, or deployments.

## Follow-up Tasks

- None. Remote required-check evidence is a PR-time gate only, and local
  preflight remains N/A for this docs/script wrapper change.

## Related Documents

- **Harness Map**: [Harness implementation map](../../00.agent-governance/harness-implementation-map.md)
- **Approval Boundaries**: [Approval boundaries](../../00.agent-governance/rules/approval-boundaries.md)
- **Harness Template**: [Harness task contract template](../../99.templates/templates/governance/harness-task-contract.template.md)
- **Scripts README**: [Scripts README](../../../scripts/README.md)
