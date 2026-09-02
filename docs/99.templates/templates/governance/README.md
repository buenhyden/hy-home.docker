---
title: Governance Templates
type: common/readme
layer: templates
owner: "@buenhyden"
---

# Governance Templates

## Overview

This directory provides the copyable authoring forms for the Stage 00 canonical
documents. Profile selection, required frontmatter, sections, and lifecycle
rules are owned by [`registry.json`](../../registry.json), not by this catalog.

## Audience

- Repository Maintainers
- Documentation Writers
- AI Agents

## Scope

Each form authors one Stage 00 document kind. Canonical human content lives in
`docs/00.agent-governance/`; provider projections are generated from it by the
registered renderer and use the [runtime forms](../runtime/) instead.

## Structure

| Stage 00 document | Registered type | Template |
| --- | --- | --- |
| SDLC contract | `governance/sdlc` | [contract.template.md](./contract.template.md) |
| Policy | `governance/policy` | [control.template.md](./control.template.md) |
| Hook rule | `governance/hook-policy` | [rule.template.md](./rule.template.md) |
| Provider adapter | `governance/provider` | [provider.template.md](./provider.template.md) |
| Role | `governance/role` | [role.template.md](./role.template.md) |
| Skill | `governance/skill` | [skill.template.md](./skill.template.md) |

Stage 00 documents carry no `artifact_id`; their identity is the canonical path.

## How to Work in This Area

1. Select the profile from the [Stage 99 registry](../../registry.json).
2. Copy the matching form and replace every placeholder.
3. Edit only the canonical Stage 00 source.
4. Run `python3 scripts/validation/run-ci-gate.py --profile full`.
5. Regenerate the registered provider projections and record evidence in the
   active Task.

## Related Documents

- [Template catalog](../README.md)
- [Runtime projection forms](../runtime/)
- [Stage 00 governance](../../../00.agent-governance/README.md)
- [Provider registry](../../../00.agent-governance/providers/registry.yaml)
