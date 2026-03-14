---
title: 'Consolidated Agent Instructions and Documentation Flat Taxonomy PRD'
status: 'Draft'
version: 'v1.1.0'
owner: 'Antigravity'
layer: 'product'
---

# PRD: Consolidated Agent Instructions & Flat Taxonomy

## 1. Overview

This project aims to consolidate all AI agent instructions into `docs/agentic/`, enforce a flat documentation taxonomy with mandatory `layer` metadata, and implement an efficient lazy-loading gateway for agents.

## 2. Goals

- Eliminate instruction duplication between `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
- Enforce 100% metadata coverage for `layer` identification.
- Optimize agent context usage through explicit lazy-loading markers.

## 3. Requirements

- **[REQ-01]** Detailed instructions moved to `docs/agentic/instructions.md`.
- **[REQ-02]** `AGENTS.md` reduced to a shared gateway pointer (< 10 lines).
- **[REQ-03]** All files in `docs/` must contain `layer: <name>` in YAML frontmatter.
- **[REQ-04]** `gateway.md` must link to all core documentation directories.
- **[REQ-05]** Support `[LOAD:*]` markers for automated instruction loading.

## 4. Success Criteria

- Agents can navigate the repository solely through `gateway.md` pointers.
- No absolute paths or `file://` links remain in agent instructions.
- Metadata is present and valid for all Markdown files.
