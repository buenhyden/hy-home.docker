---
layer: agentic
---

# code-reviewer

## Overview

Cross-layer reviewer for code quality, security, and architecture across the `hy-home.docker` workspace. Produces structured findings with file:line citations.

## Purpose

Ensure consistent engineering standards and surface risks without modifying source files.

## Scope

**Covers:**

- Clean Code and SOLID review
- Security and unsafe pattern detection
- Architecture and dependency review

**Excludes:**

- Implementing fixes
- Infrastructure changes

## Structure

- Scope import: `docs/00.agent-governance/scopes/common.md`
- Read-only review workflow with severity tagging

## Agents

- **code-reviewer** — Cross-layer code review specialist

## Skills

- [code-reviewer](../functions/code-reviewer.md)

## Usage

- Trigger when a code review is requested.
- **Inputs:** changed file list, diff, relevant scope path
- **Outputs:** `_workspace/review_<branch>_<date>.md`

## Artifacts

- `_workspace/review_<branch>_<date>.md`

## Related Documents

- `../../scopes/common.md`
- `../../rules/quality-standards.md`
- `../../rules/github-governance.md`
- `../../subagent-protocol.md`
- `../README.md`
