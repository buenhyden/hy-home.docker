# Final Documentation Standardization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Eliminate documentation redundancy, enforce strict naming conventions, and scrub all remaining boilerplate to achieve a 100% "Hardened" status for the Documentation Hub.

**Architecture:** This plan uses a "Consolidate and Purge" approach. We will merge overlapping doc intents into dated canonical versions, rename un-dated files to match their PRDs, and use global regex to ensure metadata consistency.

**Tech Stack:** Bash (sed, grep, mv, rm), Markdown, YAML metadata.

---

### Task 1: Redundancy Purge

**Files:**

- Delete: `docs/ard/doc-refactor-ard.md`
- Delete: `docs/ard/refactor-docs-ard.md`
- Delete: `docs/ard/refactor-agent-documentation-ard.md`
- Delete: `docs/ard/agentic-framework-cycle-2-ard.md`
- Delete: `docs/ard/final-alignment-ard.md`
- Delete: `docs/ard/rule-refactor-ard.md`
- Delete: `docs/ard/meta-framework-ard.md`
- Delete: `docs/ard/documentation-system-ard.md`
- Delete: `docs/prd/documentation-framework-prd.md`
- Delete: `docs/prd/final-alignment-prd.md`

**Step 1: Execute deletions**
Run: `rm docs/ard/doc-refactor-ard.md docs/ard/refactor-docs-ard.md docs/ard/refactor-agent-documentation-ard.md docs/ard/agentic-framework-cycle-2-ard.md docs/ard/final-alignment-ard.md docs/ard/rule-refactor-ard.md docs/ard/meta-framework-ard.md docs/ard/documentation-system-ard.md docs/prd/documentation-framework-prd.md docs/prd/final-alignment-prd.md`

**Step 2: Commit cleanup**
Run: `git commit -m "docs: remove redundant and overlapping documentation fragments"`

### Task 2: Filename Hardening (ARD Family)

**Files:**

- Rename: `docs/ard/2026-02-27-observability-ard.md` -> `docs/ard/2026-02-27-observability-ard.md`
- Rename: `docs/ard/2026-02-27-infra-automation-ard.md` -> `docs/ard/2026-02-27-infra-automation-ard.md`
- Rename: `docs/ard/2026-02-27-infra-baseline-ard.md` -> `docs/ard/2026-02-27-infra-baseline-ard.md`
- Rename: `docs/ard/2026-02-27-messaging-ard.md` -> `docs/ard/2026-02-27-messaging-ard.md`
- Rename: `docs/ard/2026-02-26-system-optimization-ard.md` -> `docs/ard/2026-02-26-system-optimization-ard.md`

**Step 1: Execute renames and update cross-links in PRDs**
Run: `mv docs/ard/2026-02-27-observability-ard.md docs/ard/2026-02-27-observability-ard.md`
Run: `mv docs/ard/2026-02-27-infra-automation-ard.md docs/ard/2026-02-27-infra-automation-ard.md`
Run: `mv docs/ard/2026-02-27-infra-baseline-ard.md docs/ard/2026-02-27-infra-baseline-ard.md`
Run: `mv docs/ard/2026-02-27-messaging-ard.md docs/ard/2026-02-27-messaging-ard.md`
Run: `mv docs/ard/2026-02-26-system-optimization-ard.md docs/ard/2026-02-26-system-optimization-ard.md`

**Step 2: Update internal references**
Run: `sed -i "s|2026-02-27-observability-ard.md|2026-02-27-observability-ard.md|g" docs/**/*.md`
Run: `sed -i "s|2026-02-27-infra-automation-ard.md|2026-02-27-infra-automation-ard.md|g" docs/**/*.md`
Run: `sed -i "s|2026-02-27-infra-baseline-ard.md|2026-02-27-infra-baseline-ard.md|g" docs/**/*.md`
Run: `sed -i "s|2026-02-27-messaging-ard.md|2026-02-27-messaging-ard.md|g" docs/**/*.md`
Run: `sed -i "s|2026-02-26-system-optimization-ard.md|2026-02-26-system-optimization-ard.md|g" docs/**/*.md`

**Step 3: Commit**
Run: `git commit -m "docs: enforce YYYY-MM-DD- naming convention for ARD family"`

### Task 3: Placeholder Scrubbing

**Files:**

- Modify: `docs/specs/2026-03-15-meta-framework-spec.md`
- Modify: `docs/operations/incidents/2026-03-15-doc-path-inconsistency.md`
- Modify: `docs/runbooks/rule-maintenance.md`

**Step 1: Remove boilerplate text**
Update the files to remove `[Explain...]`, `[Requirement 1]`, `[Optional]`, etc.

**Step 2: Verify**
Run: `grep -rnE "\[(Explain|Requirement|Optional)\]" docs`
Expected: Empty output.

### Task 4: Metadata Standardization

**Files:**

- Modify: `docs/**/*.md`

**Step 1: Remove quotes from layer tags**
Run: `sed -i "s/layer: agentic/layer: agentic/g" docs/**/*.md`
Run: `sed -i "s/layer: infra/layer: infra/g" docs/**/*.md`
Run: `sed -i "s/layer: architecture/layer: architecture/g" docs/**/*.md`
Run: `sed -i "s/layer: ops/layer: ops/g" docs/**/*.md`
Run: `sed -i "s/layer: common/layer: common/g" docs/**/*.md`
Run: `sed -i "s/layer: product/layer: product/g" docs/**/*.md`
Run: `sed -i "s/layer: plans/layer: plans/g" docs/**/*.md`

**Step 2: Verify consistency**
Run: `grep -r "layer:" docs`

---
