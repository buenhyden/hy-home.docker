---
profile_id: data
status: active
artifact_id: DATA-0075
artifact_type: data
parent_ids: []
created: '2026-08-23'
updated: '2026-08-23'
observed_at: '2026-08-23'
---

# Reference: HADS Profile

**Version 1.0.0** · Human-AI Document Standard reference · 2026-06-02

## AI READING INSTRUCTION

Read `[SPEC]` and `[BUG]` blocks for authoritative facts.
Read `[NOTE]` only if additional context is needed.
`[?]` blocks are unverified and require explicit uncertainty.

## Overview

**[SPEC]**
This document records the approved reference profile and validator boundaries for applying HADS in `hy-home.docker`.

**[NOTE]**
HADS is not a format for rewriting the entire documentation system at once. In this repository, it first operates as a mandatory profile limited to `docs/90.references/data/hads/`.

**[NOTE]**
Scope correction, 2026-08-29. The bounding directory named above no longer
exists: `49522aa1` removed `docs/90.references/data/hads/` and its two files on
2026-08-23, and this document is the surviving half of that package. The
mandatory profile therefore currently applies to no document at all, so the
sentence above states a bound rather than an active control. The earlier
sentence is kept as the record of the approved boundary and is not withdrawn.
Whether the profile is rescoped, retired, or given a new subject directory is a
governance decision that also moves `REQ-0024-FR-0005`,
`docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md` and
`docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md`,
all three of which bound the profile to the same removed path. Owner: the unit
that next revises the HADS rollout.

## Purpose

**[SPEC]**

- Define the HADS structure that is mandatory for this reference category.
- Preserve the repository's existing stage-gate documentation contract.
- Provide validator-backed evidence for HADS usage without converting unrelated documents.

## Repository Role

**[SPEC]**

- This document supports `docs/00.agent-governance/policies/documentation-protocol.md`.
- This document supports `docs/99.templates/README.md`.
- This document does not replace active governance policy, templates, plans, tasks, runbooks, or runtime files.

## Scope

### In Scope

**[SPEC]**

- HADS header requirements.
- AI reading instruction requirements.
- HADS block-tag formatting requirements.
- Reference-stage compatibility requirements.

### Out of Scope

**[SPEC]**

- Mandatory conversion of all existing stage documents.
- Runtime or deployment behavior.
- External publication of a HADS validator.
- Secret values, credentials, tokens, private keys, shell history, or raw logs.

## Definitions / Facts

**[SPEC]**

| Term | Definition |
| --- | --- |
| HADS | Human-AI Document Standard for Markdown technical documentation. |
| AI reading instruction | A section before content that tells AI readers which blocks are authoritative. |
| `**[SPEC]**` | Authoritative fact block. |
| `**[NOTE]**` | Context block for background and rationale. |
| `**[BUG] ...**` | Verified failure and fix block. |
| `**[?]**` | Unverified or inferred claim block. |

**[BUG] Missing HADS manifest**

- Symptom: A HADS document is hard for agents to parse deterministically.
- Cause: The file lacks `## AI READING INSTRUCTION` before the first content section.
- Fix: Add the AI reading instruction before `## Overview` or any other content section.

## Source Rules

**[SPEC]**

- Prefer repo-local governance documents for repository-specific policy.
- Use HADS skill documentation only as a format reference, not as active repository policy.
- Re-check external HADS facts before using them to change repository-wide rules.

## Sources

**[SPEC]**

- [Documentation Protocol](../../../00.agent-governance/policies/documentation-protocol.md) - repository documentation policy and HADS boundary.
- [Template Catalog](../../../99.templates/README.md) - reference template and target-stage mapping.
- Task Evidence - approval-gate implementation history.

## Maintenance

**[SPEC]**

- **Owner**: Documentation Specialist / Rules Engineer
- **Review Cadence**: Review when HADS profile requirements or repository validators change.
- **Update Trigger**: Update when `docs/90.references/data/hads/` validator rules, HADS block semantics, or template compatibility rules change.

## Related Documents

**[SPEC]**

- **References Index**: [../README.md](../../README.md)
- **HADS Category README**: [README.md](README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../../00.agent-governance/policies/documentation-protocol.md)
- **Template Catalog**: [../../99.templates/README.md](../../../99.templates/README.md)
- **Repo Contract Checker**: [../../../scripts/validation/check-repo-contracts.sh](../../../../scripts/validation/check-repo-contracts.sh)

## Schema

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Provenance

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Inventory

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Refresh

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Consumers

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Traceability

This package preserves its existing data evidence under the Stage 99 `data` contract.
