---
title: "Agent Glossary"
version: "0.1.0"
type: "governance/control"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-19"
created: "2026-11-19"
observed_at: "2026-11-19"
review_cycle: "on-contract-change"
---

# Agent Glossary

## Overview

Agent- and provider-only terms that a person working outside an agent runtime
does not need. Every shared term, including the common Term IDs, is defined
once in the [Repository Vocabulary](../../docs/00.workspace/01.project/glossary.md);
this file never restates or narrows one of them.

## Scope

Included: the meanings of provider adapters, native mechanics, renderer
cleanup, model and permission routing, and skill invocation. Excluded: common
Term IDs and the local extensions every contributor uses, which stay in the
Repository Vocabulary.

## Rules

### Terms

| Term | Definition | Not to Confuse | Policy Owner |
| --- | --- | --- | --- |
| Adapter | An authored provider file that owns loading and syntax differences only | A Projection | `.claude/provider.md`, `.codex/provider.md` |
| Native mechanics | Provider runtime configuration such as settings and hook registration | Native Runtime Evidence | [Providers index](../governance/providers/README.md) |
| Quarantine | The renderer's nonzero cleanup handoff | A successful regeneration | [Providers index](../governance/providers/README.md) |
| Work profile | A named workload class mapped to a provider model and reasoning control | A Document Profile | Provider Registry |
| Permission profile | `read-only` or `workspace-write`, translated per provider | Approval | Provider Registry |
| Explicit invocation | A skill runs only when named; discovery alone never selects or empowers it | Discovery | [Agentic policy](../governance/agentic.md) |

## Evidence

### Provenance

On 2026-11-19 SPEC-0212 TSK-0096 moved these six rows unchanged in wording
from the Local Extensions of the Repository Vocabulary, when that vocabulary
moved to `docs/00.workspace/01.project/glossary.md`. No meaning changed.

### Refresh Triggers

- A provider adapter, renderer or Provider Registry binding changes meaning.
- A term here becomes shared by people outside an agent runtime; it then moves
  to the Repository Vocabulary.

## Related Documents

- [Repository Vocabulary](../../docs/00.workspace/01.project/glossary.md)
- [Knowledge index](README.md)
- [Providers index](../governance/providers/README.md)
