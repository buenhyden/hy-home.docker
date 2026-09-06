---
title: "Repository Vocabulary"
version: "0.1.0"
type: "governance/knowledge"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-06"
created: "2026-09-06"
observed_at: "2026-09-06"
review_cycle: "on-contract-change"
---

# Repository Vocabulary

## Overview

Terms this repository uses with a narrower meaning than their general one. Each
entry states the meaning and names the document that owns the rule. A definition
here is a reading aid, never the rule itself.

## Scope

Vocabulary that appears in canonical governance, Stage 99 contracts, the
workflow contract, and validator output. Excluded: general software terms used
in their ordinary sense, and vendor product terminology owned by the Provider
Registry.

## Document and Lifecycle Terms

| Term | Meaning here | Rule owner |
| --- | --- | --- |
| Spec Package | A directory holding one bounded change's `spec.md`, optional `plan.md`, and numbered Tasks | [documentation protocol](../governance/documentation-protocol.md) |
| Task | The sole ledger for what actually happened: commands, exit codes, review, blockers, commits | [SDLC](../governance/sdlc.md) |
| Profile | A Stage 99 entry binding a path pattern to required frontmatter, sections, identity, and lifecycle | `docs/99.templates/registry.json` |
| Lifecycle | The named status set and permitted transitions for a profile; `living` and `spec` differ | `docs/99.templates/registry.json` |
| Identity space | The monotonic allocator for an artifact prefix; an issued number is never reused | [documentation protocol](../governance/documentation-protocol.md) |
| Preservation | Moving a terminal document's frozen body to Stage 98 unchanged; Git proves the source | [documentation protocol](../governance/documentation-protocol.md) |
| Tombstone | One disposition record for one retired package or document, under a `tomb-` prefix | [documentation protocol](../governance/documentation-protocol.md) |
| Supersession | Replacing an accepted decision through a reciprocal lineage, not by rewriting it | [documentation protocol](../governance/documentation-protocol.md) |
| Promotion receipt | The Task section connecting each acceptance criterion to its durable Stage 01, 02, or 05 owner | [SDLC](../governance/sdlc.md) |

## Governance and Provider Terms

| Term | Meaning here | Rule owner |
| --- | --- | --- |
| Canonical source | An authored file under `.agents/`; never a generated output | [agent governance index](../README.md) |
| Projection | A generated native file rendered from a canonical source by the registered renderer | [providers index](../governance/providers/README.md) |
| Adapter | An authored provider file owning loading and syntax differences only | `.claude/provider.md`, `.codex/provider.md` |
| Native mechanics | Provider runtime configuration such as settings and hook registration | Provider Registry |
| Quarantine | The renderer's nonzero cleanup handoff; it is not a successful regeneration | [providers index](../governance/providers/README.md) |
| Work profile | A named workload class mapped to a provider model and reasoning control | Provider Registry |
| Permission profile | `read-only` or `workspace-write`, translated per provider | Provider Registry |
| Explicit invocation | A skill runs only when named; discovery alone never selects or empowers it | [agentic policy](../governance/agentic.md) |
| Fail closed | An unknown or unsafe input is preserved and reported, never auto-deleted or auto-approved | [agentic policy](../governance/agentic.md) |

## Verification Terms

| Term | Meaning here | Rule owner |
| --- | --- | --- |
| Suite | One of the six named public groupings of gate nodes | `.github/workflow-contract.yml` |
| Gate node | One addressable entry in the executable graph | `.github/workflow-contract.yml` |
| Leaf | A gate node that executes an entrypoint rather than expanding to children | `.github/workflow-contract.yml` |
| Profile, gate sense | `changed` or `full`; the two public validation profiles | `.github/workflow-contract.yml` |
| Canonical invocation identity | Resolved path, normalized argv, profile, and execution context; unique per plan | `scripts/validation/ci_gate_runner.py` |
| Changed-path rule | The prefix-to-suite mapping that selects suites for a changed file | `.github/workflow-contract.yml` |
| Controlled wrapper | The single approved all-files pre-commit route; direct `pre-commit run` is prohibited | [environment constraints](../governance/environment-constraints.md) |
| Generated-artifact freshness | A generated output must be reproduced by its generator, never hand-edited to pass | [quality standards](../governance/quality-standards.md) |

## Evidence Classes

These are not interchangeable. A claim carries the weakest class that supports it.

| Class | What it establishes |
| --- | --- |
| Configured | A setting is declared in a tracked file |
| Repository-enforced | A tracked check rejects the violation |
| Local-executed | A command ran here and produced this exit code |
| Local-parser | An installed binary contains or accepts the symbol |
| Official-source | A vendor document states it |
| Unverified runtime | The behavior was not observed in a running provider |
| Unverified entitlement | Account access to a model or feature was not confirmed |
| Unverified remote | Hosted CI, branch protection, or deployed state was not observed |

## Provenance

Compiled from tracked sources at repository commit
`9ede309a5b1feba91e6f8b973a729716b14c55ab` on 2026-09-06: canonical governance
policies, the Provider Registry, the Stage 99 registry, and the workflow
contract. Each row names its rule owner so a reader verifies the term against
that document rather than against this table.

## Refresh Triggers

- A governance policy introduces or retires a term.
- A Stage 99 lifecycle, profile, or identity relation changes.
- A public suite or profile name changes in the workflow contract.
- An evidence class is added or redefined by the quality standards.

## Related Documents

- [Knowledge index](README.md)
- [Repository authority map](repository-map.md)
- [Documentation protocol](../governance/documentation-protocol.md)
- [Quality standards](../governance/quality-standards.md)
