---
status: active
artifact_id: reference:agentic-engineering-research:scope-application-matrix
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Scope Application Matrix

## Overview

This leaf provides the closed eight-scope routing model for the current draft.
It includes D4's evidence-limited architecture-practice composition; it neither
adopts a practice nor fills the two unresolved ADR evidence gaps.

## Purpose

Make each authored foundation claim explicit about applicability, adoption
conditions, verification, and limits without adding scope values or policy.

## Scope

The closed axis is `agentic`, `architecture`, `common`, `docs`, `infra`, `ops`,
`qa`, and `security`. Named agents are owners or consumers, not additional
scope values.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `SAM-001` | SPEC-0137 defines exactly eight general Stage 00 role scopes for this draft. | tracked workspace configuration | VERIFIED | `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` | Every leaf must supply exactly one row for each scope. |
| `SAM-002` | Stage 00 separates policy, role, skill, and provider-registry ownership; provider adapters translate rather than own shared behavior. | tracked workspace configuration | VERIFIED | `docs/00.agent-governance/` | Route gaps to the canonical owner instead of extending this advisory pack. |
| `SCOPE-COMP-001` | Advisory composition routes a stated documentation need through Diataxis reader form, a C4 structural view, an arc42 outline, and a decision-ready ADR only where the cited evidence is sufficient. | advisory synthesis | ADVISORY | current typed owner/path | Adoption requires owner review, source-state check, and a scoped content check; it does not adopt a practice or fill ADR gaps. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SAM-SRC-001` | `SAM-001` | Agentic Engineering Research Pack Rebuild Specification / workspace | [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | The axis constrains this draft; it does not establish final acceptance. |
| `SAM-SRC-002` | `SAM-002` | Agentic Engineering Policy and Provider Adapters / workspace | [agentic policy](../../../00.agent-governance/policies/agentic.md); [provider adapters](../../../00.agent-governance/providers/README.md); [provider registry](../../../00.agent-governance/providers/registry.yaml) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | Provider runtime acceptance remains `needs_revalidation`; no provider probe occurred. |

`SCOPE-COMP-001` reuses the allowed canonical claim inputs
`DOCARCH-C4-001`, `DOCARCH-ARC42-001`, `SDLCDOC-ADR-001`,
`SDLCDOC-ADR-002`, `SDLCDOC-ADR-003`, and `DOCARCH-COMP-001`, together with
tracked workspace evidence. Diataxis is available through the existing
`DOCARCH-COMP-001` input. This advisory synthesis adds no independent source
ID; ADR lifecycle and Architecture Description/Spec relationships remain
`UNVERIFIED`.

## Architecture Practice Delta Claims

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `SCOPE-COMP-001` | `scope-application-matrix.md` | synthesis-only | `—` |

## Architecture Practice Scope Application

| Claim ID | Scope | Disposition | Adoption conditions | Limitations | Verification |
| --- | --- | --- | --- | --- | --- |
| `SCOPE-COMP-001` | agentic | applies | Select reader form and structural view for an agent boundary. | ADR gaps remain UNVERIFIED. | Review typed owner and linked evidence. |
| `SCOPE-COMP-001` | architecture | applies | Combine C4 view, arc42 outline, and decision-ready ADR deliberately. | No implied lifecycle/relationship rule. | Inspect C4/arc42/ADR evidence states. |
| `SCOPE-COMP-001` | common | applies | Use composition only for a stated communication need. | Advisory, not policy. | Check scope and audience. |
| `SCOPE-COMP-001` | docs | applies | Choose Diataxis form and self-contained diagram details. | No mandatory template. | Review form, legend, and links. |
| `SCOPE-COMP-001` | infra | applies | Use deployment view only where an infra owner needs it. | C4 container is not Docker proof. | Confirm infra owner/path. |
| `SCOPE-COMP-001` | ops | applies | Use dynamic/deployment communication for a catalog or incident concern. | No operation observed. | Confirm catalog/packet owner. |
| `SCOPE-COMP-001` | qa | applies | Review diagram readability and evidence limits. | No certification. | Inspect labels and source rows. |
| `SCOPE-COMP-001` | security | applies | Include security-relevant relationships when scoped. | No threat-model run. | Review scoped evidence. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Follow the approved Spec, Plan, and Task before agentic work. | Read governing paths at the literal baseline. | This is routing, not agent execution proof. |
| architecture | applies | Route architecture decisions to their canonical artifacts and owners; investigate whether a C4 view, arc42 outline, or ADR is needed before adoption. | Confirm the tracked owner/path, source state, and scoped diff; seek separate approval for runtime observation. | D4 composition is advisory; ADR lifecycle and AD/Spec relationships remain UNVERIFIED. |
| common | applies | Apply shared-worktree and approval-boundary constraints. | Inspect only the exact owned-path diff. | A shared rule is not observed enforcement. |
| docs | applies | Apply the research and generic-reference document contracts. | Check frontmatter, headings, and local destinations. | The draft pack has no parent router. |
| infra | applies | Inspect tracked infrastructure configuration; seek separate approval for runtime observation. | Confirm the cited configuration path and scoped diff. | Configuration cannot demonstrate deployment. |
| ops | applies | Route an operational need to its owner and inspect tracked records before use. | Confirm the record path and scoped diff; seek separate approval for live operation. | No run or incident is inferred. |
| qa | applies | Perform scoped document and path checks after the unit is final. | Record actual commands and results in Task 0004; seek separate approval for execution-environment checks. | Full acceptance checks remain deferred. |
| security | applies | Keep sources local and avoid secret, credential, or remote-state access. | Confirm cited sources are tracked documentation; seek separate approval for control testing. | No control effectiveness is evaluated. |

## Maintenance

Update the general routing only when the Spec's closed axis or the cited Stage
00 ownership changes. Refresh composition only with authorized cross-practice
evidence and sibling files present.

## Related Documents

- [Research pack README](./README.md)
- [Workspace baseline](./workspace-baseline.md)
- [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md)

## Architecture Practice Composition Links

- [Documentation architecture](./documentation-architecture.md)
- [SDLC document roles](./sdlc-document-roles.md)
