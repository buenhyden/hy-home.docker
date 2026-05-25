---
status: approved
---
<!-- Target: docs/03.specs/home-docker-revalidation-deferred-follow-up/spec.md -->

# Home Docker Revalidation Deferred Follow-up Specification

## Overview (KR)

이 문서는 2026-05-25 `hy-home.docker` workspace audit 결과를 재검증하고, 기존 감사에서 남은 deferred 항목을 값·런타임 변경 없이 추적 가능하게 고정하는 명세다. 구현 대상은 문서 산출물, 검증 evidence, metadata-only 비교 결과이며 Compose runtime, secret value, actual `.env` value, remote GitHub 설정은 변경하지 않는다.

## Strategic Boundaries & Non-goals

- 이 명세는 current local `main` 기반 감사 결과의 revalidation과 deferred register를 소유한다.
- 기존 2026-05-25 audit improvement 문서는 baseline evidence로 취급하고 다시 쓰지 않는다.
- `projects/storybook/mcp/`는 pre-existing untracked no-touch 범위로 보존한다.
- Docker start/stop, deployment, port/network/volume/permission mutation, secret value work, actual `.env` sync, remote GitHub branch protection, CI required-check enforcement는 범위 밖이다.
- Broad ARD/ADR cleanup, `.agents/skills` compatibility mirroring, file deletion candidates는 별도 승인 전까지 deferred 상태로 남긴다.

## Related Inputs

- **PRD**: 명시적 PRD 없음. 이 작업은 approved audit follow-up and governance evidence closure다.
- **ARD**: 명시적 신규 ARD 없음. 기존 `hy-home.docker` modular Compose and agent-governance architecture를 따른다.
- **Related ADRs**: 신규 ADR 없음. 런타임 또는 아키텍처 결정 변경이 없다.
- **Baseline Plan**: [2026-05-25 home docker workspace audit improvement plan](../../04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Baseline Task**: [2026-05-25 home docker workspace audit improvement task](../../04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md)
- **Release Runbook**: [release-management.md](../../05.operations/runbooks/release-management.md)

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
- **Release Runbook**: [release-management.md](../../05.operations/runbooks/release-management.md)
- **Governance Memory Progress**: [progress.md](../../00.agent-governance/memory/progress.md)
- **Graphify Report**: [GRAPH_REPORT.md](../../../graphify-out/GRAPH_REPORT.md)
