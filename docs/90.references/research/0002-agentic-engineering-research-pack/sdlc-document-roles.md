---
status: active
artifact_id: reference:agentic-engineering-research:sdlc-document-roles
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# SDLC Document Roles

## Overview

The registry supplies current typed document roles. External practice can
illuminate a role, but local ownership controls publication and lifecycle.

## Purpose

Make the handoffs between product, architecture, planning, operations, and
delivery evidence concrete while preserving two unresolved ADR boundaries.

## Scope

This is an advisory role comparison. `ARD` is local historical terminology,
not an asserted external standard. Stage 99 registry metadata is the sole
machine authority; support material is legacy.

## Definitions / Facts

| Role | Purpose / trigger | Owner / consumer / system | Evidence, rules, and relationships |
| --- | --- | --- | --- |
| PRD | External convention; current local needs are integrated into a Requirements Package when stakeholder needs trigger requirements work. | Requirements owner; architecture and delivery consumers; `REQ` system. | SPEC-0153 integrates PRD/SRS/interface needs; it is not a separate current profile. |
| Architecture Description | Current `AD` explains context, boundaries, components, flow, deployment, and qualities when a durable structure must be communicated. | Architecture owner; Spec/ADR consumers; `AD` system. | Registry defines the profile; it complements, not replaces, decisions. |
| ARD | Retained dated architecture record for enduring boundaries, concerns, views, constraints, and qualities; triggered when requirements need broader framing. | Historical System Architect; ADR/Spec consumers; old Stage 02 requirements route. | `sdlc-document-roles.md:108` in the retained dated leaf; historical-only local terminology, not current policy or an external standard. It cannot establish ADR relationships. |
| ADR | Durable record of a decision-ready architecturally significant choice. Trigger: alternatives and drivers exist. | Owner: architecture; consumer: downstream decision work; system: `ADR`. | Evidence: `SDLCDOC-ADR-001`; rules: structured Markdown and explicit assumptions. AD/Spec relationship is explicitly deferred to `SDLCDOC-ADR-003` `UNVERIFIED`. |
| Spec | Approved behavior and boundaries. Trigger: a change needs agreed intent. | Owner: Stage 03; consumers: Plan and Task; system: `SPEC`. | Evidence: `SDR-001`; rules: typed Spec contract. It supplies the durable upstream boundary. |
| Plan | Proposed execution sequence. Trigger: approved behavior needs coordinated work. | Owner: Stage 03; consumers: implementers; system: `Plan`. | Evidence: `SDR-001`; rules: scoped steps and verification. It must not replace approval or durable evidence. |
| Task | Progress and evidence ledger. Trigger: approved work begins. | Owner: Stage 03; consumers: reviewers; system: `Task`. | Evidence: `SDR-001`; rules: record actual checks. It links work to its Spec/Plan without becoming either. |
| Guide | Learning-oriented operational explanation. Trigger: a reader needs orientation. | Owner: operations catalog; consumer: operator; system: catalog. | Evidence: `SDR-002`; rules: explain use, not deterministic action. It complements Policy and Runbook. |
| Policy | Normative operational constraint. Trigger: a control or boundary is required. | Owner: operations catalog; consumer: operator; system: catalog. | Evidence: `SDR-002`; rules: state constraints. It constrains, but does not replace, a procedure. |
| Runbook | Deterministic operator action. Trigger: implemented behavior needs a repeatable procedure. | Owner: operations catalog; consumer: operator; system: catalog. | Evidence: `SDR-002`; rules: executable procedure and recovery. It is distinct from teaching and policy. |
| Incident | Event response record with open, mitigated, closed states. Trigger: an operational event. | Owner: incident responder; consumer: postmortem author; system: incident packet. | Evidence: `SDR-003`; rules: retain response evidence. It precedes learning, not a completed living document. |
| Postmortem | Blameless learning record. Trigger: an incident has sufficient evidence for review. | Owner: incident team; consumer: prevention work; system: incident packet. | Evidence: `SDR-003`; rules: review causes and actions. It relates to, but does not erase, the incident. |
| Release evidence | A release event uses tag, notes, and assets. Trigger: a version is released. | Release publisher; Task plus Git/PR own ordinary delivery; release consumers use event evidence. | `SDR-004`; no standalone local Release profile. SemVer describes public API versioning, not deployment. |

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `SDR-001` | Stage 03 assigns Spec, Plan, and Task distinct behavior, execution, and evidence roles. | tracked workspace configuration | VERIFIED | `docs/03.specs/` | Preserve durable capture before cleanup. |
| `SDR-002` | Guide, Policy, and Runbook have distinct learning, constraint, and deterministic-procedure purposes. | tracked workspace configuration | VERIFIED | operations catalog convention | Choose by reader and operational need. |
| `SDR-003` | Incident packets pair response evidence with postmortem learning; external NIST and SRE material informs, but does not prove, local practice. | tracked + historical retained source | VERIFIED | incident packet convention | Keep incident state separate from living-document retirement. |
| `SDR-004` | GitHub release evidence consists of release tags, notes, and assets; SemVer is an API-versioning convention rather than deployment evidence. | historical retained source | HISTORICAL VERIFIED | GitHub release event | Do not invent a local Release profile or infer deployment. |
| `SDR-005` | Current local requirements work integrates PRD-style needs in `REQ`, while current `AD` owns durable architecture communication. | tracked workspace configuration | VERIFIED | SPEC-0153 and registry | This is a local role binding, not external-role proof. |
| `SDR-006` | The retained ARD leaf records historical boundaries, concerns, views, constraints, and qualities under an old Stage 02 route. | historical retained source | HISTORICAL VERIFIED | retained `sdlc-document-roles.md:108` | Historical local context only; it cannot support an ADR boundary. |
| `SDLCDOC-ADR-001` | MADR supports structured Markdown ADRs for architecture and related decisions, with explicit assumptions and maintainability rationale. | retained delta evidence | VERIFIED | Task 0004 ADR-ROLE | It does not replace Architecture Description. |
| `SDLCDOC-ADR-002` | Retained status discussion does not establish a complete ADR lifecycle or supersession rule. | retained delta evidence | UNVERIFIED | Task 0004 ADR-LIFECYCLE | Do not assert the missing boundary. |
| `SDLCDOC-ADR-003` | Retained MADR overview does not establish relationships to Architecture Description or Spec. | retained delta evidence | UNVERIFIED | Task 0004 ADR-RELATIONSHIPS | Do not infer relationships from local schema. |

