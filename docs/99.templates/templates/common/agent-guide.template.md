---
title: "{{TITLE}}"
version: "0.1.0"
type: "common/agent-guide"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Route to canonical owners; do not copy a policy, role, or skill body into this file. -->

# {{TITLE}}

## Scope

### Allowed Scope

<!-- Author prompt: Name the folder's purpose, the paths an agent may change below it, and what is out of scope. -->

{{ALLOWED_SCOPE_AND_NON_GOALS}}

### Instruction Precedence

<!-- Author prompt: Say that when this guide and the owner of a rule it summarizes disagree, the owner wins and the guide is corrected, and link the bootstrap precedence order; never add a rank of your own. -->

{{INSTRUCTION_PRECEDENCE}}

## Workflow

### Intake

<!-- Author prompt: Link the `.agents/` policies, roles, skills, prompts and hook rules, and the `.claude/` and `.codex/` adapters and hooks an agent loads before working here. -->

{{CANONICAL_SOURCES}}

### Execution

<!-- Author prompt: List the folder-specific steps and obligations an agent follows while changing a file here. -->

{{INSPECT_CHANGE_AND_LOCAL_OBLIGATIONS}}

## Boundaries

### Authority

<!-- Author prompt: Say when an agent stops and reports, and which approval owner decides; this guide grants no tool, path, permission or approval. -->

{{STOP_AND_ESCALATE}}

### Secrets and External Effects

<!-- Author prompt: Name the protected actions: secret handling, generated files, live or remote effects and the approval each needs. -->

{{PROTECTED_ACTIONS}}

## Verification

### Checks

<!-- Author prompt: Name only registered commands that exist. -->

{{REQUIRED_CHECKS}}

### Reporting

<!-- Author prompt: Say where check evidence and handoff state are recorded, what the checks do not prove, and link the human-facing documents. -->

{{EVIDENCE_LIMITS_AND_HANDOFF}}
