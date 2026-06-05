<!-- Target: docs/90.references/hads/README.md -->

# HADS References

> HADS reference profile and validation boundary for AI-readable documentation

## Overview

`docs/90.references/hads` stores the approved Human-AI Document Standard (HADS)
reference profile for this repository.

This category does not replace active documentation policy in
`docs/00.agent-governance/`. It provides stable reference material and a bounded
pilot surface where HADS structure is mandatory and validator-backed.

## Category Role

This folder defines how HADS reference documents are written and validated in
`hy-home.docker`. Non-README Markdown files in this category must satisfy both
the reference-stage contract and the HADS profile enforced by
`scripts/validation/check-repo-contracts.sh`.

## Language Rule

HADS profile terms, block tags, validator wording, and AI-readable instructions may remain English. Korean explanatory notes are allowed when they help human readers, but they must not replace required HADS labels, source-backed facts, or validation terminology.

## Audience

이 README의 주요 독자:

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- HADS reference profile
- HADS block-tag validation boundary
- Source-backed HADS usage facts
- Links to repository documentation policy

### Out of Scope

- Mandatory conversion of all active stage documents
- Runtime policy or runbook instructions
- External HADS validator distribution
- Secret values, credentials, tokens, private keys, or raw logs

## Structure

```text
docs/90.references/hads/
├── README.md        # This file
└── profile.md       # HADS profile reference and validation contract
```

## Current References

- [profile.md](./profile.md) - HADS profile and validation contract

## Reference Rules

1. Non-README files in this category must include a HADS version declaration.
2. The AI reading instruction must appear before the first content section.
3. HADS block tags must be bold and on their own line.
4. Reference-stage sections remain required so HADS docs do not become active policy.

## How to Work in This Area

1. Use [reference.template.md](../../99.templates/reference.template.md) as the
   reference-stage base.
2. Add HADS header, AI reading instruction, and block tags before drafting facts.
3. Run `bash scripts/validation/check-repo-contracts.sh` after edits.
4. Keep active governance changes in `docs/00.agent-governance/`.

## Examples

- Use `**[SPEC]**` for stable repository facts.
- Use `**[NOTE]**` for context that helps humans understand tradeoffs.
- Use `**[BUG] ...**` only for verified failure/fix records.

## Related Documents

- [references index](../README.md)
- [HADS profile](./profile.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [repo contract checker](../../../scripts/validation/check-repo-contracts.sh)
