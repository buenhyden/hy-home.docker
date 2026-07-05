---
status: completed
---
<!-- Target: docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md -->

# Home Docker Revalidation Deferred Follow-up Specification

## Overview

This specification revalidates the 2026-05-25 `hy-home.docker` workspace audit results and makes the deferred items from the prior audit traceable without changing values or runtime state. The implementation scope is documentation artifacts, validation evidence, and metadata-only comparison results; it does not change Compose runtime, secret values, actual `.env` values, or remote GitHub settings.

## Strategic Boundaries & Non-goals

- This specification owns revalidation of the audit results from the current local `main` baseline and the deferred register.
- The existing 2026-05-25 audit improvement documents are treated as baseline evidence and are not rewritten.
- `projects/storybook/mcp/` remains a pre-existing untracked no-touch surface.
- Docker start/stop, deployment, port/network/volume/permission mutation, secret value work, actual `.env` synchronization, remote GitHub branch protection, and CI required-check enforcement are out of scope.
- Broad ARD/ADR cleanup, `.agents/skills` compatibility mirroring, and file deletion candidates remain deferred until separately approved.

## Related Inputs

- **PRD**: No explicit PRD. This work is an approved audit follow-up and governance evidence closure.
- **ARD**: No explicit new ARD. It follows the existing `hy-home.docker` modular Compose and agent-governance architecture.
- **Related ADRs**: No new ADR. There is no runtime or architecture decision change.
- **Baseline Plan**: [2026-05-25 home docker workspace audit improvement plan](../../04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Baseline Task**: [2026-05-25 home docker workspace audit improvement task](../../04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Release Runbook**: [release-management.md](../../05.operations/runbooks/00-workspace/release-management.md)

## Contracts

- **Config Contract**: `.env.example`, `.env`, secret registries, Compose files, and validation scripts are evidence sources only; this follow-up must not edit runtime config or value-bearing files.
- **Data / Interface Contract**: No service API, data schema, Docker network, Docker volume, port, or deployment interface changes are allowed.
- **Governance Contract**: Revalidation evidence must live in canonical Stage 03/04 artifacts and `docs/00.agent-governance/memory/progress.md`; Graphify is advisory when health is advisory.

## Core Design

- **Component Boundary**: Create a dedicated spec, execution plan, and execution task for revalidation/deferred tracking; apply low-risk runbook clarification when reviewer evidence shows a local release-gate mismatch.
- **Key Dependencies**: `AGENTS.md`, `docs/00.agent-governance/rules/*`, stage templates, prior 2026-05-25 audit artifacts, repo validation scripts, and Graphify health output.
- **Tech Stack**: Markdown, Bash validators, metadata-only shell comparisons, optional Storybook Node 24 coverage command if QA evidence is touched.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Store revalidation state as Markdown tables: Coverage Ledger, Gap Registry, Reviewer Ledger, Verification Log, and Deferred Register.
- **Migration / Transition Plan**: Do not migrate old audit artifacts. Link to them as historical baseline and add this follow-up as the current revalidation record.

## Interfaces & Data Structures

### Core Interfaces

| Interface | Shape | Purpose |
| --- | --- | --- |
| Coverage Ledger | Markdown table keyed by area | Shows what was revalidated and where evidence lives |
| Gap Registry | Markdown table keyed by gap | Records decision, owner, status, validation |
| Deferred Register | Markdown table keyed by residual risk | Separates operator/runtime work from this doc-only follow-up |
| Verification Log | Markdown table keyed by command | Captures pass/fail/advisory evidence without raw secret output |

## API Contract (If Applicable)

Not applicable. This follow-up does not expose or change an external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist with governance, infra, QA, and CI/CD reviewer inputs.
- **Inputs**: Approved user plan, repo governance rules, prior audit artifacts, validators, metadata-only env/secret comparisons, reviewer outputs.
- **Outputs**: Template-compliant spec/plan/task artifacts, progress log update, optional generated LLM Wiki index refresh, final verification summary.
- **Success Definition**: Repository checks pass or are explicitly reported as advisory/deferred, and no runtime/value-bearing surfaces are changed.

## Tools & Tool Contract (If Applicable)

- Use `rg`, `sed`, `find`, and repo validators for discovery and verification.
- Use metadata-only shell commands for `.env` and secret registry comparison; do not print values.
- Use sub-agent reviewer passes as evidence inputs only; live repository files and validators remain authoritative.
- Do not run `pre-commit` manually.

## Prompt / Policy Contract (If Applicable)

- User-facing response defaults to Korean.
- Governance files under `docs/00.agent-governance/` remain English.
- Memory and Graphify are advisory context, not active policy.
- Secret values, credentials, shell history, and raw logs must not be copied into docs or responses.

## Memory & Context Strategy (If Applicable)

- Use the workspace-audit revalidation memory pattern for no-touch and evidence-driven closure.
- Record final progress in `docs/00.agent-governance/memory/progress.md`.
- Do not create a new durable memory note unless a reusable out-of-scope issue is found beyond the existing deferred register.

## Guardrails (If Applicable)

- **Input Guardrails**: Read only the minimum metadata required; do not inspect secret value files or print `.env` values.
- **Output Guardrails**: Store only counts, key names, IDs, env-var names, file paths, command names, and pass/fail/advisory results.
- **Blocked Conditions**: Stop or defer if completion requires Docker runtime state, remote GitHub admin access, secret mutation, actual `.env` edits, broad architecture cleanup, or deletion.
- **Escalation Rule**: Any runtime, remote, credential, deployment, or destructive action requires a separate user approval.

## Evaluation (If Applicable)

- **Eval Types**: governance validation, docs traceability, template/security baseline, QuickWin baseline, hardening baseline, Compose static validation, secrets check, Graphify health, metadata comparison.
- **Metrics**: zero repo-contract failures, zero doc-traceability failures, no value-bearing file edits, no no-touch path changes.
- **Datasets / Fixtures**: live repository files on the implementation branch.
- **How to Run**: execute the commands listed in `## Verification`.

## Edge Cases & Error Handling

- If Graphify remains advisory, record that status and corroborate claims against tracked source and validators.
- If new untracked docs are invisible to generated indexes, stage only intentional follow-up artifacts before refreshing the generated index.
- If Storybook coverage is not touched, do not run browser or local dev-server checks.
- If validators surface unrelated historical gaps, record them as deferred unless the approved scope directly owns the fix.

## Failure Modes & Fallback / Human Escalation

| Failure Mode | Fallback | Human Escalation |
| --- | --- | --- |
| Validator fails on changed docs | Patch only the changed documentation contract | Required only if fix would widen scope |
| Metadata comparison requires value inspection | Stop at counts/key names and mark value work deferred | Required for any value-bearing review |
| Remote branch protection state is needed | Mark remote enforcement unverified | Required before calling GitHub APIs or changing settings |
| Runtime validation requires starting services | Keep static Compose validation only | Required for any start/stop/deploy operation |

## Verification

```bash
git status --short --branch
git diff --check HEAD
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-template-security-baseline.sh
bash scripts/validation/check-quickwin-baseline.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/validate-docker-compose.sh --preflight
bash scripts/validation/validate-docker-compose.sh
bash scripts/operations/gen-secrets.sh --check
bash scripts/knowledge/report-graphify-health.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Spec, plan, task, README links, and progress log are updated within approved scope.
- **VAL-SPC-002**: Metadata-only env/secret comparison records counts and drift names without values.
- **VAL-SPC-003**: Repo governance/docs/static infra checks pass or advisory/deferred statuses are clearly recorded.
- **VAL-SPC-004**: `projects/storybook/mcp/` remains untracked and untouched.
- **VAL-SPC-005**: Deferred runtime, remote, secret, actual `.env`, broad architecture cleanup, and deletion work remains out of scope.

## Related Documents

- **Plan**: [2026-05-25 home docker revalidation deferred follow-up plan](../../04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- **Tasks**: [2026-05-25 home docker revalidation deferred follow-up task](../../04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- **Baseline Plan**: [2026-05-25 home docker workspace audit improvement plan](../../04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Baseline Task**: [2026-05-25 home docker workspace audit improvement task](../../04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Release Runbook**: [release-management.md](../../05.operations/runbooks/00-workspace/release-management.md)
- **Governance Memory Progress**: [progress.md](../../00.agent-governance/memory/progress.md)
- **Graphify Report**: [GRAPH_REPORT.md](../../../graphify-out/GRAPH_REPORT.md)
