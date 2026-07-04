---
status: superseded
---

<!-- Target: docs/03.specs/template-system-reorganization/README.md -->

# Template System Reorganization Specification

> Design contract for reorganizing `docs/99.templates` into copyable templates
> and non-copyable support governance.

## Overview

`docs/03.specs/template-system-reorganization` preserves the first design
contract for the `docs/99.templates` reorganization. The current replacement is
[Template System Contract Standardization](../template-system-contract-standardization/spec.md).

This folder is retained as transition/reference evidence. Use the replacement
spec and Stage 99 support contracts for current template, frontmatter, archive,
and governance rules.

## Audience

This README is for:

- Documentation Writers
- Repository Maintainers
- AI Agents
- QA Engineers

## Status

This specification is superseded by
[Template System Contract Standardization](../template-system-contract-standardization/spec.md).
The original migration was implemented through the Stage 04 template-system
reorganization plan and task evidence.

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

1. Use the replacement spec before changing `docs/99.templates`.
2. Use this folder only for transition history and earlier implementation
   rationale.
3. Record gaps discovered outside the approved scope instead of fixing unrelated
   docs or runtime surfaces.

## Related Documents

- [spec.md](./spec.md)
- [current replacement spec](../template-system-contract-standardization/spec.md)
- [docs/03.specs README](../README.md)
- [template catalog](../../99.templates/README.md)
- [documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [repo contract validation](../../../scripts/validation/check-repo-contracts.sh)