## Architecture Practice Delta Claims

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `SDLCDOC-ADR-001` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-002` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-003` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |

## Architecture Practice Direct-Page Evidence

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `ADR-ROLE` | `SDR-SRC-001` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | 2026-08-28 | VERIFIED |
| `ADR-LIFECYCLE` | `SDR-SRC-002` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDR-SRC-003` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SDR-SRC-001` | `SDLCDOC-ADR-001` | Use Markdown Architectural Decision Records / MADR | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | retained delta evidence | MADR 4.0.0 chosen option | 2026-08-28 | Chosen option is not proof it is latest or locally adopted. |
| `SDR-SRC-002` | `SDLCDOC-ADR-002` | Add Status Field / MADR | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | retained delta evidence | no stated revision | 2026-08-28 | `UNVERIFIED`: partial status page is insufficient. |
| `SDR-SRC-003` | `SDLCDOC-ADR-003` | About MADR / MADR | `https://adr.github.io/madr/` | retained delta evidence | rendered template/news | 2026-08-28 | `UNVERIFIED`: AD means Architectural Decision, not Architecture Description. |
| `SDR-SRC-004` | `SDR-001`, `SDR-002`, `SDR-003` | Registry and SPEC-0153 / workspace | [registry](../../../99.templates/registry.json); [SPEC-0153](../../../03.specs/0153-workspace-governance-simplification/spec.md) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Local configuration is not external-role proof. |
| `SDR-SRC-005` | `SDR-003` | NIST SP 800-61r3 and Google SRE postmortems | [NIST](https://csrc.nist.gov/pubs/sp/800/61/r3/final); [Google SRE](https://sre.google/sre-book/postmortem-culture/) | historical retained source | NIST final Apr 2025; retained 2026-08-08 observation | 2026-08-08 | Practices inform incident/postmortem analysis only; they do not prove local operation. |
| `SDR-SRC-006` | `SDR-004` | GitHub releases and Semantic Versioning | [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases); [SemVer](https://semver.org/) | historical retained source | retained 2026-08-08 observation | 2026-08-08 | Tags, notes, assets, and API versioning do not prove deployment. |
| `SDR-SRC-007` | `SDR-005` | Requirements/AD role bindings / workspace | [SPEC-0153](../../../03.specs/0153-workspace-governance-simplification/spec.md); [registry](../../../99.templates/registry.json) | tracked workspace configuration | `29d947b4bec58bec35d8555c27f2b3550634fe43` | 2026-08-28 | Local configuration does not establish an external PRD or AD standard. |
| `SDR-SRC-008` | `SDR-006` | Retained dated SDLC document roles / workspace | [dated leaf](../2026-08-08-agentic-engineering-research-pack/sdlc-document-roles.md) | historical retained source | line 108, retained 2026-08-08 record | 2026-08-08 | Historical terminology only; never use it to rescue `SDLCDOC-ADR-002` or `SDLCDOC-ADR-003`. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Agents consume approved Spec and Task boundaries. | Inspect Stage 03 links. | No agent behavior proof. |
| architecture | applies | Use AD for structure and ADR for decision-ready choices. | Confirm registry profiles. | ADR gaps remain UNVERIFIED. |
| common | applies | Keep owner/consumer handoffs explicit. | Review role table. | Advisory analysis. |
| docs | applies | Publish typed documents in registered paths. | Check registry path patterns. | Legacy support is not authority. |
| infra | applies | Apply Guide/Policy/Runbook roles to infrastructure catalog subjects. | Confirm `docs/05.operations/catalog/<domain>/<subject>/` ownership. | No runtime claim. |
| ops | applies | Select Guide, Policy, Runbook, Incident, or Postmortem by purpose. | Check catalog/packet convention. | No live incident is asserted. |
| qa | applies | Attach verification evidence to Task. | Inspect Task evidence. | A Task record is not execution proof. |
| security | applies | Use Policy constraints and incident handling boundaries. | Inspect scoped source references. | No control effectiveness claim. |

## Architecture Practice Composition Links

- [Documentation architecture](./documentation-architecture.md)
- [Scope application matrix](./scope-application-matrix.md)

## Maintenance

Refresh role mapping with the registry or approved local architecture changes.
Do not repair either `UNVERIFIED` ADR claim using an older source, local schema,
or an alternative claim owner.

## Related Documents

- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [Documentation architecture](./documentation-architecture.md)
