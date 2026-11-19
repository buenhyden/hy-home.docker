---
title: "Docker Workspace Vocabulary"
version: "0.13.0"
type: "governance/control"
status: "active"
owner: "@buenhyden"
updated: "2026-11-20"
created: "2026-09-06"
observed_at: "2026-11-20"
review_cycle: "on-contract-change"
---

# Docker Workspace Vocabulary

## Overview

This file owns narrower meanings and concrete bindings in this Docker
workspace. Common Term IDs, foundation concepts and agent/provider terms
have one meaning owner in the
[Repository Vocabulary](../../../.agents/knowledge/glossary.md).
A local binding names its policy owner and never changes the common meaning
or grants permission to operate a service.

## Scope

Included: this repository's document lifecycle, gate names and operational
context. Excluded: common definitions, service inventories, runtime state,
secrets and provider settings. Product profile names remain owned by
[POL-0078](../../05.operations/02.policies/01.common/0078-compose-profile-vocabulary.md);
this vocabulary routes to that owner instead of copying its table.

## Rules

### Local Terms

| Term | Definition | Not to Confuse | Policy Owner |
| --- | --- | --- | --- |
| Canonical location | Here a canonical source is an authored file under `docs/00.workspace/` or `.agents/`, or the Stage owner a policy names | A generated projection | [Agent governance index](../../../.agents/README.md) |
| Adoption record | This repository records each adoption, with its revision and effective date, in its own Task; a configured surface alone is tracked configuration, not adoption | Adoption by another repository | [Approval boundaries](../04.quality/approval-boundaries.md) |
| Acceptance record | Acceptance is recorded only in a Task's Criterion Acceptance table; a runtime accepting a value or a risk acceptance is not Acceptance | Runtime acceptance | [SDLC](../03.process/sdlc.md#sequence) |
| Retirement, here | Still-current meaning moves to its owner and the file is deleted in the same change once the retirement preconditions hold; Git history keeps the body | Removal without retirement | [Documentation protocol](../03.process/documentation-protocol.md#document-retention-and-retirement) |
| Archive, here | Git history is the archive; Stage 98 holds only its README | A tracked archive copy | [Documentation protocol](../03.process/documentation-protocol.md#document-retention-and-retirement) |
| Historical Audit ID | A key such as OPEN-01 to OPEN-14 that names an item of an earlier audit. It is not a current state, file name or issue number | A currently open work item | This vocabulary; current verdicts live in the owning Task |
| Registry file | The Registry is `docs/99.templates/registry.json` | A template | [Documentation protocol](../03.process/documentation-protocol.md) |
| Document Profile entry | A Registry entry binding a path pattern to a role's required frontmatter, sections, identity, lifecycle and template | Profile, gate sense | [Documentation protocol](../03.process/documentation-protocol.md) |
| Supersession lineage | Outside Stages 01 to 03, the newer document lists predecessors in `supersedes` and the older names its one successor in `superseded_by`; Stage 01 to 03 successors record the replaced substance in their lineage section instead: `Traceability` in a Requirement Package, `Adoption Boundaries` in an Architecture Description, and a `Supersession` heading in an ADR's `Authority and Effect` | A one-way mention | [Documentation protocol](../03.process/documentation-protocol.md) |
| Resolves row | In a Task Evidence table, a later required PASS row for a shared criterion, with the same Check (Method and Command from lifecycle generation 8) and Work Unit, names the earlier non-PASS row in its `Resolves` column | Any newer PASS | [SDLC](../03.process/sdlc.md#sequence) |
| Spec Package | A directory holding one bounded change's `spec.md`, optional `plan.md`, and numbered Tasks | A long-lived requirement or design | [Documentation protocol](../03.process/documentation-protocol.md) |
| Lifecycle | The named status set and permitted transitions for a profile; `living` and `spec` differ | The SDLC stage or document stage | [Documentation protocol](../03.process/documentation-protocol.md) |
| Identity space | The monotonic allocator for an artifact prefix; an issued number is never reused | A display order | [Documentation protocol](../03.process/documentation-protocol.md) |
| Reserved history | The Registry list of retired numbers per identity space; it only grows | A removal record | [Documentation protocol](../03.process/documentation-protocol.md#document-retention-and-retirement) |
| Promotion receipt | The Task section connecting each acceptance criterion to its durable Stage 01, 02 or 05 or governance owner, with the target commit, consumer check, acceptance row and residual owner | Promotion itself | [SDLC](../03.process/sdlc.md#sequence) |
| Tracked configuration | What a configured hook, provider surface or renderer parity proves: the setting is tracked | Adoption or a live event | [Approval boundaries](../04.quality/approval-boundaries.md) |
| Runtime acceptance | Whether an active provider runtime accepted a configured value, observed natively; a kind of Native Runtime Evidence | Acceptance | [Provider capability matrix](../../../.agents/governance/provider-capability-matrix.md) |
| Fail closed | An unknown or unsafe input is preserved and reported, never auto-deleted or auto-approved | Silent skip | [Agentic policy](../../../.agents/governance/agentic.md) |
| QA | Applicable verification and review of the changed contract | Acceptance | [Quality standards](../04.quality/quality-standards.md) |
| CI | Hosted validation of a named event and revision | Deployment | [GitHub governance](../03.process/github-governance.md) |
| CD | Authorized artifact promotion and deployment; a changelog check or rehearsal alone is not deployment | Release Operation readiness | [Documentation protocol](../03.process/documentation-protocol.md#release-evidence-boundary) |
| Workflow | GitHub event-triggered automation composed of jobs | A Spec Package workflow | `.github/workflow-contract.yml` |
| Job | One execution unit in a workflow; not necessarily a required status check | Required status check | `.github/workflow-contract.yml` |
| Required status check | A named source-bound context required by remote protection for the relevant revision | Any passing job | `.github/rulesets/main-protection.md` |
| Check | Validation that reports a result without rewriting source | Fix | [Quality standards](../04.quality/quality-standards.md) |
| Fix | An explicitly requested source transformation followed by diff review and verification | Check | [Quality standards](../04.quality/quality-standards.md) |
| Fixture | Deterministic input with a focused behavior or independent serialized consumer | Production data | [Quality standards](../04.quality/quality-standards.md) |
| Local completion | Reviewed local changes and applicable checks and commits with explicit limits | Completion of integration or deployment | [Task checklists](../04.quality/task-checklists.md) |
| Merge readiness | Actual required checks and reviews for the relevant PR revision and verified protection | Acceptance | [GitHub governance](../03.process/github-governance.md) |
| Suite | One of the six named public groupings of gate nodes | A test module | `.github/workflow-contract.yml` |
| Gate node | One addressable entry in the executable graph | A workflow job | `.github/workflow-contract.yml` |
| Leaf | A gate node that executes an entrypoint rather than expanding to children | A suite | `.github/workflow-contract.yml` |
| Profile, gate sense | `changed` or `full`; the two public validation profiles | Document Profile | `.github/workflow-contract.yml` |
| Canonical invocation identity | Resolved path, normalized argv, profile and execution context; unique per plan | A command string | `scripts/validation/ci_gate_runner.py` |
| Changed-path rule | The prefix-to-suite mapping that selects suites for a changed file | A required status check | `.github/workflow-contract.yml` |
| Controlled wrapper | The single approved all-files pre-commit route; direct `pre-commit run` is prohibited | A direct hook run | [Quality standards](../04.quality/quality-standards.md#4-execution-boundary) |
| Generated-artifact freshness | A generated output must be reproduced by its generator, never hand-edited to pass | Projection | [Quality standards](../04.quality/quality-standards.md) |
| Evidence class | The weakest observation that supports a claim: configured, repository-enforced, local-executed, local-parser, official-source, or an unverified runtime, entitlement or remote state | Evidence itself; one class does not prove another | [Output style](../../../.agents/governance/output-style.md) |
| Structural Ownership | The `rel.structural-ownership` relation: a Plan, Task, data model contract, research or audit member, or postmortem names in `parent_ids` the document that structurally contains it | The frontmatter `owner`, which names a person | [Documentation protocol](../03.process/documentation-protocol.md#link-types-and-document-relations) |
| Constraint | The `rel.constraint` relation: a Requirements package, Architecture description, ADR or Spec names in `parent_ids` the document that constrains it | Structural Ownership | [Documentation protocol](../03.process/documentation-protocol.md#link-types-and-document-relations) |
| Change Impact | The `rel.change-impact` relation from an owner to its consumers, derived from Authority, Constraint and Structural Ownership when a document is removed or moved; no document records it | A hand-kept reverse-state table | [Documentation protocol](../03.process/documentation-protocol.md#link-types-and-document-relations) |
| Traceability heading | The Requirement Package lineage section that holds its basis and supersession records; an Architecture Description holds them in `Decisions and Adoption` / `Adoption Boundaries` and an ADR in `Decision` / `Authority and Effect` | The `rel.traceability` relation, which a Task's evidence rows and links write | [Documentation protocol](../03.process/documentation-protocol.md#link-types-and-document-relations) |
| Promote (older Specs and labs) | In SPEC-0259 and SPEC-0261 (retired), moving a draft operations document to `active` after it matched the source; in SPEC-0263, moving a lab workload into the managed stack under its `promotion.yaml` and the lab promotion policy | The common Promotion term, which hands lasting meaning to its owner through a Plan | [SDLC](../03.process/sdlc.md#sequence) |
| HOME context | The operating-host context described by AD-0031; its component and deployment boundaries are owned there | A separate experiment or a sandbox result | [AD-0031](../../02.architecture/01.descriptions/0031-home-development-host.md) |
| LAB context | The repository's experiment context; entrypoint and isolation guarantees depend on the selected LAB owner | A Compose profile automatically providing isolation | [Environment constraints](../../../.agents/governance/environment-constraints.md) |
| Compose profile, local binding | A selection name registered by POL-0078, distinct from this file's gate-profile sense | A Document Profile, permission profile or security boundary | [POL-0078](../../05.operations/02.policies/01.common/0078-compose-profile-vocabulary.md) |

## Evidence

### Provenance

Read from tracked source at `30bfa6543fd60bbce9f38efedc1728e9b1e382a0`
on 2026-11-20: the previous Repository Vocabulary's Local Extensions,
AD-0031, POL-0078 and the linked policy owners. SPEC-0212 TSK-0096's
2026-11-19 relocation remains historical evidence. The direct P03 1.1.0
requirement restores common meanings to `.agents/knowledge/glossary.md`,
merges the six agent-only rows there, and retains these local bindings here.
No common Term ID or definition is copied into this local owner. The
Historical Audit ID entry explains old references without reopening them.

### Refresh Triggers

- A linked policy changes a local binding or its authoritative location.
- The adopted vocabulary or a public suite/profile name changes.
- A local meaning becomes shared; migrate it rather than defining it twice.

## Related Documents

- [Repository Vocabulary](../../../.agents/knowledge/glossary.md)
- [Workspace index](../README.md)
- [Documentation protocol](../03.process/documentation-protocol.md)
- [SDLC](../03.process/sdlc.md)
- [Quality standards](../04.quality/quality-standards.md)
