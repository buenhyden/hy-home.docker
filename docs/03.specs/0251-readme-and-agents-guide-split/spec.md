---
title: "README and Agent Guide Split Specification"
version: "0.1.3"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0251"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-11-03"
---

# README and Agent Guide Split Specification

## Overview

### Intent

A folder README mixes guidance for people with instructions for AI agents, and
no rule says which folders need agent-specific working rules. This change gives
each audience its own file: `README.md` for people and a folder `AGENTS.md` for
agents, placed only where the folder's role needs one.

### Owning Requirements

REQ-0024 asks for one canonical agent governance home that providers route to.
AD-0027 places provider adapters under `.claude/` and `.codex/`. The user
directed that READMEs target people, AGENTS.md files target agents, each
AGENTS.md route to the matching `.agents/`, `.claude/` and `.codex/` owners,
and AGENTS.md exist only where a folder's role warrants one, with an explicit
placement rule.

SPEC-0251 has parent_ids REQ-0024 and AD-0027. It makes concrete REQ-0024 (one canonical agent governance home that providers route to) and the AD-0027 constraint that provider adapters live under `.claude/` and `.codex/`. The body cites no REQ-0024-FR or NFR identifier.

## Scope

### In Scope

- A placement rule and AGENTS.md shape in the documentation protocol, a
  bootstrap load step, and provider loading notes.
- A Registry `folder-agent-guide` profile and `governance/agent-guide`
  template.
- Folder AGENTS.md files in `docs/01.requirements/`, `docs/02.architecture/`,
  `docs/03.specs/`, `docs/05.operations/`, `docs/90.references/`,
  `docs/99.templates/`, `infra/`, `scripts/` and `tests/`.
- Moving agent-directed sections out of the matching READMEs.
- Loader changes so a stage root accepts its `AGENTS.md`.

### Non-goals

- Root `AGENTS.md` and `CLAUDE.md`, which stay the bootstrap entry shims.
- Folder `CLAUDE.md` pointers and every folder not listed above.
- Rewriting README content beyond the agent-directed parts.

## Behavior Contract

### Normal Behavior

Each listed folder carries a `README.md` written for people and an
`AGENTS.md` written in English for agents. The AGENTS.md follows the
`governance/agent-guide` template, routes to canonical owners, and names only
registered checks. Stage loaders, the operations catalog and the Stage 90
corpus accept an `AGENTS.md` at their root, and a folder router stays a router.

The Registry, schemas and templates stay the only machine authority for paths
and profiles. Outside `docs/`, an AGENTS.md links no individual numbered-stage
document.

### Failure and Edge Cases

An `AGENTS.md` at a path the Registry profile does not list fails the
placement test in the document-governance suite, which compares tracked folder
guides with the profile paths. Under `docs/`, the stage loaders and the metadata
check also reject it as an unregistered stage entry; outside `docs/` only the
placement test catches it. A new folder guide that does not start at `draft`
fails the metadata check.

A folder AGENTS.md grants no tool, path, permission or approval and ranks below
canonical governance. A README no longer carries an `AI Agent Guidance`
section.

**Observable failures.** A folder guide copies a policy body, names a check that does not exist, or a
stage loader rejects its own `AGENTS.md`.

**Stop boundaries.** This Task pushes nothing and merges nothing. The coordinator pushes the
branch and opens the pull request under the user's instruction to continue the
approved plan, and the user merges.

## Acceptance Criteria

### Criteria

1. The documentation protocol defines the audience split, the placement rule
   with the folder list, the AGENTS.md shape, and the language rule for
   AGENTS.md; bootstrap and both provider adapters state how a folder guide is
   loaded.
2. The nine folder AGENTS.md files exist under the `folder-agent-guide`
   profile, route to real `.agents/`, `.claude/` and `.codex/` owners, and
   name only commands that exist.
3. The matching READMEs carry no agent-directed section and point to their
   AGENTS.md.
4. The document gates, the document-governance suites, the agent governance
   contract and renderer parity pass locally, with actual results in the Task.

### Evidence Requirements

- Criteria 1 to 3 are observed by reading the documentation protocol, bootstrap, provider adapters, the nine folder AGENTS.md files and their READMEs.
- Criterion 2 is checked by the placement test in the document-governance suite and by confirming each routed owner and named command exists.
- Criterion 4 is verified by running the document gates, the document-governance suites, the agent governance contract and renderer parity locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and accepts the Spec.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-readme-and-agents-guide-split.md)

### Historical and Navigation

No historical or navigation link applies; the package links only its Plan and Task.
