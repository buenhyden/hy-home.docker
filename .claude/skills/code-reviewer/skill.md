---
name: code-reviewer
description: >
  Cross-layer code review orchestrator for the workspace. Use for review requests covering
  style, security, performance, and architecture. Supports full reviews and focused reviews.
  Reports findings only and never applies fixes automatically.
---

# code-reviewer

Workspace code review orchestration skill.
Use the review taxonomy from the active governance harness set: style, security,
performance, and architecture.

## Review Modes

| Mode | Use When | Primary Actor | Supporting Actor |
| --- | --- | --- | --- |
| Full review | General review or PR review | `code-reviewer` | `workflow-supervisor` |
| Security-focused | Secrets, auth, unsafe input, workflow security | `code-reviewer` | `security-auditor` |
| Infra-focused | Compose, scripts, infra diffs | `code-reviewer` | `iac-reviewer` |

## Review Taxonomy

Evaluate the requested scope across these lenses:

1. **Style** — naming, readability, consistency, unnecessary complexity
2. **Security** — trust boundaries, secret handling, injection and unsafe execution patterns
3. **Performance** — complexity, redundant work, resource pressure, operational bottlenecks
4. **Architecture** — cohesion, dependency direction, ownership boundaries, extensibility

## Workflow

### Phase 1 — Prepare

- identify the target paths, diff, or review scope
- save organized context to `_workspace/00_input.md` when the task is broad enough to warrant it
- choose full or focused mode

### Phase 2 — Review

`code-reviewer` produces a structured report with:

- exact file and line references
- severity tags: `BLOCK`, `WARN`, `NIT`
- explicit assumptions or missing context

Escalate to:

- `security-auditor` for infra secrets, workflow security, or critical security findings
- `iac-reviewer` for infrastructure drift or resource-limit concerns

### Phase 3 — Synthesize

- consolidate findings into `_workspace/review_<branch>_<date>.md`
- prioritize issues by severity
- keep summaries brief and actionable

## Error Handling

| Situation | Action |
| --- | --- |
| Scope too large | Review changed files first and note the boundary |
| Missing diff or context | Continue with available files and state the limitation |
| Cross-domain conflict | Ask `workflow-supervisor` to arbitrate before final synthesis |

## Related Documents

- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `.claude/agents/code-reviewer.md`
- `.claude/agents/security-auditor.md`
- `.claude/agents/iac-reviewer.md`
- `.claude/agents/workflow-supervisor.md`
