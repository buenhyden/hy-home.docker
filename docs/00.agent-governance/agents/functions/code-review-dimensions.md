---
layer: agentic
---

# code-review-dimensions

## Overview

Reference pattern library for the four code review dimensions: Security, Architecture (SOLID), Performance, and Style. Provides OWASP/CWE checklists, code smell to refactoring mappings, and cross-domain conflict resolution guidance.

## Purpose

Give the code-reviewer agent a consistent, workspace-calibrated reference set so findings are reproducible and severity-tagged correctly.

## Scope

**Covers:**

- Security: OWASP Top 10 (2021), CWE Top 25, Docker/container YAML patterns, language-specific vulnerability descriptions (Python, JS, Java, Go)
- Architecture: SOLID violation signals, code smell → refactoring mapping (Martin Fowler catalog)
- Performance: cyclomatic/cognitive complexity thresholds, memory/concurrency/DB anti-patterns
- Style: language style guides (PEP 8, Airbnb JS, Effective Go, Rust Style), auto-fixable indicators
- Cross-domain conflict resolution (security vs. performance, DRY vs. readability)

**Excludes:**

- Threat modeling (see container-threat-modeling)
- Deployment security gates (see ci-cd-patterns)

## Structure

- Domain 1 Security → Domain 2 Architecture → Domain 3 Performance → Domain 4 Style → Cross-domain conflicts

## Agents

- **code-reviewer** — primary caller

## Skills

- This function is a reusable orchestration skill.

## Usage

- Loaded automatically by code-reviewer during four-domain review execution.
- **Inputs:** changed file list + diff
- **Outputs:** findings table with severity tags (BLOCK/WARN/NIT)

## Artifacts

- `_workspace/review_<branch>_<YYYY-MM-DD>.md`

## Related Documents

- `../../scopes/common.md`
- `../functions/code-reviewer.md`
- `../README.md`
