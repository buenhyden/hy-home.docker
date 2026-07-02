---
status: draft
---

<!-- Target: docs/03.specs/template-system-reorganization/README.md -->

# Template System Reorganization Specification

> Design contract for reorganizing `docs/99.templates` into copyable templates
> and non-copyable support governance.

## Overview

`docs/03.specs/template-system-reorganization` defines the design contract for
the `docs/99.templates` reorganization. The work separates template bodies from
template governance, normalizes frontmatter responsibilities, and prepares the
validator and governance surfaces for nested template paths.

This folder is a design surface only. The implementation target remains
`docs/99.templates/`, relevant Stage 00 governance rules, validation scripts,
and only the direct reference fallout needed to keep the repository contract
coherent.

## Audience

This README is for:

- Documentation Writers
- Repository Maintainers
- AI Agents
- QA Engineers

## Status

This specification is a draft design contract. It becomes the input to a Stage
04 execution plan after user review and approval.

## Scope

### In Scope

- Target taxonomy for `docs/99.templates/templates/`
- Target taxonomy for `docs/99.templates/support/`
- Frontmatter schema and vocabulary design
- Template-to-document mapping rules
- Validator, governance, and direct-reference update boundaries
- Legacy template, legacy section, and duplicate-purpose cleanup strategy

### Out of Scope

- Immediate runtime, Compose, secret, provider, or CI behavior changes
- Broad rewrite of every existing stage document body
- New active policies outside the approved template-governance surface
- Remote GitHub state changes
- Full corpus migration beyond validation-required fallout

## Structure

```text
template-system-reorganization/
├── README.md  # This file
└── spec.md    # Template system reorganization design contract
```

## How to Work in This Area

1. Read [spec.md](./spec.md) before changing `docs/99.templates`.
2. Treat this spec as the implementation boundary for the first migration
   cycle.
3. Record gaps discovered outside the approved scope instead of fixing unrelated
   docs or runtime surfaces.
4. Create the Stage 04 plan only after this design is reviewed and approved.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs README](../README.md)
- [template catalog](../../99.templates/README.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [repo contract validation](../../../scripts/validation/check-repo-contracts.sh)
