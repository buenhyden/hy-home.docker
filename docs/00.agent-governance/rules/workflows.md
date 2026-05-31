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
- **Code review**: `code-reviewer` + `code-review-dimensions` → structured findings.
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

## 3. Routing Rules

1. `workflow-supervisor` selects the workflow and delegates each step to the right
   worker agent with exactly one primary scope (`subagent-protocol.md`).
2. Each step writes intermediate artifacts to `_workspace/` and audit handoffs per
   the Communication Protocol.
3. The `policy-gate-agent` step must pass before any stage document is marked complete.
4. Read `memory/progress.md` before starting and append after completing the workflow.

## Related Documents

- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/provider-capability-matrix.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `docs/00.agent-governance/agents/README.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
