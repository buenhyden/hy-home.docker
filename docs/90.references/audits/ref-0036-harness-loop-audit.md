---
status: superseded
artifact_id: ref-0036
artifact_type: audit
parent_ids:
- ref-0026
observed_at: '2026-07-07'
---

<!-- Target: docs/90.references/audits/ref-0036-harness-loop-audit.md -->

# Reference: Superseded Harness and Loop Audit Mapping

## Overview

This leaf is a mapping-only record for the former 2026-07-07 harness/loop audit.

## Purpose

Route verified themes to current criterion reports and reject stale provider claims.

## Repository Role

Superseded provenance only; not current implementation evidence.

## Scope

### In Scope

- Merge/reject disposition and current destinations.

### Out of Scope

- Current provider behavior, parity, status, or recommendations.

## Definitions / Facts

| Field | Disposition |
| --- | --- |
| Canonical destinations | [Harness](ref-0025-harness-engineering-implementation.md), [loop](ref-0027-loop-engineering-implementation.md), [provider](ref-0028-provider-harness-loop-implementation.md), and [workspace](ref-0032-workspace-rules-environment-implementation.md) reports. |
| Verified merged claims | Bounded plan/task/review loops, provider-specific hook/adaptor differences, semantic-eval incompleteness, and Graphify freshness as a manual/advisory concern. |
| Rejected unsupported claims | “Self-healing” error parsing, blanket Claude/Codex maturity, Gemini lacking native hooks/subagents, universal wrapper absence without contract context, and sandbox parity conclusions. |
| Current-truth warning | Current provider facts and workspace adoption are separate; use HAR, LOOP, PIC, and WRE criteria only. |

## Source Rules

- Do not restore narrative maturity claims.
- Revalidate mutable provider facts through the canonical research ledger.

## Sources

- [Canonical audit README](ref-0019-readme.md) - current audit boundary.
- `Provider research` (retiring 2026-07-05 pack, cited without a path because pre-deletion gate 4 admits no clickable link; `provider-implementation-comparison` leaf) - current provider criteria.

## Maintenance

- **Owner**: Agentic Workflow Specialist.
- **Review Cadence**: None for current status.
- **Update Trigger**: Supersession-route correction only.

## Related Documents

- [Superseded pack README](ref-0033-readme.md)
- [Canonical audit README](ref-0019-readme.md)
