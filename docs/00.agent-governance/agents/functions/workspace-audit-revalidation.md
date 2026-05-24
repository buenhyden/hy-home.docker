---
layer: agentic
---

# workspace-audit-revalidation

## Overview

Bounded revalidation workflow for completed Home Docker workspace-audit
artifacts.

## Purpose

Keep audit evidence current and auditable without creating duplicate full-audit
documents or expanding into deferred runtime, secret, remote, deployment, or
deletion work.

## Scope

**Covers:**

- Existing workspace-audit Plan/Task evidence
- Bounded revalidation addenda
- Omission-review and Skill-review follow-ups
- Progress-log updates
- Local verification and branch cleanup

**Excludes:**

- New full-audit documents unless explicitly approved
- Secret values and actual `.env` values
- Docker runtime start/stop/log checks
- Remote GitHub settings verification
- Deployment, release, and deletion-risk work

## Structure

- Bootstrap repo governance and Graphify posture
- Confirm canonical Task/progress evidence targets
- Apply scoped in-place evidence updates
- Preserve explicit deferrals
- Run repo gates and report results

## Agents

- **doc-writer** — owns canonical documentation updates
- **workflow-supervisor** — coordinates multi-lens follow-up work when needed

## Skills

- Runtime mirror: `.claude/skills/workspace-audit-revalidation/skill.md`

## Usage

- Trigger after a completed workspace audit needs revalidation or a follow-up
  review lens.
- **Inputs:** existing audit Plan/Task, user-approved review scope, current repo
  state.
- **Outputs:** updated canonical Task evidence, progress-log row, verification
  results, and task-sized commit when committing is approved.

## Artifacts

- `docs/04.execution/tasks/*workspace-audit*.md`
- `docs/00.agent-governance/memory/progress.md`

## Related Documents

- `../../scopes/agentic.md`
- `../../scopes/docs.md`
- `../../rules/stage-authoring-matrix.md`
- `../../rules/github-governance.md`
- `../README.md`
