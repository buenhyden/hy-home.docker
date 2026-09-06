---
title: "Canonical Knowledge and Prompt Surfaces"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "architecture"
artifact_id: "ADR-0034"
parent_ids:
- "AD-0027"
created: "2026-09-06"
---

# Canonical Knowledge and Prompt Surfaces

## Context

`.agents/` owns three registered categories: `governance/` for policy,
`roles/` for identity and permission, and `skills/` for callable procedure.
Two recurring needs have no owner in that set.

The first is verified navigational knowledge. An agent that opens this
repository must learn which surface belongs to which authority, what the
repository's own vocabulary means, and which gate covers a given change.
That routing knowledge currently lives implicitly across policy prose, the
Stage 90 LLM Wiki data packages, and the Stage 99 registry. Reconstructing it
per session costs context and produces inconsistent answers.

The second is reusable prompt contracts. Task handoff, independent diff
review, commit-message drafting, and test authoring each need a stable input
and output contract that is not a procedure. `.agents/skills/` owns ordered
procedure steps and is the wrong shape for an input/output envelope, and
copying either one into the other creates a second authority.

`.agents/README.md` currently states that no common runtime, memory,
installer, or generated role surface is introduced under the canonical home.
That sentence was written to stop a retired shared progress ledger from
returning to the canonical home.
`scripts/lib/agent_governance/agent_governance_contract.py` enforces that
intent twice: `ROOT_ENTRIES` pins the canonical root inventory, and its
unsupported-token pattern rejects the retired ledger and handoff path names
in tracked text.

## Decision Drivers

- Short-term execution state must stay in the current Spec Package Task; no
  second progress or handoff authority may return.
- Verified long-lived knowledge needs a home that is not a policy body and not
  a Stage 90 dated observation.
- Reusable input/output contracts need a home that is not an ordered procedure.
- Any new canonical category must fail closed through the same registry,
  contract, and template machinery as the existing three.
- A new category must not become a place to duplicate policy, design, or
  runbook bodies.

## Options Considered

**Option A — Add `knowledge/` and `prompts/` as canonical categories.**
Both become registered roots under `.agents/` with their own Stage 99
profiles, templates, lifecycle mapping, and contract inventory entries.
`knowledge/` holds routing and vocabulary that points at canonical owners.
`prompts/` holds input/output contracts that point at skills for procedure.
Cost: four new Stage 99 profiles, two templates, and a contract change.

**Option B — Put both under `.agents/governance/`.**
Reuses the existing `governance-policy` profile with no contract change.
Rejected: it makes navigational summaries and prompt envelopes read as
normative policy, which is exactly the second-authority failure the current
policy set is built to prevent.

**Option C — Put knowledge in Stage 90 and prompts in `.agents/skills/`.**
Reuses existing owners with no new category. Rejected: Stage 90 is
explicitly non-normative dated evidence with a research/audit/data lifecycle,
so a living routing map does not fit its freshness model; and a skill's
registered sections are `Preconditions`/`Procedure`/`Gates`, which forces a
prompt contract to be written as a procedure it is not.

**Option D — Do nothing.**
Rejected: the routing knowledge and prompt contracts continue to be
reconstructed per session, and the agency-agents capability-intake decision
boundary stays without a current owner.

## Decision

Adopt Option A.

`.agents/knowledge/` holds verified, living, non-normative knowledge that
routes a reader to a canonical owner. It owns a project map of surface to
authority, a repository vocabulary index, and a verification surface map.
It never holds a policy body, a detailed design, a specification, or a runbook;
it links to the owner instead. Each member declares its observation date and
refresh trigger so staleness is detectable rather than assumed.

`.agents/prompts/` holds reusable prompt contracts. Each member declares its
purpose, required inputs, output contract, prohibitions, failure handling, and
the roles, skills, and evaluation criteria it applies under. A prompt never
restates a skill's ordered procedure; it names the skill and the role whose
permission profile governs the work.

Neither category holds execution state. The current Spec Package Task remains
the only progress and handoff authority, and the existing unsupported-token
guard against the retired shared progress ledger stays in force unchanged.

Both categories are registered the same way the existing three are: a Stage 99
profile pair per category (a member profile and an index profile), a copyable
template, a `living` lifecycle mapping, a `canonical_sources` entry per file,
and an entry in the canonical root inventory the agent governance contract
pins.

## Consequences

**Enabling.** An agent resolves surface ownership and repository vocabulary by
reading one registered file instead of inferring it. Handoff, review, commit
messaging, and test authoring gain stable contracts that survive a session
boundary and are readable by either provider from the same canonical path.
The capability-intake decision boundary gains a place to be routed from.

**Costs.** The canonical root inventory grows from three directories to five.
Four Stage 99 profiles, two templates, and the template catalog must stay in
step with the contract's profile set; a mismatch fails closed in
`check-agent-governance-contract.py` and the document metadata suite rather
than degrading silently.

**Risks.** The named risk is drift into a second authority: a knowledge file
that starts as a routing table and accumulates rules, or a prompt that grows a
procedure. The registered required sections and the review gate are the
control. A knowledge or prompt file that states an obligation is a defect to
route back to `governance/`, not a new rule.

**Not changed.** Role identities, permission profiles, work profiles, model
translations, hook bindings, public suite names, and the two public validation
profiles are unchanged. No provider gains a permission, tool, or model it did
not have. Discovery of a new canonical file grants no approval.

## Traceability

- **Requirement**: [REQ-0024 Agent Governance Standardization](../../01.requirements/0024-agent-governance-standardization.md)
- **Architecture**: [AD-0027 Agent Governance Canonical Adapter](../descriptions/0027-agent-governance-canonical-adapter.md)
- **Prior decision**: [ADR-0032 Canonical Agent Governance Home](0032-canonical-agent-governance-home.md)
- **Implementation**: [SPEC-0175 Governance Knowledge and Prompt Surface](../../03.specs/0175-governance-knowledge-and-prompt-surface/spec.md)
- **Governance entry**: [canonical agent governance](../../../.agents/README.md)

## Compliance

`scripts/validation/check-agent-governance-contract.py` proves the canonical
root inventory and the registered profile set agree. The document metadata and
lifecycle suites prove every file under the two new roots matches a registered
profile and lifecycle. `scripts/operations/provider_surface_renderer.py --check`
proves the new categories introduce no provider projection drift. No local
result here proves native runtime discovery, provider entitlement, Hosted CI,
or remote branch protection.

## Follow-up

- Transition this decision from `proposed` to `accepted` only after SPEC-0175
  records the contract, registry, and suite evidence for the implemented roots.
- Decide separately whether the Stage 90 curated repository map (DATA-0083)
  consolidates into `.agents/knowledge/`; that move touches the LLM Wiki
  generator, `llms.txt`, and a registered data lifecycle, so it is not part of
  this decision.
- Restore a current owner for the external capability-intake decision boundary
  that [RES-0002-m0003](../../90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md)
  describes but the current Provider Registry no longer carries.
