---
name: workspace-audit-revalidation
description: >
  Revalidate completed hy-home.docker workspace-audit artifacts without creating
  duplicate audit docs. Use when asked to refresh, recheck, extend, or prove a
  prior Home Docker workspace audit, bounded revalidation, omission review, or
  follow-up Skill review while preserving runtime, secret-value, remote GitHub,
  deployment, deletion, and untracked Storybook MCP deferrals.
---

# workspace-audit-revalidation

Reusable workflow for bounded revalidation of completed `hy-home.docker`
workspace-audit evidence.

## Trigger Examples

Use this skill for requests like:

- "Revalidate the existing Home Docker workspace audit artifacts."
- "Check whether the bounded revalidation plan missed anything."
- "Review the completed audit with another planning or Skill lens and update evidence."
- "Create or improve audit evidence without duplicating the canonical Task."

Do not use it for a brand-new infrastructure audit that has no existing Plan or
Task artifact.

## Core Rule

Improve canonical evidence in place. Do not create duplicate full-audit docs.

The canonical evidence target is the existing dated Task under
`docs/04.execution/tasks/`, with progress recorded in
`docs/00.agent-governance/memory/progress.md`.

## Bootstrap

1. Read `AGENTS.md`.
2. Read `graphify-out/GRAPH_REPORT.md`; if Graphify is advisory, treat it only
   as navigation and corroborate against tracked files.
3. Load the active primary scope from `docs/00.agent-governance/scopes/`.
4. For docs work, load `docs/00.agent-governance/scopes/docs.md` and
   `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
5. For branch or merge work, load
   `docs/00.agent-governance/rules/github-governance.md`.

## Branch Discipline

1. Start from a clean tracked tree when possible.
2. Leave pre-existing untracked `projects/storybook/mcp/` untouched.
3. Create a `codex/` branch before mutating files.
4. Stage only files that belong to the audit evidence update.
5. If the user asks for local integration, fast-forward merge to `main` and
   delete the development branch.

## Evidence Targets

Update only the existing canonical evidence unless the user explicitly approves
a new artifact.

Common rows and sections:

- Task table row for the new follow-up work
- Phase checklist section
- Review matrix or decision matrix
- Decision Log row
- Change Scope row
- Verification Log row
- Skill Review row when a Skill lens is used
- `docs/00.agent-governance/memory/progress.md` work-log row

## Safety Boundaries

Keep these skipped or deferred unless separately approved:

- actual `.env` values
- secret value files
- Docker runtime start/stop/log work
- deployment or release
- remote GitHub settings verification
- deletion-risk changes
- untracked Storybook MCP work

Compare `.env.example` and `.env` by key name only. Compare sensitive registries
by metadata fields only. Never print or commit secrets.

## Skill Creation Gate

Create or edit a Skill only when all are true:

1. A repeated workflow is proven by current Task or memory evidence.
2. The user approves Skill creation or improvement.
3. There are concrete trigger examples.
4. The new or changed Skill can be validated with repo checks or a
   Skill-specific validation command.

If any condition is missing, record a candidate-only decision instead of
mutating `.claude/skills/`, `.agents/skills/`, or external Skill roots.

## Required Verification

Run these after approved docs or Skill edits:

```bash
bash scripts/knowledge/report-graphify-health.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
git diff --check
git status --short --branch
```

Run additional validators when the change touches those areas:

- `bash scripts/validation/validate-docker-compose.sh` for Compose changes
- `bash scripts/validation/check-template-security-baseline.sh` for template or security-baseline changes
- `bash scripts/validation/check-quickwin-baseline.sh` for QuickWin baseline changes
- `bash scripts/hardening/check-all-hardening.sh` for hardening changes
- `bash -n <changed shell scripts>` for changed shell scripts

## Completion Report

Report:

- files changed
- branch, commit, and merge status
- verification commands and outcomes
- explicit deferrals
- remaining untracked `projects/storybook/mcp/` status when present
