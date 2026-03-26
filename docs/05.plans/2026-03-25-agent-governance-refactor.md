# Agent Governance Infrastructure Refactor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Standardize and optimize the `hy-home.docker` agent governance infrastructure by refactoring root shims, centralizing rules, and completing the technical scope dictionary.

**Architecture:** Use a JIT-loading shim pattern for root instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) that redirects context to a centralized `docs/00.agent-governance/` hub. Scopes follow the "Golden 5" documentation pattern.

**Tech Stack:** Markdown, Stage-Gate Taxonomy (01-11).

---

## Task 1: Optimize Root Shims

**Files:**

- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `GEMINI.md`

**Step 1: Simplify AGENTS.md**
Ensure it is the absolute minimal entry point.

**Step 2: Simplify CLAUDE.md**
Remove redundant instructions and point to `docs/00.agent-governance/claude-provider.md`.

**Step 3: Simplify GEMINI.md**
Remove redundant instructions and point to `docs/00.agent-governance/gemini-provider.md`.

**Step 4: Commit**
`git add AGENTS.md CLAUDE.md GEMINI.md && git commit -m "docs: optimize root agent shims for JIT loading"`

---

## Task 2: Standardize Governance Hub README

**Files:**

- Modify: `docs/00.agent-governance/README.md`

**Step 1: Apply "Golden 5" pattern to README**
Refactor sections to align with `Context`, `Requirements`, `Implementation Flow`, `Operational Procedures`, and `Maintenance`.

**Step 2: Update Layer Map**
Ensure all 13 layers are listed and linked correctly.

**Step 3: Commit**
`git add docs/00.agent-governance/README.md && git commit -m "docs: standardize agent governance hub README"`

---

## Task 4: Complete Missing Scopes

**Files:**

- Create: `docs/00.agent-governance/scopes/common.md`
- Create: `docs/00.agent-governance/scopes/mobile.md`
- Create: `docs/00.agent-governance/scopes/entry.md`
- Create: `docs/00.agent-governance/scopes/meta.md`
- Create: `docs/00.agent-governance/scopes/agentic.md`

**Step 1: Create common.md**
Define shared engineering standards (naming, formatting, etc.).

**Step 2: Create mobile.md**
Define mobile-specific constraints (React Native/Expo).

**Step 3: Create entry.md**
Define entrypoint/gateway constraints (Traefik/Nginx).

**Step 4: Create meta.md**
Define repository metadata and taxonomy rules.

**Step 5: Create agentic.md**
Consolidate agent behavior protocols (e.g., `<thinking>` usage, tool usage).

**Step 6: Commit**
`git add docs/00.agent-governance/scopes/*.md && git commit -m "docs: complete technical scope dictionary"`

---

## Task 5: Align Provider Configurations

**Files:**

- Modify: `docs/00.agent-governance/claude-provider.md`
- Modify: `docs/00.agent-governance/gemini-provider.md`

**Step 1: Update claude-provider.md**
Incorporate instructions moved from `CLAUDE.md`.

**Step 2: Update gemini-provider.md**
Incorporate instructions moved from `GEMINI.md`.

**Step 3: Commit**
`git add docs/00.agent-governance/*-provider.md && git commit -m "docs: align provider-specific configurations"`

---

## Task 6: Final Quality Audit

**Step 1: Run Quality Report**
Use `@[/claude-md-improver]` principles to evaluate the new structure.

**Step 2: Final Polish**
Fix any broken links or inconsistent headers.

**Step 3: Commit**
`git commit -m "docs: final governance infrastructure audit and polish" --allow-empty`

---

## Verification Plan

### Manual Verification

1. Verify all links in `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` work.
2. Verify all 13 scopes are present in `docs/00.agent-governance/scopes/`.
3. Verify all files start with `layer: <name>` frontmatter.
4. Verify the `[LOAD:...]` markers in `README.md` correctly point to existing taxonomy folders.
