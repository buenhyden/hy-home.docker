---
layer: agentic
---

# adr-writing

## Overview

MADR-extended ADR writing framework with CAP theorem, ATAM, and quality attribute weighted scoring. Provides a structured approach to Architecture Decision Records for infrastructure, security, operations, data, and architecture decisions.

## Purpose

Ensure architecture decisions are captured with rigorous tradeoff analysis, traceable rationale, and consistent format so future agents and humans can understand and challenge past decisions.

## Scope

**Covers:**

- ADR status lifecycle (Proposed → Accepted → Deprecated/Superseded)
- Category-prefixed numbering (INFRA/SEC/OPS/DATA/ARCH)
- MADR-extended template sections (Status, Decision Drivers, Quality Attribute Assessment, Validation Criteria, Change History)
- CAP theorem classification guide (CP/AP/CA with tool assignments)
- Weighted quality attribute scoring matrix by decision type
- Simplified ATAM 6-step procedure
- ADR writing quality checklist (10 required elements)

**Excludes:**

- Modifying existing ADR files in `docs/03.adr/` (read-only without explicit user approval)
- Implementation of the decision (handled by domain agents)

## Structure

- Status lifecycle → category numbering → template filling → quality attribute scoring → ATAM → checklist

## Agents

- **doc-writer** — primary caller

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger for any significant architectural or infrastructure decision.
- **Inputs:** decision topic + context + alternatives considered
- **Outputs:** `docs/03.adr/NNNN-<category>-<short-title>.md`

## Artifacts

- `docs/03.adr/NNNN-<category>-<short-title>.md`

## Related Documents

- `../../scopes/docs.md`
- `../../rules/documentation-protocol.md`
- `../README.md`
