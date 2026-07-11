---
layer: agentic
---

# Workflows

Single source of truth for the repeatable, multi-step workflows in `hy-home.docker`.
A workflow is an ordered chain of orchestration skills routed by `workflow-supervisor`.
All runtimes execute the same workflows; the steps are provider-neutral governance
functions (`agents/functions/`) exposed per the Provider Capability Matrix.

## 1. Stage-Gate Documentation Pipeline

The primary workflow follows the stage-gate lifecycle. Each step loads the mapped
template and authoring row from `rules/stage-authoring-matrix.md` (the authoring
contract — do not duplicate it here).

| Step | Stage                             | Orchestration skill                                            | Worker agent                       | Output                       |
| ---- | --------------------------------- | -------------------------------------------------------------- | ---------------------------------- | ---------------------------- |
| 1    | 01 requirements → 02 architecture | `requirements-to-design-agent`                                 | `doc-writer`                       | PRD → ARD/ADR                |
| 2    | 03 specs                          | `compose-stack-agent` (infra) / `requirements-to-design-agent` | `doc-writer`, `infra-implementer`  | Spec + contracts             |
| 3    | 04 execution plans                | `execution-plan-agent`                                         | `workflow-supervisor`              | Plan                         |
| 4    | 04 execution tasks                | `task-breakdown-agent`                                         | worker per scope                   | Task evidence                |
| 5    | 05 operations                     | `ops-runbook-agent`                                            | `incident-responder`, `doc-writer` | Guides / policies / runbooks |
| Gate | all stages                        | `policy-gate-agent`                                            | `workflow-supervisor`              | Pass/fail before completion  |

## 2. Supporting Workflows

- **Infrastructure change**: `compose-stack-agent` → `infra-validate` / `infra-cross-validate`
  → `iac-reviewer` / `drift-detector` review → ADR/spec/runbook authoring.
- **Code review**: request (after self-review and local checks pass) → `code-reviewer` + `code-review-dimensions` review → structured findings → author resolves or replies to each finding and re-verifies → re-request. Follow the `rules/git-workflow.md` Pull Request Protocol.
- **Quality Assurance**: `test-automator` / `e2e-testing` → `qa-engineer` review → test reports.
- **CI/CD Pipeline**: `deployment-pipeline-design` (+ external `deployment-procedures`) → `ci-cd-engineer` execution → deployment reports.
- **Security audit**: `security-audit` + `container-threat-modeling` → findings + mitigations.
- **Incident response**: `incident-response` → incident/postmortem docs (Stage 05).
- **Knowledge / governance**: `knowledge-map-agent`, `workspace-audit-revalidation`.
- **Skill Development**: external `writing-skills` / `skill-creator` → `skill-creator` agent → new reusable skill.
- **Hook Development**: external `writing-hookify-rules` / `hook-development` → `hook-developer` agent → new `.local.md` hook.
- **Governance Configuration**: external `update-config` → `rules-engineer` agent → policy updates.
- **Style Enforcement**: `style-validation` → `style-enforcer` execution → standardized markdown/output.

Backtick names without an "external" prefix are workspace functions in
`agents/functions/` and are exposed through provider adapters per the Provider
Capability Matrix. Names marked **external** are existing external/runtime
skills (e.g. `skill-creator`, `hook-development`, `writing-hookify-rules`,
`update-config`, `writing-skills`, `deployment-procedures`); meta agents invoke
them directly and the workspace does not duplicate them as functions.

## 3. External Strategy Adaptation

External strategy skills may shape how an agent works, but active repository
artifacts still use the stage taxonomy in `docs/01` to `docs/05`, `docs/90`,
and `docs/99`.

