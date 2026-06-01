---
status: active
---
<!-- Target: docs/90.references/hads/profile.md -->

# Reference: HADS Profile

**Version 1.0.0** · Human-AI Document Standard reference · 2026-06-02

## AI READING INSTRUCTION

Read `[SPEC]` and `[BUG]` blocks for authoritative facts.
Read `[NOTE]` only if additional context is needed.
`[?]` blocks are unverified and require explicit uncertainty.

## Overview (KR)

**[SPEC]**
이 문서는 `hy-home.docker`에서 HADS를 적용하는 승인된 reference profile과 validator 경계를 정리한다.

**[NOTE]**
HADS는 전체 문서 체계를 한 번에 재작성하기 위한 형식이 아니다. 이 repository에서는 먼저 `docs/90.references/hads/`에 한정해 mandatory profile로 운영한다.

## Purpose

**[SPEC]**

- Define the HADS structure that is mandatory for this reference category.
- Preserve the repository's existing stage-gate documentation contract.
- Provide validator-backed evidence for HADS usage without converting unrelated documents.

## Repository Role

**[SPEC]**

- This document supports `docs/00.agent-governance/rules/documentation-protocol.md`.
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
- Fix: Add the AI reading instruction before `## Overview (KR)` or any other content section.

## Source Rules

**[SPEC]**

- Prefer repo-local governance documents for repository-specific policy.
- Use HADS skill documentation only as a format reference, not as active repository policy.
- Re-check external HADS facts before using them to change repository-wide rules.

## Sources

**[SPEC]**

- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md) - repository documentation policy and HADS boundary.
- [Template Catalog](../../99.templates/README.md) - reference template and target-stage mapping.
- [Task Evidence](../../04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md) - approval-gate implementation history.

## Maintenance

**[SPEC]**

- **Owner**: Documentation Specialist / Rules Engineer
- **Review Cadence**: Review when HADS profile requirements or repository validators change.
- **Update Trigger**: Update when `docs/90.references/hads/` validator rules, HADS block semantics, or template compatibility rules change.

## Related Documents

**[SPEC]**

- **References Index**: [../README.md](../README.md)
- **HADS Category README**: [README.md](./README.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Template Catalog**: [../../99.templates/README.md](../../99.templates/README.md)
- **Repo Contract Checker**: [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)
