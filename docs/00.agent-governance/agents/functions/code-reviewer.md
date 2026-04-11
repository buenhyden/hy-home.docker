---
layer: agentic
---

# code-reviewer

## Overview

Cross-layer code review orchestration function for the workspace. Applies style, security, performance, and architecture review taxonomy without auto-fixing code.

## Purpose

Provide a repeatable review workflow that produces structured, severity-tagged findings and routes specialized concerns to the right worker agents.

## Scope

**Covers:**

- full and focused code reviews
- file and diff review workflows
- cross-domain finding prioritization

**Excludes:**

- implementing fixes
- infrastructure mutation

## Structure

- Runtime mirror: `.claude/skills/code-reviewer/skill.md`
- Review taxonomy: style, security, performance, architecture

## Agents

- **code-reviewer** — primary reviewer
- **workflow-supervisor** — arbitration and synthesis support
- **security-auditor** — security escalation path
- **iac-reviewer** — infrastructure escalation path

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger when a code review is requested.
- **Inputs:** target files, diff, scope, optional review mode
- **Outputs:** `_workspace/review_<branch>_<date>.md`

## Artifacts

- `_workspace/review_<branch>_<date>.md`

## Related Documents

- `../../rules/quality-standards.md`
- `../../rules/github-governance.md`
- `../../subagent-protocol.md`
- `../README.md`