| Strategy discipline                | Canonical repository adaptation                                                                                                                                                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill applicability before action  | Check relevant Stage 00 functions, provider adapters, and requested external skills before mutating state.                                                                                                                             |
| Brainstorming / design exploration | Capture approved outcomes in PRD, ARD/ADR, Spec, or Plan artifacts; do not create active `docs/superpowers/**` specs.                                                                                                                  |
| Writing implementation plans       | Use `docs/04.execution/plans/**` and `docs/99.templates/templates/sdlc/plan.template.md`.                                                                                                                                                             |
| Executing plans                    | Use `docs/04.execution/tasks/**` and record task-by-task evidence.                                                                                                                                                                     |
| Test-driven development            | Follow `scopes/qa.md`; mark docs-only or policy-only coverage N/A with rationale.                                                                                                                                                      |
| Systematic debugging               | Establish root cause before fixes; incidents and recurring failures use Stage 05 incident/postmortem paths where applicable.                                                                                                           |
| Verification before completion     | Completion claims require command output, manual evidence, or explicit skipped-check rationale.                                                                                                                                        |
| Requesting / receiving code review | Request review only after self-review and local checks pass; resolve or reply to each finding, re-run affected checks, and record incorporated changes before re-requesting. Follow the `rules/git-workflow.md` Pull Request Protocol. |
| Finishing a branch                 | Follow `rules/github-governance.md` and `rules/git-workflow.md`: verify, inspect diff/status, stage scoped files only, and commit/PR by approval. When approved, run all-files pre-commit only through `scripts/validation/run-agent-precommit-all-files.sh` in a clean linked worktree and record its evidence manually. |

Controlled-wrapper evidence is limited to Git-visible, non-ignored repository
paths. It does not claim ignored/outside-write detection or process/filesystem
sandboxing.

HADS is mandatory only for the approved `docs/90.references/data/hads/` reference
profile. It may guide AI-readable documentation elsewhere, but existing
templates are not converted and HADS block tags are not required outside that
profile unless a future plan explicitly approves that rollout.

## 4. Skill Lifecycle Gate

Reusable functions and provider skills follow the same lifecycle regardless of
runtime:

| Lifecycle Step      | Required Agent Action                                                                                                                       | Canonical Evidence                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Discovery           | Identify requested, named, or obviously applicable workspace functions and external skills before mutation.                                 | Task notes or plan assumptions identify the considered skill set.                                        |
| Applicability       | Decide whether each skill changes the work method, output artifact, or validation scope.                                                    | Inapplicable skills are recorded as N/A only when they were requested or materially relevant.            |
| Provider loading    | Load the provider adapter file (`.claude/skills/`, `.codex/skills/`, `.agents/skills/`) or external skill instructions needed for the task. | The loaded source is reflected in the task narrative or session audit trail.                             |
| Canonical artifact  | Write the resulting plan, task, policy, runbook, code, or review output to the repository's canonical stage path.                           | Active artifacts live under `docs/01` to `docs/05`, `docs/90`, `docs/99`, or the scoped runtime surface. |
| Validation evidence | Run the relevant local checks, record CI-only gates, or explain skipped checks.                                                             | `docs/04.execution/tasks/` and progress logs capture the command, outcome, and rationale.                |

Provider-local skill files may describe runtime mechanics, but they do not own
the lifecycle policy above.

The exact provider-neutral lifecycle is
`discovery -> applicability -> provider loading -> canonical artifact -> validation evidence`.
For changed or new target Markdown, validation evidence includes
`python3 scripts/validation/check-document-metadata.py --mode check-changed`
with a safe base. At an approved final QA gate, all-files pre-commit uses only
`scripts/validation/run-agent-precommit-all-files.sh`; direct agent execution
remains prohibited, and evidence is limited to reviewed Git-visible,
non-ignored repository paths.

## 5. Routing Rules

1. `workflow-supervisor` selects the workflow and delegates each step to the right
   worker agent with exactly one primary scope (`subagent-protocol.md`).
2. Each step writes intermediate artifacts to `_workspace/repo-support/` and audit handoffs per
   the Communication Protocol.
3. The `policy-gate-agent` step must pass before any stage document is marked complete.
4. Read `memory/progress.md` before starting and append after completing the workflow.

## Related Documents

- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/provider-capability-matrix.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/agents/README.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
