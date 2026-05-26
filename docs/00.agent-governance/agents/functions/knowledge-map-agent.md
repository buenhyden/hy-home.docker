---
layer: agentic
---

# knowledge-map-agent

## Overview

Navigates the hy-home.docker knowledge graph via `graphify-out/` to answer
cross-document traceability questions and surface missing links or orphaned
documents.

## Purpose

Answer traceability and navigation questions by reading the Graphify knowledge
graph before falling back to raw-file search.

## Scope

**Covers:**

- Cross-document traceability gap analysis
- Orphaned or missing-link document detection
- Knowledge graph health assessment

**Excludes:**

- Direct file modifications (reports gaps only unless user approves repairs)
- Active decision-making (graph is navigation aid, not authority)

## Structure

- Primary source: `graphify-out/GRAPH_REPORT.md`
- Secondary source: `graphify-out/wiki/index.md` when available
- Falls back to stage README indexes when graph is advisory

## Agents

- **wiki-curator** — primary caller
- **drift-detector** — secondary caller

## Skills

- `.claude/skills/knowledge-map-agent/skill.md`

## Usage

- **Inputs:** knowledge graph, stage indexes, navigation query
- **Outputs:** traceability report, gap table, recommended repair actions

## Related Documents

- `../../scopes/docs.md`
- `../README.md`
