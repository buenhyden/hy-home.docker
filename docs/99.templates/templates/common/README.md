---
title: Common Templates
type: common/readme
layer: templates
owner: "@buenhyden"
---

# Common Templates

## Overview

This directory provides the navigation README forms. The Stage 99 Registry owns
profile selection, required metadata, sections, and lifecycle rules.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

Use one README form per container kind. Research, Audit, and Data use the
registered References forms; a necessary minimal recovery record uses the
Tombstone form.

## Structure

| Need | Registered type | Template |
| --- | --- | --- |
| 스테이지 루트 탐색 README | `common/readme` | [readme-stage.template.md](./readme-stage.template.md) |
| Operations 도메인 README | `operation/domain-readme` | [readme-domain.template.md](./readme-domain.template.md) |
| Stage 03 Spec Package README | `sdlc/package-readme` | [readme-package.template.md](./readme-package.template.md) |
| Evidence package | — | [References templates](../references/) |
| Minimal recovery record | `archive/tombstone` | [Tombstone template](../archive/tombstone.template.md) |

## How to Work in This Area

1. Resolve the role in the [Registry](../../registry.json).
2. Copy its registered source and replace all placeholders.
3. Run the document-contract gate.

Do not copy historical templates from Git into current authoring workflows.

## Related Documents

- [templates catalog](../README.md)
- [Stage 99 authority](../../README.md)
- [Registry](../../registry.json)
